import numpy as np
from scipy.sparse import csr_matrix

from src.trade.ge import solve_ge


def _toy_matrix():
    return csr_matrix(
        np.array(
            [
                [0.1, 0.12, 0.02],
                [0.05, 0.08, 0.07],
                [0.03, 0.10, 0.05],
            ]
        )
    )


def test_solve_ge_converges_under_alternative_damping():
    v0 = np.ones(3)
    A = _toy_matrix()
    wedges = np.array([0.02, -0.015, 0.01])

    for damp in (0.3, 0.85):
        res = solve_ge(v0, wedges, A, sigma_origin=4.0, damp=damp, linear=False)
        assert res['converged']
        assert res['residuals']['goods'] < 1e-8


def test_solve_ge_linear_small_shock_matches_non_linear_with_low_damp():
    v0 = np.ones(3)
    A = _toy_matrix()
    tiny = np.array([1e-4, -1.2e-4, 9e-5])

    res_low_damp = solve_ge(v0, tiny, A, sigma_origin=4.0, damp=0.3, linear=False)
    res_linear = solve_ge(v0, tiny, A, sigma_origin=4.0, linear=True)

    assert np.allclose(res_low_damp['p'], res_linear['p'], rtol=5e-4, atol=5e-5)
