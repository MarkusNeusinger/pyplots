"""pyplots.ai
bar-stacked: Stacked Bar Chart
Library: lets-plot | Python 3.13
Quality: pending | Created: 2025-12-25
"""

import pandas as pd
from lets_plot import *


LetsPlot.setup_html()

# Data: Quarterly sales by product category
data = {
    "quarter": ["Q1", "Q2", "Q3", "Q4"] * 4,
    "product": ["Electronics"] * 4 + ["Furniture"] * 4 + ["Clothing"] * 4 + ["Accessories"] * 4,
    "sales": [
        120,
        145,
        165,
        190,  # Electronics
        85,
        92,
        78,
        110,  # Furniture
        65,
        88,
        95,
        72,  # Clothing
        45,
        52,
        48,
        58,  # Accessories
    ],
}
df = pd.DataFrame(data)

# Define custom colors (Python Blue first, then complementary colors)
colors = ["#306998", "#FFD43B", "#DC2626", "#10B981"]

# Create stacked bar chart
plot = (
    ggplot(df, aes(x="quarter", y="sales", fill="product"))
    + geom_bar(stat="identity", position="stack", width=0.7, alpha=0.9)
    + scale_fill_manual(values=colors)
    + labs(title="bar-stacked · letsplot · pyplots.ai", x="Quarter", y="Sales (Thousands $)", fill="Product Category")
    + theme_minimal()
    + theme(
        plot_title=element_text(size=28, face="bold"),
        axis_title=element_text(size=22),
        axis_text=element_text(size=18),
        legend_title=element_text(size=20),
        legend_text=element_text(size=18),
        legend_position="right",
        panel_grid_major_x=element_blank(),
        panel_grid_minor=element_blank(),
    )
    + ggsize(1600, 900)
)

# Save as PNG (scale 3x for 4800x2700 px)
ggsave(plot, "plot.png", path=".", scale=3)

# Save as HTML for interactivity
ggsave(plot, "plot.html", path=".")
