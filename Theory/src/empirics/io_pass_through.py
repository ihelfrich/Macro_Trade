import numpy as np
import pandas as pd
from src.empirics.utils import ols
from src.trade.io import io_prices
from src.common.io import write_table

def pass_through(panel):
    A = panel['A'].values[0] # Assuming A is the same for all
    shock = panel['shock'].values
    dlog_va = panel['dlog_va'].values
    
    dlog_p_model = io_prices(A, shock)
    beta, se, _, _, _, _ = ols(dlog_va, dlog_p_model)
    
    r2 = 1 - np.sum((dlog_va - beta[0] - beta[1]*dlog_p_model)**2) / np.sum((dlog_va - np.mean(dlog_va))**2)
    
    table = pd.DataFrame({'beta': beta, 'se': se, 'r2': r2})
    write_table(table, 'tables/io_pass_through.csv')
    
    return {'beta': beta, 'se': se, 'r2': r2}