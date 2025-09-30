
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Tri-node results
df_tri_node = pd.read_csv('sims/out/tri_node_results.csv')
plt.figure()
df_tri_node.plot(x='kappa', y=['WA_reroute', 'WB_reroute', 'WC_reroute'], kind='line')
df_tri_node.plot(x='kappa', y=['WA_sever', 'WB_sever', 'WC_sever'], kind='line', linestyle='--')
plt.legend(['A (reroute)', 'B (reroute)', 'C (reroute)', 'A (sever)', 'B (sever)', 'C (sever)'])
plt.xlabel('Kappa shock')
plt.ylabel('Welfare ratio')
plt.title('Tri-node welfare vs. kappa')
plt.savefig('figs/bounds_kappa.png')
plt.close()

max_gap = np.max(df_tri_node['Wglobal_reroute'] - df_tri_node['Wglobal_sever'])
print(f"Max gap between reroute and sever: {max_gap:.4f}")

# IO results
df_io = pd.read_csv('sims/out/io_results.csv')
plt.figure()
df_io.plot(x='rho', y='total_price_change', kind='line')
plt.xlabel('Spectral radius (rho)')
plt.ylabel('Total price change')
plt.title('IO amplification')
plt.savefig('figs/io_amplification.png')
plt.close()

# Granular results
df_granular = pd.read_csv('sims/out/granular_results.csv')
plt.figure()
for zeta in df_granular['zeta'].unique():
    df_zeta = df_granular[df_granular['zeta'] == zeta]
    plt.plot(df_zeta['s'], df_zeta['loss'], label=f'zeta = {zeta}')
plt.xlabel('Concentration (s)')
plt.ylabel('Welfare loss')
plt.title('Convexity in granular exposure')
plt.legend()
plt.savefig('figs/convexity_granular.png')
plt.close()

# Non-homothetic results
df_nh = pd.read_csv('sims/out/nonhomothetic_results.csv')
plt.figure()
df_nh.plot(x='price_shock', y='dispersion', kind='line')
plt.xlabel('Price shock on luxury good')
plt.ylabel('Welfare dispersion')
plt.title('Non-homothetic welfare dispersion')
plt.savefig('figs/nh_dispersion.png')
plt.close()

print("Figures created.")
