"""
hexbin-basic: Basic Hexbin Plot
Library: seaborn
"""

import matplotlib.pyplot as plt
import numpy as np


# Data - clustered bivariate distribution (10,000 points)
np.random.seed(42)
n_points = 10000

# Create clusters for more interesting density patterns
cluster1_x = np.random.randn(n_points // 2) * 1.5 + 2
cluster1_y = np.random.randn(n_points // 2) * 1.5 + 2
cluster2_x = np.random.randn(n_points // 2) * 2 - 2
cluster2_y = np.random.randn(n_points // 2) * 2 - 1

x = np.concatenate([cluster1_x, cluster2_x])
y = np.concatenate([cluster1_y, cluster2_y])

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

# Hexbin plot with viridis colormap for perceptual uniformity
hb = ax.hexbin(x, y, gridsize=30, cmap="viridis", mincnt=1)

# Colorbar for density scale
cbar = fig.colorbar(hb, ax=ax, pad=0.02)
cbar.set_label("Point Count", fontsize=20)
cbar.ax.tick_params(labelsize=16)

# Labels and styling
ax.set_xlabel("X Value", fontsize=20)
ax.set_ylabel("Y Value", fontsize=20)
ax.set_title("hexbin-basic · seaborn · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
