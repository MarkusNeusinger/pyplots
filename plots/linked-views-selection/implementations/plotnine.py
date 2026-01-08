""" pyplots.ai
linked-views-selection: Multiple Linked Views with Selection Sync
Library: plotnine 0.15.2 | Python 3.13.11
Quality: 78/100 | Created: 2026-01-08
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    annotate,
    coord_cartesian,
    element_blank,
    element_line,
    element_rect,
    element_text,
    facet_wrap,
    geom_bar,
    geom_histogram,
    geom_point,
    geom_vline,
    ggplot,
    labs,
    position_stack,
    scale_alpha_identity,
    scale_color_manual,
    scale_fill_manual,
    scale_size_identity,
    scale_x_continuous,
    scale_y_continuous,
    theme,
    theme_minimal,
)

# Data - Multivariate dataset with 3 clusters
np.random.seed(42)
n_per_cluster = 50

categories = np.repeat(["Cluster A", "Cluster B", "Cluster C"], n_per_cluster)

# Generate x, y coordinates for each cluster
x = np.concatenate([
    np.random.normal(2.5, 0.6, n_per_cluster),   # Cluster A - left
    np.random.normal(5.5, 0.7, n_per_cluster),   # Cluster B - right (will be selected)
    np.random.normal(4.0, 0.8, n_per_cluster),   # Cluster C - middle
])

y = np.concatenate([
    np.random.normal(3.0, 0.5, n_per_cluster),   # Cluster A
    np.random.normal(5.5, 0.6, n_per_cluster),   # Cluster B
    np.random.normal(2.0, 0.7, n_per_cluster),   # Cluster C
])

# Additional value dimension
value = np.concatenate([
    np.random.normal(30, 6, n_per_cluster),   # Cluster A
    np.random.normal(55, 8, n_per_cluster),   # Cluster B
    np.random.normal(42, 7, n_per_cluster),   # Cluster C
])

# Simulate brush selection: points with x > 4.5 (roughly selects Cluster B)
selection_threshold = 4.5
selected = x > selection_threshold

df = pd.DataFrame({
    "x": x,
    "y": y,
    "category": categories,
    "value": value,
    "selected": selected,
})

# Create selection state column
df["selection_state"] = np.where(df["selected"], "Selected", "Unselected")
# Alpha and size based on selection for visual emphasis
df["point_alpha"] = np.where(df["selected"], 0.9, 0.25)
df["point_size"] = np.where(df["selected"], 5, 3)

# Colors
color_selected = "#306998"    # Python Blue
color_unselected = "#CCCCCC"  # Gray
color_highlight = "#FFD43B"   # Python Yellow for selection line

n_selected = int(selected.sum())
n_total = len(df)

# ============================================================
# Create long-form data for faceted multi-view visualization
# ============================================================

# View 1: Scatter plot data (x vs y)
scatter_data = df[["x", "y", "category", "selection_state", "point_alpha", "point_size"]].copy()
scatter_data["view"] = "1. Scatter Plot (x vs y)"
scatter_data["plot_x"] = scatter_data["x"]
scatter_data["plot_y"] = scatter_data["y"]

# View 2: Value vs Category - shows distribution by category
value_view_data = df[["value", "category", "selection_state", "point_alpha", "point_size"]].copy()
value_view_data["view"] = "2. Value by Category"
# Map categories to numeric positions for x-axis
cat_map = {"Cluster A": 1, "Cluster B": 2, "Cluster C": 3}
value_view_data["plot_x"] = value_view_data["category"].map(cat_map) + np.random.uniform(-0.2, 0.2, len(value_view_data))
value_view_data["plot_y"] = value_view_data["value"]
value_view_data["x"] = value_view_data["plot_x"]  # Keep for consistency
value_view_data["y"] = value_view_data["plot_y"]

# View 3: X vs Value - another angle on the data
xy_value_data = df[["x", "value", "category", "selection_state", "point_alpha", "point_size"]].copy()
xy_value_data["view"] = "3. X vs Value"
xy_value_data["plot_x"] = xy_value_data["x"]
xy_value_data["plot_y"] = xy_value_data["value"]
xy_value_data["y"] = xy_value_data["value"]  # Keep for consistency

# Combine all views
combined_df = pd.concat([scatter_data, value_view_data, xy_value_data], ignore_index=True)

# ============================================================
# FACETED VISUALIZATION: Multiple linked views with selection
# ============================================================

# Selection line data for the scatter plot facet
vline_df = pd.DataFrame({
    "xintercept": [selection_threshold],
    "view": ["1. Scatter Plot (x vs y)"]
})

# Also add selection line for X vs Value view
vline_df2 = pd.DataFrame({
    "xintercept": [selection_threshold],
    "view": ["3. X vs Value"]
})
vline_all = pd.concat([vline_df, vline_df2], ignore_index=True)

faceted_plot = (
    ggplot(combined_df, aes("plot_x", "plot_y", color="selection_state", alpha="point_alpha", size="point_size"))
    + geom_point()
    + geom_vline(
        aes(xintercept="xintercept"),
        data=vline_all,
        linetype="dashed",
        color=color_highlight,
        size=1.2,
    )
    + facet_wrap("~view", scales="free", ncol=3)
    + scale_color_manual(
        values={"Selected": color_selected, "Unselected": color_unselected},
        name="Selection"
    )
    + scale_alpha_identity()
    + scale_size_identity()
    + labs(
        x="",
        y="",
        title=f"linked-views-selection · plotnine · pyplots.ai\nSelection: x > {selection_threshold} ({n_selected}/{n_total} points selected)"
    )
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        text=element_text(size=14),
        axis_title=element_text(size=18),
        axis_text=element_text(size=14),
        plot_title=element_text(size=24, weight="bold", ha="center"),
        legend_text=element_text(size=16),
        legend_title=element_text(size=18),
        legend_position="bottom",
        panel_grid_major=element_line(color="#E5E5E5", size=0.5, alpha=0.5),
        panel_grid_minor=element_blank(),
        strip_text=element_text(size=16, weight="bold"),
        panel_spacing=0.4,
        strip_background=element_rect(fill="#F5F5F5", color="none"),
    )
)

faceted_plot.save("plot.png", dpi=300)
