"""pyplots.ai
hexbin-map-geographic: Hexagonal Binning Map
Library: seaborn | Python 3.13
Quality: pending | Created: 2025-01-20
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Set seaborn style for consistent aesthetics
sns.set_theme(style="white")

# Data: Simulated taxi pickup locations in New York City area
np.random.seed(42)
n_points = 5000

# NYC bounding box approximately
center_lon, center_lat = -73.98, 40.75
lon = np.random.normal(center_lon, 0.08, n_points)
lat = np.random.normal(center_lat, 0.05, n_points)

# Add clustering for realistic density patterns
# Manhattan cluster (higher density)
mask1 = np.random.random(n_points) < 0.4
lon[mask1] = np.random.normal(-73.97, 0.015, np.sum(mask1))
lat[mask1] = np.random.normal(40.78, 0.015, np.sum(mask1))

# Downtown/Financial District cluster
mask2 = np.random.random(n_points) < 0.2
lon[mask2] = np.random.normal(-74.01, 0.01, np.sum(mask2))
lat[mask2] = np.random.normal(40.71, 0.012, np.sum(mask2))

# Brooklyn cluster
mask3 = np.random.random(n_points) < 0.15
lon[mask3] = np.random.normal(-73.95, 0.025, np.sum(mask3))
lat[mask3] = np.random.normal(40.68, 0.018, np.sum(mask3))

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Create hexbin plot - seaborn uses matplotlib underneath
hexbin = ax.hexbin(lon, lat, gridsize=35, cmap="YlOrRd", mincnt=1, alpha=0.85, edgecolors="white", linewidths=0.4)

# Add colorbar with appropriate sizing
cbar = plt.colorbar(hexbin, ax=ax, shrink=0.8, pad=0.02, aspect=25)
cbar.set_label("Pickup Count", fontsize=18, labelpad=10)
cbar.ax.tick_params(labelsize=14)

# Add geographic reference lines (simulating map grid)
ax.axhline(y=40.75, color="#888888", linewidth=0.8, linestyle="--", alpha=0.5)
ax.axvline(x=-74.0, color="#888888", linewidth=0.8, linestyle="--", alpha=0.5)

# Add geographic annotations for context
ax.annotate("Manhattan", xy=(-73.85, 40.82), fontsize=12, color="#333333", ha="center", alpha=0.7, fontweight="bold")
ax.annotate("Brooklyn", xy=(-73.95, 40.65), fontsize=12, color="#333333", ha="center", alpha=0.7, fontweight="bold")
ax.annotate(
    "Financial\nDistrict", xy=(-74.08, 40.71), fontsize=10, color="#333333", ha="center", alpha=0.7, fontweight="bold"
)

# Styling
ax.set_xlabel("Longitude", fontsize=20)
ax.set_ylabel("Latitude", fontsize=20)
ax.tick_params(axis="both", labelsize=14)

# Title with required format
ax.set_title("NYC Taxi Pickups · hexbin-map-geographic · seaborn · pyplots.ai", fontsize=22, pad=15)

# Set axis limits to focus on data area with padding
lon_margin = (lon.max() - lon.min()) * 0.1
lat_margin = (lat.max() - lat.min()) * 0.1
ax.set_xlim(lon.min() - lon_margin, lon.max() + lon_margin)
ax.set_ylim(lat.min() - lat_margin, lat.max() + lat_margin)

# Add subtle grid
ax.grid(True, alpha=0.3, linestyle="-", linewidth=0.5)

# Add a subtle background to indicate land area
ax.set_facecolor("#f5f5f5")

# Equal aspect ratio for proper geographic representation
ax.set_aspect("equal", adjustable="box")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
