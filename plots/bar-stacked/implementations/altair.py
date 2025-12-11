"""
bar-stacked: Stacked Bar Chart
Library: altair
"""

import altair as alt
import pandas as pd


# Data - Monthly sales by product category
data = pd.DataFrame(
    {
        "period": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug"] * 4,
        "category": ["Electronics"] * 8 + ["Clothing"] * 8 + ["Home & Garden"] * 8 + ["Sports"] * 4 + ["Sports"] * 4,
        "value": [
            # Electronics
            45000,
            52000,
            48000,
            61000,
            55000,
            58000,
            67000,
            72000,
            # Clothing
            32000,
            28000,
            35000,
            42000,
            38000,
            45000,
            48000,
            52000,
            # Home & Garden
            18000,
            22000,
            28000,
            35000,
            32000,
            29000,
            25000,
            21000,
            # Sports
            15000,
            18000,
            22000,
            28000,
            35000,
            42000,
            38000,
            32000,
        ],
    }
)

# Define custom color scale using the style guide palette
color_scale = alt.Scale(
    domain=["Electronics", "Clothing", "Home & Garden", "Sports"], range=["#306998", "#FFD43B", "#059669", "#DC2626"]
)

# Define period order
period_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug"]

# Create stacked bar chart
chart = (
    alt.Chart(data)
    .mark_bar()
    .encode(
        x=alt.X(
            "period:N",
            sort=period_order,
            title="Month",
            axis=alt.Axis(labelFontSize=16, titleFontSize=20, labelAngle=0),
        ),
        y=alt.Y("sum(value):Q", title="Sales ($)", axis=alt.Axis(labelFontSize=16, titleFontSize=20, format="~s")),
        color=alt.Color(
            "category:N",
            scale=color_scale,
            title="Product Category",
            legend=alt.Legend(titleFontSize=16, labelFontSize=16),
        ),
        order=alt.Order("category:N", sort="ascending"),
        tooltip=["period:N", "category:N", alt.Tooltip("value:Q", title="Sales", format="$,.0f")],
    )
    .properties(width=1600, height=900, title=alt.Title(text="Monthly Sales by Product Category", fontSize=20))
)

# Save as PNG and HTML
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
