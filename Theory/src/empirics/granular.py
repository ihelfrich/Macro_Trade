"""Granular exposure diagnostics for trade shocks."""

from __future__ import annotations

import numpy as np
from numpy.linalg import lstsq


def compute_exposure_concentration(shares, shocks):
    """Return aggregate exposure and Herfindahl index for firm shocks."""

    shares = np.asarray(shares, dtype=float)
    shocks = np.asarray(shocks, dtype=float)
    if shares.shape != shocks.shape:
        raise ValueError("shares and shocks must have matching shapes")
    total = shares.sum()
    if total <= 0:
        raise ValueError("shares must sum to a positive number")
    weights = shares / total
    exposure = float(np.dot(weights, shocks))
    hhi = float(np.dot(weights, weights))
    return exposure, hhi


def estimate_convexity(loss, s):
    """Estimate quadratic convexity of welfare loss as a function of exposure."""

    loss = np.asarray(loss, dtype=float)
    s = np.asarray(s, dtype=float)
    if loss.shape != s.shape:
        raise ValueError("loss and exposure arrays must align")
    X = np.column_stack([np.ones_like(s), s, s**2])
    coeffs, _, _, _ = lstsq(X, loss, rcond=None)
    resid = loss - X @ coeffs
    n, k = X.shape
    XtX_inv = np.linalg.inv(X.T @ X)

    S = np.zeros((k, k))
    for i in range(n):
        xi = X[i : i + 1, :]
        S += resid[i] ** 2 * (xi.T @ xi)
    if n > k:
        S *= n / (n - k)

    vcov = XtX_inv @ S @ XtX_inv
    se = np.sqrt(np.diag(vcov))
    curvature = coeffs[2]
    se_curv = se[2]
    ci = (
        float(curvature - 1.96 * se_curv),
        float(curvature + 1.96 * se_curv),
    )
    return {
        'curvature': float(curvature),
        'se': float(se_curv),
        'ci': ci,
        'beta': coeffs,
        'vcov': vcov,
    }
