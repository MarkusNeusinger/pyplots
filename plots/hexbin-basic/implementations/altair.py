""" pyplots.ai
hexbin-basic: Basic Hexbin Plot
Library: altair 6.0.0 | Python 3.13.11
Quality: 78/100 | Created: 2025-12-23
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

# Plot - 2D density heatmap with hexagonal appearance
# Altair doesn't have native hexbin, so we use rect mark with 2D binning
# to achieve a similar density visualization effect
chart = (
    alt.Chart(df)
    .mark_rect(cornerRadius=3)
    .encode(
        x=alt.X("x:Q", bin=alt.Bin(maxbins=25), title="X Value", axis=alt.Axis(labelFontSize=18, titleFontSize=22)),
        y=alt.Y("y:Q", bin=alt.Bin(maxbins=25), title="Y Value", axis=alt.Axis(labelFontSize=18, titleFontSize=22)),
        color=alt.Color(
            "count():Q",
            scale=alt.Scale(scheme="viridis"),
            legend=alt.Legend(
                title="Density (Count)", titleFontSize=20, labelFontSize=16, gradientLength=300, gradientThickness=25
            ),
        ),
        tooltip=[
            alt.Tooltip("x:Q", bin=alt.Bin(maxbins=25), title="X Range"),
            alt.Tooltip("y:Q", bin=alt.Bin(maxbins=25), title="Y Range"),
            alt.Tooltip("count():Q", title="Count"),
        ],
    )
    .properties(
        width=1400, height=800, title=alt.Title("hexbin-basic · altair · pyplots.ai", fontSize=28, anchor="middle")
    )
    .configure_axis(grid=False)
    .configure_view(strokeWidth=0)
)

# Save
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
