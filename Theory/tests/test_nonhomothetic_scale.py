
import numpy as np
from src.trade.nonhomothetic import welfare_ev_ratio, check_luxury_share

def test_luxury_share_at_scale():
    N = 10
    K = 2
    y_grid = np.linspace(100, 1000, N)
    p = np.array([1.0, 1.0])
    alpha = np.tile(np.array([0.3, 0.7]), (N, 1)) # Good 2 is luxury
    gamma = np.tile(np.array([10.0, 10.0]), (N, 1))
    assert check_luxury_share(y_grid, p, alpha, gamma)

def test_ev_ratio_monotonicity():
    N = 10
    K = 2
    y0 = np.linspace(100, 1000, N)
    p0 = np.array([1.0, 1.0])
    p1_low = np.array([1.0, 1.1])
    p1_high = np.array([1.0, 1.2])
    alpha = np.tile(np.array([0.5, 0.5]), (N, 1))
    gamma = np.tile(np.array([10.0, 10.0]), (N, 1))

    ev_low = welfare_ev_ratio(y0, p0, p1_low, alpha, gamma)
    ev_high = welfare_ev_ratio(y0, p0, p1_high, alpha, gamma)
    assert np.all(ev_high > ev_low)
