"""
contour-basic: Basic Contour Plot
Library: altair
"""

import altair as alt
import numpy as np
import pandas as pd


# Linear interpolation for contour edge crossings
def interp(za, zb, a, b, level):
    """Interpolate position where contour crosses between two points."""
    t = (level - za) / (zb - za) if zb != za else 0.5
    return a + t * (b - a)


# Marching squares to extract contour lines from 2D grid
def extract_contours(x, y, Z, levels):
    """Extract contour line segments using marching squares algorithm."""
    segments = []

    for level in levels:
        for i in range(len(y) - 1):
            for j in range(len(x) - 1):
                # Get 4 corners of cell
                z00 = Z[i, j]
                z10 = Z[i + 1, j]
                z01 = Z[i, j + 1]
                z11 = Z[i + 1, j + 1]

                # Calculate which corners are above/below level
                case = 0
                if z00 >= level:
                    case |= 1
                if z10 >= level:
                    case |= 2
                if z01 >= level:
                    case |= 4
                if z11 >= level:
                    case |= 8

                # Skip if all corners same side
                if case == 0 or case == 15:
                    continue

                x0, x1 = x[j], x[j + 1]
                y0, y1 = y[i], y[i + 1]

                # Edge midpoints where contour crosses
                edges = {}
                if (case & 1) != (case & 2) >> 1:  # Bottom edge
                    edges["bottom"] = (interp(z00, z10, x0, x0, level), interp(z00, z10, y0, y1, level))
                if (case & 2) >> 1 != (case & 8) >> 3:  # Right edge
                    edges["right"] = (interp(z10, z11, x0, x1, level), interp(z10, z11, y1, y1, level))
                if (case & 4) >> 2 != (case & 8) >> 3:  # Top edge
                    edges["top"] = (interp(z01, z11, x1, x1, level), interp(z01, z11, y0, y1, level))
                if (case & 1) != (case & 4) >> 2:  # Left edge
                    edges["left"] = (interp(z00, z01, x0, x1, level), interp(z00, z01, y0, y0, level))

                # Connect appropriate edges based on case
                edge_list = list(edges.values())
                if len(edge_list) >= 2:
                    segments.append(
                        {
                            "x1": edge_list[0][0],
                            "y1": edge_list[0][1],
                            "x2": edge_list[1][0],
                            "y2": edge_list[1][1],
                            "level": level,
                        }
                    )
                    if len(edge_list) == 4:  # Saddle point
                        segments.append(
                            {
                                "x1": edge_list[2][0],
                                "y1": edge_list[2][1],
                                "x2": edge_list[3][0],
                                "y2": edge_list[3][1],
                                "level": level,
                            }
                        )

    return pd.DataFrame(segments)


# Data - 2D Gaussian function on meshgrid
np.random.seed(42)
x = np.linspace(-3, 3, 80)
y = np.linspace(-3, 3, 80)
X, Y = np.meshgrid(x, y)

# Two overlapping Gaussian peaks
Z = np.exp(-((X - 1) ** 2 + (Y - 1) ** 2)) + 0.8 * np.exp(-((X + 1) ** 2 + (Y + 0.5) ** 2))

# Flatten to DataFrame for filled contour background
df_fill = pd.DataFrame({"x": X.ravel(), "y": Y.ravel(), "z": Z.ravel()})

# Extract contour lines at specific levels
levels = np.linspace(0.1, 1.6, 12)
df_lines = extract_contours(x, y, Z, levels)

# Filled contour background using rect marks
filled = (
    alt.Chart(df_fill)
    .mark_rect()
    .encode(
        x=alt.X("x:Q", bin=alt.Bin(maxbins=80), title="X Value"),
        y=alt.Y("y:Q", bin=alt.Bin(maxbins=80), title="Y Value"),
        color=alt.Color(
            "mean(z):Q",
            scale=alt.Scale(scheme="viridis"),
            title="Z Value",
            legend=alt.Legend(titleFontSize=20, labelFontSize=18, gradientLength=450, gradientThickness=30),
        ),
    )
)

# Contour lines overlaid
lines = (
    alt.Chart(df_lines)
    .mark_rule(strokeWidth=2.5, opacity=0.85)
    .encode(
        x="x1:Q",
        y="y1:Q",
        x2="x2:Q",
        y2="y2:Q",
        color=alt.Color("level:Q", scale=alt.Scale(scheme="viridis"), legend=None),
    )
)

# Combine filled regions and contour lines
chart = (
    (filled + lines)
    .properties(width=1450, height=815, title="contour-basic · altair · pyplots.ai")
    .configure_title(fontSize=32, anchor="middle")
    .configure_axis(labelFontSize=20, titleFontSize=24, tickSize=10)
    .configure_view(strokeWidth=0)
)

# Save as PNG (scale_factor=3.0 for ~4800x2700)
chart.save("plot.png", scale_factor=3.0)

# Save interactive HTML
chart.save("plot.html")
