""" pyplots.ai
hexbin-basic: Basic Hexbin Plot
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 86/100 | Created: 2025-12-23
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Data - simulate GPS coordinates for urban traffic hotspot analysis
np.random.seed(42)

# Create realistic GPS coordinate clusters representing traffic hotspots
# Using a larger dataset (50,000 points) to demonstrate hexbin advantage over scatter
n_points = 50000

# Downtown business district - high density
downtown = np.random.multivariate_normal([-73.985, 40.748], [[0.0001, 0.00005], [0.00005, 0.0001]], n_points // 2)

# Airport area - medium density
airport = np.random.multivariate_normal([-73.875, 40.775], [[0.00008, -0.00003], [-0.00003, 0.00008]], n_points // 3)

# Shopping district - smaller cluster
shopping = np.random.multivariate_normal([-73.965, 40.785], [[0.00004, 0], [0, 0.00006]], n_points // 6)

# Combine clusters into DataFrame for seaborn
longitude = np.concatenate([downtown[:, 0], airport[:, 0], shopping[:, 0]])
latitude = np.concatenate([downtown[:, 1], airport[:, 1], shopping[:, 1]])
df = pd.DataFrame({"Longitude": longitude, "Latitude": latitude})

# Set seaborn style for clean aesthetics
sns.set_style("whitegrid")
sns.set_context("talk", font_scale=1.2)

# Create figure using seaborn's JointGrid for hexbin visualization
g = sns.JointGrid(data=df, x="Longitude", y="Latitude", height=9, ratio=6)

# Main hexbin plot using seaborn's plot_joint with matplotlib hexbin
g.plot_joint(plt.hexbin, gridsize=35, cmap="viridis", mincnt=1, edgecolors="none")

# Marginal distributions using seaborn's histplot
g.plot_marginals(sns.histplot, kde=True, color="#306998", alpha=0.6)

# Add colorbar to show density scale
cbar = g.figure.colorbar(g.ax_joint.collections[0], ax=g.ax_joint, pad=0.02)
cbar.set_label("Point Count", fontsize=20)
cbar.ax.tick_params(labelsize=16)

# Labels and title with proper sizing
g.ax_joint.set_xlabel("Longitude (°W)", fontsize=20)
g.ax_joint.set_ylabel("Latitude (°N)", fontsize=20)
g.figure.suptitle("hexbin-basic · seaborn · pyplots.ai", fontsize=24, y=1.02)
g.ax_joint.tick_params(axis="both", labelsize=16)

# Adjust grid to be subtle
g.ax_joint.grid(True, alpha=0.3, linestyle="--")

# Resize figure to match expected dimensions
g.figure.set_size_inches(16, 9)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
