
import numpy as np
import pandas as pd
from src.empirics.utils import ols_cluster
from src.common.io import write_table, write_fig
import matplotlib.pyplot as plt

def compute_exposure(shares, shocks):
    return shares @ shocks

def build_panel(N_units, T_pre, T_post, seed=42):
    np.random.seed(seed)
    n_periods = T_pre + T_post
    exposure = np.random.rand(N_units)
    y = np.random.randn(N_units, n_periods)
    for t in range(T_pre, n_periods):
        y[:, t] += 2.0 * exposure
    
    df = pd.DataFrame(y, columns=[f'y_{t}' for t in range(n_periods)])
    df['i'] = np.arange(N_units)
    df['exposure'] = exposure
    return pd.melt(df, id_vars=['i', 'exposure'], var_name='t', value_name='y')

def event_study(panel, dep='y', treat='exposure', unit='i', time='t', pre_L=4, post_L=4, cluster='i'):
    panel['t'] = panel['t'].str.replace('y_', '').astype(int)
    T_pre = pre_L + 1
    
    y = panel[dep].values
    X = np.zeros((len(panel), pre_L + post_L))
    
    for t in range(pre_L + post_L + 1):
        if t == pre_L: # Omit reference period
            continue
        col_idx = t if t < pre_L else t - 1
        mask = panel['t'] == t
        X[mask, col_idx] = panel[treat][mask]
        
    beta, se, vcov, n, k = ols_cluster(y, X, panel[cluster].values)
    
    # Pre-trend test (joint F-test on pre-trend coefficients)
    pre_trend_coefs = beta[1:pre_L+1]
    pre_trend_vcov = vcov[1:pre_L+1, 1:pre_L+1]
    f_stat = (pre_trend_coefs.T @ np.linalg.inv(pre_trend_vcov) @ pre_trend_coefs) / pre_L
    from scipy.stats import f
    pretrend_p = 1 - f.cdf(f_stat, pre_L, n - k)
    
    table = pd.DataFrame({'beta': beta[1:], 'se': se[1:]})
    
    # Create plot
    fig, ax = plt.subplots()
    periods = list(range(-pre_L, 0)) + list(range(1, post_L + 1))
    ax.errorbar(periods, beta[1:], yerr=se[1:], fmt='o')
    ax.axhline(0, color='black', linestyle='--')
    ax.axvline(-0.5, color='red', linestyle='--')
    write_fig(fig, 'figs/es_plot.png')
    
    return {'beta': beta, 'se': se, 'pretrend_p': pretrend_p, 'table': table}
