""" pyplots.ai
histogram-basic: Basic Histogram
Library: altair 6.0.0 | Python 3.14.0
Quality: 87/100 | Created: 2025-12-23
"""

import altair as alt
import numpy as np
import pandas as pd


# Data
np.random.seed(42)
values = np.concatenate(
    [np.random.normal(loc=170, scale=8, size=400), np.random.normal(loc=185, scale=5, size=100)]
)  # Heights in cm — slight right skew from taller subgroup

df = pd.DataFrame({"height": values})

# Plot
chart = (
    alt.Chart(df)
    .mark_bar(color="#306998", stroke="#1e4a6e", strokeWidth=0.5)
    .encode(
        alt.X("height:Q", bin=alt.Bin(maxbins=30), title="Height (cm)"),
        alt.Y("count()", title="Frequency"),
        tooltip=[
            alt.Tooltip("height:Q", bin=alt.Bin(maxbins=30), title="Height Range"),
            alt.Tooltip("count()", title="Count"),
        ],
    )
    .properties(width=1600, height=900, title=alt.Title("histogram-basic · altair · pyplots.ai", fontSize=28))
    .configure_axis(labelFontSize=18, titleFontSize=22, grid=False)
    .configure_axisY(grid=True, gridColor="#cccccc", gridOpacity=0.2, gridDash=[4, 4])
    .configure_view(strokeWidth=0)
)

# Save
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
