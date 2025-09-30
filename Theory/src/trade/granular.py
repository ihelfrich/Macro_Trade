import numpy as np

def granular_welfare_ratio(s, zeta, epsilon, psi):
    """
    s: share of cross-bloc expenditure borne by top-k firms (concentration)
    zeta: Pareto tail (firm sales), lower => fatter tail
    epsilon: trade elasticity
    psi: cross-bloc share
    Mechanism: a granular wedge multiplies effective ψ by g(s, ζ) ≥ 1.
    Use g(s,ζ) = (1 - s)**(-1/max(1.01, ζ)) as a parsimonious form.
    Return W'/W under severance: (1 - g*psi)^{1/epsilon}, truncated at [0,1].
    """
    g = (1.0 - s)**(-1.0 / max(1.01, zeta))
    eff_psi = min(0.99, g * psi)
    return max(0.0, (1.0 - eff_psi) ** (1.0 / epsilon))