"""pyplots.ai
contour-filled: Filled Contour Plot
Library: altair | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - Gaussian peaks on a 2D grid (60x60 for smooth contours)
np.random.seed(42)
n_points = 60
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
        "z": Z.ravel(),
    }
)

# Create filled contour using mark_rect with explicit x2/y2 bounds
chart = (
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
