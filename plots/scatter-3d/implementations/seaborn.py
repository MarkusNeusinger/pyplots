"""pyplots.ai
scatter-3d: 3D Scatter Plot
Library: seaborn | Python 3.13
Quality: pending | Created: 2025-12-25
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Set seaborn style for consistent aesthetics
sns.set_theme(style="whitegrid")
sns.set_context("talk", font_scale=1.2)

# Data: 3D clustered data representing molecular positions
np.random.seed(42)
n_points = 150

# Create 3 clusters in 3D space
cluster1_x = np.random.normal(2, 0.8, 50)
cluster1_y = np.random.normal(2, 0.8, 50)
cluster1_z = np.random.normal(2, 0.8, 50)

cluster2_x = np.random.normal(5, 1.0, 50)
cluster2_y = np.random.normal(5, 1.0, 50)
cluster2_z = np.random.normal(3, 1.0, 50)

cluster3_x = np.random.normal(3.5, 0.9, 50)
cluster3_y = np.random.normal(7, 0.9, 50)
cluster3_z = np.random.normal(6, 0.9, 50)

x = np.concatenate([cluster1_x, cluster2_x, cluster3_x])
y = np.concatenate([cluster1_y, cluster2_y, cluster3_y])
z = np.concatenate([cluster1_z, cluster2_z, cluster3_z])

# Color encoding: fourth dimension based on distance from origin
color_values = np.sqrt(x**2 + y**2 + z**2)

# Create 3D plot (square format for 3D symmetry)
fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(111, projection="3d")

# Get seaborn color palette for the colormap
cmap = sns.color_palette("viridis", as_cmap=True)

# Create scatter plot with color encoding
scatter = ax.scatter(x, y, z, c=color_values, cmap=cmap, s=150, alpha=0.7, edgecolors="#306998", linewidths=1.5)

# Styling - axis labels with units
ax.set_xlabel("X Position (nm)", fontsize=20, labelpad=15)
ax.set_ylabel("Y Position (nm)", fontsize=20, labelpad=15)
ax.set_zlabel("Z Position (nm)", fontsize=20, labelpad=15)

# Title
ax.set_title("Molecular Positions · scatter-3d · seaborn · pyplots.ai", fontsize=24, pad=20)

# Tick label sizes
ax.tick_params(axis="x", labelsize=14)
ax.tick_params(axis="y", labelsize=14)
ax.tick_params(axis="z", labelsize=14)

# Add colorbar for the fourth dimension
cbar = plt.colorbar(scatter, ax=ax, shrink=0.6, aspect=15, pad=0.1)
cbar.set_label("Distance from Origin (nm)", fontsize=18)
cbar.ax.tick_params(labelsize=14)

# Set viewing angle for better perspective
ax.view_init(elev=25, azim=45)

# Adjust pane colors for better contrast
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False
ax.xaxis.pane.set_edgecolor("gray")
ax.yaxis.pane.set_edgecolor("gray")
ax.zaxis.pane.set_edgecolor("gray")

# Grid styling
ax.xaxis._axinfo["grid"]["color"] = (0.5, 0.5, 0.5, 0.3)
ax.yaxis._axinfo["grid"]["color"] = (0.5, 0.5, 0.5, 0.3)
ax.zaxis._axinfo["grid"]["color"] = (0.5, 0.5, 0.5, 0.3)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
