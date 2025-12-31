"""pyplots.ai
subplot-mosaic: Mosaic Subplot Layout with Varying Sizes
Library: plotnine | Python 3.13
Quality: pending | Created: 2025-12-31
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from plotnine import (
    aes,
    element_line,
    element_rect,
    element_text,
    geom_bar,
    geom_line,
    geom_point,
    geom_text,
    geom_tile,
    ggplot,
    labs,
    scale_color_manual,
    scale_fill_gradient2,
    scale_fill_manual,
    theme,
    theme_minimal,
)


# Data - Product performance dashboard
np.random.seed(42)

# Daily metrics for overview chart (Panel A - large top panel)
n_days = 60
days = np.arange(n_days)
products = ["Alpha", "Beta", "Gamma"]
colors = ["#306998", "#FFD43B", "#5DADE2"]

df_overview = pd.concat(
    [
        pd.DataFrame({"day": days, "sales": 100 + i * 15 + np.cumsum(np.random.randn(n_days) * 3), "product": name})
        for i, name in enumerate(products)
    ],
    ignore_index=True,
)

# Category performance (Panel B - medium right panel)
categories = ["Q1", "Q2", "Q3", "Q4"]
revenues = [48, 35, 42, 55]
df_category = pd.DataFrame({"quarter": categories, "revenue": revenues})
df_category["quarter"] = pd.Categorical(df_category["quarter"], categories=categories, ordered=True)

# Distribution data (Panel C - bottom left)
df_scatter = pd.DataFrame({"units": np.random.uniform(50, 400, 80), "margin": 15 + np.random.randn(80) * 8})
df_scatter["margin"] = df_scatter["margin"] + 0.03 * df_scatter["units"]

# Heatmap data (Panel D - bottom middle)
regions = ["North", "South", "East", "West"]
metrics_list = ["Sales", "Profit", "Growth"]
heatmap_vals = np.random.rand(len(metrics_list), len(regions)) * 100
df_heat = pd.DataFrame(
    [
        {"region": regions[j], "metric": metrics_list[i], "value": heatmap_vals[i, j]}
        for i in range(len(metrics_list))
        for j in range(len(regions))
    ]
)
df_heat["region"] = pd.Categorical(df_heat["region"], categories=regions, ordered=True)
df_heat["metric"] = pd.Categorical(df_heat["metric"], categories=metrics_list[::-1], ordered=True)

# Small metric panel (Panel E - bottom right)
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
monthly_perf = [82, 78, 91, 88, 95, 92]
df_monthly = pd.DataFrame({"month": months, "score": monthly_perf})
df_monthly["month"] = pd.Categorical(df_monthly["month"], categories=months, ordered=True)

# Create all plotnine plots with proper theming
base_theme = theme_minimal() + theme(
    plot_title=element_text(size=18, face="bold", ha="center"),
    axis_title=element_text(size=14),
    axis_text=element_text(size=11),
    legend_text=element_text(size=11),
    legend_title=element_text(size=13, face="bold"),
    panel_grid_major=element_line(color="#cccccc", alpha=0.3),
    panel_grid_minor=element_line(alpha=0),
    panel_background=element_rect(fill="white"),
)

# Panel A: Sales Overview - plotnine line + point plot
p_overview = (
    ggplot(df_overview, aes(x="day", y="sales", color="product"))
    + geom_line(size=1.2, alpha=0.9)
    + geom_point(size=2, alpha=0.6)
    + scale_color_manual(values=colors)
    + labs(x="Day", y="Sales (Units)", color="Product")
    + base_theme
    + theme(legend_position="right", figure_size=(10, 5))
)

# Panel B: Quarterly Revenue - plotnine bar plot
p_category = (
    ggplot(df_category, aes(x="quarter", y="revenue", fill="quarter"))
    + geom_bar(stat="identity", width=0.7, show_legend=False)
    + scale_fill_manual(values=["#306998", "#4A8BBF", "#6BA3D6", "#FFD43B"])
    + labs(x="Quarter", y="Revenue (k$)")
    + base_theme
    + theme(figure_size=(5, 5))
)

# Panel C: Units vs Margin - plotnine scatter plot
p_scatter = (
    ggplot(df_scatter, aes(x="units", y="margin"))
    + geom_point(size=3, color="#306998", alpha=0.7)
    + labs(x="Units Sold", y="Margin (%)")
    + base_theme
    + theme(figure_size=(5, 3))
)

# Panel D: Regional Performance - plotnine heatmap with geom_tile
p_heatmap = (
    ggplot(df_heat, aes(x="region", y="metric", fill="value"))
    + geom_tile(color="white", size=1)
    + geom_text(aes(label="value"), format_string="{:.0f}", size=9, color="white")
    + scale_fill_gradient2(low="#FFD43B", mid="#5DADE2", high="#306998", midpoint=50)
    + labs(x="Region", y="", fill="Score")
    + base_theme
    + theme(legend_position="right", figure_size=(5, 3))
)

# Panel E: Monthly Score - plotnine bar plot
p_monthly = (
    ggplot(df_monthly, aes(x="month", y="score"))
    + geom_bar(stat="identity", fill="#306998", width=0.6)
    + labs(x="Month", y="Score")
    + base_theme
    + theme(figure_size=(5, 3))
)

# Use plotnine's composition to create a mosaic-like layout
# Pattern approximation: (A|A|B) / (A|A|B) / (C|D|E)
# Since plotnine doesn't support true spanning, we use composition

# Create the composition
# Top section: overview (2/3) | category (1/3) - repeated for visual weight
# Bottom section: scatter | heatmap | monthly
top_row = p_overview | p_category
bottom_row = p_scatter | p_heatmap | p_monthly
full_layout = top_row / bottom_row

# Draw the composed layout
fig = full_layout.draw()

# Adjust figure size for 4800x2700 target
fig.set_size_inches(16, 9)

# Adjust spacing
fig.subplots_adjust(top=0.88, bottom=0.08, left=0.06, right=0.94, hspace=0.35, wspace=0.25)

# Add main figure title using suptitle
fig.suptitle("subplot-mosaic · plotnine · pyplots.ai", fontsize=28, fontweight="bold", y=0.98)

# Save
fig.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
plt.close(fig)
