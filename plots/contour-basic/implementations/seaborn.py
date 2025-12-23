"""pyplots.ai
contour-basic: Basic Contour Plot
Library: seaborn | Python 3.13
Quality: pending | Created: 2025-12-23
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Data - Bivariate distribution to demonstrate contour density
np.random.seed(42)
n_points = 2000

# Create multimodal distribution with two centers
mean1 = [0, 0]
mean2 = [3, 2]
cov = [[1, 0.5], [0.5, 1]]

# Generate samples from two Gaussian clusters
samples1 = np.random.multivariate_normal(mean1, cov, n_points // 2)
samples2 = np.random.multivariate_normal(mean2, cov, n_points // 2)
x = np.concatenate([samples1[:, 0], samples2[:, 0]])
y = np.concatenate([samples1[:, 1], samples2[:, 1]])

# Create plot (4800x2700 px)
fig, ax = plt.subplots(figsize=(16, 9))
sns.set_style("whitegrid")

# Filled contour using seaborn's kdeplot
sns.kdeplot(
    x=x,
    y=y,
    fill=True,
    levels=15,
    cmap="viridis",
    alpha=0.9,
    ax=ax,
    cbar=True,
    cbar_kws={"label": "Density", "shrink": 0.85},
)

# Add contour lines for clarity
sns.kdeplot(x=x, y=y, levels=15, color="white", linewidths=0.8, alpha=0.6, ax=ax)

# Labels and styling
ax.set_xlabel("X Coordinate", fontsize=20)
ax.set_ylabel("Y Coordinate", fontsize=20)
ax.set_title("contour-basic · seaborn · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)

# Style colorbar
cbar = ax.collections[0].colorbar
if cbar:
    cbar.ax.tick_params(labelsize=16)
    cbar.set_label("Density", fontsize=20)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
