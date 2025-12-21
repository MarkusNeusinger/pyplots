""" pyplots.ai
scatter-basic: Basic Scatter Plot
Library: altair 6.0.0 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-13
"""

import altair as alt
import numpy as np
import pandas as pd


# Data
np.random.seed(42)
x = np.random.randn(100) * 2 + 10
y = x * 0.8 + np.random.randn(100) * 2

df = pd.DataFrame({"x": x, "y": y})

# Plot
chart = (
    alt.Chart(df)
    .mark_point(filled=True, size=200, opacity=0.7, color="#306998")
    .encode(x=alt.X("x:Q", title="X Value"), y=alt.Y("y:Q", title="Y Value"), tooltip=["x:Q", "y:Q"])
    .properties(width=1600, height=900, title=alt.Title("scatter-basic · altair · pyplots.ai", fontSize=28))
    .configure_axis(labelFontSize=18, titleFontSize=22, grid=True, gridOpacity=0.3)
    .configure_view(strokeWidth=0)
)

# Save
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
