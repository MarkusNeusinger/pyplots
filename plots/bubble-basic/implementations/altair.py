"""
bubble-basic: Basic Bubble Chart
Library: altair
"""

import altair as alt
import numpy as np
import pandas as pd


# Data
np.random.seed(42)
n = 50

x = np.random.randn(n) * 20 + 50
y = x * 0.6 + np.random.randn(n) * 15 + 20
size = np.abs(np.random.randn(n) * 30 + 50)  # Positive values for bubble size

df = pd.DataFrame({"x": x, "y": y, "size": size})

# Chart
chart = (
    alt.Chart(df)
    .mark_circle(opacity=0.6, color="#306998")
    .encode(
        x=alt.X("x:Q", title="X Value", scale=alt.Scale(zero=False)),
        y=alt.Y("y:Q", title="Y Value", scale=alt.Scale(zero=False)),
        size=alt.Size(
            "size:Q",
            title="Size Value",
            scale=alt.Scale(range=[100, 3000]),  # Min/max bubble size in pixels^2
            legend=alt.Legend(titleFontSize=18, labelFontSize=16),
        ),
        tooltip=["x:Q", "y:Q", "size:Q"],
    )
    .properties(width=1600, height=900, title="bubble-basic · altair · pyplots.ai")
    .configure_title(fontSize=28, anchor="middle")
    .configure_axis(labelFontSize=18, titleFontSize=22, gridOpacity=0.3)
)

# Save
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
