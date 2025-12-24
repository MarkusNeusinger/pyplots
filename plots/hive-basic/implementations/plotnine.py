""" pyplots.ai
hive-basic: Basic Hive Plot
Library: plotnine 0.15.2 | Python 3.13.11
Quality: 72/100 | Created: 2025-12-24
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    coord_fixed,
    element_text,
    geom_point,
    geom_segment,
    geom_text,
    ggplot,
    labs,
    scale_color_manual,
    theme,
    theme_void,
    xlim,
    ylim,
)


# Set seed for reproducibility
np.random.seed(42)

# Create sample software module dependency network
# Nodes: modules categorized by type (core, utility, interface)
nodes = pd.DataFrame(
    {
        "id": [
            "auth",
            "db",
            "cache",
            "logger",
            "config",
            "validator",
            "api",
            "web",
            "cli",
            "core",
            "utils",
            "crypto",
            "http",
            "parser",
            "router",
            "session",
            "queue",
            "storage",
            "monitor",
            "scheduler",
        ],
        "category": [
            "core",
            "core",
            "utility",
            "utility",
            "utility",
            "utility",
            "interface",
            "interface",
            "interface",
            "core",
            "utility",
            "utility",
            "utility",
            "utility",
            "interface",
            "core",
            "utility",
            "utility",
            "utility",
            "utility",
        ],
        "degree": [8, 7, 5, 6, 4, 5, 6, 5, 4, 9, 3, 4, 5, 3, 5, 6, 4, 5, 4, 3],
    }
)

# Edges: dependencies between modules
edges = pd.DataFrame(
    {
        "source": [
            "api",
            "api",
            "api",
            "web",
            "web",
            "web",
            "cli",
            "cli",
            "auth",
            "auth",
            "auth",
            "db",
            "db",
            "cache",
            "logger",
            "config",
            "validator",
            "core",
            "core",
            "core",
            "router",
            "router",
            "session",
            "session",
            "http",
            "crypto",
            "queue",
            "storage",
            "monitor",
        ],
        "target": [
            "auth",
            "db",
            "logger",
            "auth",
            "session",
            "router",
            "config",
            "logger",
            "db",
            "crypto",
            "session",
            "cache",
            "logger",
            "logger",
            "config",
            "utils",
            "logger",
            "db",
            "cache",
            "logger",
            "http",
            "auth",
            "cache",
            "crypto",
            "parser",
            "utils",
            "storage",
            "logger",
            "logger",
        ],
    }
)

# Hive plot parameters
# 3 axes for the 3 categories
axis_angles = {"core": 90, "utility": 210, "interface": 330}  # degrees
axis_colors = {"core": "#306998", "utility": "#FFD43B", "interface": "#4ECDC4"}

# Calculate node positions on axes
# Nodes positioned along axis by degree (higher degree = further from center)


def get_axis_position(category, degree, max_degree, idx_in_axis, count_in_axis):
    """Calculate Cartesian coordinates for a node on its axis."""
    angle_deg = axis_angles[category]
    angle_rad = np.radians(angle_deg)

    # Normalize degree to radial distance (0.3 to 0.95 of axis length)
    # Add small offset based on index to prevent overlapping
    base_radius = 0.3 + (degree / max_degree) * 0.6
    jitter = (idx_in_axis - count_in_axis / 2) * 0.02
    radius = np.clip(base_radius + jitter, 0.25, 0.98)

    x = radius * np.cos(angle_rad)
    y = radius * np.sin(angle_rad)
    return x, y


# Assign positions to nodes
max_degree = nodes["degree"].max()

# Count nodes per category for jittering
category_counts = nodes.groupby("category").cumcount()
category_totals = nodes.groupby("category")["id"].transform("count")

nodes["idx_in_axis"] = category_counts
nodes["count_in_axis"] = category_totals

positions = []
for _, row in nodes.iterrows():
    x, y = get_axis_position(row["category"], row["degree"], max_degree, row["idx_in_axis"], row["count_in_axis"])
    positions.append({"id": row["id"], "x": x, "y": y, "category": row["category"]})

node_positions = pd.DataFrame(positions)

# Create axis lines data (from center to edge)
axis_lines = []
for cat, angle in axis_angles.items():
    angle_rad = np.radians(angle)
    axis_lines.append(
        {"x": 0, "y": 0, "xend": 1.05 * np.cos(angle_rad), "yend": 1.05 * np.sin(angle_rad), "category": cat}
    )
axis_df = pd.DataFrame(axis_lines)

# Create edge data with Bezier curves (quadratic approximation using control points)
edge_data = []
for _, row in edges.iterrows():
    src_pos = node_positions[node_positions["id"] == row["source"]].iloc[0]
    tgt_pos = node_positions[node_positions["id"] == row["target"]].iloc[0]

    src_cat = src_pos["category"]
    tgt_cat = tgt_pos["category"]

    # Determine if edge is within same axis or between axes
    if src_cat == tgt_cat:
        # Same axis: curve inward toward center
        mid_factor = 0.3
    else:
        # Different axes: curve through center area
        mid_factor = 0.15

    # Simple curved edge using multiple segments
    # Control point toward center
    ctrl_x = mid_factor * (src_pos["x"] + tgt_pos["x"]) / 2
    ctrl_y = mid_factor * (src_pos["y"] + tgt_pos["y"]) / 2

    # Generate points along quadratic Bezier curve
    n_points = 20
    for i in range(n_points):
        t0 = i / n_points
        t1 = (i + 1) / n_points

        # Quadratic Bezier: B(t) = (1-t)^2*P0 + 2*(1-t)*t*P1 + t^2*P2
        x0 = (1 - t0) ** 2 * src_pos["x"] + 2 * (1 - t0) * t0 * ctrl_x + t0**2 * tgt_pos["x"]
        y0 = (1 - t0) ** 2 * src_pos["y"] + 2 * (1 - t0) * t0 * ctrl_y + t0**2 * tgt_pos["y"]
        x1 = (1 - t1) ** 2 * src_pos["x"] + 2 * (1 - t1) * t1 * ctrl_x + t1**2 * tgt_pos["x"]
        y1 = (1 - t1) ** 2 * src_pos["y"] + 2 * (1 - t1) * t1 * ctrl_y + t1**2 * tgt_pos["y"]

        edge_data.append({"x": x0, "y": y0, "xend": x1, "yend": y1, "src_cat": src_cat, "tgt_cat": tgt_cat})

edge_df = pd.DataFrame(edge_data)

# Create axis labels
axis_labels = []
for cat, angle in axis_angles.items():
    angle_rad = np.radians(angle)
    axis_labels.append(
        {"x": 1.18 * np.cos(angle_rad), "y": 1.18 * np.sin(angle_rad), "label": cat.upper(), "category": cat}
    )
label_df = pd.DataFrame(axis_labels)

# Create the plot
plot = (
    ggplot()
    # Draw edges first (behind nodes) with transparency
    + geom_segment(aes(x="x", y="y", xend="xend", yend="yend"), data=edge_df, color="#888888", size=0.5, alpha=0.25)
    # Draw axis lines
    + geom_segment(aes(x="x", y="y", xend="xend", yend="yend", color="category"), data=axis_df, size=2.5, alpha=0.7)
    # Draw nodes
    + geom_point(aes(x="x", y="y", color="category"), data=node_positions, size=6, alpha=0.9)
    # Add axis labels
    + geom_text(aes(x="x", y="y", label="label", color="category"), data=label_df, size=14, fontweight="bold")
    # Color scale
    + scale_color_manual(values=axis_colors)
    # Styling
    + coord_fixed(ratio=1)
    + xlim(-1.4, 1.4)
    + ylim(-1.4, 1.4)
    + labs(title="hive-basic · plotnine · pyplots.ai")
    + theme_void()
    + theme(
        figure_size=(12, 12),
        plot_title=element_text(size=22, ha="center", weight="bold"),
        legend_position="none",
        plot_margin=0.05,
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
