"""Welfare accounting following Baqaee–Farhi style network expansions."""

from __future__ import annotations

import numpy as np
from scipy.sparse import identity, issparse
from scipy.sparse.linalg import splu


def welfare_first_order(dlog_p, domar) -> float:
    """First-order welfare change ``d log W`` from price shocks."""

    dlog_p = np.asarray(dlog_p, dtype=float)
    domar = np.asarray(domar, dtype=float)
    return -float(domar @ dlog_p)


def welfare_second_order(dlog_p, domar, Hess) -> float:
    """Second-order welfare change including curvature corrections."""

    dlog_p = np.asarray(dlog_p, dtype=float)
    domar = np.asarray(domar, dtype=float)
    Hess = np.asarray(Hess, dtype=float)
    quad = float(dlog_p.T @ Hess @ dlog_p)
    return -float(domar @ dlog_p) - 0.5 * quad


def build_network_hessian(A, elasticities):
    r"""Construct the Baqaee–Farhi network Hessian.

    The second-order term for real income shocks can be expressed as

    .. math:: \tfrac{1}{2} d\log p' H d\log p

    where ``H = L' diag(ε) L`` and ``L = (I - A^T)^{-1}`` is the
    Leontief inverse of the price system.  ``elasticities`` collects
    sectoral curvature objects (e.g. demand or supply elasticities).

    Parameters
    ----------
    A : ndarray or sparse matrix, shape (K, K)
        Input coefficients with spectral radius strictly below one.
    elasticities : ndarray, shape (K,)
        Non-negative curvature terms.  Larger values imply stronger
        second-order amplification.

    Returns
    -------
    ndarray, shape (K, K)
        Symmetric positive semi-definite Hessian tightening welfare bounds.
    """

    A = _asarray_or_sparse(A)
    eps = np.asarray(elasticities, dtype=float)
    K = eps.shape[0]

    if eps.ndim != 1 or A.shape[0] != K:
        raise ValueError("Elasticities must be a 1-D array aligned with A.")

    L = _compute_leontief_inverse(A)
    diag_eps = np.diag(eps)
    H = L.T @ diag_eps @ L
    # Numerical symmetrisation guards against round-off
    return 0.5 * (H + H.T)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _asarray_or_sparse(A):
    if issparse(A):
        return A.tocsr()
    return np.asarray(A, dtype=float)


def _compute_leontief_inverse(A):
    if issparse(A):
        K = A.shape[0]
        M = identity(K, format='csc') - A.transpose().tocsc()
        lu = splu(M)
        e = np.eye(K)
        cols = [lu.solve(e[:, i]) for i in range(K)]
        return np.column_stack(cols)

    M = np.eye(A.shape[0]) - A.T
    return np.linalg.inv(M)
