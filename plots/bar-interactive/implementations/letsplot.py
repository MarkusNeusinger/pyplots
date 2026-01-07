"""pyplots.ai
bar-interactive: Interactive Bar Chart with Hover and Click
Library: letsplot | Python 3.13
Quality: pending | Created: 2025-01-07
"""

import os
import shutil

import pandas as pd
from lets_plot import *  # noqa: F403, F405


LetsPlot.setup_html()

# Data - Quarterly product sales with additional tooltip info
data = {
    "category": ["Electronics", "Clothing", "Home & Garden", "Sports", "Books", "Toys", "Beauty", "Automotive"],
    "value": [125000, 89000, 67000, 54000, 42000, 38000, 31000, 28000],
    "growth": [12.5, 8.2, -3.4, 15.7, 2.1, -5.8, 9.3, 4.6],
    "units_sold": [4200, 6800, 2100, 1800, 8500, 3200, 4100, 950],
}
df = pd.DataFrame(data)

# Calculate percentage of total for tooltips
df["percentage"] = (df["value"] / df["value"].sum() * 100).round(1)

# Create interactive bar chart with hover tooltips
plot = (
    ggplot(df, aes(x="category", y="value", fill="category"))
    + geom_bar(
        stat="identity",
        tooltips=layer_tooltips()
        .title("@category")
        .line("Revenue|$@{value}")
        .line("% of Total|@{percentage}%")
        .line("Units Sold|@{units_sold}")
        .line("YoY Growth|@{growth}%"),
        show_legend=False,
        size=0.5,
        color="white",
    )
    + scale_fill_manual(values=["#306998", "#3B7EAD", "#4A93C2", "#59A8D7", "#68BDEC", "#77D2FF", "#FFD43B", "#FFDF5F"])
    + labs(title="bar-interactive · letsplot · pyplots.ai", x="Product Category", y="Revenue ($)")
    + scale_y_continuous(format="${,.0f}")
    + theme_minimal()
    + theme(
        plot_title=element_text(size=24, face="bold"),
        axis_title_x=element_text(size=20),
        axis_title_y=element_text(size=20),
        axis_text_x=element_text(size=14, angle=25),
        axis_text_y=element_text(size=16),
        panel_grid_major_x=element_blank(),
        panel_grid_minor=element_blank(),
        panel_grid_major_y=element_line(color="#E0E0E0", size=0.5),
    )
    + ggsize(1600, 900)
)

# Save as PNG (scale 3x for 4800x2700)
ggsave(plot, "plot.png", scale=3)
ggsave(plot, "plot.html")

# lets-plot saves to lets-plot-images subfolder - move files to current directory
if os.path.exists("lets-plot-images/plot.png"):
    shutil.move("lets-plot-images/plot.png", "plot.png")
if os.path.exists("lets-plot-images/plot.html"):
    shutil.move("lets-plot-images/plot.html", "plot.html")
if os.path.exists("lets-plot-images"):
    shutil.rmtree("lets-plot-images")
