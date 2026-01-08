"""pyplots.ai
scatter-brush-zoom: Interactive Scatter Plot with Brush Selection and Zoom
Library: letsplot 4.8.2 | Python 3.13.11
Quality: 65/100 | Created: 2026-01-08
"""

import numpy as np
import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    element_blank,
    element_text,
    geom_point,
    geom_text,
    ggplot,
    ggsize,
    labs,
    layer_tooltips,
    scale_color_manual,
    theme,
    theme_minimal,
)
from lets_plot.export import ggsave


LetsPlot.setup_html()

# Data - Generate clustered data for brush selection demonstration
np.random.seed(42)

# Create 4 distinct clusters with different sizes
n_per_cluster = [80, 120, 100, 100]
centers = [(20, 60), (50, 30), (70, 70), (40, 80)]
spreads = [8, 12, 10, 6]
categories = ["Cluster A", "Cluster B", "Cluster C", "Cluster D"]

x_data, y_data, colors, labels = [], [], [], []
point_id = 0
for n, (cx, cy), spread, cat in zip(n_per_cluster, centers, spreads, categories, strict=True):
    for _ in range(n):
        x_data.append(np.random.normal(cx, spread))
        y_data.append(np.random.normal(cy, spread))
        colors.append(cat)
        labels.append(f"P{point_id:03d}")
        point_id += 1

df = pd.DataFrame({"x": x_data, "y": y_data, "category": colors, "label": labels})

# Create tooltips for hover interaction - shows point details
tooltips = (
    layer_tooltips()
    .title("@label")
    .line("Category: @category")
    .line("X: @x (units)")
    .line("Y: @y (units)")
    .format("x", ".1f")
    .format("y", ".1f")
)

# Create interactive scatter plot
# lets-plot HTML export includes built-in toolbar with:
# - Pan (drag to move around)
# - Wheel zoom (scroll to zoom in/out)
# - Box zoom (select area to zoom)
# - Reset (double-click to reset view)
plot = (
    ggplot(df, aes(x="x", y="y", color="category"))
    + geom_point(size=5, alpha=0.7, tooltips=tooltips)
    + scale_color_manual(values=["#306998", "#FFD43B", "#DC2626", "#059669"])
    + labs(
        x="X Value (units)", y="Y Value (units)", title="scatter-brush-zoom · letsplot · pyplots.ai", color="Category"
    )
    + theme_minimal()
    + theme(
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        plot_title=element_text(size=24),
        legend_title=element_text(size=18),
        legend_text=element_text(size=16),
        panel_grid_major=element_blank(),
        panel_grid_minor=element_blank(),
    )
    + ggsize(1600, 900)
)

# Add annotation explaining interactive features (visible in static PNG)
# Create annotation data
annotation_df = pd.DataFrame(
    {"x": [85], "y": [95], "text": ["Interactive HTML: Use toolbar for pan, zoom, box-select, and reset"]}
)

plot = plot + geom_text(
    aes(x="x", y="y", label="text"), data=annotation_df, inherit_aes=False, size=12, color="#666666", hjust=1
)

# Save static PNG (scaled 3x for 4800x2700 px)
ggsave(plot, "plot.png", path=".", scale=3)

# Save interactive HTML with zoom, pan, and hover capabilities
# The HTML viewer includes a toolbar with:
# - Pan mode: click and drag to navigate
# - Wheel zoom: scroll to zoom in/out
# - Box zoom: draw rectangle to zoom to area (brush-like selection)
# - Reset: double-click or use reset button to restore original view
ggsave(plot, "plot.html", path=".")
