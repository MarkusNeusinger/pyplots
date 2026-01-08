# ruff: noqa: F403, F405
"""pyplots.ai
linked-views-selection: Multiple Linked Views with Selection Sync
Library: letsplot | Python 3.13
Quality: pending | Created: 2025-01-08
"""

import numpy as np
import pandas as pd
from lets_plot import *


LetsPlot.setup_html()

# Data - Multivariate dataset with numeric and categorical columns
np.random.seed(42)
n = 200

# Create clusters with different characteristics
categories = np.repeat(["Group A", "Group B", "Group C", "Group D"], n // 4)
cluster_centers_x = {"Group A": 2, "Group B": 5, "Group C": 3, "Group D": 6}
cluster_centers_y = {"Group A": 3, "Group B": 2, "Group C": 6, "Group D": 5}

x = np.array([cluster_centers_x[c] + np.random.randn() * 0.8 for c in categories])
y = np.array([cluster_centers_y[c] + np.random.randn() * 0.8 for c in categories])
value = x * 10 + np.random.randn(n) * 8 + 30

df = pd.DataFrame({"x": x, "y": y, "category": categories, "value": value})

# Colors matching Python theme
colors = ["#306998", "#FFD43B", "#4B8BBE", "#646464"]

# Common theme for all plots - scaled for 4800x2700 output
common_theme = theme_minimal() + theme(
    axis_title=element_text(size=18),
    axis_text=element_text(size=14),
    plot_title=element_text(size=20, face="bold"),
    legend_text=element_text(size=14),
    legend_title=element_text(size=16),
)

# Main scatter plot with selection
scatter = (
    ggplot(df, aes("x", "y", color="category"))
    + geom_point(
        size=6, alpha=0.8, tooltips=layer_tooltips().line("@category").line("x: @x").line("y: @y").line("value: @value")
    )
    + scale_color_manual(values=colors)
    + labs(x="Measurement X", y="Measurement Y", title="Scatter Plot (Select Points)")
    + common_theme
    + theme(legend_position="none")
    + ggsize(700, 500)
)

# Histogram of values by category
histogram = (
    ggplot(df, aes("value", fill="category"))
    + geom_histogram(bins=20, alpha=0.7, color="white", size=0.3)
    + scale_fill_manual(values=colors)
    + labs(x="Value", y="Count", title="Value Distribution")
    + common_theme
    + theme(legend_position="none")
    + ggsize(700, 500)
)

# Bar chart showing category counts
category_counts = df.groupby("category").size().reset_index(name="count")

bar = (
    ggplot(category_counts, aes("category", "count", fill="category"))
    + geom_bar(stat="identity", alpha=0.8, width=0.7)
    + scale_fill_manual(values=colors)
    + labs(x="Category", y="Count", title="Category Distribution")
    + common_theme
    + theme(legend_position="none")
    + ggsize(700, 500)
)

# Create a simple legend-only plot for the fourth panel
legend_df = pd.DataFrame(
    {"category": ["Group A", "Group B", "Group C", "Group D"], "x": [1, 1, 1, 1], "y": [4, 3, 2, 1]}
)

legend_plot = (
    ggplot(legend_df, aes("x", "y", color="category", label="category"))
    + geom_point(size=10)
    + geom_text(hjust=0, nudge_x=0.15, size=16)
    + scale_color_manual(values=colors)
    + scale_x_continuous(limits=[0.5, 2.5])
    + scale_y_continuous(limits=[0, 5])
    + labs(title="Legend")
    + theme_void()
    + theme(plot_title=element_text(size=20, face="bold"), legend_position="none")
    + ggsize(400, 500)
)

# Combine plots using gggrid for linked views layout
combined = gggrid([scatter, histogram, bar, legend_plot], ncol=2, align=True)

# Add overall title and size
combined = (
    combined
    + ggtitle("linked-views-selection · letsplot · pyplots.ai")
    + ggsize(1600, 900)
    + theme(plot_title=element_text(size=28, face="bold"))
)

# Save as PNG (use path parameter to save in current directory)
ggsave(combined, "plot.png", scale=3, path=".")

# Save as HTML (interactive version with linking)
ggsave(combined, "plot.html", path=".")
