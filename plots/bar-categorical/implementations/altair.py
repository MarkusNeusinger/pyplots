"""pyplots.ai
bar-categorical: Categorical Count Bar Chart
Library: altair | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - Product categories from retail transactions
np.random.seed(42)
categories = ["Electronics", "Clothing", "Home & Garden", "Sports", "Books", "Toys"]
# Generate realistic distribution (electronics and clothing more popular)
weights = [0.25, 0.22, 0.18, 0.15, 0.12, 0.08]
n_transactions = 150
data = np.random.choice(categories, size=n_transactions, p=weights)
df = pd.DataFrame({"Product Category": data})

# Create chart with automatic count aggregation
chart = (
    alt.Chart(df)
    .mark_bar(color="#306998", cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
    .encode(
        x=alt.X(
            "Product Category:N",
            title="Product Category",
            sort="-y",  # Sort by count descending
            axis=alt.Axis(labelFontSize=18, titleFontSize=22, labelAngle=-30),
        ),
        y=alt.Y("count():Q", title="Number of Transactions", axis=alt.Axis(labelFontSize=18, titleFontSize=22)),
        tooltip=[alt.Tooltip("Product Category:N", title="Category"), alt.Tooltip("count():Q", title="Count")],
    )
    .properties(
        width=1600, height=900, title=alt.Title("bar-categorical · altair · pyplots.ai", fontSize=28, anchor="middle")
    )
    .configure_axis(gridColor="#cccccc", gridOpacity=0.3)
    .configure_view(strokeWidth=0)
)

# Save as PNG (1600 × 3 = 4800, 900 × 3 = 2700)
chart.save("plot.png", scale_factor=3.0)

# Save interactive HTML
chart.save("plot.html")
