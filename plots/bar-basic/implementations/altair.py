""" pyplots.ai
bar-basic: Basic Bar Chart
Library: altair 6.0.0 | Python 3.13.11
Quality: 93/100 | Created: 2025-12-23
"""

import altair as alt
import pandas as pd


# Data - Product sales by category (realistic retail scenario)
data = pd.DataFrame(
    {
        "category": ["Electronics", "Clothing", "Home & Garden", "Sports", "Books", "Toys", "Food"],
        "value": [45200, 32100, 28400, 21800, 18500, 15200, 12300],
    }
)

# Chart
chart = (
    alt.Chart(data)
    .mark_bar(color="#306998", cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
    .encode(
        x=alt.X(
            "category:N",
            title="Product Category",
            sort="-y",
            axis=alt.Axis(labelAngle=-45, labelFontSize=18, titleFontSize=22),
        ),
        y=alt.Y("value:Q", title="Sales ($)", axis=alt.Axis(labelFontSize=18, titleFontSize=22, format="$,.0f")),
        tooltip=[alt.Tooltip("category:N", title="Category"), alt.Tooltip("value:Q", title="Sales", format="$,.0f")],
    )
    .properties(width=1500, height=800, title=alt.Title(text="bar-basic · altair · pyplots.ai", fontSize=28))
    .configure_view(strokeWidth=0)
    .configure_axis(grid=True, gridOpacity=0.3, gridDash=[4, 4])
)

# Save as PNG (scale_factor=3 gives 4500x2400, close to target 4800x2700)
chart.save("plot.png", scale_factor=3.0)

# Save interactive HTML
chart.save("plot.html")
