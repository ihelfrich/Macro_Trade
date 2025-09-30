import numpy as np
import pandas as pd

from src.trade.nonhomothetic import (
    check_luxury_share,
    sg_demands,
    sg_expenditure,
    welfare_ev_ratio,
)
from src.empirics.engel import estimate_sg_from_budgets


def _stone_geary_synthetic(alpha, gamma, incomes, prices):
    incomes = np.asarray(incomes)
    prices = np.asarray(prices)
    alpha = np.asarray(alpha)
    gamma = np.asarray(gamma)
    subsistence_cost = prices @ gamma
    residual = incomes - subsistence_cost
    residual = residual.reshape(-1, 1)
    demands = gamma + (alpha * residual) / prices
    exp = demands * prices
    return exp


def test_vectorised_demands_and_expenditure():
    prices = np.array([1.0, 1.5])
    alpha = np.array([0.4, 0.6])
    gamma = np.array([5.0, 8.0])
    incomes = np.array([50.0, 60.0, 80.0])

    demands = sg_demands(incomes, prices, alpha, gamma)
    assert demands.shape == (3, 2)
    util = np.prod((demands - gamma) ** alpha, axis=1)
    exp = sg_expenditure(prices, util, alpha, gamma)
    assert np.allclose(exp, incomes)


def test_welfare_ev_ratio_monotone_in_price():
    y0 = np.array([100.0, 120.0])
    p0 = np.array([1.0, 1.0])
    alpha = np.array([[0.3, 0.7], [0.4, 0.6]])
    gamma = np.array([[10.0, 5.0], [8.0, 6.0]])

    p1 = np.array([1.0, 1.2])
    p2 = np.array([1.0, 1.4])

    ev1 = welfare_ev_ratio(y0, p0, p1, alpha, gamma)
    ev2 = welfare_ev_ratio(y0, p0, p2, alpha, gamma)

    assert np.all(ev1 >= 1.0)
    assert np.all(ev2 >= ev1)


def test_luxury_share_monotonicity():
    y_grid = np.linspace(100, 200, 5)
    p = np.array([1.0, 1.0])
    alpha = np.tile(np.array([0.3, 0.7]), (len(y_grid), 1))
    gamma = np.tile(np.array([10.0, 10.0]), (len(y_grid), 1))
    assert check_luxury_share(y_grid, p, alpha, gamma)


def test_estimate_sg_from_budgets():
    alpha_true = np.array([0.3, 0.7])
    gamma_true = np.array([8.0, 4.0])
    prices = np.array([1.0, 1.5])
    subsistence_cost = prices @ gamma_true
    incomes = np.linspace(subsistence_cost, 200, 40)

    exp = _stone_geary_synthetic(alpha_true, gamma_true, incomes, prices)
    df = pd.DataFrame(
        {
            "group": np.repeat("A", exp.shape[0] * exp.shape[1]),
            "income": np.tile(incomes, exp.shape[1]),
            "good": np.repeat(["g1", "g2"], exp.shape[0]),
            "expenditure": exp.T.reshape(-1),
            "price": np.repeat(prices, exp.shape[0]),
        }
    )

    alpha_hat, gamma_hat = estimate_sg_from_budgets(df)

    np.testing.assert_allclose(alpha_hat["A"], alpha_true, atol=5e-2)
    np.testing.assert_allclose(gamma_hat["A"], gamma_true, atol=1.0)
