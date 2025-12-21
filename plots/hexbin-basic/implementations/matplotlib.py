""" pyplots.ai
hexbin-basic: Basic Hexbin Plot
Library: matplotlib 3.10.8 | Python 3.13.11
Quality: 100/100 | Created: 2025-12-14
"""

import matplotlib.pyplot as plt
import numpy as np


# Data - generate clustered bivariate data
np.random.seed(42)
n_points = 10000

# Create multiple clusters for interesting density patterns
cluster1_x = np.random.randn(n_points // 2) * 1.5 + 2
cluster1_y = np.random.randn(n_points // 2) * 1.5 + 2
cluster2_x = np.random.randn(n_points // 3) * 1.0 - 2
cluster2_y = np.random.randn(n_points // 3) * 1.0 - 1
cluster3_x = np.random.randn(n_points // 6) * 0.8 + 1
cluster3_y = np.random.randn(n_points // 6) * 0.8 - 2

x = np.concatenate([cluster1_x, cluster2_x, cluster3_x])
y = np.concatenate([cluster1_y, cluster2_y, cluster3_y])

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

# Create hexbin plot with viridis colormap
hb = ax.hexbin(x, y, gridsize=30, cmap="viridis", mincnt=1)

# Add colorbar to show density scale
cbar = fig.colorbar(hb, ax=ax)
cbar.set_label("Count", fontsize=20)
cbar.ax.tick_params(labelsize=16)

# Labels and styling
ax.set_xlabel("X Value", fontsize=20)
ax.set_ylabel("Y Value", fontsize=20)
ax.set_title("hexbin-basic · matplotlib · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
