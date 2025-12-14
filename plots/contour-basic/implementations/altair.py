"""
contour-basic: Basic Contour Plot
Library: altair
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - 2D Gaussian function on meshgrid
np.random.seed(42)
x = np.linspace(-3, 3, 60)
y = np.linspace(-3, 3, 60)
X, Y = np.meshgrid(x, y)

# Two overlapping Gaussian peaks
Z = np.exp(-((X - 1) ** 2 + (Y - 1) ** 2)) + 0.8 * np.exp(-((X + 1) ** 2 + (Y + 0.5) ** 2))

# Flatten to DataFrame for Altair
df = pd.DataFrame({"x": X.ravel(), "y": Y.ravel(), "z": Z.ravel()})

# Create filled contour using rect marks
# Altair doesn't have native contour, so we use heatmap-style visualization
chart = (
    alt.Chart(df)
    .mark_rect()
    .encode(
        x=alt.X("x:Q", bin=alt.Bin(maxbins=60), title="X Value"),
        y=alt.Y("y:Q", bin=alt.Bin(maxbins=60), title="Y Value"),
        color=alt.Color(
            "mean(z):Q",
            scale=alt.Scale(scheme="viridis"),
            title="Z Value",
            legend=alt.Legend(titleFontSize=20, labelFontSize=18, gradientLength=450, gradientThickness=30),
        ),
    )
    .properties(width=1450, height=815, title="contour-basic · altair · pyplots.ai")
    .configure_title(fontSize=32, anchor="middle")
    .configure_axis(labelFontSize=20, titleFontSize=24, tickSize=10)
    .configure_view(strokeWidth=0)
)

# Save as PNG (scale_factor=3.0 for ~4800x2700)
chart.save("plot.png", scale_factor=3.0)

# Save interactive HTML
chart.save("plot.html")
