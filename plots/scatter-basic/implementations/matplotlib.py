""" pyplots.ai
scatter-basic: Basic Scatter Plot
Library: matplotlib 3.10.8 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-13
"""

import matplotlib.pyplot as plt
import numpy as np


# Data - correlated data with noise
np.random.seed(42)
x = np.random.randn(150) * 2 + 10
y = x * 0.8 + np.random.randn(150) * 1.5

# Create plot
fig, ax = plt.subplots(figsize=(16, 9))
ax.scatter(x, y, alpha=0.7, s=200, color="#306998", edgecolors="white", linewidths=0.5)

# Labels and styling
ax.set_xlabel("X Value", fontsize=20)
ax.set_ylabel("Y Value", fontsize=20)
ax.set_title("scatter-basic · matplotlib · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)
ax.grid(True, alpha=0.3, linestyle="--")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
