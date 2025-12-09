"""
area-stacked: Stacked Area Chart
Library: plotnine
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    element_line,
    element_text,
    geom_area,
    ggplot,
    labs,
    scale_fill_brewer,
    scale_x_datetime,
    theme,
    theme_minimal,
)


# Data - Monthly revenue by product line over 2 years
np.random.seed(42)
dates = pd.date_range(start="2022-01-01", periods=24, freq="MS")

# Generate realistic revenue data with trends
base_product_a = 50 + np.cumsum(np.random.randn(24) * 2)
base_product_b = 35 + np.cumsum(np.random.randn(24) * 1.5)
base_product_c = 25 + np.cumsum(np.random.randn(24) * 1.2)
base_product_d = 15 + np.cumsum(np.random.randn(24) * 0.8)

# Ensure all values are positive
product_a = np.maximum(base_product_a, 10)
product_b = np.maximum(base_product_b, 8)
product_c = np.maximum(base_product_c, 5)
product_d = np.maximum(base_product_d, 3)

# Create wide dataframe first
df_wide = pd.DataFrame(
    {"date": dates, "Product A": product_a, "Product B": product_b, "Product C": product_c, "Product D": product_d}
)

# Convert to long format for plotnine
df = df_wide.melt(id_vars=["date"], var_name="product", value_name="revenue")

# Order products by average magnitude (largest at bottom for stable stacking)
# The order in the categorical determines stacking order (first = bottom)
product_order = ["Product A", "Product B", "Product C", "Product D"]
df["product"] = pd.Categorical(df["product"], categories=product_order, ordered=True)

# Create plot
plot = (
    ggplot(df, aes(x="date", y="revenue", fill="product"))
    + geom_area(alpha=0.8, position="stack")
    + labs(x="Month", y="Revenue ($ millions)", title="Monthly Revenue by Product Line", fill="Product Line")
    + scale_fill_brewer(type="qual", palette="Set2")
    + scale_x_datetime(date_labels="%b %Y", date_breaks="3 months")
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        plot_title=element_text(size=20, ha="center"),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        axis_text_x=element_text(rotation=45, ha="right"),
        legend_title=element_text(size=16),
        legend_text=element_text(size=14),
        panel_grid_major=element_line(color="#CCCCCC", size=0.5, alpha=0.3),
        panel_grid_minor=element_line(color="#EEEEEE", size=0.25, alpha=0.2),
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
