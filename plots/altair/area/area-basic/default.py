"""
area-basic: Basic Area Chart
Library: altair
"""

import altair as alt
import pandas as pd


# Data
data = pd.DataFrame({"month": [1, 2, 3, 4, 5, 6], "sales": [100, 150, 130, 180, 200, 220]})

# Create chart with area and line
area = (
    alt.Chart(data)
    .mark_area(opacity=0.5, color="#306998")
    .encode(
        x=alt.X("month:Q", title="Month", axis=alt.Axis(labelFontSize=16, titleFontSize=20)),
        y=alt.Y("sales:Q", title="Sales", axis=alt.Axis(labelFontSize=16, titleFontSize=20)),
    )
)

line = alt.Chart(data).mark_line(color="#306998", strokeWidth=2).encode(x="month:Q", y="sales:Q")

chart = (
    (area + line)
    .properties(width=1600, height=900, title=alt.Title("Basic Area Chart", fontSize=20))
    .configure_axis(grid=True, gridOpacity=0.3)
)

# Save
chart.save("plot.png", scale_factor=3.0)
