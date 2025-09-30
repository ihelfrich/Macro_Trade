
import yaml
import numpy as np
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.trade.io import io_prices

with open('sims/configs/io_strength.yaml', 'r') as f:
    config = yaml.safe_load(f)

A_base = np.array(config['A_base'])
shock = np.array(config['shock'])

results = []
for scale in config['rho_scales']:
    A = A_base * scale
    rho = np.max(np.abs(np.linalg.eigvals(A)))
    price_change = io_prices(A, shock)
    results.append([rho, np.sum(price_change)])

df = pd.DataFrame(results, columns=['rho', 'total_price_change'])
df.to_csv('sims/out/io_results.csv', index=False)

print("IO simulation complete. Results saved to sims/out/io_results.csv")
