import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar

# Parameters
P1 = 100000.0    # Current price (USD)
P0 = 80000.0     # Purchase price (USD)
Q = 1.0          # Quantity of BTC
beta = 10000.0   # Risk penalty
alpha = 0.5      # MR scaling
tau = 0.1        # Base trend strength
tau_strong = 0.5 # Strong trend strength

# Define functions
def marginal_utility(L, Q, P1, beta, tau):
    """Compute MU = P1 * (1 + tau * L) / (P1 * Q * (1 + tau * L) - beta * L)"""
    denominator = P1 * Q * (1 + tau * L) - beta * L
    return np.where(denominator > 0, P1 * (1 + tau * L) / denominator, np.inf)

def marginal_return(L, Q, P1, P0, alpha, tau):
    """Compute MR = Q * (P1 * L - P0) * (1 + tau) / (1 + alpha * L^2)"""
    return Q * (P1 * L - P0) * (1 + tau) / (1 + alpha * L**2)

def lambda_function(L, Q, P1, P0, beta, alpha, tau):
    """Compute lambda = MU / MR"""
    mu = marginal_utility(L, Q, P1, beta, tau)
    mr = marginal_return(L, Q, P1, P0, alpha, tau)
    return np.where(mr != 0, mu / mr, np.inf)

# Optimize lambda to find optimal L
def neg_lambda(L, Q, P1, P0, beta, alpha, tau):
    """Negative lambda for minimization"""
    return -lambda_function(L, Q, P1, P0, beta, alpha, tau)

# Generate leverage values
L = np.linspace(1, 4, 100)  # Leverage from 1x to 4x

# Compute lambda and MU for base and strong trends
lambda_base = lambda_function(L, Q, P1, P0, beta, alpha, tau)
lambda_strong = lambda_function(L, Q, P1, P0, beta, alpha, tau_strong)
MU_base = marginal_utility(L, Q, P1, beta, tau)
MU_strong = marginal_utility(L, Q, P1, beta, tau_strong)

# Find optimal leverage
opt_result_base = minimize_scalar(neg_lambda, bounds=(1, 4), args=(Q, P1, P0, beta, alpha, tau))
opt_L_base = opt_result_base.x
opt_lambda_base = lambda_function(opt_L_base, Q, P1, P0, beta, alpha, tau)

opt_result_strong = minimize_scalar(neg_lambda, bounds=(1, 4), args=(Q, P1, P0, beta, alpha, tau_strong))
opt_L_strong = opt_result_strong.x
opt_lambda_strong = lambda_function(opt_L_strong, Q, P1, P0, beta, alpha, tau_strong)

print(f"Optimal Leverage (tau={tau}): L={opt_L_base:.2f}, lambda={opt_lambda_base:.6f}")
print(f"Optimal Leverage (tau={tau_strong}): L={opt_L_strong:.2f}, lambda={opt_lambda_strong:.6f}")

# Plot lambda vs. leverage
plt.figure(figsize=(8, 6))
plt.plot(L, lambda_base, label=f'λ (τ={tau})', color='blue')
plt.plot(L, lambda_strong, label=f'λ (τ={tau_strong})', color='red', linestyle='--')
plt.scatter([opt_L_base, opt_L_strong], [opt_lambda_base, opt_lambda_strong], color='black', label='Optimal L')
plt.xlabel('Leverage (L)')
plt.ylabel('λ (MU/MR)')
plt.title('λ vs. Leverage (Left Side of Laffer-like Curve)')
plt.legend()
plt.grid(True)
plt.show()

# Plot MU vs. leverage
plt.figure(figsize=(8, 6))
plt.plot(L, MU_base, label=f'MU (τ={tau})', color='blue')
plt.plot(L, MU_strong, label=f'MU (τ={tau_strong})', color='red', linestyle='--')
plt.xlabel('Leverage (L)')
plt.ylabel('Marginal Utility (MU)')
plt.title('Marginal Utility vs. Leverage (Trend-Driven)')
plt.legend()
plt.grid(True)
plt.show()