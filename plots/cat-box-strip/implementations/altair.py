""" pyplots.ai
cat-box-strip: Box Plot with Strip Overlay
Library: altair 6.0.0 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-30
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - Different experimental treatments with varying distributions
np.random.seed(42)
n_per_group = 40

data = pd.DataFrame(
    {
        "Treatment": (
            ["Control"] * n_per_group
            + ["Treatment A"] * n_per_group
            + ["Treatment B"] * n_per_group
            + ["Treatment C"] * n_per_group
        ),
        "Response": np.concatenate(
            [
                np.random.normal(50, 8, n_per_group),  # Control - centered
                np.random.normal(62, 10, n_per_group),  # Treatment A - higher, more spread
                np.random.normal(45, 5, n_per_group),  # Treatment B - lower, tight
                np.random.exponential(15, n_per_group) + 35,  # Treatment C - skewed with outliers
            ]
        ),
    }
)

# Box plot layer
box = (
    alt.Chart(data)
    .mark_boxplot(size=80, color="#306998", opacity=0.6, median={"color": "#FFD43B", "strokeWidth": 4})
    .encode(
        x=alt.X(
            "Treatment:N", title="Treatment Group", axis=alt.Axis(labelFontSize=18, titleFontSize=22, labelAngle=0)
        ),
        y=alt.Y(
            "Response:Q",
            title="Response Value",
            axis=alt.Axis(labelFontSize=18, titleFontSize=22),
            scale=alt.Scale(zero=False),
        ),
    )
)

# Strip plot layer with jitter
strip = (
    alt.Chart(data)
    .mark_circle(size=120, color="#306998", opacity=0.7)
    .encode(x=alt.X("Treatment:N"), y=alt.Y("Response:Q"), xOffset="jitter:Q")
    .transform_calculate(jitter="random() * 40 - 20")
)

# Combine layers
chart = (
    (box + strip)
    .properties(
        width=1600, height=900, title=alt.Title("cat-box-strip · altair · pyplots.ai", fontSize=28, anchor="middle")
    )
    .configure_axis(labelFontSize=18, titleFontSize=22, gridOpacity=0.3)
    .configure_view(strokeWidth=0)
)

# Save
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
