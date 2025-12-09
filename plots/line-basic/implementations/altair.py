"""
line-basic: Basic Line Plot
Library: altair
"""

import altair as alt
import pandas as pd


# Data
data = pd.DataFrame({"time": [1, 2, 3, 4, 5, 6, 7], "value": [10, 15, 13, 18, 22, 19, 25]})

# Create line chart
line = (
    alt.Chart(data)
    .mark_line(strokeWidth=2, color="#306998")
    .encode(
        x=alt.X("time:Q", title="Time", axis=alt.Axis(labelFontSize=16, titleFontSize=20)),
        y=alt.Y("value:Q", title="Value", axis=alt.Axis(labelFontSize=16, titleFontSize=20)),
    )
)

# Add points on the line for clarity
points = alt.Chart(data).mark_point(size=100, color="#306998", filled=True).encode(x="time:Q", y="value:Q")

# Combine and configure chart
chart = (
    (line + points)
    .properties(width=1600, height=900, title=alt.Title("Basic Line Plot", fontSize=20))
    .configure_view(strokeWidth=0)
    .configure_axis(grid=True, gridOpacity=0.3)
)

# Save as PNG (1600 × 900 at scale 3 = 4800 × 2700 px)
chart.save("plot.png", scale_factor=3.0)
