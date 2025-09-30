"""Econometric utilities for modern trade empirics."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, Iterable, Tuple

import numpy as np
import pandas as pd
from scipy import stats


def add_const(X):
    X = np.asarray(X, dtype=float)
    if X.ndim == 1:
        X = X.reshape(-1, 1)
    ones = np.ones((X.shape[0], 1))
    return np.hstack([ones, X])


def ols(y, X):
    y = np.asarray(y, dtype=float).reshape(-1)
    Xc = add_const(X)
    beta = np.linalg.lstsq(Xc, y, rcond=None)[0]
    resid = y - Xc @ beta
    n, k = Xc.shape
    sigma2 = (resid @ resid) / (n - k)
    XtX_inv = np.linalg.inv(Xc.T @ Xc)
    vcov = sigma2 * XtX_inv
    se = np.sqrt(np.diag(vcov))
    return beta, se, resid, vcov, n, k


def ols_cluster(y, X, cluster):
    y = np.asarray(y, dtype=float).reshape(-1)
    Xc = add_const(X)
    beta = np.linalg.lstsq(Xc, y, rcond=None)[0]
    resid = y - Xc @ beta
    XtX_inv = np.linalg.inv(Xc.T @ Xc)
    vcov = _cluster_vcov(Xc, resid, np.asarray(cluster), XtX_inv)
    se = np.sqrt(np.diag(vcov))
    return beta, se, vcov, Xc.shape[0], Xc.shape[1]


def ols_2way(y, X, cluster1, cluster2):
    y = np.asarray(y, dtype=float).reshape(-1)
    Xc = add_const(X)
    beta = np.linalg.lstsq(Xc, y, rcond=None)[0]
    resid = y - Xc @ beta
    XtX_inv = np.linalg.inv(Xc.T @ Xc)
    c1 = np.asarray(cluster1)
    c2 = np.asarray(cluster2)
    vcov1 = _cluster_vcov(Xc, resid, c1, XtX_inv)
    vcov2 = _cluster_vcov(Xc, resid, c2, XtX_inv)
    vcov12 = _cluster_vcov(Xc, resid, list(zip(c1, c2)), XtX_inv)
    vcov = vcov1 + vcov2 - vcov12
    se = np.sqrt(np.diag(vcov))
    return beta, se, vcov


def weak_iv_fstat(x, xhat, k_excl):
    x = np.asarray(x, dtype=float)
    xhat = np.asarray(xhat, dtype=float)
    if x.ndim != 1:
        x = x.reshape(-1)
    if xhat.ndim != 1:
        xhat = xhat.reshape(-1)
    n = len(x)
    if n <= k_excl + 1:
        return float('inf')
    tss = np.sum((x - x.mean()) ** 2)
    rss = np.sum((x - xhat) ** 2)
    if tss <= 1e-12:
        return 0.0
    r2 = 1 - rss / tss
    df_num = k_excl
    df_den = n - k_excl - 1
    if df_den <= 0:
        return float('inf')
    return float((r2 / df_num) / ((1 - r2) / df_den))


def sun_abraham(panel: pd.DataFrame, dep='y', treat='D', unit='i', time='t'):
    df = panel[[unit, time, dep, treat]].copy()
    df = df.sort_values([unit, time]).reset_index(drop=True)
    df['_unit'] = df[unit].astype('category').cat.codes.to_numpy()
    df['_time'] = df[time].astype('category').cat.codes.to_numpy()

    treat_map = df[df[treat] == 1].groupby(unit)[time].min()
    treat_time = df[unit].map(treat_map).to_numpy()
    df['_treat_time'] = treat_time
    df.loc[df['_treat_time'].isna(), '_treat_time'] = np.inf
    df['_rel'] = df[time].to_numpy(dtype=float) - df['_treat_time'].to_numpy(dtype=float)

    cohorts = sorted(t for t in np.unique(df['_treat_time']) if np.isfinite(t))
    if not cohorts:
        return {
            'betas': np.array([]),
            'ses': np.array([]),
            'pretrend_p': 1.0,
            'table': pd.DataFrame(columns=['rel_time', 'beta', 'se']),
        }

    rel_candidates = sorted(set(df.loc[np.isfinite(df['_rel']), '_rel']) - {-1.0})
    rel_candidates = [int(r) for r in rel_candidates]

    n = len(df)
    columns = []
    keys = []
    for g in cohorts:
        mask_g = (df['_treat_time'] == g)
        if not mask_g.any():
            continue
        rel_times = df.loc[mask_g & (df[treat] == 1) | (mask_g & (df[time] >= g)), '_rel']
        for r in rel_candidates:
            col = ((mask_g) & (np.isfinite(df['_rel'])) & (np.isclose(df['_rel'], r))).to_numpy(float)
            if col.sum() == 0:
                continue
            columns.append(col)
            keys.append((g, r))

    if not columns:
        return {
            'betas': np.array([]),
            'ses': np.array([]),
            'pretrend_p': 1.0,
            'table': pd.DataFrame(columns=['rel_time', 'beta', 'se']),
        }

    X = np.column_stack(columns)
    unit_idx = df['_unit'].to_numpy()
    time_idx = df['_time'].to_numpy()
    y = df[dep].to_numpy(dtype=float)

    X_dd = np.column_stack([_double_demean(col, unit_idx, time_idx) for col in columns])
    y_dd = _double_demean(y, unit_idx, time_idx)

    beta = np.linalg.lstsq(X_dd, y_dd, rcond=None)[0]
    resid = y_dd - X_dd @ beta
    XtX_inv = np.linalg.inv(X_dd.T @ X_dd)
    vcov = _cluster_vcov(X_dd, resid, unit_idx, XtX_inv)
    se = np.sqrt(np.diag(vcov))

    cohort_sizes = df.replace(np.inf, np.nan).dropna(subset=['_treat_time']).groupby('_treat_time')[unit].nunique()
    cohort_weights = {g: cohort_sizes.get(g, 0) for g in cohorts}
    total_weight = sum(cohort_weights.values())
    weight_vectors: Dict[int, np.ndarray] = {}
    unique_rel = sorted({key[1] for key in keys})
    for r in unique_rel:
        w = np.zeros(len(keys))
        for idx, (g, rel) in enumerate(keys):
            if rel == r and total_weight > 0:
                w[idx] = cohort_weights.get(g, 0) / total_weight
        weight_vectors[r] = w

    W = np.vstack([weight_vectors[r] for r in unique_rel]) if unique_rel else np.zeros((0, len(keys)))
    agg_coefs = W @ beta if unique_rel else np.array([])
    agg_vcov = W @ vcov @ W.T if unique_rel else np.zeros((0, 0))
    agg_se = np.sqrt(np.diag(agg_vcov)) if unique_rel else np.array([])

    table = pd.DataFrame({'rel_time': unique_rel, 'beta': agg_coefs, 'se': agg_se})

    pre_idx = [i for i, r in enumerate(unique_rel) if r < 0]
    if pre_idx:
        b_pre = agg_coefs[pre_idx]
        cov_pre = agg_vcov[np.ix_(pre_idx, pre_idx)]
        try:
            chi = float(b_pre.T @ np.linalg.pinv(cov_pre) @ b_pre)
            pretrend_p = float(stats.chi2.sf(chi, len(pre_idx)))
        except np.linalg.LinAlgError:
            pretrend_p = 1.0
    else:
        pretrend_p = 1.0

    return {
        'betas': agg_coefs,
        'ses': agg_se,
        'pretrend_p': pretrend_p,
        'table': table,
    }


def iv2sls_cluster(y, X, Z, cluster):
    y = np.asarray(y, dtype=float).reshape(-1)
    X = np.asarray(X, dtype=float)
    if X.ndim == 1:
        X = X.reshape(-1, 1)
    Z = np.asarray(Z, dtype=float)
    if Z.ndim == 1:
        Z = Z.reshape(-1, 1)
    n = len(y)
    X_exog = np.ones((n, 1))
    X_all = np.hstack([X_exog, X])
    Z_all = np.hstack([X_exog, Z])
    ZTZ_inv = np.linalg.inv(Z_all.T @ Z_all)
    Pz = Z_all @ ZTZ_inv @ Z_all.T
    X_hat = Pz @ X_all
    beta = np.linalg.solve(X_all.T @ X_hat, X_hat.T @ y)
    resid = y - X_all @ beta
    XtX_inv = np.linalg.inv(X_all.T @ X_hat)
    vcov = _cluster_vcov(X_hat, resid, np.asarray(cluster), XtX_inv)
    se = np.sqrt(np.diag(vcov))

    # First-stage diagnostics
    F_stats = []
    for j in range(1, X_all.shape[1]):
        dep = X_all[:, j]
        beta_fs = np.linalg.lstsq(Z_all, dep, rcond=None)[0]
        fitted = Z_all @ beta_fs
        F = _f_stat(dep, fitted, Z_all.shape[1] - 1, n - Z_all.shape[1])
        F_stats.append(F)
    F_first = float(min(F_stats)) if F_stats else np.nan
    KP_rk = float(F_first * (Z_all.shape[1] - 1)) if F_stats else np.nan

    # Anderson-Rubin test for beta=0 (slope coefficients)
    if X.shape[1] == 1:
        ar_stat, ar_p = _anderson_rubin(y, X, X_exog, Z, 0.0)
        ar_ci = _ar_confidence_interval(y, X, X_exog, Z, beta[1], grid=201, alpha=0.05)
    else:
        ar_stat, ar_p, ar_ci = np.nan, 1.0, (np.nan, np.nan)

    liml_beta = _liml(y, X, X_exog, Z)

    return {
        'beta': beta,
        'se': se,
        'vcov': vcov,
        'F_first': F_first,
        'KP_rk': KP_rk,
        'LIML': liml_beta,
        'AR_stat': ar_stat,
        'AR_p': ar_p,
        'AR_CI': ar_ci,
    }


def anderson_rubin(y, X, Z):
    ar_stat, ar_p = _anderson_rubin(y, X[:, None] if X.ndim == 1 else X, np.ones((len(y), 1)), Z, 0.0)
    return ar_p


def liml(y, X, Z):
    return _liml(y, X[:, None] if X.ndim == 1 else X, np.ones((len(y), 1)), Z)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _cluster_vcov(X, resid, clusters, XtX_inv):
    clusters = np.asarray(clusters)
    if clusters.ndim == 0:
        clusters = clusters.reshape(-1, 1)
    if clusters.dtype == object:
        clusters = np.array(list(clusters), dtype=float)
    unique = np.unique(clusters, axis=0)
    n, k = X.shape
    if unique.shape[0] <= 1:
        return np.zeros((k, k))
    S = np.zeros((k, k))
    for g in unique:
        idx = np.all(clusters == g, axis=1) if clusters.ndim == 2 else (clusters == g)
        if not np.any(idx):
            continue
        Xg = X[idx]
        ug = resid[idx]
        score = Xg.T @ ug
        S += np.outer(score, score)
    scale = unique.shape[0] / (unique.shape[0] - 1)
    scale *= (n - 1) / (n - k)
    return XtX_inv @ S @ XtX_inv * scale


def _double_demean(v, unit_idx, time_idx):
    v = np.asarray(v, dtype=float).reshape(-1)
    grand = v.mean()
    unit_counts = np.bincount(unit_idx, minlength=unit_idx.max() + 1)
    time_counts = np.bincount(time_idx, minlength=time_idx.max() + 1)
    unit_sums = np.bincount(unit_idx, weights=v, minlength=unit_counts.size)
    time_sums = np.bincount(time_idx, weights=v, minlength=time_counts.size)
    unit_means = np.divide(unit_sums, unit_counts, out=np.zeros_like(unit_sums), where=unit_counts > 0)
    time_means = np.divide(time_sums, time_counts, out=np.zeros_like(time_sums), where=time_counts > 0)
    return v - unit_means[unit_idx] - time_means[time_idx] + grand


def _f_stat(y, fitted, df_num, df_den):
    if df_num <= 0 or df_den <= 0:
        return float('inf')
    y = np.asarray(y, dtype=float)
    fitted = np.asarray(fitted, dtype=float)
    tss = np.sum((y - y.mean()) ** 2)
    rss = np.sum((y - fitted) ** 2)
    if tss <= 1e-12:
        return 0.0
    r2 = 1 - rss / tss
    return float((r2 / df_num) / ((1 - r2) / df_den))


def _anderson_rubin(y, X, X_exog, Z, beta0):
    y = np.asarray(y, dtype=float)
    X = np.asarray(X, dtype=float)
    if X.ndim == 1:
        X = X.reshape(-1, 1)
    Z = np.asarray(Z, dtype=float)
    if Z.ndim == 1:
        Z = Z.reshape(-1, 1)
    n = len(y)
    beta0 = np.atleast_1d(beta0)
    if beta0.size != X.shape[1]:
        beta0 = np.repeat(beta0, X.shape[1])
    y_tilde = y - X @ beta0
    Z_full = np.hstack([X_exog, Z])
    beta = np.linalg.lstsq(Z_full, y_tilde, rcond=None)[0]
    fitted = Z_full @ beta
    F = _f_stat(y_tilde, fitted, Z.shape[1], n - Z_full.shape[1])
    p = float(stats.f.sf(F, Z.shape[1], max(n - Z_full.shape[1], 1)))
    return F, p


def _ar_confidence_interval(y, X, X_exog, Z, center, grid=201, alpha=0.05):
    span = 4.0
    grid_vals = np.linspace(center - span, center + span, grid)
    accept = []
    for b0 in grid_vals:
        _, p = _anderson_rubin(y, X, X_exog, Z, b0)
        if p > alpha:
            accept.append(b0)
    if not accept:
        return (np.nan, np.nan)
    return (min(accept), max(accept))


def _liml(y, X, X_exog, Z):
    y = np.asarray(y, dtype=float)
    if X.ndim == 1:
        X = X.reshape(-1, 1)
    Z = np.asarray(Z, dtype=float)
    if Z.ndim == 1:
        Z = Z.reshape(-1, 1)
    X_all = np.hstack([X_exog, X])
    Z_all = np.hstack([X_exog, Z])
    ZTZ_inv = np.linalg.inv(Z_all.T @ Z_all)
    Pz = Z_all @ ZTZ_inv @ Z_all.T
    beta = np.linalg.solve(X_all.T @ Pz @ X_all, X_all.T @ Pz @ y)
    return beta
