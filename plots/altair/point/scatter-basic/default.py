"""
scatter-basic: Basic Scatter Plot
Library: altair
"""

import altair as alt
import numpy as np
import pandas as pd


# Data
np.random.seed(42)
x = np.random.randn(100) * 2 + 10
y = x * 0.8 + np.random.randn(100) * 2

data = pd.DataFrame({"x": x, "y": y})

# Create chart
chart = (
    alt.Chart(data)
    .mark_point(filled=True, opacity=0.7, size=100, color="#306998")
    .encode(x=alt.X("x:Q", title="X Value"), y=alt.Y("y:Q", title="Y Value"))
    .properties(width=1600, height=900, title="Basic Scatter Plot")
    .configure_axis(labelFontSize=16, titleFontSize=20)
    .configure_title(fontSize=20)
)

# Save as PNG (1600 * 3 = 4800px, 900 * 3 = 2700px)
chart.save("plot.png", scale_factor=3.0)
