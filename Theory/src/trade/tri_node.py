import numpy as np

def ces_gravity(productivities, taus, epsilon):
    """
    Return bilateral expenditure share matrix Π (3x3) given fundamentals.
    productivities: array shape (3,), T_i
    taus: matrix shape (3,3), iceberg costs τ_ij (>=1), diagonals = 1
    epsilon: scalar trade elasticity (>1 typical)
    Uses Eaton-Kortum/CES form: share_{ij} ∝ (T_j / (p_i * τ_ij)**epsilon)
    Solves for price indices p_i via fixed point.
    """
    n_countries = productivities.shape[0]
    prices = np.ones(n_countries)
    for _ in range(100):
        new_prices = np.sum(productivities * (taus.T / prices)**(-epsilon), axis=1)**(-1/epsilon)
        if np.max(np.abs(new_prices - prices)) < 1e-10:
            break
        prices = 0.5 * new_prices + 0.5 * prices

    expenditure_shares = (productivities * (taus.T / prices)**(-epsilon)).T / np.sum(productivities * (taus.T / prices)**(-epsilon), axis=1)
    return expenditure_shares.T

def tri_node_welfare(alpha_k, epsilon_k, Pi0, tau0, kappa, productivities=None):
    """
    Given baseline shares Pi0 and costs tau0, apply a κ-shock on AB & BA:
      τ'_AB = τ_AB*(1+kappa), τ'_BA = τ_BA*(1+kappa)
    Recompute Π' with ces_gravity. Compute λ_i = Σ_k α_k * Π_{ii,k} (home share),
    then welfare by region i:
      W_i'/W_i = Π_k (λ'_{i,k} / λ_{i,k})^{-α_k/ε_k}
    Return np.array([W_A, W_B, W_C]), Π' for diagnostics.
    """
    if productivities is None:
        productivities = np.ones(3)
    
    tau1 = tau0.copy()
    tau1[0, 1] = tau0[0, 1] * (1 + kappa)
    tau1[1, 0] = tau0[1, 0] * (1 + kappa)

    Pi1 = ces_gravity(productivities, tau1, np.mean(epsilon_k))

    lambda_i0 = np.diag(Pi0)
    lambda_i1 = np.diag(Pi1)

    welfare_ratios = (lambda_i1 / lambda_i0)**(-np.sum(alpha_k) / np.mean(epsilon_k))
    return welfare_ratios, Pi1

def tri_node_welfare_sever(alpha_k, epsilon_k, Pi0):
    """Pure severance benchmark: set λ'_i = 1 in each sector, same formula."""
    lambda_i0 = np.diag(Pi0)
    welfare_ratios = (1.0 / lambda_i0)**(-np.sum(alpha_k) / np.mean(epsilon_k))
    return welfare_ratios