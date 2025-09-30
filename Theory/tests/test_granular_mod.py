import numpy as np
from src.empirics.granular import compute_exposure_concentration, estimate_convexity


def test_compute_exposure_concentration():
    shares = np.array([0.1, 0.2, 0.3, 0.4])
    shocks = np.array([0.01, 0.02, 0.03, 0.04])
    s, hhi = compute_exposure_concentration(shares, shocks)
    assert np.isclose(s, 0.03)
    assert np.isclose(hhi, 0.3)


def test_estimate_convexity():
    s = np.linspace(0, 1, 200)
    loss = 0.1 * s + 0.5 * s**2
    res = estimate_convexity(loss, s)
    assert np.isclose(res['curvature'], 0.5, atol=1e-3)
    assert res['ci'][0] < 0.5 < res['ci'][1]
