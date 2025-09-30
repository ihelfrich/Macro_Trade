import numpy as np
from scipy.sparse import csr_matrix

from src.trade.ge import solve_ge
from src.trade.welfare import (
    build_network_hessian,
    welfare_first_order,
    welfare_second_order,
)


def _setup():
    A = csr_matrix(
        np.array(
            [
                [0.1, 0.18, 0.0],
                [0.05, 0.1, 0.12],
                [0.03, 0.2, 0.08],
            ]
        )
    )
    v0 = np.ones(3)
    base = solve_ge(v0, np.zeros_like(v0), A, sigma_origin=4.0, linear=False)
    return A, v0, base


def test_first_and_second_order_align_for_small_shocks():
    A, v0, base = _setup()
    tiny_wedge = np.array([1e-4, -1e-4, 8e-5])
    res_tiny = solve_ge(v0, tiny_wedge, A, sigma_origin=4.0, linear=False)
    dlog_p = np.log(res_tiny['p'] / base['p'])

    H = build_network_hessian(A, np.full(3, 0.2))

    w1 = welfare_first_order(dlog_p, base['domar'])
    w2 = welfare_second_order(dlog_p, base['domar'], H)

    assert np.isclose(w1, w2, atol=1e-8)


def test_second_order_tightens_against_ge():
    A, v0, base = _setup()
    wedge = np.array([0.05, -0.04, 0.03])
    res = solve_ge(v0, wedge, A, sigma_origin=4.0, linear=False)
    dlog_p = np.log(res['p'] / base['p'])

    H = build_network_hessian(A, np.full(3, 0.2))

    w1 = welfare_first_order(dlog_p, base['domar'])
    w2 = welfare_second_order(dlog_p, base['domar'], H)
    w_exact = -float(res['domar'] @ dlog_p)

    assert abs(w2 - w_exact) < abs(w1 - w_exact)
