"""General-equilibrium solvers for the trade model."""

from __future__ import annotations

import math
from typing import Dict

import numpy as np
from scipy.sparse import identity, issparse
from scipy.sparse.linalg import splu

from src.trade.io import compute_domar


def solve_ge(
    p0: np.ndarray,
    wedges: np.ndarray,
    A,
    sigma_origin: float,
    tol: float = 1e-10,
    maxit: int = 2000,
    damp: float = 0.5,
    linear: bool = False,
) -> Dict[str, object]:
    """Solve the global GE price system with optional linearised mode.

    Parameters
    ----------
    p0 : ndarray, shape (K,)
        Baseline value-added prices.  These are *not* gross prices.
    wedges : ndarray, shape (K,)
        Log wedges applied to value-added prices.  The perturbed
        value-added vector is ``p0 * exp(wedges)``.
    A : ndarray or sparse matrix, shape (K, K)
        Input-output coefficients with spectral radius strictly below one.
        Columns correspond to the purchasing sector.
    sigma_origin : float
        Reserved for Armington extensions (unused but kept for API stability).
    tol : float, default 1e-10
        Stopping tolerance for the non-linear solver expressed in sup-norm.
    maxit : int, default 2000
        Maximum number of Newton/fixed-point iterations.
    damp : float, default 0.5
        Damping parameter applied to Newton steps to aid convergence.
    linear : bool, default False
        If ``True`` return the first-order solution ``d log p = (I - A.T)^{-1} d log v``.

    Returns
    -------
    dict
        Contains ``p`` (gross prices), ``domar`` weights, ``shares`` (value-added and
        gross-output shares), ``residuals`` (goods-market sup-norm, Walras-law residual,
        and final step size), a convergence flag, and iteration count.
    """

    del sigma_origin  # reserved argument

    A = _asarray_or_sparse(A)
    K = len(p0)
    p0 = np.asarray(p0, dtype=float).reshape(K)
    wedges = np.asarray(wedges, dtype=float).reshape(K)
    v = p0 * np.exp(wedges)

    M = _build_price_matrix(A)
    solver = _factorize(M)

    baseline_prices = solver(p0)

    if linear:
        dlog_p = solver(wedges)
        p = baseline_prices * np.exp(dlog_p)
        residual_vec = M @ p - v
        domar = compute_domar(A, v)
        shares = {
            'value_added': v / v.sum(),
            'gross_output': p / p.sum(),
        }
        residuals = {
            'goods': float(np.linalg.norm(residual_vec, ord=np.inf)),
            'walras': float(abs(residual_vec.sum())),
            'delta': float(np.linalg.norm(dlog_p, ord=np.inf)),
        }
        return {
            'p': p,
            'domar': domar,
            'shares': shares,
            'residuals': residuals,
            'converged': True,
            'iters': 1,
        }

    p = baseline_prices.copy()
    converged = False
    delta_norm = math.inf

    for it in range(1, maxit + 1):
        residual_vec = M @ p - v
        goods_res = np.linalg.norm(residual_vec, ord=np.inf)
        if goods_res < tol:
            converged = True
            delta_norm = 0.0
            break

        step = solver(-residual_vec)
        delta = damp * step
        delta_norm = np.linalg.norm(delta, ord=np.inf)
        p = np.maximum(p + delta, 1e-12)

        if delta_norm < tol:
            converged = True
            break

    residual_vec = M @ p - v
    goods_res = np.linalg.norm(residual_vec, ord=np.inf)
    walras_res = abs(residual_vec.sum())

    domar = compute_domar(A, v)
    shares = {
        'value_added': v / v.sum(),
        'gross_output': p / p.sum(),
    }

    residuals = {
        'goods': float(goods_res),
        'walras': float(walras_res),
        'delta': float(delta_norm),
    }

    return {
        'p': p,
        'domar': domar,
        'shares': shares,
        'residuals': residuals,
        'converged': bool(converged),
        'iters': it if converged else maxit,
    }


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _asarray_or_sparse(A):
    if issparse(A):
        return A.tocsr()
    return np.asarray(A, dtype=float)


def _build_price_matrix(A):
    if issparse(A):
        K = A.shape[0]
        return identity(K, format='csc') - A.transpose().tocsc()
    return np.eye(A.shape[0]) - A.T


def _factorize(M):
    if issparse(M):
        lu = splu(M)
        return lambda b: lu.solve(np.asarray(b, dtype=float))

    Minv = np.linalg.inv(M)
    return lambda b: Minv @ np.asarray(b, dtype=float)

