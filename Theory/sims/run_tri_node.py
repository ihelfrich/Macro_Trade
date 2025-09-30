import yaml
import numpy as np
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.trade.tri_node import tri_node_welfare, tri_node_welfare_sever, ces_gravity
from src.common.io import write_table

with open('sims/configs/tri_node_baseline.yaml', 'r') as f:
    config = yaml.safe_load(f)

alpha_k = np.array(config['alpha_k'])
epsilon_k = np.array(config['epsilon_k'])
tau0 = np.array(config['tau0'])
T = np.ones(3)
Pi0 = ces_gravity(T, tau0, np.mean(epsilon_k))

results = []
for kappa in config['kappa_grid']:
    w_reroute, _ = tri_node_welfare(alpha_k, epsilon_k, Pi0, tau0, kappa, T)
    w_sever = tri_node_welfare_sever(alpha_k, epsilon_k, Pi0)
    
    results.append([kappa] + list(w_reroute) + list(w_sever))

df = pd.DataFrame(results, columns=['kappa', 'WA_reroute', 'WB_reroute', 'WC_reroute', 'WA_sever', 'WB_sever', 'WC_sever'])

df['Wglobal_reroute'] = df[['WA_reroute', 'WB_reroute', 'WC_reroute']].mean(axis=1)
df['Wglobal_sever'] = df[['WA_sever', 'WB_sever', 'WC_sever']].mean(axis=1)
df['gap_global'] = df['Wglobal_reroute'] - df['Wglobal_sever']

assert (df['Wglobal_reroute'] + 1e-10 >= df['Wglobal_sever']).all(), "Dominance violated"

write_table(df, 'sims/out/tri_node_results.csv')

# Create LaTeX table
tex_df = df[['kappa', 'Wglobal_reroute', 'Wglobal_sever', 'gap_global']].round(4)
tex_df.columns = ['kappa', 'WglobalReroute', 'WglobalSever', 'gapGlobal']
with open("tables/tri_node_gap.tex", "w") as f:
    f.write(tex_df.to_latex(index=False))

print("Tri-node simulation complete. Results saved to sims/out/tri_node_results.csv and tables/tri_node_gap.tex")