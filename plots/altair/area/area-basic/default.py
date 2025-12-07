"""
area-basic: Basic Area Chart
Library: altair
"""

import altair as alt
import pandas as pd


# Data
data = pd.DataFrame(
    {
        "month": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "sales": [100, 150, 130, 180, 200, 220, 195, 240, 260, 230, 280, 310],
    }
)

# Create chart with area and line
chart = (
    alt.Chart(data)
    .mark_area(opacity=0.5, color="#306998", line={"color": "#306998", "strokeWidth": 2})
    .encode(
        x=alt.X("month:Q", title="Month", axis=alt.Axis(labelFontSize=16, titleFontSize=20)),
        y=alt.Y("sales:Q", title="Sales", axis=alt.Axis(labelFontSize=16, titleFontSize=20)),
    )
    .properties(width=1600, height=900, title=alt.TitleParams(text="Basic Area Chart", fontSize=20))
    .configure_view(strokeWidth=0)
    .configure_axis(grid=True, gridOpacity=0.3)
)

# Save (1600 × 900 × 3 = 4800 × 2700)
chart.save("plot.png", scale_factor=3.0)
