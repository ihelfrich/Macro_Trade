"""Input-output utilities for general-equilibrium calculations."""

from __future__ import annotations

import numpy as np
from scipy.sparse import identity, issparse
from scipy.sparse.linalg import splu


def io_prices(A, sector_price_shock):
    """Small-change Leontief price pass-through.

    Parameters
    ----------
    A : ndarray or sparse matrix, shape (K, K)
        Input coefficient matrix with spectral radius strictly below one.
        Columns correspond to purchasing sectors, so ``A.T`` enters the
        price system.
    sector_price_shock : ndarray, shape (K,)
        Exogenous log price wedges on value added.

    Returns
    -------
    ndarray
        Log price response ``d log p`` solving ``(I - A.T) dlog p = shock``.
    """

    A = _asarray_or_sparse(A)
    K = A.shape[0]
    shock = np.asarray(sector_price_shock, dtype=float).reshape(K)
    M = _build_m_price_operator(A)

    if issparse(M):
        solver = splu(M)
        return solver.solve(shock)

    return np.linalg.solve(M, shock)


def domar_weights(value_added_shares):
    """Legacy helper returning normalized Domar weights.

    Notes
    -----
    For backwards compatibility tests keep using this thin wrapper.
    New code should rely on :func:`compute_domar` so that gross-output
    feedback is handled rigorously.
    """

    shares = np.asarray(value_added_shares, dtype=float)
    if shares.ndim != 1:
        shares = shares.reshape(-1)
    total = shares.sum()
    if total <= 0:
        raise ValueError("Value-added shares must sum to a positive number.")
    return shares / total


def compute_domar(A, VA):
    r"""Compute Domar weights from an IO matrix and value-added vector.

    The Domar weight of sector ``i`` equals its gross-output share
    in GDP, i.e. ``ω_i = p_i x_i / \text{GDP}``.  Under a Leontief
    production network this can be recovered from the value-added vector
    ``VA`` and the technology matrix ``A`` by solving the linear system

    .. math:: (I - A^\top)\,ω = s,

    where ``s`` are value-added shares ``VA / Σ VA``.  When ``I - A^T``
    is numerically singular we fall back on the right Perron vector of
    ``A^T`` (profitable industries) scaled to unit sum.

    Parameters
    ----------
    A : ndarray or sparse matrix, shape (K, K)
        Input coefficients with spectral radius below one.
    VA : ndarray, shape (K,)
        Value added in nominal terms (need not be normalized).

    Returns
    -------
    ndarray, shape (K,)
        Domar weights summing to one.
    """

    A = _asarray_or_sparse(A)
    K = A.shape[0]
    va = np.asarray(VA, dtype=float).reshape(K)
    total_va = va.sum()
    if total_va <= 0:
        raise ValueError("Value-added vector must sum to a positive number.")
    s = va / total_va

    M = _build_m_price_operator(A)

    try:
        if issparse(M):
            solver = splu(M)
            domar = solver.solve(s)
        else:
            domar = np.linalg.solve(M, s)
    except Exception:  # pragma: no cover - rare fallback path
        domar = _perron_fallback(A)
        domar /= domar.sum()
        return domar

    domar = np.maximum(domar, 0.0)
    total = domar.sum()
    if total <= 0:
        domar = _perron_fallback(A)
        domar /= domar.sum()
        return domar

    domar /= total
    return domar


def welfare_from_prices(dlog_p, domar_w):
    """First-order welfare change from price movements."""

    return -float(np.asarray(dlog_p, dtype=float) @ np.asarray(domar_w, dtype=float))


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _asarray_or_sparse(A):
    if issparse(A):
        return A.tocsr()
    return np.asarray(A, dtype=float)


def _build_m_price_operator(A):
    """Return the price system matrix ``I - A.T`` in matching storage."""

    if issparse(A):
        K = A.shape[0]
        return identity(K, format='csc') - A.transpose().tocsc()
    return np.eye(A.shape[0]) - A.T


def _perron_fallback(A):
    """Compute the dominant right eigenvector of ``A.T`` as a fallback."""

    if issparse(A):
        from scipy.sparse.linalg import eigs

        vec = eigs(A.transpose(), k=1, which='LR', return_eigenvectors=True)[1][:, 0].real
    else:
        _, vecs = np.linalg.eig(np.asarray(A, dtype=float).T)
        vec = vecs[:, 0].real
    vec = np.abs(vec)
    if vec.sum() == 0:
        vec = np.ones_like(vec)
    return vec
