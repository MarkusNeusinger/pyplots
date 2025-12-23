""" pyplots.ai
contour-basic: Basic Contour Plot
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 72/100 | Created: 2025-12-23
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Data - Bivariate temperature distribution from weather station measurements
# Simulates temperature readings across a geographic region with two warm centers
np.random.seed(42)

# Generate 2000 data points representing temperature sensor readings
# Two clusters representing urban heat islands at different locations
n_samples = 2000

# Northern urban center (warmer, larger area)
x1 = np.random.normal(loc=25, scale=8, size=n_samples // 2)  # Latitude proxy
y1 = np.random.normal(loc=35, scale=6, size=n_samples // 2)  # Longitude proxy

# Southern urban center (slightly cooler, smaller area)
x2 = np.random.normal(loc=55, scale=5, size=n_samples // 2)  # Latitude proxy
y2 = np.random.normal(loc=20, scale=4, size=n_samples // 2)  # Longitude proxy

# Combine the two distributions
x = np.concatenate([x1, x2])
y = np.concatenate([y1, y2])

# Create plot (4800x2700 px)
fig, ax = plt.subplots(figsize=(16, 9))

# Use seaborn's kdeplot for 2D density contours - this is seaborn's native contour function
# Shows both filled contours and contour lines
sns.kdeplot(
    x=x,
    y=y,
    ax=ax,
    fill=True,
    levels=12,
    cmap="viridis",
    alpha=0.9,
    thresh=0.05,
    cbar=True,
    cbar_kws={"label": "Probability Density", "shrink": 0.85},
)

# Add contour lines for additional clarity
sns.kdeplot(x=x, y=y, ax=ax, fill=False, levels=12, colors="white", linewidths=0.8, alpha=0.7)

# Labels and styling
ax.set_xlabel("Easting (km)", fontsize=20)
ax.set_ylabel("Northing (km)", fontsize=20)
ax.set_title("contour-basic · seaborn · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)

# Style the colorbar
cbar = ax.collections[0].colorbar
if cbar:
    cbar.ax.tick_params(labelsize=16)
    cbar.set_label("Probability Density", fontsize=20)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
