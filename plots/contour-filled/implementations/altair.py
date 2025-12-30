"""pyplots.ai
contour-filled: Filled Contour Plot
Library: altair 6.0.0 | Python 3.13
Quality: 85/100 | Created: 2025-12-30
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - Gaussian peaks on a 2D grid (80x80 for smooth contours)
np.random.seed(42)
n_points = 80
x = np.linspace(-3, 3, n_points)
y = np.linspace(-3, 3, n_points)
X, Y = np.meshgrid(x, y)

# Create interesting surface with two Gaussian peaks and a valley
Z = (
    1.5 * np.exp(-((X - 1) ** 2 + (Y - 1) ** 2) / 0.8)  # Peak at (1, 1)
    + 1.2 * np.exp(-((X + 1) ** 2 + (Y + 0.5) ** 2) / 1.0)  # Peak at (-1, -0.5)
    - 0.6 * np.exp(-((X) ** 2 + (Y - 1.5) ** 2) / 0.6)  # Valley at (0, 1.5)
    + 0.2 * np.sin(X * 2) * np.cos(Y * 2)  # Subtle ripples
)

# Create discrete contour levels (8 levels for better visual distinction)
n_levels = 8
z_min, z_max = Z.min(), Z.max()
levels = np.linspace(z_min, z_max, n_levels + 1)

# Bin z-values into discrete levels for filled contour appearance
Z_binned = np.digitize(Z, levels) - 1
Z_binned = np.clip(Z_binned, 0, n_levels - 1)
# Map back to level center values for color mapping
level_centers = (levels[:-1] + levels[1:]) / 2
Z_discrete = level_centers[Z_binned]

# Calculate step size for proper rectangle sizing
step = x[1] - x[0]
half_step = step / 2

# Flatten grid data for Altair with explicit rectangle bounds
df = pd.DataFrame(
    {
        "x": X.ravel() - half_step,
        "x2": X.ravel() + half_step,
        "y": Y.ravel() - half_step,
        "y2": Y.ravel() + half_step,
        "z": Z_discrete.ravel(),
        "z_raw": Z.ravel(),
    }
)

# Create filled contour using mark_rect with discrete color bands
filled_contour = (
    alt.Chart(df)
    .mark_rect()
    .encode(
        x=alt.X(
            "x:Q",
            title="X Coordinate",
            scale=alt.Scale(domain=[-3.1, 3.1]),
            axis=alt.Axis(labelFontSize=18, titleFontSize=22, tickCount=7),
        ),
        x2="x2:Q",
        y=alt.Y(
            "y:Q",
            title="Y Coordinate",
            scale=alt.Scale(domain=[-3.1, 3.1]),
            axis=alt.Axis(labelFontSize=18, titleFontSize=22, tickCount=7),
        ),
        y2="y2:Q",
        color=alt.Color(
            "z:Q",
            title="Intensity",
            scale=alt.Scale(scheme="viridis"),
            legend=alt.Legend(titleFontSize=20, labelFontSize=16, gradientLength=400, gradientThickness=25),
        ),
    )
)

# Create contour lines using isoline approach
# Extract boundary points where z crosses each level
contour_lines_data = []
for level_val in levels[1:-1]:  # Skip min/max levels
    # Find cells where the level boundary crosses
    for i in range(n_points - 1):
        for j in range(n_points - 1):
            cell_z = [Z[i, j], Z[i, j + 1], Z[i + 1, j], Z[i + 1, j + 1]]
            z_min_cell = min(cell_z)
            z_max_cell = max(cell_z)
            if z_min_cell <= level_val <= z_max_cell:
                # This cell contains the contour line
                contour_lines_data.append({"x": X[i, j], "y": Y[i, j], "level": level_val})

contour_df = pd.DataFrame(contour_lines_data)

# Add contour line markers as prominent points along level boundaries
contour_overlay = (
    alt.Chart(contour_df)
    .mark_point(size=12, opacity=0.7, color="white", filled=True)
    .encode(x=alt.X("x:Q", scale=alt.Scale(domain=[-3.1, 3.1])), y=alt.Y("y:Q", scale=alt.Scale(domain=[-3.1, 3.1])))
)

# Combine layers
chart = (
    alt.layer(filled_contour, contour_overlay)
    .properties(
        width=1400,
        height=800,
        title=alt.Title(text="contour-filled · altair · pyplots.ai", fontSize=28, anchor="middle"),
    )
    .configure_view(strokeWidth=0)
)

# Save PNG (4800 × 2700 px with scale_factor=3)
chart.save("plot.png", scale_factor=3.0)

# Save interactive HTML
chart.save("plot.html")
