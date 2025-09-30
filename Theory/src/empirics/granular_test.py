import numpy as np
import pandas as pd
from src.empirics.utils import ols_cluster
from src.common.io import write_table

def run_granular_test(y, exposure, top_firm_share, cluster):
    interaction = exposure * top_firm_share
    X = np.column_stack([exposure, interaction])
    beta, se = ols_cluster(y, X, cluster)
    
    p_int = 0.0 # Placeholder for p-value
    
    table = pd.DataFrame({'beta': beta, 'se': se, 'p': p_int})
    write_table(table, 'tables/granular_interaction.csv')
    
    return {'beta_int': beta[2], 'se_int': se[2], 'p_int': p_int}