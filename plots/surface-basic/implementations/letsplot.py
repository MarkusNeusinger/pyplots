"""
surface-basic: Basic 3D Surface Plot
Library: letsplot
"""

import numpy as np
import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    element_text,
    geom_rect,
    ggplot,
    ggsize,
    labs,
    scale_fill_viridis,
    theme,
    theme_minimal,
)
from lets_plot.export import ggsave


LetsPlot.setup_html()

# Data - create a smooth surface z = sin(sqrt(x^2 + y^2)) * exp(-0.1*(x^2+y^2))
np.random.seed(42)

# Grid setup - 40x40 for smooth surface
n_points = 40
x = np.linspace(-4, 4, n_points)
y = np.linspace(-4, 4, n_points)
X, Y = np.meshgrid(x, y)

# Surface function - Gaussian-like surface with interesting features
Z = np.sin(np.sqrt(X**2 + Y**2)) * np.exp(-0.1 * (X**2 + Y**2))

# 3D to 2D projection (elevation=25, azimuth=45)
elev_rad = np.radians(25)
azim_rad = np.radians(45)

# Rotation around z-axis (azimuth)
X_rot = X * np.cos(azim_rad) - Y * np.sin(azim_rad)
Y_rot = X * np.sin(azim_rad) + Y * np.cos(azim_rad)

# Rotation around x-axis (elevation) and project
X_proj = X_rot
Z_proj = Y_rot * np.sin(elev_rad) + Z * np.cos(elev_rad)

# Build rectangles using actual quad corners for proper filling
rect_data = []
for i in range(n_points - 1):
    for j in range(n_points - 1):
        # Use actual quad corners for x and y extents
        x1 = min(X_proj[i, j], X_proj[i, j + 1], X_proj[i + 1, j], X_proj[i + 1, j + 1])
        x2 = max(X_proj[i, j], X_proj[i, j + 1], X_proj[i + 1, j], X_proj[i + 1, j + 1])
        y1 = min(Z_proj[i, j], Z_proj[i, j + 1], Z_proj[i + 1, j], Z_proj[i + 1, j + 1])
        y2 = max(Z_proj[i, j], Z_proj[i, j + 1], Z_proj[i + 1, j], Z_proj[i + 1, j + 1])

        # Average z for color (original Z, not projected)
        avg_z = (Z[i, j] + Z[i, j + 1] + Z[i + 1, j + 1] + Z[i + 1, j]) / 4

        # Depth for sorting (painter's algorithm - back to front)
        depth = (Y_rot[i, j] + Y_rot[i, j + 1] + Y_rot[i + 1, j + 1] + Y_rot[i + 1, j]) / 4

        rect_data.append({"xmin": x1, "xmax": x2, "ymin": y1, "ymax": y2, "z": avg_z, "depth": depth})

# Sort by depth (back to front - painter's algorithm)
rect_data.sort(key=lambda r: r["depth"], reverse=True)

df = pd.DataFrame(rect_data)

# Create 3D surface visualization using projected rectangles
plot = (
    ggplot(df, aes(xmin="xmin", xmax="xmax", ymin="ymin", ymax="ymax", fill="z"))
    + geom_rect(color="#306998", size=0.1, alpha=0.9)
    + scale_fill_viridis(name="Z Value")
    + labs(x="X (projected)", y="Z (height)", title="surface-basic · letsplot · pyplots.ai")
    + theme_minimal()
    + theme(
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        plot_title=element_text(size=24),
        legend_text=element_text(size=14),
        legend_title=element_text(size=16),
        panel_grid=element_text(size=0.3),
    )
    + ggsize(1600, 900)
)

# Save PNG (scale=3 gives 4800x2700)
ggsave(plot, "plot.png", path=".", scale=3)

# Save HTML for interactivity
ggsave(plot, "plot.html", path=".")
