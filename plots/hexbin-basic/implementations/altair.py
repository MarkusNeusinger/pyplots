"""
hexbin-basic: Basic Hexbin Plot
Library: altair
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - clustered bivariate distribution (5000 points)
np.random.seed(42)

# Create multiple clusters for interesting density patterns
n_points = 5000
cluster1_x = np.random.randn(n_points // 2) * 2 + 5
cluster1_y = np.random.randn(n_points // 2) * 2 + 5
cluster2_x = np.random.randn(n_points // 3) * 1.5 + 12
cluster2_y = np.random.randn(n_points // 3) * 1.5 + 8
cluster3_x = np.random.randn(n_points // 6) * 1 + 8
cluster3_y = np.random.randn(n_points // 6) * 1 + 12

x = np.concatenate([cluster1_x, cluster2_x, cluster3_x])
y = np.concatenate([cluster1_y, cluster2_y, cluster3_y])

df = pd.DataFrame({"x": x, "y": y})

# Plot - 2D density heatmap (Altair's idiomatic approach for hexbin-like visualization)
# Altair doesn't have native hexbin, so we use rect mark with 2D binning
chart = (
    alt.Chart(df)
    .mark_rect()
    .encode(
        x=alt.X("x:Q", bin=alt.Bin(maxbins=30), title="X Value"),
        y=alt.Y("y:Q", bin=alt.Bin(maxbins=30), title="Y Value"),
        color=alt.Color(
            "count():Q",
            scale=alt.Scale(scheme="viridis"),
            legend=alt.Legend(title="Count", titleFontSize=18, labelFontSize=16),
        ),
        tooltip=[
            alt.Tooltip("x:Q", bin=alt.Bin(maxbins=30), title="X Range"),
            alt.Tooltip("y:Q", bin=alt.Bin(maxbins=30), title="Y Range"),
            alt.Tooltip("count():Q", title="Count"),
        ],
    )
    .properties(width=1400, height=800, title=alt.Title("hexbin-basic · altair · pyplots.ai", fontSize=28))
    .configure_axis(labelFontSize=18, titleFontSize=22, grid=False)
    .configure_view(strokeWidth=0)
)

# Save
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
