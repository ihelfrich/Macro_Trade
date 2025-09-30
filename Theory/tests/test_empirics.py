import sys
import os
import numpy as np
import pandas as pd

from src.empirics.exposure_ssa import build_panel, event_study
from src.empirics.exposure_iv import run_iv
from src.empirics.utils import ols, ols_cluster

def test_event_study_pretrends():
    panel = build_panel(100, 5, 5)
    res = event_study(panel)
    assert res['pretrend_p'] > 0.10

def test_iv_recovers_truth():
    n = 100
    beta_true = 2.0
    rng = np.random.default_rng(0)
    Z = rng.standard_normal((n, 2)) # Two instruments
    cluster = rng.integers(0, 10, n)
    u = rng.standard_normal(n)
    X = 0.5 * Z[:,0] + u # Endogenous variable depends on one instrument
    y = beta_true * X + 0.2 * u + rng.standard_normal(n) # Confounded outcome
    
    res = run_iv(y, X, Z, cluster)
    
    assert np.isclose(res['beta'][1], beta_true, atol=0.5)
    assert res['F_first'] >= 10 # Strong IV
    assert res['AR_p'] < 0.05 # Should reject for valid instrument if treatment effect is non-zero

def test_clustered_se():
    n = 100
    rng = np.random.default_rng(1)
    X = rng.standard_normal((n, 2))
    y = rng.standard_normal(n)
    cluster = rng.integers(0, 10, n)
    
    _, se_homo, _, _, _, _ = ols(y, X)
    _, se_cluster, _, _, _ = ols_cluster(y, X, cluster)
    
    assert not np.allclose(se_cluster, se_homo)