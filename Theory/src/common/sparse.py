"""Sparse linear algebra helpers tailored to MRIO solves."""

from __future__ import annotations

import numpy as np
from scipy.sparse import csr_matrix, identity, issparse
from scipy.sparse.linalg import LinearOperator, gmres, splu


def sparse_leontief(
    A_csr: csr_matrix,
    x: np.ndarray,
    rtol: float = 1e-10,
    maxit: int = 20000,
    precond: str | None = "jacobi",
) -> np.ndarray:
    """Solve ``(I - A)^{-1} x`` using GMRES with optional preconditioning.

    Parameters
    ----------
    A_csr : csr_matrix
        Technology matrix with spectral radius strictly below one.
    x : ndarray
        Vector (or 1-D array) representing final demand/value-added shocks.
    rtol : float, default 1e-10
        Relative tolerance passed to GMRES.
    maxit : int, default 20000
        Maximum number of iterations.
    precond : {"jacobi", "ilu", None}
        Choice of left preconditioner.  ``"jacobi"`` uses the diagonal of
        ``I - A``; ``"ilu"`` falls back to an LU factorisation if available.

    Returns
    -------
    ndarray
        Solution vector ``y`` satisfying ``(I - A) y = x``.
    """

    if not issparse(A_csr):
        A_csr = csr_matrix(A_csr)

    x = np.asarray(x, dtype=float).reshape(-1)
    K = A_csr.shape[0]
    if A_csr.shape[1] != K:
        raise ValueError("A_csr must be square.")
    if x.shape[0] != K:
        raise ValueError("Vector x must have length matching A_csr.")

    M = identity(K, format="csr") - A_csr

    preconditioner = None
    if precond == "jacobi":
        diag = M.diagonal().copy()
        diag[np.abs(diag) < 1e-12] = 1.0
        inv_diag = 1.0 / diag

        def _jacobi(vec):
            return inv_diag * vec

        preconditioner = LinearOperator((K, K), matvec=_jacobi)
    elif precond == "ilu":
        try:
            lu = splu(M.tocsc())
        except Exception as exc:  # pragma: no cover - rare failure
            raise RuntimeError("ILU preconditioner failed") from exc

        preconditioner = LinearOperator((K, K), matvec=lu.solve)
    elif precond is not None:
        raise ValueError("precond must be 'jacobi', 'ilu', or None")

    sol, info = gmres(M, x, M=preconditioner, rtol=rtol, maxiter=maxit, atol=0.0)

    if info != 0:
        raise RuntimeError(f"GMRES did not converge: info={info}")

    return sol
