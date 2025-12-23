""" pyplots.ai
hexbin-basic: Basic Hexbin Plot
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 90/100 | Created: 2025-12-23
"""

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
sns.set_theme(style="whitegrid", context="talk", font_scale=1.2)

# Create JointGrid for hexbin with marginal distributions
g = sns.JointGrid(data=df, x="Longitude", y="Latitude", height=12, ratio=5, space=0.2)

# Main hexbin plot using plot_joint
hb = g.ax_joint.hexbin(df["Longitude"], df["Latitude"], gridsize=35, cmap="viridis", mincnt=1, edgecolors="none")

# Marginal distributions using seaborn's histplot
g.plot_marginals(sns.histplot, kde=True, color="#306998", alpha=0.6, linewidth=0)

# Add colorbar to show density scale
cbar = g.figure.colorbar(hb, ax=g.ax_joint, pad=0.02, shrink=0.8)
cbar.set_label("Point Count", fontsize=20)
cbar.ax.tick_params(labelsize=16)

# Labels and title with proper sizing
g.ax_joint.set_xlabel("Longitude (°W)", fontsize=20)
g.ax_joint.set_ylabel("Latitude (°N)", fontsize=20)
g.ax_joint.tick_params(axis="both", labelsize=16)

# Subtle grid on main plot
g.ax_joint.grid(True, alpha=0.3, linestyle="--", linewidth=0.8)

# Title at top of figure
g.figure.suptitle("hexbin-basic · seaborn · pyplots.ai", fontsize=24, y=0.98)

# Adjust layout to prevent clipping
g.figure.tight_layout(rect=[0, 0, 1, 0.96])
g.savefig("plot.png", dpi=300, bbox_inches="tight")
