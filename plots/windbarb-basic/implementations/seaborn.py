""" pyplots.ai
windbarb-basic: Wind Barb Plot for Meteorological Data
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 86/100 | Created: 2026-01-11
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.patches import Circle


# Set seaborn style - use white background for better barb visibility
sns.set_theme(style="white")
sns.set_context("talk", font_scale=1.2)

# Data: Simulated surface wind observations from a grid of weather stations
np.random.seed(42)

# Create a grid of observation points (7x5 grid = 35 stations)
x_grid = np.linspace(1, 13, 7)
y_grid = np.linspace(1, 9, 5)
x, y = np.meshgrid(x_grid, y_grid)
x = x.flatten()
y = y.flatten()

n_points = len(x)

# Generate wind components with full range: calm, moderate, and strong (with pennants)
# Create varied wind field showing all barb features
base_u = 20 * np.sin(x * 0.4) + 15  # Zonal component varies with x
base_v = 15 * np.cos(y * 0.5) + 10  # Meridional component varies with y
noise_u = np.random.randn(n_points) * 8
noise_v = np.random.randn(n_points) * 8

u = base_u + noise_u  # Zonal wind component (knots)
v = base_v + noise_v  # Meridional wind component (knots)

# Force some calm winds (< 2.5 knots) - these will be shown as circles
calm_indices = [0, 17, 34]  # Corners and center
for idx in calm_indices:
    u[idx] = 0.5 * (np.random.rand() - 0.5)  # Near zero
    v[idx] = 0.5 * (np.random.rand() - 0.5)

# Force some strong winds with pennants (50+ knots)
strong_indices = [6, 14, 28]  # Scattered locations
for idx in strong_indices:
    angle = np.random.rand() * 2 * np.pi
    speed_val = 55 + np.random.rand() * 15  # 55-70 knots
    u[idx] = speed_val * np.cos(angle)
    v[idx] = speed_val * np.sin(angle)

# Calculate wind speed for color mapping
speed = np.sqrt(u**2 + v**2)

# Separate calm and non-calm winds for plotting
calm_mask = speed < 2.5
barb_mask = ~calm_mask

# Create figure with seaborn styling
fig, ax = plt.subplots(figsize=(16, 9))

# Plot wind barbs for non-calm winds using viridis colormap (colorblind-safe)
if np.any(barb_mask):
    barbs = ax.barbs(
        x[barb_mask],
        y[barb_mask],
        u[barb_mask],
        v[barb_mask],
        speed[barb_mask],
        cmap="viridis",
        length=8,
        linewidth=2,
        barb_increments={"half": 5, "full": 10, "flag": 50},
        pivot="middle",
        clim=(0, 70),
    )

    # Add colorbar for wind speed
    cbar = plt.colorbar(barbs, ax=ax, pad=0.02)
    cbar.set_label("Wind Speed (knots)", fontsize=20, rotation=270, labelpad=25)
    cbar.ax.tick_params(labelsize=16)

# Plot calm winds as open circles (standard meteorological notation)
for idx in np.where(calm_mask)[0]:
    circle = Circle((x[idx], y[idx]), radius=0.25, fill=False, edgecolor="#440154", linewidth=2)
    ax.add_patch(circle)

# Styling with seaborn-enhanced matplotlib
ax.set_xlabel("Longitude (°E)", fontsize=20)
ax.set_ylabel("Latitude (°N)", fontsize=20)
ax.set_title("windbarb-basic · seaborn · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)

# Set axis limits with padding
ax.set_xlim(-0.5, 14.5)
ax.set_ylim(-0.5, 10.5)

# Remove grid - barbs provide their own spatial structure
ax.grid(False)

# Add subtle spines for axis reference
for spine in ax.spines.values():
    spine.set_color("#888888")
    spine.set_linewidth(0.8)

# Add barb notation legend
legend_text = "Barb notation: ○ = calm (<2.5 kt), half barb = 5 kt, full barb = 10 kt, pennant ▲ = 50 kt"
ax.text(0.5, -0.08, legend_text, transform=ax.transAxes, fontsize=14, ha="center", va="top", color="#555555")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
