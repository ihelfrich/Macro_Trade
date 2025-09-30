import numpy as np
import pandas as pd

from src.empirics.utils import sun_abraham, iv2sls_cluster


def test_sun_abraham_clean_dgp():
    n_units = 20
    n_periods = 10
    units = np.arange(n_units)
    times = np.arange(n_periods)
    treat_times = {i: 5 for i in range(10)}
    treat_times.update({i: 7 for i in range(10, 15)})

    rng = np.random.default_rng(0)
    rows = []
    for i in units:
        g = treat_times.get(i, np.inf)
        for t in times:
            treated = 1 if t >= g else 0
            y = 0.1 * i + 0.05 * t + treated * 1.0 + rng.normal(scale=1e-3)
            rows.append({'i': i, 't': t, 'D': treated, 'y': y})
    panel = pd.DataFrame(rows)

    res = sun_abraham(panel)
    assert res['pretrend_p'] > 0.01
    assert (res['table'].loc[res['table']['rel_time'] < 0, 'beta'].abs() < 1e-2).all()
    table = res['table']
    rel0 = table.loc[table['rel_time'] == 0, 'beta'].iloc[0]
    assert np.isclose(rel0, 1.0, atol=1e-3)


def _simulate_iv(strength):
    rng = np.random.default_rng(0)
    n = 400
    z1 = rng.normal(size=n)
    z2 = rng.normal(size=n)
    u = rng.normal(scale=0.5, size=n)
    X = strength * z1 + strength * 0.5 * z2 + u
    eps = rng.normal(scale=0.5, size=n)
    y = 2.0 * X + 0.3 * u + eps
    Z = np.column_stack([z1, z2])
    cluster = np.floor(np.linspace(0, 19, n)).astype(int)
    return y, X, Z, cluster


def test_iv_diagnostics():
    y, X, Z, cluster = _simulate_iv(strength=0.8)
    res = iv2sls_cluster(y, X, Z, cluster)
    assert res['F_first'] > 10
    assert res['AR_p'] < 0.05
    assert res['AR_CI'][0] < 2.0 < res['AR_CI'][1]

    y_w, X_w, Z_w, cluster_w = _simulate_iv(strength=0.01)
    res_weak = iv2sls_cluster(y_w, X_w, Z_w, cluster_w)
    assert res_weak['F_first'] < 10
    assert res_weak['AR_p'] > 0.05
