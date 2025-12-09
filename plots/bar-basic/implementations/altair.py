"""
bar-basic: Basic Bar Chart
Library: altair
"""

import altair as alt
import pandas as pd


# Data
data = pd.DataFrame(
    {"category": ["Product A", "Product B", "Product C", "Product D", "Product E"], "value": [45, 78, 52, 91, 63]}
)

# Create chart
chart = (
    alt.Chart(data)
    .mark_bar(color="#306998")
    .encode(
        x=alt.X("category:N", title="Category", axis=alt.Axis(labelFontSize=16, titleFontSize=20)),
        y=alt.Y("value:Q", title="Value", axis=alt.Axis(labelFontSize=16, titleFontSize=20)),
    )
    .properties(width=1600, height=900, title=alt.Title(text="Basic Bar Chart", fontSize=20))
)

# Save as PNG (1600 × 900 with scale_factor=3 = 4800 × 2700)
chart.save("plot.png", scale_factor=3.0)
