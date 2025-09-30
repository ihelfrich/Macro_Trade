import numpy as np
import matplotlib.pyplot as plt
from trade_model import welfare_ratio_full_fragmentation

def plot_welfare_vs_psi():
    """Plots the welfare ratio as a function of psi for different epsilon values."""
    psi_values = np.linspace(0.01, 0.99, 100)
    epsilon_values = [2, 4, 6]

    plt.figure(figsize=(10, 6))

    for epsilon in epsilon_values:
        welfare_ratios = [welfare_ratio_full_fragmentation(psi, epsilon) for psi in psi_values]
        plt.plot(psi_values, welfare_ratios, label=f'epsilon = {epsilon}')

    plt.xlabel('Initial Cross-Bloc Expenditure Share (psi)')
    plt.ylabel('Welfare Ratio (W_frag / W_int)')
    plt.title('Welfare under Full Fragmentation: $W_{frag}/W_{int} = (1-\psi)^{1/\epsilon}$')
    plt.legend()
    plt.grid(True)
    plt.savefig('welfare_vs_psi.png')
    print("Plot saved as welfare_vs_psi.png")

def plot_welfare_vs_epsilon():
    """Plots the welfare ratio as a function of epsilon for different psi values."""
    epsilon_values = np.linspace(1, 10, 100)
    psi_values = [0.25, 0.5, 0.75]

    plt.figure(figsize=(10, 6))

    for psi in psi_values:
        welfare_ratios = [welfare_ratio_full_fragmentation(psi, epsilon) for epsilon in epsilon_values]
        plt.plot(epsilon_values, welfare_ratios, label=f'psi = {psi}')

    plt.xlabel('Trade Elasticity (epsilon)')
    plt.ylabel('Welfare Ratio (W_frag / W_int)')
    plt.title('Welfare under Full Fragmentation: $W_{frag}/W_{int} = (1-\psi)^{1/\epsilon}$')
    plt.legend()
    plt.grid(True)
    plt.savefig('welfare_vs_epsilon.png')
    print("Plot saved as welfare_vs_epsilon.png")

if __name__ == "__main__":
    plot_welfare_vs_psi()
    plot_welfare_vs_epsilon()