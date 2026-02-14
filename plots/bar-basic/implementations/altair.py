""" pyplots.ai
bar-basic: Basic Bar Chart
Library: altair 6.0.0 | Python 3.14
Quality: 82/100 | Created: 2025-12-23
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
bars = (
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
)

# Value labels above bars
labels = bars.mark_text(align="center", baseline="bottom", dy=-8, fontSize=16, color="#333333").encode(
    text=alt.Text("value:Q", format="$,.0f")
)

# Combine bars + labels
chart = (
    (bars + labels)
    .properties(width=1600, height=900, title=alt.Title(text="bar-basic · altair · pyplots.ai", fontSize=28))
    .configure_view(strokeWidth=0)
    .configure_axis(grid=False)
    .configure_axisY(grid=True, gridOpacity=0.2, gridDash=[4, 4])
)

# Save as PNG (scale_factor=3 gives 4800x2700 at 1600x900)
chart.save("plot.png", scale_factor=3.0)

# Save interactive HTML
chart.save("plot.html")
