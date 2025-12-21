""" pyplots.ai
arc-basic: Basic Arc Diagram
Library: plotnine 0.15.1 | Python 3.13.11
Quality: 94/100 | Created: 2025-12-17
"""

import sys


sys.path = [p for p in sys.path if not p.endswith("implementations")]

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from plotnine import (  # noqa: E402
    aes,
    element_blank,
    element_text,
    geom_path,
    geom_point,
    geom_text,
    ggplot,
    labs,
    scale_size_identity,
    theme,
)


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

# Create arc paths dataframe
arc_data = []
arc_id = 0

for start, end, weight in edges:
    x_start = x_positions[start]
    x_end = x_positions[end]

    # Arc center and radius
    x_center = (x_start + x_end) / 2
    arc_radius = abs(x_end - x_start) / 2

    # Arc height proportional to distance between nodes
    distance = abs(end - start)
    height = 0.08 * distance

    # Generate arc points (semi-circle above baseline)
    n_points = 50
    theta = np.linspace(0, np.pi, n_points)
    x_arc = x_center - arc_radius * np.cos(theta)
    y_arc = y_baseline + height * np.sin(theta)

    # Add points to dataframe with arc identifier
    for i in range(n_points):
        arc_data.append(
            {
                "x": x_arc[i],
                "y": y_arc[i],
                "arc_id": arc_id,
                "weight": weight,
                "size": 1.0 + weight * 0.8,  # Line thickness based on weight
            }
        )
    arc_id += 1

arc_df = pd.DataFrame(arc_data)

# Create nodes dataframe
node_df = pd.DataFrame({"x": x_positions, "y": [y_baseline] * n_nodes, "name": nodes})

# Create label dataframe (below nodes)
label_df = pd.DataFrame({"x": x_positions, "y": [y_baseline - 0.05] * n_nodes, "name": nodes})

# Create the plot
plot = (
    ggplot()
    # Draw arcs
    + geom_path(arc_df, aes(x="x", y="y", group="arc_id", size="size"), color="#306998", alpha=0.6)
    + scale_size_identity()
    # Draw nodes
    + geom_point(node_df, aes(x="x", y="y"), color="#FFD43B", size=10, stroke=1.5, fill="#FFD43B")
    # Add node labels
    + geom_text(label_df, aes(x="x", y="y", label="name"), size=11, color="#306998", fontweight="bold", va="top")
    + labs(title="Character Interactions · arc-basic · plotnine · pyplots.ai")
    + theme(
        figure_size=(16, 9),
        plot_title=element_text(size=24, ha="center"),
        axis_title=element_blank(),
        axis_text=element_blank(),
        axis_ticks=element_blank(),
        panel_grid=element_blank(),
        panel_background=element_blank(),
        plot_background=element_blank(),
        legend_position="none",
    )
)

# Save the plot
plot.save("plot.png", dpi=300, verbose=False)
