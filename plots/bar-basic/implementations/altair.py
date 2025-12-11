"""
bar-basic: Basic Bar Chart
Library: altair
"""

import altair as alt
import pandas as pd


# Data
data = pd.DataFrame(
    {
        "category": ["Electronics", "Clothing", "Home & Garden", "Sports", "Books", "Toys", "Food"],
        "value": [45200, 32100, 28400, 21800, 18500, 15200, 12300],
    }
)

# Chart
chart = (
    alt.Chart(data)
    .mark_bar(color="#306998", cornerRadiusTopLeft=3, cornerRadiusTopRight=3)
    .encode(
        x=alt.X(
            "category:N",
            title="Product Category",
            sort="-y",
            axis=alt.Axis(labelAngle=-45, labelFontSize=16, titleFontSize=20),
        ),
        y=alt.Y("value:Q", title="Sales ($)", axis=alt.Axis(labelFontSize=16, titleFontSize=20)),
        tooltip=[alt.Tooltip("category:N", title="Category"), alt.Tooltip("value:Q", title="Sales", format="$,.0f")],
    )
    .properties(width=1600, height=900, title=alt.Title(text="Product Sales by Category", fontSize=24))
    .configure_view(strokeWidth=0)
    .configure_axis(grid=True, gridOpacity=0.3)
)

# Save as PNG and HTML
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
