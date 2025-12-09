"""
histogram-basic: Basic Histogram
Library: altair
"""

import altair as alt
import numpy as np
import pandas as pd


# Data
np.random.seed(42)
data = pd.DataFrame({"value": np.random.normal(100, 15, 500)})

# Create histogram chart
chart = (
    alt.Chart(data)
    .mark_bar(color="#306998", opacity=0.8)
    .encode(alt.X("value:Q", bin=alt.Bin(maxbins=30), title="Value"), alt.Y("count()", title="Frequency"))
    .properties(width=1600, height=900, title="Basic Histogram")
    .configure_axis(labelFontSize=16, titleFontSize=20)
    .configure_title(fontSize=20)
)

# Save as PNG (1600 × 900 at scale 3 = 4800 × 2700)
chart.save("plot.png", scale_factor=3.0)
