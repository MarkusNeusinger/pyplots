"""pyplots.ai
contour-basic: Basic Contour Plot
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 72/100 | Created: 2025-12-23
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Data - Topographic elevation model of a terrain region
np.random.seed(42)

# Create meshgrid for terrain (50x50 resolution)
x = np.linspace(0, 10, 50)  # Distance East (km)
y = np.linspace(0, 8, 50)  # Distance North (km)
X, Y = np.meshgrid(x, y)

# Mathematical function simulating terrain elevation z = f(x, y)
# Two hills with a saddle point and gentle slope
z = (
    300 * np.exp(-((X - 3) ** 2 + (Y - 5) ** 2) / 4)  # Northern hill
    + 250 * np.exp(-((X - 7) ** 2 + (Y - 3) ** 2) / 3)  # Southern hill
    + 50 * np.sin(X * 0.5) * np.cos(Y * 0.3)  # Gentle undulations
    + 100  # Base elevation
)

# Create plot (4800x2700 px)
fig, ax = plt.subplots(figsize=(16, 9))
sns.set_style("white")  # Clean background for contour plots

# Filled contours for elevation bands
levels = np.linspace(z.min(), z.max(), 12)
filled = ax.contourf(X, Y, z, levels=levels, cmap="viridis", alpha=0.9)

# Add contour lines for clarity
contours = ax.contour(X, Y, z, levels=levels, colors="white", linewidths=0.8, alpha=0.7)

# Label key contour levels
ax.clabel(contours, inline=True, fontsize=14, fmt="%.0f m", colors="white")

# Colorbar with elevation scale
cbar = fig.colorbar(filled, ax=ax, shrink=0.85, pad=0.02)
cbar.set_label("Elevation (m)", fontsize=20)
cbar.ax.tick_params(labelsize=16)

# Labels and styling
ax.set_xlabel("Distance East (km)", fontsize=20)
ax.set_ylabel("Distance North (km)", fontsize=20)
ax.set_title("contour-basic · seaborn · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
