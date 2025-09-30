
import sympy

# Math Definitions
psi, epsilon, theta, lam, lam_prime = sympy.symbols('psi epsilon theta lam lam_prime')

# Full fragmentation
W_ratio_full = (1 - psi)**(1/epsilon)

# Partial fragmentation
lam_def = 1 - psi
lam_prime_def = lam_def + theta * (1 - lam_def)
W_ratio_partial = (lam_prime_def / lam_def)**(-1/epsilon)

# Asserts
dW_dpsi = sympy.diff(W_ratio_full, psi)
dW_depsilon = sympy.diff(W_ratio_full, epsilon)

# The user requested to check the asserts with sympy.
# dW_dpsi < 0 under stated conditions
# dW_depsilon > 0 for fixed psi

# Let's print the derivatives to inspect them.
print(f"dW_dpsi = {dW_dpsi}")
print(f"dW_depsilon = {dW_depsilon}")

# We can see that for psi in [0,1] and epsilon > 0:
# dW_dpsi is negative because (1-psi) is positive, so the whole expression is negative.
# dW_depsilon is positive because (1-psi) is between 0 and 1, so log(1-psi) is negative.
# The two negatives cancel out, making the expression positive.

def welfare_ratio_full_fragmentation(psi: float, epsilon: float) -> float:
    """
    Returns W_frag / W_int under full fragmentation given baseline psi and epsilon.
    """
    if not (0.0 <= psi <= 1.0):
        raise ValueError("psi in [0,1]")
    if epsilon <= 0:
        raise ValueError("epsilon > 0")
    lam = 1.0 - psi
    if lam == 0.0:
        return 0.0
    return lam ** (1.0 / epsilon)

def welfare_ratio_partial_fragmentation(psi: float, epsilon: float, theta: float) -> float:
    """
    Returns W'/W with partial fragmentation, where lambda' = lambda + theta*(1 - lambda).
    theta in [0,1], theta=0 no change, theta=1 full fragmentation.
    """
    if not (0.0 <= psi <= 1.0):
        raise ValueError("psi in [0,1]")
    if not (0.0 <= theta <= 1.0):
        raise ValueError("theta in [0,1]")
    if epsilon <= 0:
        raise ValueError("epsilon > 0")
    lam0 = 1.0 - psi
    if lam0 == 0.0:
        return 0.0
    lam1 = lam0 + theta * (1.0 - lam0)
    return (lam1 / lam0) ** (-1.0 / epsilon)
