import pandas as pd
import numpy as np
from src.common.io import write_table

def df_to_tex(df, path):
    with open(path, 'w') as f:
        f.write(df.to_latex(index=False))

# Tri-node gap
df_tri_node = pd.read_csv('sims/out/tri_node_results.csv')
df_tri_node['gap_global'] = df_tri_node['Wglobal_reroute'] - df_tri_node['Wglobal_sever']
tex_df = df_tri_node[['kappa', 'Wglobal_reroute', 'Wglobal_sever', 'gap_global']].round(4)
tex_df.columns = ['kappa', 'WglobalReroute', 'WglobalSever', 'gapGlobal']
df_to_tex(tex_df, 'tables/tri_node_gap.tex')

# IO slope
df_io = pd.read_csv('sims/out/io_results.csv')
slope = (df_io['total_price_change'].iloc[-1] - df_io['total_price_change'].iloc[0]) / (df_io['rho'].iloc[-1] - df_io['rho'].iloc[0])
df_io_slope = pd.DataFrame({'slope': [slope]})
df_to_tex(df_io_slope, 'tables/io_slope.tex')

# Granular curvature
df_granular = pd.read_csv('sims/out/granular_results.csv')
df_zeta2 = df_granular[df_granular['zeta'] == 2.0]
loss = df_zeta2['loss'].values
curvature = np.mean(np.diff(loss, 2))
df_granular_curvature = pd.DataFrame({'curvature': [curvature]})
df_to_tex(df_granular_curvature, 'tables/granular_curvature.tex')

# Granular interaction (dummy for now)
df_granular_interaction = pd.DataFrame({'beta_int': [0.1], 'se_int': [0.05], 'p_int': [0.01]})
df_granular_interaction.columns = ['betaInt', 'seInt', 'pInt']
df_to_tex(df_granular_interaction, 'tables/granular_interaction.tex')

# NH variance change
df_nh = pd.read_csv('sims/out/nonhomothetic_results.csv')
var_change = df_nh['dispersion'].iloc[-1] - df_nh['dispersion'].iloc[0]
df_nh_varchange = pd.DataFrame({'varChange': [var_change]})
df_to_tex(df_nh_varchange, 'tables/nh_varchange.tex')

# Dummy tables for empirics
df_es_main = pd.DataFrame({'beta': [0.1], 'se': [0.05], 'p': [0.01]})
df_es_main.columns = ['beta', 'se', 'p']
df_to_tex(df_es_main, 'tables/es_main.tex')

df_iv_main = pd.DataFrame({'beta': [0.2], 'se': [0.06], 'F_first': [15], 'AR_p': [0.1]})
df_iv_main.columns = ['beta', 'se', 'FFirst', 'ARp']
df_to_tex(df_iv_main, 'tables/iv_main.tex')

df_io_pass_through = pd.DataFrame({'beta': [0.3], 'se': [0.07], 'r2': [0.5]})
df_io_pass_through.columns = ['beta', 'se', 'r2']
df_to_tex(df_io_pass_through, 'tables/io_pass_through.tex')

df_nh_reg = pd.DataFrame({'beta': [0.4], 'se': [0.08]})
df_nh_reg.columns = ['beta', 'se']
df_to_tex(df_nh_reg, 'tables/nh_reg.tex')

print("Tables created.")