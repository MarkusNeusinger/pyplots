""" pyplots.ai
arc-basic: Basic Arc Diagram
Library: letsplot 4.8.2 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-23
"""

import numpy as np
import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    element_blank,
    element_text,
    geom_path,
    geom_point,
    geom_text,
    ggplot,
    ggsize,
    labs,
    scale_size_identity,
    theme,
    xlim,
    ylim,
)
from lets_plot.export import ggsave


LetsPlot.setup_html()

# Data: Character interactions in a story chapter
np.random.seed(42)

nodes = ["Alice", "Bob", "Carol", "David", "Eve", "Frank", "Grace", "Henry", "Iris", "Jack"]
n_nodes = len(nodes)

# Edges: pairs of connected nodes with weights (source, target, weight)
edges = [
    (0, 1, 3),  # Alice-Bob (strong connection)
    (0, 3, 2),  # Alice-David
    (1, 2, 2),  # Bob-Carol
    (2, 4, 1),  # Carol-Eve
    (3, 5, 2),  # David-Frank
    (4, 6, 1),  # Eve-Grace
    (0, 7, 1),  # Alice-Henry (long-range)
    (1, 5, 2),  # Bob-Frank
    (2, 3, 3),  # Carol-David (strong)
    (5, 8, 1),  # Frank-Iris
    (6, 9, 2),  # Grace-Jack
    (0, 9, 1),  # Alice-Jack (longest range)
    (3, 7, 2),  # David-Henry
    (7, 8, 1),  # Henry-Iris
    (8, 9, 2),  # Iris-Jack
]

# Node positions along x-axis
x_positions = np.linspace(0, 1, n_nodes)
y_baseline = 0.1

# Create arc data for geom_path
arc_data = []
for edge_id, (start, end, weight) in enumerate(edges):
    x_start = x_positions[start]
    x_end = x_positions[end]

    # Arc height proportional to distance between nodes
    distance = abs(end - start)
    height = 0.08 * distance

    # Generate points along the arc (semi-circle)
    n_points = 50
    t = np.linspace(0, np.pi, n_points)
    arc_x = x_start + (x_end - x_start) * (1 - np.cos(t)) / 2
    arc_y = y_baseline + height * np.sin(t)

    # Line width based on weight
    line_size = 1.5 + weight * 1.0

    for i in range(n_points):
        arc_data.append({"x": arc_x[i], "y": arc_y[i], "edge_id": edge_id, "weight": weight, "size": line_size})

arc_df = pd.DataFrame(arc_data)

# Node data
node_df = pd.DataFrame({"x": x_positions, "y": [y_baseline] * n_nodes, "name": nodes})

# Label data (positioned below nodes)
label_df = pd.DataFrame({"x": x_positions, "y": [y_baseline - 0.05] * n_nodes, "name": nodes})

# Create plot
plot = (
    ggplot()
    # Draw arcs with semi-transparency for overlapping connections
    + geom_path(data=arc_df, mapping=aes(x="x", y="y", group="edge_id", size="size"), color="#306998", alpha=0.6)
    + scale_size_identity()
    # Draw nodes
    + geom_point(data=node_df, mapping=aes(x="x", y="y"), size=10, color="#FFD43B", fill="#FFD43B", stroke=2, shape=21)
    # Add node labels
    + geom_text(
        data=label_df, mapping=aes(x="x", y="y", label="name"), size=14, color="#306998", fontface="bold", vjust=1
    )
    # Styling
    + xlim(-0.05, 1.05)
    + ylim(-0.15, 0.85)
    + labs(title="Character Interactions · arc-basic · letsplot · pyplots.ai")
    + theme(
        axis_title=element_blank(),
        axis_text=element_blank(),
        axis_ticks=element_blank(),
        axis_line=element_blank(),
        panel_grid=element_blank(),
        panel_background=element_blank(),
        plot_title=element_text(size=24, face="bold"),
        legend_position="none",
    )
    + ggsize(1600, 900)
)

# Save as PNG (scale 3x to get 4800 x 2700 px)
ggsave(plot, "plot.png", path=".", scale=3)

# Save as HTML for interactive viewing
ggsave(plot, "plot.html", path=".")
