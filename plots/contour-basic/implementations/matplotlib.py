"""pyplots.ai
contour-basic: Basic Contour Plot
Library: matplotlib | Python 3.13
Quality: pending | Created: 2025-12-23
"""

import matplotlib.pyplot as plt
import numpy as np


# Data - create a 2D scalar field using a mathematical function
np.random.seed(42)
x = np.linspace(-3, 3, 50)
y = np.linspace(-3, 3, 50)
X, Y = np.meshgrid(x, y)

# Z represents a surface with peaks and valleys (combination of Gaussians)
Z = (
    np.exp(-((X - 1) ** 2 + (Y - 1) ** 2))
    + 0.8 * np.exp(-((X + 1.5) ** 2 + (Y + 1) ** 2))
    - 0.5 * np.exp(-((X) ** 2 + (Y - 1.5) ** 2) / 0.5)
)

# Create plot (4800x2700 px)
fig, ax = plt.subplots(figsize=(16, 9))

# Filled contours with colormap
contourf = ax.contourf(X, Y, Z, levels=15, cmap="viridis", alpha=0.9)

# Contour lines for additional clarity
contour = ax.contour(X, Y, Z, levels=15, colors="white", linewidths=1.5, alpha=0.6)

# Label key contour levels
ax.clabel(contour, inline=True, fontsize=14, fmt="%.2f")

# Colorbar to show value scale
cbar = fig.colorbar(contourf, ax=ax, shrink=0.9, aspect=20)
cbar.set_label("Z Value", fontsize=20)
cbar.ax.tick_params(labelsize=16)

# Labels and styling
ax.set_xlabel("X Coordinate", fontsize=20)
ax.set_ylabel("Y Coordinate", fontsize=20)
ax.set_title("contour-basic · matplotlib · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
