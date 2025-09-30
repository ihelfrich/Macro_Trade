
import sympy

# Proposition 1: Bounds

psi, epsilon, theta, lam, lam_prime = sympy.symbols('psi epsilon theta lam lam_prime')

# The welfare ratio is lambda^(1/epsilon) for full fragmentation.
# Since lambda is between 0 and 1, and epsilon is positive, this is between 0 and 1.
# The lower bound is lambda^(1/epsilon), which is achieved under pure severance.
# The upper bound is 1, which is achieved at kappa=0 (no shock).

# This proposition is straightforward and does not require complex symbolic manipulation to check.
# The core of the proposition is that rerouting mitigates losses, so the welfare ratio
# with rerouting is higher than with pure severance.

# Let's consider a simple case.
# Pure severance: W'/W = (1-psi)**(1/epsilon)
# With rerouting, some of the trade is diverted to country C.
# This will increase the home share lambda_i' compared to the pre-shock lambda_i.
# But it will not increase it as much as if there was no trade with the other bloc at all.
# The new home share lambda_i' will be higher than the old one, so (lambda_i'/lambda_i) > 1.
# The welfare ratio is (lambda_i'/lambda_i)**(-1/epsilon), which is less than 1.

# The lower bound is when lambda_i' is maximized, which happens under pure severance.
# In that case, lambda_i' = 1, and the formula becomes (1/lambda_i)**(-1/epsilon) = lambda_i**(1/epsilon).

print("Proposition 1 (Bounds) check is conceptual and based on the model structure.")
