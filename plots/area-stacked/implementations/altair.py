"""
area-stacked: Stacked Area Chart
Library: altair
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - monthly revenue by product line over 2 years
np.random.seed(42)
dates = pd.date_range(start="2022-01-01", periods=24, freq="MS")

# Generate realistic revenue data with trends
base = np.linspace(100, 150, 24)
product_a = base + np.random.randn(24) * 10  # Core product - largest
product_b = base * 0.7 + np.random.randn(24) * 8  # Secondary product
product_c = base * 0.4 + np.random.randn(24) * 5  # Growing product
product_d = base * 0.25 + np.random.randn(24) * 3  # New product

# Ensure no negative values
product_a = np.maximum(product_a, 20)
product_b = np.maximum(product_b, 15)
product_c = np.maximum(product_c, 10)
product_d = np.maximum(product_d, 5)

# Create DataFrame in long format for Altair
df = pd.DataFrame(
    {"date": dates, "Product A": product_a, "Product B": product_b, "Product C": product_c, "Product D": product_d}
)

# Melt to long format
df_long = df.melt(id_vars=["date"], var_name="Product", value_name="Revenue")

# Define color palette from style guide
colors = ["#306998", "#FFD43B", "#DC2626", "#059669"]

# Create stacked area chart
chart = (
    alt.Chart(df_long)
    .mark_area(opacity=0.75)
    .encode(
        x=alt.X("date:T", title="Date", axis=alt.Axis(format="%b %Y", labelAngle=-45)),
        y=alt.Y("Revenue:Q", title="Revenue ($K)", stack="zero"),
        color=alt.Color(
            "Product:N", scale=alt.Scale(range=colors), legend=alt.Legend(title="Product Line", orient="top-right")
        ),
        order=alt.Order("Product:N", sort="descending"),
        tooltip=["date:T", "Product:N", alt.Tooltip("Revenue:Q", format=".1f")],
    )
    .properties(width=1600, height=900, title="Monthly Revenue by Product Line")
    .configure_title(fontSize=20)
    .configure_axis(labelFontSize=16, titleFontSize=20)
    .configure_legend(labelFontSize=16, titleFontSize=16)
)

# Save as PNG (scale_factor=3 for 4800x2700)
chart.save("plot.png", scale_factor=3.0)

# Save as HTML for interactivity
chart.interactive().save("plot.html")
