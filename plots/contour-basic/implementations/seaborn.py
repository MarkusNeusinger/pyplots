"""
contour-basic: Basic Contour Plot
Library: seaborn
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Set seaborn style for better aesthetics
sns.set_theme(style="whitegrid")

# Data - create a 50x50 meshgrid
np.random.seed(42)
x = np.linspace(-3, 3, 50)
y = np.linspace(-3, 3, 50)
X, Y = np.meshgrid(x, y)

# Mathematical function: Gaussian-like surface with multiple peaks
Z = np.exp(-(X**2) - Y**2) + 0.6 * np.exp(-((X - 1.5) ** 2) - (Y - 1) ** 2)

# Create plot (4800x2700 px)
fig, ax = plt.subplots(figsize=(16, 9))

# Filled contours with seaborn-compatible colormap
contourf = ax.contourf(X, Y, Z, levels=15, cmap="viridis", alpha=0.9)

# Contour lines for clarity
contour = ax.contour(X, Y, Z, levels=15, colors="white", linewidths=1.5, alpha=0.5)

# Label key contour levels
ax.clabel(contour, inline=True, fontsize=14, fmt="%.2f", colors="white")

# Colorbar to show value scale
cbar = fig.colorbar(contourf, ax=ax, shrink=0.9, aspect=30)
cbar.ax.tick_params(labelsize=16)
cbar.set_label("Surface Value (Z)", fontsize=20)

# Labels and styling
ax.set_xlabel("X Coordinate", fontsize=20)
ax.set_ylabel("Y Coordinate", fontsize=20)
ax.set_title("contour-basic · seaborn · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)

# Remove grid for cleaner contour display
ax.grid(False)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
