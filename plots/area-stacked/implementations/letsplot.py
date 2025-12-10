"""
area-stacked: Stacked Area Chart
Library: letsplot
"""

import numpy as np
import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    element_blank,
    element_line,
    element_text,
    geom_area,
    ggplot,
    ggsave,
    ggsize,
    labs,
    scale_fill_manual,
    theme,
    theme_minimal,
)


LetsPlot.setup_html()

# Data - Monthly revenue by product line over 2 years
np.random.seed(42)
dates = pd.date_range(start="2022-01-01", periods=24, freq="MS")

# Create revenue data for 4 product lines with realistic patterns
base_values = [120, 80, 60, 40]
product_names = ["Product A", "Product B", "Product C", "Product D"]

data = {"date": [], "product": [], "revenue": []}

for i, product in enumerate(product_names):
    # Add some trend and seasonality
    trend = np.linspace(0, 20, 24) if i < 2 else np.linspace(0, 10, 24)
    seasonal = 15 * np.sin(np.linspace(0, 4 * np.pi, 24))
    noise = np.random.randn(24) * 5
    values = base_values[i] + trend + seasonal + noise
    values = np.maximum(values, 10)  # Ensure positive values

    data["date"].extend(dates)
    data["product"].extend([product] * 24)
    data["revenue"].extend(values)

df = pd.DataFrame(data)

# Color palette from style guide
colors = ["#306998", "#FFD43B", "#DC2626", "#059669"]

# Create stacked area chart
plot = (
    ggplot(df, aes(x="date", y="revenue", fill="product"))
    + geom_area(alpha=0.8, position="stack")
    + scale_fill_manual(values=colors)
    + labs(x="Month", y="Revenue (thousands $)", title="Monthly Revenue by Product Line", fill="Product")
    + theme_minimal()
    + theme(
        axis_text=element_text(size=16),
        axis_title=element_text(size=20),
        plot_title=element_text(size=20),
        legend_text=element_text(size=16),
        legend_title=element_text(size=16),
        panel_grid_major=element_line(color="#cccccc", size=0.5),
        panel_grid_minor=element_blank(),
    )
    + ggsize(1600, 900)
)

# Save as PNG and HTML
ggsave(plot, "plot.png", path=".", scale=3)
ggsave(plot, "plot.html", path=".")
