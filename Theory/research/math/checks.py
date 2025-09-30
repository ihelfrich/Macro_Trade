
import sympy

def check_signs():
    psi, epsilon = sympy.symbols('psi epsilon')
    W = (1 - psi)**(1/epsilon)
    
    dW_dpsi = sympy.diff(W, psi)
    dW_depsilon = sympy.diff(W, epsilon)
    
    # For psi in (0,1) and epsilon > 0
    # dW_dpsi should be negative
    # dW_depsilon should be positive
    
    return dW_dpsi.subs({psi:0.5, epsilon:4}) < 0 and dW_depsilon.subs({psi:0.5, epsilon:4}) > 0

if __name__ == '__main__':
    if check_signs():
        print("Sign checks passed.")
    else:
        print("Sign checks failed.")
