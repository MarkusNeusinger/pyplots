""" pyplots.ai
histogram-basic: Basic Histogram
Library: altair 6.0.0 | Python 3.13.11
Quality: 99/100 | Created: 2025-12-13
"""

import altair as alt
import numpy as np
import pandas as pd


# Data
np.random.seed(42)
values = np.random.normal(loc=170, scale=10, size=500)  # Heights in cm

df = pd.DataFrame({"height": values})

# Plot
chart = (
    alt.Chart(df)
    .mark_bar(color="#306998")
    .encode(
        alt.X("height:Q", bin=alt.Bin(maxbins=30), title="Height (cm)"),
        alt.Y("count()", title="Frequency"),
        tooltip=[
            alt.Tooltip("height:Q", bin=alt.Bin(maxbins=30), title="Height Range"),
            alt.Tooltip("count()", title="Count"),
        ],
    )
    .properties(width=1600, height=900, title=alt.Title("histogram-basic · altair · pyplots.ai", fontSize=28))
    .configure_axis(labelFontSize=18, titleFontSize=22)
    .configure_view(strokeWidth=0)
)

# Save
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
