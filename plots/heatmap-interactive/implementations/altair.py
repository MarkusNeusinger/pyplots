""" pyplots.ai
heatmap-interactive: Interactive Heatmap with Hover and Zoom
Library: altair 6.0.0 | Python 3.13.11
Quality: 91/100 | Created: 2026-01-08
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - Product performance matrix (15 products x 12 months)
np.random.seed(42)
products = [f"Product {chr(65 + i)}" for i in range(15)]
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Generate realistic sales performance data with seasonal patterns
base_performance = np.random.uniform(40, 80, size=(15, 12))
# Add seasonal variation (summer peak, winter dip)
seasonal = np.sin(np.linspace(0, 2 * np.pi, 12)) * 15
# Add product-specific trends
product_trend = np.linspace(-10, 10, 15).reshape(-1, 1)
values = base_performance + seasonal + product_trend
values = np.clip(values, 0, 100)  # Ensure 0-100 range

# Create long-form DataFrame for Altair
data = []
for i, product in enumerate(products):
    for j, month in enumerate(months):
        data.append({"Product": product, "Month": month, "Performance": round(values[i, j], 1)})
df = pd.DataFrame(data)

# Month order for proper sorting
month_order = months

# Create interactive heatmap
selection = alt.selection_interval(bind="scales")

chart = (
    alt.Chart(df)
    .mark_rect(stroke="white", strokeWidth=1)
    .encode(
        x=alt.X(
            "Month:N", sort=month_order, title="Month", axis=alt.Axis(labelFontSize=16, titleFontSize=20, labelAngle=0)
        ),
        y=alt.Y("Product:N", sort=products, title="Product", axis=alt.Axis(labelFontSize=14, titleFontSize=20)),
        color=alt.Color(
            "Performance:Q",
            scale=alt.Scale(scheme="viridis", domain=[0, 100]),
            legend=alt.Legend(title="Performance Score", titleFontSize=16, labelFontSize=14, gradientLength=300),
        ),
        tooltip=[
            alt.Tooltip("Product:N", title="Product"),
            alt.Tooltip("Month:N", title="Month"),
            alt.Tooltip("Performance:Q", title="Score", format=".1f"),
        ],
    )
    .properties(
        width=1400,
        height=800,
        title=alt.Title("heatmap-interactive · altair · pyplots.ai", fontSize=28, anchor="middle"),
    )
    .add_params(selection)
    .configure_axis(grid=False)
    .configure_view(strokeWidth=0)
)

# Save PNG (target ~4800x2700 with scale_factor=3 from 1400x800)
chart.save("plot.png", scale_factor=3.0)

# Save interactive HTML for altair
chart.save("plot.html")
