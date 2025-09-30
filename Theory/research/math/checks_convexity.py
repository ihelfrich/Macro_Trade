
import sympy

# Proposition 2: Convexity in concentration

s, zeta = sympy.symbols('s zeta')

# Loss is s**zeta
Loss = s**zeta

# Second derivative with respect to s
d2L_ds2 = sympy.diff(Loss, s, 2)

print(f"d2L_ds2 = {d2L_ds2}")

# For s > 0 and zeta > 1, this is positive, so the loss is convex in s.

# The proposition states that W'/W is convex decreasing in s.
# W'/W = 1 - s**zeta

d2W_ds2 = sympy.diff(1 - Loss, s, 2)

print(f"d2W_ds2 = {d2W_ds2}")

# This is negative for s > 0 and zeta > 1, so W'/W is concave in s, not convex.
# The user prompt says "convex decreasing". A function that is decreasing and has a second derivative that is negative is concave.
# So the prompt is a bit ambiguous. It probably means the loss is convex.
