""" pyplots.ai
bar-sorted: Sorted Bar Chart
Library: altair 6.0.0 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-30
"""

import altair as alt
import pandas as pd


# Data: Product sales figures (realistic business context)
data = pd.DataFrame(
    {
        "Product": [
            "Laptop",
            "Smartphone",
            "Tablet",
            "Headphones",
            "Smartwatch",
            "Camera",
            "Keyboard",
            "Monitor",
            "Speaker",
            "Mouse",
        ],
        "Sales": [4850, 3920, 2780, 2340, 1890, 1650, 1420, 1180, 950, 720],
    }
)

# Sort data by sales in descending order
data = data.sort_values("Sales", ascending=False).reset_index(drop=True)

# Create sorted bar chart (horizontal for better label readability)
chart = (
    alt.Chart(data)
    .mark_bar(
        color="#306998",  # Python Blue
        cornerRadiusEnd=4,
    )
    .encode(
        x=alt.X("Sales:Q", title="Sales (Units)", axis=alt.Axis(labelFontSize=18, titleFontSize=22)),
        y=alt.Y(
            "Product:N",
            sort="-x",  # Sort by x-value descending
            title="Product",
            axis=alt.Axis(labelFontSize=18, titleFontSize=22),
        ),
        tooltip=["Product:N", "Sales:Q"],
    )
    .properties(
        width=1400, height=800, title=alt.Title("bar-sorted · altair · pyplots.ai", fontSize=28, anchor="middle")
    )
    .configure_axis(grid=True, gridOpacity=0.3, gridDash=[4, 4])
    .configure_view(strokeWidth=0)
)

# Save as PNG (4800 x 2700 at scale_factor=3)
chart.save("plot.png", scale_factor=3.0)

# Save interactive HTML version
chart.save("plot.html")
