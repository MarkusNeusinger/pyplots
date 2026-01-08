""" pyplots.ai
heatmap-interactive: Interactive Heatmap with Hover and Zoom
Library: letsplot 4.8.2 | Python 3.13.11
Quality: 91/100 | Created: 2026-01-08
"""

import numpy as np
import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    element_blank,
    element_text,
    geom_tile,
    ggplot,
    ggsize,
    labs,
    layer_tooltips,
    scale_fill_gradient2,
    scale_x_discrete,
    scale_y_discrete,
    theme,
    theme_minimal,
)
from lets_plot.export import ggsave


LetsPlot.setup_html()

# Data - Product sales matrix (20 products × 12 months)
np.random.seed(42)

products = [f"Product {chr(65 + i)}" for i in range(20)]
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Generate sales data with seasonal patterns and product variations
base_sales = np.random.randint(50, 200, size=(20, 12))
seasonal_factor = np.array([0.8, 0.7, 0.9, 1.0, 1.1, 1.2, 1.3, 1.2, 1.1, 1.0, 1.4, 1.6])
product_factor = np.linspace(0.6, 1.4, 20).reshape(-1, 1)
sales_matrix = (base_sales * seasonal_factor * product_factor).astype(int)

# Convert to long format for lets-plot
data = []
for i, product in enumerate(products):
    for j, month in enumerate(months):
        data.append({"Product": product, "Month": month, "Sales": sales_matrix[i, j]})

df = pd.DataFrame(data)

# Create interactive heatmap with tooltips
plot = (
    ggplot(df, aes(x="Month", y="Product", fill="Sales"))
    + geom_tile(tooltips=layer_tooltips().title("@Product").line("Month: @Month").line("Sales: @Sales units"))
    + scale_fill_gradient2(low="#306998", mid="#F0F0F0", high="#FFD43B", midpoint=df["Sales"].median())
    + scale_x_discrete(limits=months)
    + scale_y_discrete(limits=products[::-1])
    + labs(title="heatmap-interactive · letsplot · pyplots.ai", x="Month", y="Product", fill="Sales (units)")
    + theme_minimal()
    + theme(
        plot_title=element_text(size=24, face="bold"),
        axis_title=element_text(size=20),
        axis_text_x=element_text(size=14, angle=45),
        axis_text_y=element_text(size=12),
        legend_title=element_text(size=16),
        legend_text=element_text(size=14),
        panel_grid=element_blank(),
    )
    + ggsize(1600, 900)
)

# Save PNG (scale 3x for 4800 × 2700 px)
ggsave(plot, "plot.png", path=".", scale=3)

# Save interactive HTML
ggsave(plot, "plot.html", path=".")
