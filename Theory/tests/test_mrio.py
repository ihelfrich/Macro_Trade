from pathlib import Path

import numpy as np
from scipy.sparse import csr_matrix

from src.data.mrio_loader import load_mrio
from src.common.sparse import sparse_leontief


def test_mrio_loader():
    A_csr, VA, Y, sectors, countries = load_mrio(source='SYNTH')
    K = len(sectors) * len(countries)
    assert A_csr.shape == (K, K)
    assert VA.shape == (K,)
    assert Y.shape == (K,)
    assert len(sectors) == 10
    assert len(countries) == 3
    # Spectral radius < 1 implies diagonal dominance -> column sums < 1
    assert np.all(A_csr.toarray().sum(axis=0) < 1.0)


def test_mrio_loader_oecd_sml():
    A_csr, VA, Y, sectors, countries = load_mrio(
        source='OECD_SML', year=2017, path=Path('2017-2022_SML')
    )
    K = len(sectors) * len(countries)
    assert len(sectors) == 50
    assert len(countries) >= 80
    assert A_csr.shape == (K, K)
    assert VA.shape == (K,)
    assert Y.shape == (K,)
    assert np.all(np.isfinite(A_csr.data))
    assert np.isfinite(VA).all()
    assert np.isfinite(Y).all()
    assert VA.sum() > 0
    assert Y.sum() >= 0


def test_sparse_leontief():
    A_dense = np.array([[0.1, 0.2], [0.3, 0.1]])
    A_csr = csr_matrix(A_dense)
    x = np.array([1.0, 1.0])

    I = np.eye(2)
    leontief_dense = np.linalg.inv(I - A_dense) @ x

    leontief_sparse = sparse_leontief(A_csr, x)

    assert np.allclose(leontief_dense, leontief_sparse, atol=1e-6)


def test_sparse_leontief_with_ilu():
    A_dense = np.array([[0.05, 0.04, 0.02], [0.03, 0.02, 0.04], [0.01, 0.05, 0.02]])
    A_csr = csr_matrix(A_dense)
    x = np.array([0.5, 0.75, 1.0])

    expected = np.linalg.solve(np.eye(3) - A_dense, x)
    result = sparse_leontief(A_csr, x, precond='ilu')

    assert np.allclose(expected, result, atol=1e-8)
