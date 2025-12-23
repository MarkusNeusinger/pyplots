"""pyplots.ai
hexbin-basic: Basic Hexbin Plot
Library: seaborn | Python 3.13
Quality: pending | Created: 2025-12-23
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Data - create clustered distribution with multiple density regions
np.random.seed(42)

# Create multiple clusters to show density variation
n_points = 5000
cluster1 = np.random.multivariate_normal([2, 2], [[1, 0.5], [0.5, 1]], n_points // 2)
cluster2 = np.random.multivariate_normal([6, 6], [[0.5, -0.3], [-0.3, 0.5]], n_points // 3)
cluster3 = np.random.multivariate_normal([7, 2], [[0.3, 0], [0, 0.8]], n_points // 6)

# Combine clusters
x = np.concatenate([cluster1[:, 0], cluster2[:, 0], cluster3[:, 0]])
y = np.concatenate([cluster1[:, 1], cluster2[:, 1], cluster3[:, 1]])

# Set seaborn style for clean aesthetics
sns.set_style("whitegrid")
sns.set_context("talk", font_scale=1.2)

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Create hexbin plot using matplotlib's hexbin via the axes
# Seaborn provides styling but hexbin is a matplotlib function
hb = ax.hexbin(x, y, gridsize=30, cmap="viridis", mincnt=1, edgecolors="none")

# Add colorbar to show density scale
cbar = plt.colorbar(hb, ax=ax, pad=0.02)
cbar.set_label("Point Count", fontsize=20)
cbar.ax.tick_params(labelsize=16)

# Labels and title with proper sizing
ax.set_xlabel("X Coordinate", fontsize=20)
ax.set_ylabel("Y Coordinate", fontsize=20)
ax.set_title("hexbin-basic \u00b7 seaborn \u00b7 pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)

# Adjust grid to be subtle
ax.grid(True, alpha=0.3, linestyle="--")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
