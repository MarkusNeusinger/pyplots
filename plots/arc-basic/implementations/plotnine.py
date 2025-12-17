"""
arc-basic: Basic Arc Diagram
Library: plotnine
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    element_blank,
    element_text,
    geom_path,
    geom_point,
    geom_text,
    ggplot,
    labs,
    scale_color_manual,
    theme,
    theme_minimal,
)


# Data
np.random.seed(42)
nodes = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
n_nodes = len(nodes)
node_positions = {name: i for i, name in enumerate(nodes)}

# Create edges with varying distances (short, medium, long-range connections)
edges = [
    ("A", "B", 1),  # Short-range
    ("B", "C", 1),
    ("C", "D", 1),
    ("A", "D", 2),  # Medium-range
    ("D", "F", 2),
    ("E", "G", 2),
    ("B", "E", 2),
    ("A", "F", 3),  # Long-range
    ("C", "H", 3),
    ("B", "I", 3),
    ("D", "J", 3),
    ("A", "J", 3),  # Very long-range
    ("F", "I", 2),
]

# Node data
node_df = pd.DataFrame({"node": nodes, "x": range(n_nodes), "y": [0] * n_nodes})

# Create arc paths - each arc is a curved path between two nodes
arc_data = []
for i, (source, target, _weight) in enumerate(edges):
    x_start = node_positions[source]
    x_end = node_positions[target]
    distance = abs(x_end - x_start)

    # Arc height proportional to distance between nodes
    height = distance * 0.4

    # Generate points along a semicircular arc
    n_points = 50
    t = np.linspace(0, np.pi, n_points)
    x_mid = (x_start + x_end) / 2
    radius = abs(x_end - x_start) / 2

    x_arc = x_mid + radius * np.cos(np.pi - t) if x_end > x_start else x_mid + radius * np.cos(t)
    y_arc = height * np.sin(t)

    for j in range(n_points):
        arc_data.append({"arc_id": i, "x": x_arc[j], "y": y_arc[j], "distance": distance})

arc_df = pd.DataFrame(arc_data)

# Categorize distance for coloring
arc_df["distance_cat"] = pd.Categorical(
    arc_df["distance"].apply(lambda d: "Short" if d <= 1 else ("Medium" if d <= 2 else "Long")),
    categories=["Short", "Medium", "Long"],
    ordered=True,
)

# Plot
plot = (
    ggplot()
    + geom_path(data=arc_df, mapping=aes(x="x", y="y", group="arc_id", color="distance_cat"), size=1.5, alpha=0.6)
    + geom_point(data=node_df, mapping=aes(x="x", y="y"), size=6, color="#306998")
    + geom_text(data=node_df, mapping=aes(x="x", y="y", label="node"), nudge_y=-0.25, size=14, color="#306998")
    + scale_color_manual(
        values={"Short": "#306998", "Medium": "#FFD43B", "Long": "#E55039"}, name="Connection\nDistance"
    )
    + labs(title="arc-basic \u00b7 plotnine \u00b7 pyplots.ai", x="Node Position", y="Arc Height")
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        text=element_text(size=14),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        plot_title=element_text(size=24),
        legend_text=element_text(size=16),
        legend_title=element_text(size=18),
        axis_text_y=element_blank(),
        axis_ticks_major_y=element_blank(),
        panel_grid_major_y=element_blank(),
        panel_grid_minor_y=element_blank(),
    )
)

plot.save("plot.png", dpi=300)
