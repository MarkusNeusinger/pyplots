""" pyplots.ai
linked-views-selection: Multiple Linked Views with Selection Sync
Library: plotnine 0.15.2 | Python 3.13.11
Quality: 75/100 | Created: 2026-01-08
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    element_blank,
    element_line,
    element_text,
    facet_wrap,
    geom_point,
    geom_vline,
    ggplot,
    labs,
    scale_alpha_identity,
    scale_color_manual,
    scale_x_continuous,
    scale_y_continuous,
    theme,
    theme_minimal,
)


# Data - Multivariate dataset with 3 clusters
np.random.seed(42)
n_per_cluster = 50

categories = np.repeat(["Cluster A", "Cluster B", "Cluster C"], n_per_cluster)

x = np.concatenate(
    [
        np.random.normal(2.5, 0.6, n_per_cluster),
        np.random.normal(5.5, 0.7, n_per_cluster),
        np.random.normal(4.0, 0.8, n_per_cluster),
    ]
)

y = np.concatenate(
    [
        np.random.normal(3.0, 0.5, n_per_cluster),
        np.random.normal(5.5, 0.6, n_per_cluster),
        np.random.normal(2.0, 0.7, n_per_cluster),
    ]
)

value = np.concatenate(
    [
        np.random.normal(30, 6, n_per_cluster),
        np.random.normal(55, 8, n_per_cluster),
        np.random.normal(42, 7, n_per_cluster),
    ]
)

# Selection: x > 4.5 (roughly selects Cluster B and part of Cluster C)
selection_threshold = 4.5
selected = x > selection_threshold

# Create main dataframe
df = pd.DataFrame(
    {
        "x": x,
        "y": y,
        "category": categories,
        "value": value,
        "selected": selected,
        "selection_state": np.where(selected, "Selected", "Unselected"),
        "point_alpha": np.where(selected, 0.9, 0.3),
    }
)

n_selected = int(selected.sum())
n_total = len(df)

# Colors - colorblind-safe palette
color_selected = "#306998"
color_unselected = "#AAAAAA"
color_threshold = "#FFD43B"

# Prepare long-format data for faceted view
# View 1: Scatter (x vs y)
df_scatter = df[["x", "y", "selection_state", "point_alpha"]].copy()
df_scatter["view"] = "1. Scatter (X vs Y)"
df_scatter["x_val"] = df_scatter["x"]
df_scatter["y_val"] = df_scatter["y"]
df_scatter["show_threshold"] = True

# View 2: X vs Value
df_xval = df[["x", "value", "selection_state", "point_alpha"]].copy()
df_xval["view"] = "2. X vs Value"
df_xval["x_val"] = df_xval["x"]
df_xval["y_val"] = df_xval["value"]
df_xval["show_threshold"] = True

# View 3: Y vs Value
df_yval = df[["y", "value", "selection_state", "point_alpha"]].copy()
df_yval["view"] = "3. Y vs Value"
df_yval["x_val"] = df_yval["y"]
df_yval["y_val"] = df_yval["value"]
df_yval["show_threshold"] = False

# Combine for faceted scatter views
df_long = pd.concat(
    [
        df_scatter[["view", "x_val", "y_val", "selection_state", "point_alpha", "show_threshold"]],
        df_xval[["view", "x_val", "y_val", "selection_state", "point_alpha", "show_threshold"]],
        df_yval[["view", "x_val", "y_val", "selection_state", "point_alpha", "show_threshold"]],
    ],
    ignore_index=True,
)

# Create threshold line data for views that need it
threshold_df = pd.DataFrame(
    {"view": ["1. Scatter (X vs Y)", "2. X vs Value"], "threshold": [selection_threshold, selection_threshold]}
)

# Create faceted plot with 3 coordinated views
plot = (
    ggplot(df_long, aes("x_val", "y_val", color="selection_state", alpha="point_alpha"))
    + geom_point(size=4)
    + geom_vline(
        data=threshold_df, mapping=aes(xintercept="threshold"), linetype="dashed", color=color_threshold, size=1.2
    )
    + facet_wrap("~view", scales="free", ncol=3)
    + scale_color_manual(name="Selection", values={"Selected": color_selected, "Unselected": color_unselected})
    + scale_alpha_identity()
    + scale_x_continuous(breaks=lambda x: np.linspace(min(x), max(x), 5))
    + scale_y_continuous(breaks=lambda x: np.linspace(min(x), max(x), 5))
    + labs(
        title=f"linked-views-selection · plotnine · pyplots.ai\nSelection: x > {selection_threshold} highlights {n_selected}/{n_total} points across all views",
        x="",
        y="",
    )
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        text=element_text(size=16),
        axis_title=element_text(size=20),
        axis_text=element_text(size=14),
        axis_text_x=element_text(rotation=0),
        plot_title=element_text(size=22, weight="bold", ha="center"),
        legend_text=element_text(size=16),
        legend_title=element_text(size=18),
        legend_position="bottom",
        legend_direction="horizontal",
        strip_text=element_text(size=18, weight="bold"),
        panel_grid_major=element_line(color="#E0E0E0", size=0.4, alpha=0.5),
        panel_grid_minor=element_blank(),
        panel_spacing=0.4,
        plot_margin=0.05,
    )
)

# Save directly without PIL composition
plot.save("plot.png", dpi=300, verbose=False)
