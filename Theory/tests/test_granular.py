import numpy as np

from src.trade.granular import granular_welfare_ratio
from src.empirics.utils import ols

def test_granular_properties():
    psi = 0.5
    epsilon = 4.0
    zeta = 2.0

    # Test s=0 case
    w_s0 = granular_welfare_ratio(0.0, zeta, epsilon, psi)
    assert np.isclose(w_s0, (1 - psi)**(1/epsilon))

    # Test convexity of the loss
    s_grid = np.linspace(0, 0.5, 10)
    loss_ratios = 1 - np.array([granular_welfare_ratio(s, zeta, epsilon, psi) for s in s_grid])
    assert np.all(np.diff(loss_ratios) > 0)
    assert np.all(np.diff(loss_ratios, 2) > 0)

    # Regression-based convexity check
    s2 = s_grid**2
    X = np.column_stack([s_grid, s2])
    beta, se, resid, vcov, n, k = ols(loss_ratios, X)
    assert beta[2] > 0