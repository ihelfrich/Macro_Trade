import numpy as np
import pandas as pd
from src.empirics.utils import iv2sls_cluster, weak_iv_fstat, anderson_rubin
from src.common.io import write_table

def run_iv(y, X, Z, cluster):
    res_iv = iv2sls_cluster(y, X, Z, cluster)
    
    table = pd.DataFrame({'beta': res_iv['beta'], 'se': res_iv['se'], 't': res_iv['beta']/res_iv['se'], 'p': 0.0, 'F_first': res_iv['F_first'], 'AR_p': res_iv['AR_p']})
    write_table(table, 'tables/iv_main.csv')
    
    return res_iv