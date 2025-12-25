""" pyplots.ai
scatter-3d: 3D Scatter Plot
Library: matplotlib 3.10.8 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-25
"""

import matplotlib.pyplot as plt
import numpy as np


# Data - Create 3 clusters in 3D space
np.random.seed(42)

# Cluster 1: Lower left region
n1 = 60
x1 = np.random.randn(n1) * 1.5 + 2
y1 = np.random.randn(n1) * 1.5 + 2
z1 = np.random.randn(n1) * 1.5 + 2

# Cluster 2: Upper right region
n2 = 50
x2 = np.random.randn(n2) * 1.2 + 7
y2 = np.random.randn(n2) * 1.2 + 7
z2 = np.random.randn(n2) * 1.2 + 7

# Cluster 3: Middle-high region
n3 = 40
x3 = np.random.randn(n3) * 1.0 + 5
y3 = np.random.randn(n3) * 1.0 + 4
z3 = np.random.randn(n3) * 1.0 + 9

# Combine clusters
x = np.concatenate([x1, x2, x3])
y = np.concatenate([y1, y2, y3])
z = np.concatenate([z1, z2, z3])

# Color based on z-value to add fourth dimension visualization
colors = z

# Create 3D plot
fig = plt.figure(figsize=(16, 9))
ax = fig.add_subplot(111, projection="3d")

# Scatter plot with color encoding
scatter = ax.scatter(x, y, z, c=colors, cmap="viridis", s=120, alpha=0.7, edgecolors="white", linewidth=0.5)

# Add colorbar
cbar = fig.colorbar(scatter, ax=ax, shrink=0.6, aspect=20, pad=0.1)
cbar.set_label("Z Value", fontsize=18)
cbar.ax.tick_params(labelsize=14)

# Labels and styling
ax.set_xlabel("X Dimension", fontsize=18, labelpad=15)
ax.set_ylabel("Y Dimension", fontsize=18, labelpad=15)
ax.set_zlabel("Z Dimension", fontsize=18, labelpad=15)
ax.set_title("scatter-3d · matplotlib · pyplots.ai", fontsize=24, pad=20)

# Tick parameters
ax.tick_params(axis="x", labelsize=14)
ax.tick_params(axis="y", labelsize=14)
ax.tick_params(axis="z", labelsize=14)

# Set viewing angle for better visualization
ax.view_init(elev=25, azim=45)

# Add subtle grid
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False
ax.xaxis.pane.set_edgecolor("gray")
ax.yaxis.pane.set_edgecolor("gray")
ax.zaxis.pane.set_edgecolor("gray")
ax.xaxis.pane.set_alpha(0.3)
ax.yaxis.pane.set_alpha(0.3)
ax.zaxis.pane.set_alpha(0.3)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
