"""pyplots.ai
chart-export-menu: Chart with Built-in Export Menu
Library: altair | Python 3.13
Quality: pending | Created: 2026-01-19
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - Monthly sales data over a year
np.random.seed(42)
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
base_sales = [85, 92, 105, 115, 130, 145, 155, 148, 135, 120, 105, 95]
product_a = [v + np.random.randint(-10, 10) for v in base_sales]
product_b = [v * 0.7 + np.random.randint(-5, 8) for v in base_sales]

df = pd.DataFrame(
    {"Month": months * 2, "Sales": product_a + product_b, "Product": ["Product A"] * 12 + ["Product B"] * 12}
)

# Sort months correctly
month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Create chart with export menu (Altair has built-in export via action menu)
chart = (
    alt.Chart(df)
    .mark_line(point=alt.OverlayMarkDef(size=120), strokeWidth=3)
    .encode(
        x=alt.X("Month:N", sort=month_order, title="Month", axis=alt.Axis(labelFontSize=18, titleFontSize=22)),
        y=alt.Y("Sales:Q", title="Sales (thousands)", axis=alt.Axis(labelFontSize=18, titleFontSize=22)),
        color=alt.Color(
            "Product:N",
            scale=alt.Scale(domain=["Product A", "Product B"], range=["#306998", "#FFD43B"]),
            legend=alt.Legend(titleFontSize=18, labelFontSize=16),
        ),
        tooltip=["Month", "Product", "Sales"],
    )
    .properties(
        width=1600,
        height=900,
        title=alt.Title(text="chart-export-menu \u00b7 altair \u00b7 pyplots.ai", fontSize=28, anchor="middle"),
    )
    .configure_axis(labelFontSize=18, titleFontSize=22)
    .configure_legend(titleFontSize=18, labelFontSize=16)
)

# Save PNG (static image for preview)
chart.save("plot.png", scale_factor=3.0)

# Save HTML with built-in export menu (actions enabled by default)
# The export menu appears as "..." in top-right corner with Save as SVG/PNG options
chart.save("plot.html")
