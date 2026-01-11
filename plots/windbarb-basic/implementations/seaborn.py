""" pyplots.ai
windbarb-basic: Wind Barb Plot for Meteorological Data
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 78/100 | Created: 2026-01-11
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Set seaborn style for clean aesthetics
sns.set_theme(style="whitegrid")
sns.set_context("talk", font_scale=1.2)

# Data: Simulated surface wind observations from a grid of weather stations
np.random.seed(42)

# Create a grid of observation points (8x6 grid = 48 stations)
x_grid = np.linspace(0, 14, 8)
y_grid = np.linspace(0, 10, 6)
x, y = np.meshgrid(x_grid, y_grid)
x = x.flatten()
y = y.flatten()

# Generate wind components (u=zonal, v=meridional) in knots
# Create a varied wind field with different speeds and directions
base_u = 15 * np.sin(x * 0.3) + 10  # Zonal component varies with x
base_v = 10 * np.cos(y * 0.4) + 5  # Meridional component varies with y
noise_u = np.random.randn(len(x)) * 5
noise_v = np.random.randn(len(x)) * 5

u = base_u + noise_u  # Zonal wind component (knots)
v = base_v + noise_v  # Meridional wind component (knots)

# Calculate wind speed for color mapping
speed = np.sqrt(u**2 + v**2)

# Create figure with seaborn styling
fig, ax = plt.subplots(figsize=(16, 9))

# Plot wind barbs using matplotlib's barbs (seaborn doesn't have native barbs)
# Seaborn provides the styling context
barbs = ax.barbs(
    x,
    y,
    u,
    v,
    speed,
    cmap="YlOrRd",
    length=8,
    linewidth=2,
    barb_increments={"half": 5, "full": 10, "flag": 50},
    pivot="middle",
)

# Add colorbar for wind speed
cbar = plt.colorbar(barbs, ax=ax, pad=0.02)
cbar.set_label("Wind Speed (knots)", fontsize=20)
cbar.ax.tick_params(labelsize=16)

# Styling with seaborn-enhanced matplotlib
ax.set_xlabel("Longitude (°E)", fontsize=20)
ax.set_ylabel("Latitude (°N)", fontsize=20)
ax.set_title("windbarb-basic · seaborn · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)

# Set axis limits with padding
ax.set_xlim(-1, 15)
ax.set_ylim(-1, 11)

# Adjust grid for subtle appearance
ax.grid(True, alpha=0.3, linestyle="--")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
