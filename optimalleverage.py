import numpy as np
import matplotlib.pyplot as plt

# Pparameters
Q = 1.0          # Quantity
P1 = 100000      # Current price
P0 = 80000       # Price purchased
V = 10000        # Additional wealth

# λ = 1 / [Q * (P1 * L - P0)]
def lambda_leverage(L, Q, P1, P0):
    denominator = Q * (P1 * L - P0)
    # Avoid division by zero or negative values
    return np.where(denominator != 0, 1 / denominator, np.inf)

# MU = P1 / (P1 * Q + V)
def marginal_utility(Q, P1, V):
    return P1 / (P1 * Q + V)

# Leverage values
L = np.linspace(1, 5, 100)  # Leverage - 1x to 5x

# Lambda for base case
lambda_values = lambda_leverage(L, Q, P1, P0)

# Lambda for larger portfolio (e.g., Q = 5)
Q_large = 5.0
lambda_large = lambda_leverage(L, Q_large, P1, P0)

# MU for interpretation
MU = marginal_utility(Q, P1, V)
MU_large = marginal_utility(Q_large, P1, V)

print(f"Marginal Utility (Q={Q}): {MU:.6f}")
print(f"Marginal Utility (Q={Q_large}): {MU_large:.6f}")

# Plotting
plt.figure(figsize=(8, 6))
plt.plot(L, lambda_values, label=f'λ (Q={Q})', color='blue')
plt.plot(L, lambda_large, label=f'λ (Q={Q_large})', color='red', linestyle='--')
plt.xlabel('Leverage (L)')
plt.ylabel('λ')
plt.title('Optimal Leverage: λ vs. Leverage')
plt.legend()
plt.grid(True)
plt.yscale('log') 
plt.show()
