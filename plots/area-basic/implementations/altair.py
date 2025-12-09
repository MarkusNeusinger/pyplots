"""
area-basic: Basic Area Chart
Library: altair
"""

import altair as alt
import pandas as pd


# Data
data = pd.DataFrame(
    {
        "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        "sales": [120, 135, 148, 162, 175, 195, 210, 198, 185, 170, 158, 190],
    }
)

# Create chart with area and line
chart = (
    alt.Chart(data)
    .mark_area(opacity=0.7, color="#306998", line={"color": "#306998", "strokeWidth": 2})
    .encode(
        x=alt.X("month:O", title="Month", sort=None, axis=alt.Axis(labelFontSize=16, titleFontSize=20)),
        y=alt.Y("sales:Q", title="Sales", axis=alt.Axis(labelFontSize=16, titleFontSize=20)),
    )
    .properties(width=1600, height=900, title=alt.TitleParams(text="Monthly Sales", fontSize=20))
    .configure_view(strokeWidth=0)
    .configure_axis(grid=True, gridOpacity=0.3)
)

# Save (1600 × 900 × 3 = 4800 × 2700)
chart.save("plot.png", scale_factor=3.0)
