""" pyplots.ai
bar-3d: 3D Bar Chart
Library: matplotlib 3.10.8 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-30
"""

import matplotlib.pyplot as plt
import numpy as np


# Data - Sales by Product and Quarter
np.random.seed(42)
products = ["Product A", "Product B", "Product C", "Product D", "Product E"]
quarters = ["Q1", "Q2", "Q3", "Q4"]

n_products = len(products)
n_quarters = len(quarters)

# Generate realistic sales data (in thousands)
sales = np.array(
    [
        [120, 135, 142, 158],  # Product A - steady growth
        [85, 92, 78, 95],  # Product B - fluctuating
        [200, 185, 210, 225],  # Product C - highest performer
        [65, 70, 82, 88],  # Product D - moderate growth
        [150, 145, 160, 142],  # Product E - variable
    ]
)

# Create figure with 3D projection
fig = plt.figure(figsize=(16, 9))
ax = fig.add_subplot(111, projection="3d")

# Set up grid positions
xpos = np.arange(n_products)
ypos = np.arange(n_quarters)
xpos_mesh, ypos_mesh = np.meshgrid(xpos, ypos, indexing="ij")

xpos_flat = xpos_mesh.flatten()
ypos_flat = ypos_mesh.flatten()
zpos_flat = np.zeros_like(xpos_flat)

# Bar dimensions
dx = 0.6
dy = 0.6
dz = sales.flatten()

# Create color gradient based on height for better depth perception
colors = plt.cm.viridis((dz - dz.min()) / (dz.max() - dz.min()))

# Plot 3D bars with transparency
ax.bar3d(xpos_flat, ypos_flat, zpos_flat, dx, dy, dz, color=colors, alpha=0.85, edgecolor="#333333", linewidth=0.5)

# Styling
ax.set_xlabel("Product", fontsize=20, labelpad=15)
ax.set_ylabel("Quarter", fontsize=20, labelpad=15)
ax.set_zlabel("Sales (thousands $)", fontsize=20, labelpad=15)
ax.set_title("bar-3d · matplotlib · pyplots.ai", fontsize=24, pad=20)

# Set tick labels
ax.set_xticks(xpos + dx / 2)
ax.set_xticklabels(products, fontsize=14)
ax.set_yticks(ypos + dy / 2)
ax.set_yticklabels(quarters, fontsize=14)
ax.tick_params(axis="z", labelsize=14)

# Set viewing angle for best visibility
ax.view_init(elev=25, azim=45)

# Add colorbar to reinforce z-values
sm = plt.cm.ScalarMappable(cmap="viridis", norm=plt.Normalize(vmin=dz.min(), vmax=dz.max()))
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax, shrink=0.6, aspect=15, pad=0.1)
cbar.set_label("Sales (thousands $)", fontsize=16)
cbar.ax.tick_params(labelsize=14)

plt.savefig("plot.png", dpi=300, bbox_inches="tight")
