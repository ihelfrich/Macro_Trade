import numpy as np
from scipy.sparse import csr_matrix

from src.trade.ge import solve_ge


def _toy_matrix():
    return csr_matrix(
        np.array(
            [
                [0.1, 0.2, 0.0],
                [0.05, 0.1, 0.15],
                [0.02, 0.25, 0.1],
            ]
        )
    )


def test_ge_zero_wedge_identity():
    K = 3
    v0 = np.ones(K)
    A = _toy_matrix()

    res_linear = solve_ge(v0, np.zeros(K), A, sigma_origin=4.0, linear=True)
    res_exact = solve_ge(v0, np.zeros(K), A, sigma_origin=4.0, linear=False)

    assert np.allclose(res_linear['p'], res_exact['p'], atol=1e-12)
    assert res_exact['converged']
    assert res_exact['residuals']['goods'] < 1e-12
    assert res_exact['residuals']['walras'] < 1e-12


def test_linearization_matches_small_shock():
    v0 = np.ones(3)
    A = _toy_matrix()
    wedges = np.array([1e-4, -2e-4, 1.5e-4])

    res_linear = solve_ge(v0, wedges, A, sigma_origin=4.0, linear=True)
    res_exact = solve_ge(v0, wedges, A, sigma_origin=4.0, linear=False)

    assert np.allclose(res_linear['p'], res_exact['p'], rtol=5e-4, atol=1e-6)
    assert res_linear['residuals']['goods'] < 5e-4
    assert res_linear['residuals']['walras'] < 1e-4


def test_newton_converges_and_residuals_small():
    v0 = np.ones(3)
    A = _toy_matrix()
    wedges = np.array([0.05, -0.04, 0.03])

    res = solve_ge(v0, wedges, A, sigma_origin=4.0, linear=False)

    assert res['converged']
    assert res['residuals']['goods'] < 1e-10
    assert res['residuals']['walras'] < 1e-8
    assert res['residuals']['delta'] < 1e-10
