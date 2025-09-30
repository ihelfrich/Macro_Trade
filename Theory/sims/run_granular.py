
import yaml
import numpy as np
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.trade.granular import granular_welfare_ratio

with open('sims/configs/granular.yaml', 'r') as f:
    config = yaml.safe_load(f)

epsilon = config['epsilon']

results = []
for zeta in config['zeta_values']:
    for s in config['s_grid']:
        loss = 1 - granular_welfare_ratio(s, zeta, epsilon, 0.5) # psi=0.5 is a placeholder
        results.append([zeta, s, loss])

df = pd.DataFrame(results, columns=['zeta', 's', 'loss'])
df.to_csv('sims/out/granular_results.csv', index=False)

print("Granular simulation complete. Results saved to sims/out/granular_results.csv")
