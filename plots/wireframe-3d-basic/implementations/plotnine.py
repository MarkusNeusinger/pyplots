"""
wireframe-3d-basic: Basic 3D Wireframe Plot
Library: plotnine

Note: plotnine doesn't have native 3D support.
Using matplotlib 3D directly with plotnine-style aesthetics.
"""

import matplotlib.pyplot as plt
import numpy as np


# Data - Ripple function z = sin(sqrt(x^2 + y^2))
np.random.seed(42)
x = np.linspace(-4, 4, 40)
y = np.linspace(-4, 4, 40)
X, Y = np.meshgrid(x, y)

# Ripple function creates concentric waves from origin
R = np.sqrt(X**2 + Y**2)
Z = np.sin(R)

# Create 3D figure (16:9 aspect ratio for 4800x2700 at 300 dpi)
fig = plt.figure(figsize=(16, 9))
ax = fig.add_subplot(111, projection="3d")

# Draw wireframe with Python Blue color
ax.plot_wireframe(X, Y, Z, color="#306998", linewidth=0.8, alpha=0.9)

# Set viewing angle (elevation and azimuth per spec)
ax.view_init(elev=30, azim=45)

# Style axes with scaled font sizes for 4800x2700 resolution
ax.set_xlabel("X", fontsize=20, labelpad=15)
ax.set_ylabel("Y", fontsize=20, labelpad=15)
ax.set_zlabel("Z", fontsize=20, labelpad=15)

# Title in required format
ax.set_title("wireframe-3d-basic · plotnine · pyplots.ai", fontsize=28, fontweight="bold", pad=30)

# Scale tick labels for visibility
ax.tick_params(axis="both", labelsize=14)
ax.tick_params(axis="z", labelsize=14)

# Subtle grid (3D axes have grid by default, adjust pane colors)
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False
ax.xaxis.pane.set_edgecolor("#cccccc")
ax.yaxis.pane.set_edgecolor("#cccccc")
ax.zaxis.pane.set_edgecolor("#cccccc")
ax.grid(True, alpha=0.3, linestyle="--")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
