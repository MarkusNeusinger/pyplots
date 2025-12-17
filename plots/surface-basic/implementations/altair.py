"""
surface-basic: Basic 3D Surface Plot
Library: altair
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - create a smooth surface z = sin(x) * cos(y)
np.random.seed(42)

# Grid setup - 40x40 for smooth surface
n_points = 40
x = np.linspace(-3, 3, n_points)
y = np.linspace(-3, 3, n_points)
X, Y = np.meshgrid(x, y)

# Surface function
Z = np.sin(X) * np.cos(Y)

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

        rect_data.append({"x1": x1, "x2": x2, "y1": y1, "y2": y2, "z": avg_z, "depth": depth})

# Sort by depth (back to front - painter's algorithm)
rect_data.sort(key=lambda r: r["depth"], reverse=True)

# Assign order for rendering
for idx, r in enumerate(rect_data):
    r["order"] = idx

df_rects = pd.DataFrame(rect_data)

# Create surface chart with filled rectangles
surface = (
    alt.Chart(df_rects)
    .mark_rect(strokeWidth=0.5, stroke="#306998", strokeOpacity=0.3)
    .encode(
        x=alt.X("x1:Q", axis=alt.Axis(title="X (projected)", labelFontSize=18, titleFontSize=22)),
        y=alt.Y("y1:Q", axis=alt.Axis(title="Z (height)", labelFontSize=18, titleFontSize=22)),
        x2=alt.X2("x2:Q"),
        y2=alt.Y2("y2:Q"),
        color=alt.Color(
            "z:Q",
            scale=alt.Scale(scheme="viridis"),
            legend=alt.Legend(title="Z Value", titleFontSize=20, labelFontSize=16),
        ),
        order=alt.Order("order:Q"),
    )
)

# Combine into final chart
chart = (
    surface.properties(width=1600, height=900, title=alt.Title("surface-basic · altair · pyplots.ai", fontSize=28))
    .configure_axis(grid=True, gridOpacity=0.3, gridDash=[6, 4])
    .configure_view(strokeWidth=0)
)

# Save outputs
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
