
import yaml
import numpy as np
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.trade.nonhomothetic import welfare_ev_ratio

with open('sims/configs/nonhomothetic.yaml', 'r') as f:
    config = yaml.safe_load(f)

income = np.array(config['income'])
prices0 = np.array(config['prices0'])
alpha = np.array(config['alpha'])
gamma = np.array(config['gamma'])

results = []
for shock in config['price_shocks']:
    prices1 = np.array([1, shock])
    welfare_ratios = [welfare_ev_ratio(np.array([income[i]]), prices0, prices1, np.array([[alpha[i], 1-alpha[i]]]), np.array([[gamma[i], gamma[i]]])) for i in range(len(income))]
    dispersion = np.var(welfare_ratios)
    results.append([shock, dispersion])

df = pd.DataFrame(results, columns=['price_shock', 'dispersion'])
df.to_csv('sims/out/nonhomothetic_results.csv', index=False)

print("Non-homothetic simulation complete. Results saved to sims/out/nonhomothetic_results.csv")
