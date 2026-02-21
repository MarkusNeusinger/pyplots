""" pyplots.ai
hexbin-basic: Basic Hexbin Plot
Library: matplotlib 3.10.8 | Python 3.14.3
Quality: 88/100 | Created: 2026-02-21
"""

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np


# Data - simulated city sensor readings with clustered hotspots
np.random.seed(42)
n_points = 10000

# Three distinct sensor clusters at different locations and densities
downtown_x = np.random.randn(n_points // 2) * 1.5 + 2
downtown_y = np.random.randn(n_points // 2) * 1.5 + 2
industrial_x = np.random.randn(n_points // 3) * 1.0 - 2
industrial_y = np.random.randn(n_points // 3) * 1.0 - 1
suburb_x = np.random.randn(n_points // 6) * 0.8 + 1
suburb_y = np.random.randn(n_points // 6) * 0.8 - 2

longitude = np.concatenate([downtown_x, industrial_x, suburb_x])
latitude = np.concatenate([downtown_y, industrial_y, suburb_y])

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

hb = ax.hexbin(
    longitude,
    latitude,
    gridsize=30,
    cmap="viridis",
    mincnt=1,
    linewidths=0.3,
    edgecolors="white",
    norm=mcolors.LogNorm(),
)

# Colorbar
cbar = fig.colorbar(hb, ax=ax, shrink=0.85, pad=0.02)
cbar.set_label("Sensor Reading Count", fontsize=20)
cbar.ax.tick_params(labelsize=16)

# Style
ax.set_xlabel("Longitude (km)", fontsize=20)
ax.set_ylabel("Latitude (km)", fontsize=20)
ax.set_title("hexbin-basic · matplotlib · pyplots.ai", fontsize=24, fontweight="medium")
ax.tick_params(axis="both", labelsize=16)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.set_facecolor("#fafafa")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
