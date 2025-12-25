""" pyplots.ai
scatter-3d: 3D Scatter Plot
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 35/100 | Created: 2025-12-25
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Set seaborn style for consistent aesthetics
sns.set_theme(style="whitegrid")
sns.set_context("talk", font_scale=1.2)

# Data: 3D clustered data representing molecular positions
np.random.seed(42)

# Create 3 clusters in 3D space
n_per_cluster = 50

cluster1_x = np.random.normal(2, 0.8, n_per_cluster)
cluster1_y = np.random.normal(2, 0.8, n_per_cluster)
cluster1_z = np.random.normal(2, 0.8, n_per_cluster)

cluster2_x = np.random.normal(5, 1.0, n_per_cluster)
cluster2_y = np.random.normal(5, 1.0, n_per_cluster)
cluster2_z = np.random.normal(3, 1.0, n_per_cluster)

cluster3_x = np.random.normal(3.5, 0.9, n_per_cluster)
cluster3_y = np.random.normal(7, 0.9, n_per_cluster)
cluster3_z = np.random.normal(6, 0.9, n_per_cluster)

# Fourth dimension: energy values (color encoding)
cluster1_energy = np.random.uniform(0.5, 2.0, n_per_cluster)
cluster2_energy = np.random.uniform(1.5, 3.5, n_per_cluster)
cluster3_energy = np.random.uniform(3.0, 5.0, n_per_cluster)

x = np.concatenate([cluster1_x, cluster2_x, cluster3_x])
y = np.concatenate([cluster1_y, cluster2_y, cluster3_y])
z = np.concatenate([cluster1_z, cluster2_z, cluster3_z])
energy = np.concatenate([cluster1_energy, cluster2_energy, cluster3_energy])

# Create 3D plot (square format 3600x3600 at dpi=300)
fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(111, projection="3d")

# Get seaborn colormap for the fourth dimension (energy)
cmap = sns.color_palette("viridis", as_cmap=True)

# Create scatter plot with color encoding for fourth dimension (energy)
scatter = ax.scatter(x, y, z, c=energy, cmap=cmap, s=150, alpha=0.7, edgecolors="white", linewidths=0.8)

# Styling - axis labels with units and increased padding
ax.set_xlabel("X Position (nm)", fontsize=20, labelpad=20)
ax.set_ylabel("Y Position (nm)", fontsize=20, labelpad=20)
ax.set_zlabel("Z Position (nm)", fontsize=20, labelpad=20)

# Title
ax.set_title("scatter-3d · seaborn · pyplots.ai", fontsize=24, pad=25)

# Tick label sizes
ax.tick_params(axis="x", labelsize=14, pad=8)
ax.tick_params(axis="y", labelsize=14, pad=8)
ax.tick_params(axis="z", labelsize=14, pad=8)

# Add colorbar for the fourth dimension (energy)
cbar = plt.colorbar(scatter, ax=ax, shrink=0.5, aspect=20, pad=0.12)
cbar.set_label("Energy (eV)", fontsize=18, labelpad=15)
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

# Adjust subplot to prevent label cutoff
fig.subplots_adjust(left=0.05, right=0.85, bottom=0.05, top=0.95)

plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
