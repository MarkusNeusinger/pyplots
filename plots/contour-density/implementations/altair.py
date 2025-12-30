"""pyplots.ai
contour-density: Density Contour Plot
Library: altair 6.0.0 | Python 3.13.11
Quality: 72/100 | Created: 2025-12-30
"""

import altair as alt
import numpy as np
import pandas as pd
from scipy.stats import gaussian_kde


# Data - simulating temperature and humidity measurements showing natural clusters
np.random.seed(42)

# Create three distinct clusters representing different climate conditions
n1 = 150
temp1 = np.random.normal(15, 4, n1)
humidity1 = np.random.normal(30, 8, n1)

n2 = 200
temp2 = np.random.normal(25, 5, n2)
humidity2 = np.random.normal(55, 10, n2)

n3 = 150
temp3 = np.random.normal(38, 4, n3)
humidity3 = np.random.normal(75, 8, n3)

# Combine data
temperature = np.concatenate([temp1, temp2, temp3])
humidity = np.concatenate([humidity1, humidity2, humidity3])

# Compute 2D KDE for contour lines
xy = np.vstack([temperature, humidity])
kde = gaussian_kde(xy)

# Create grid for density estimation (80x80 for smooth contours)
n_grid = 80
x_grid = np.linspace(temperature.min() - 5, temperature.max() + 5, n_grid)
y_grid = np.linspace(humidity.min() - 5, humidity.max() + 5, n_grid)
xx, yy = np.meshgrid(x_grid, y_grid)
positions = np.vstack([xx.ravel(), yy.ravel()])
z = kde(positions).reshape(xx.shape)


# Marching squares algorithm for contour line extraction
def extract_contours(Z, level, x_coords, y_coords):
    """Extract contour line segments using marching squares."""
    rows, cols = Z.shape
    segments = []

    for i in range(rows - 1):
        for j in range(cols - 1):
            z00, z01, z10, z11 = Z[i, j], Z[i, j + 1], Z[i + 1, j], Z[i + 1, j + 1]
            x0, x1 = x_coords[j], x_coords[j + 1]
            y0, y1 = y_coords[i], y_coords[i + 1]

            case = sum([1 << k for k, v in enumerate([z00, z01, z10, z11]) if v >= level])
            if case in (0, 15):
                continue

            def interp(v1, v2, c1, c2):
                if abs(v2 - v1) < 1e-10:
                    return (c1 + c2) / 2
                t = (level - v1) / (v2 - v1)
                return c1 + t * (c2 - c1)

            edges = {
                "top": (interp(z00, z01, x0, x1), y0),
                "bottom": (interp(z10, z11, x0, x1), y1),
                "left": (x0, interp(z00, z10, y0, y1)),
                "right": (x1, interp(z01, z11, y0, y1)),
            }

            cases = {
                1: [("left", "top")],
                2: [("top", "right")],
                3: [("left", "right")],
                4: [("bottom", "left")],
                5: [("top", "bottom")],
                6: [("top", "left"), ("bottom", "right")]
                if (z00 + z11) / 2 >= level
                else [("top", "right"), ("bottom", "left")],
                7: [("bottom", "right")],
                8: [("right", "bottom")],
                9: [("left", "bottom"), ("right", "top")]
                if (z00 + z11) / 2 >= level
                else [("left", "top"), ("right", "bottom")],
                10: [("top", "bottom")],
                11: [("left", "bottom")],
                12: [("left", "right")],
                13: [("top", "right")],
                14: [("left", "top")],
            }

            for e1, e2 in cases.get(case, []):
                segments.append(
                    {"x1": edges[e1][0], "y1": edges[e1][1], "x2": edges[e2][0], "y2": edges[e2][1], "level": level}
                )

    return segments


# Create filled density background with discrete levels
n_levels = 12
z_min, z_max = z.min(), z.max()
levels = np.linspace(z_min, z_max, n_levels + 1)
z_binned = np.digitize(z, levels) - 1
z_binned = np.clip(z_binned, 0, n_levels - 1)
level_centers = (levels[:-1] + levels[1:]) / 2
z_discrete = level_centers[z_binned]

step = x_grid[1] - x_grid[0]
half_step = step / 2

df_fill = pd.DataFrame(
    {
        "x": xx.ravel() - half_step,
        "x2": xx.ravel() + half_step,
        "y": yy.ravel() - half_step,
        "y2": yy.ravel() + half_step,
        "density": z_discrete.ravel(),
    }
)

# Extract contour lines at multiple density levels
contour_levels = np.linspace(z.max() * 0.1, z.max() * 0.9, 8)
all_segments = []
for lvl in contour_levels:
    all_segments.extend(extract_contours(z, lvl, x_grid, y_grid))

contour_df = pd.DataFrame(all_segments)

# Filled density background
x_domain = [x_grid.min() - 1, x_grid.max() + 1]
y_domain = [y_grid.min() - 1, y_grid.max() + 1]

filled = (
    alt.Chart(df_fill)
    .mark_rect()
    .encode(
        x=alt.X("x:Q", scale=alt.Scale(domain=x_domain), title="Temperature (°C)"),
        x2="x2:Q",
        y=alt.Y("y:Q", scale=alt.Scale(domain=y_domain), title="Humidity (%)"),
        y2="y2:Q",
        color=alt.Color(
            "density:Q",
            scale=alt.Scale(scheme="blues"),
            title="Density",
            legend=alt.Legend(titleFontSize=20, labelFontSize=16, gradientLength=400, gradientThickness=25),
        ),
    )
)

# Contour lines using mark_rule for crisp isolines
contour_lines = (
    alt.Chart(contour_df)
    .mark_rule(strokeWidth=2, opacity=0.8, color="#1a4d80")
    .encode(
        x=alt.X("x1:Q", scale=alt.Scale(domain=x_domain)),
        y=alt.Y("y1:Q", scale=alt.Scale(domain=y_domain)),
        x2="x2:Q",
        y2="y2:Q",
    )
)

# Combine filled background with contour lines
chart = (
    alt.layer(filled, contour_lines)
    .properties(
        width=1400,
        height=800,
        title=alt.Title(text="contour-density · altair · pyplots.ai", fontSize=28, anchor="middle"),
    )
    .configure_axis(labelFontSize=18, titleFontSize=22, grid=True, gridColor="#cccccc", gridOpacity=0.3)
    .configure_view(strokeWidth=0)
)

# Save as PNG (1400 * 3 = 4200, 800 * 3 = 2400 - close to target)
chart.save("plot.png", scale_factor=3.0)

# Save as interactive HTML
chart.save("plot.html")
