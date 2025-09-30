import numpy as np
import pandas as pd
from src.empirics.utils import ols_cluster
from src.trade.nonhomothetic import welfare_index
from src.common.io import write_table, write_fig
import matplotlib.pyplot as plt

def run_nh_dispersion_test(y0, p0, p1, alpha, gamma, luxury_exposure, cluster):
    n_households = len(y0)
    welfare_ratios = np.zeros(n_households)
    for i in range(n_households):
        welfare_ratios[i] = welfare_index(y0[i], p0, p1, np.array([alpha[i], 1-alpha[i]]), np.array([gamma[i], gamma[i]]))
        
    dlog_W = np.log(welfare_ratios)
    var_change = np.var(dlog_W)
    
    beta, se = ols_cluster(dlog_W, luxury_exposure, cluster)
    
    table_reg = pd.DataFrame({'beta': beta, 'se': se})
    write_table(table_reg, 'tables/nh_reg.csv')
    
    table_var = pd.DataFrame({'var_change': [var_change]})
    write_table(table_var, 'tables/nh_varchange.csv')
    
    # Create histogram
    fig, ax = plt.subplots()
    ax.hist(dlog_W, bins=20)
    ax.set_xlabel('log welfare change')
    ax.set_ylabel('Frequency')
    write_fig(fig, 'figs/nh_hist.png')
    
    return {'var_change': var_change, 'beta': beta, 'se': se}