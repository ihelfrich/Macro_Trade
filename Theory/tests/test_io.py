import numpy as np

from src.trade.io import io_prices, domar_weights, welfare_from_prices

def test_io_no_linkages():
    A = np.zeros((2, 2))
    shock = np.array([0.1, 0.05])
    dlog_p = io_prices(A, shock)
    assert np.allclose(dlog_p, shock)

    va_shares = np.array([0.5, 0.5])
    dw = domar_weights(va_shares)
    welfare_loss = welfare_from_prices(dlog_p, dw)
    assert np.isclose(welfare_loss, -0.075)

def test_io_monotonicity():
    shock = np.array([0.1, 0.0])
    losses = []
    rhos = np.linspace(0, 0.95, 5)
    for rho_scale in rhos:
        A = np.array([[0.2, 0.3], [0.4, 0.1]]) * rho_scale
        dlog_p = io_prices(A, shock)
        loss = welfare_from_prices(dlog_p, domar_weights([0.5, 0.5]))
        losses.append(loss)
    assert np.all(np.diff(losses) <= 0) # Losses should be increasing