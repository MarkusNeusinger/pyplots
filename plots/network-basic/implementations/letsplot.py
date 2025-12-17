"""
network-basic: Basic Network Graph
Library: lets-plot
"""

import numpy as np
import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    coord_fixed,
    element_blank,
    element_text,
    geom_point,
    geom_segment,
    geom_text,
    ggplot,
    ggsize,
    labs,
    scale_color_manual,
    scale_size_identity,
    theme,
    theme_minimal,
)
from lets_plot.export import ggsave


LetsPlot.setup_html()

# Social network data: 20 people with friendship connections
np.random.seed(42)

nodes = [
    {"id": 0, "label": "Alice", "group": "Marketing"},
    {"id": 1, "label": "Bob", "group": "Engineering"},
    {"id": 2, "label": "Carol", "group": "Engineering"},
    {"id": 3, "label": "David", "group": "Marketing"},
    {"id": 4, "label": "Eve", "group": "Design"},
    {"id": 5, "label": "Frank", "group": "Engineering"},
    {"id": 6, "label": "Grace", "group": "Design"},
    {"id": 7, "label": "Henry", "group": "Marketing"},
    {"id": 8, "label": "Ivy", "group": "Engineering"},
    {"id": 9, "label": "Jack", "group": "Design"},
    {"id": 10, "label": "Kate", "group": "Marketing"},
    {"id": 11, "label": "Leo", "group": "Engineering"},
    {"id": 12, "label": "Mia", "group": "Design"},
    {"id": 13, "label": "Nick", "group": "Marketing"},
    {"id": 14, "label": "Olivia", "group": "Engineering"},
    {"id": 15, "label": "Paul", "group": "Design"},
    {"id": 16, "label": "Quinn", "group": "Marketing"},
    {"id": 17, "label": "Rose", "group": "Engineering"},
    {"id": 18, "label": "Sam", "group": "Design"},
    {"id": 19, "label": "Tom", "group": "Marketing"},
]

# Edges (friendships) - mix of within-group and cross-group connections
edges = [
    (0, 3),
    (0, 7),
    (0, 10),
    (0, 1),  # Alice connections
    (1, 2),
    (1, 5),
    (1, 8),
    (1, 14),  # Bob connections (engineering hub)
    (2, 5),
    (2, 11),
    (2, 17),  # Carol
    (3, 7),
    (3, 16),
    (3, 4),  # David
    (4, 6),
    (4, 9),
    (4, 12),  # Eve (design hub)
    (5, 8),
    (5, 11),  # Frank
    (6, 9),
    (6, 15),
    (6, 18),  # Grace
    (7, 10),
    (7, 13),  # Henry
    (8, 14),
    (8, 17),  # Ivy
    (9, 12),
    (9, 15),  # Jack
    (10, 13),
    (10, 16),
    (10, 19),  # Kate
    (11, 14),
    (11, 17),  # Leo
    (12, 15),
    (12, 18),  # Mia
    (13, 16),
    (13, 19),  # Nick
    (14, 17),  # Olivia
    (15, 18),  # Paul
    (16, 19),  # Quinn
]

n_nodes = len(nodes)


# Simple force-directed layout (Fruchterman-Reingold style)
def spring_layout(nodes, edges, iterations=100, k=None):
    """Compute spring layout positions for network nodes."""
    n = len(nodes)
    if k is None:
        k = np.sqrt(1.0 / n)  # Optimal distance

    # Initialize random positions
    pos = np.random.rand(n, 2) * 2 - 1

    for iteration in range(iterations):
        # Temperature decreases over iterations
        temp = 1.0 - iteration / iterations

        # Calculate repulsive forces (all pairs)
        displacement = np.zeros((n, 2))
        for i in range(n):
            for j in range(i + 1, n):
                delta = pos[i] - pos[j]
                dist = max(np.linalg.norm(delta), 0.01)
                # Repulsive force
                force = (k * k / dist) * (delta / dist)
                displacement[i] += force
                displacement[j] -= force

        # Calculate attractive forces (edges only)
        for src, tgt in edges:
            delta = pos[src] - pos[tgt]
            dist = max(np.linalg.norm(delta), 0.01)
            # Attractive force
            force = (dist * dist / k) * (delta / dist)
            displacement[src] -= force
            displacement[tgt] += force

        # Apply forces with temperature cooling
        for i in range(n):
            disp_norm = max(np.linalg.norm(displacement[i]), 0.01)
            pos[i] += (displacement[i] / disp_norm) * min(disp_norm, temp * 0.5)

        # Keep within bounds
        pos = np.clip(pos, -1, 1)

    return pos


# Compute layout
positions = spring_layout(nodes, edges, iterations=150)

# Calculate node degrees for sizing
degrees = [0] * n_nodes
for src, tgt in edges:
    degrees[src] += 1
    degrees[tgt] += 1

# Prepare node dataframe
node_data = []
for i, node in enumerate(nodes):
    node_data.append(
        {
            "x": positions[i, 0],
            "y": positions[i, 1],
            "label": node["label"],
            "group": node["group"],
            "degree": degrees[i],
            "size": 8 + degrees[i] * 2,  # Size based on connections
        }
    )
df_nodes = pd.DataFrame(node_data)

# Prepare edge dataframe
edge_data = []
for src, tgt in edges:
    edge_data.append(
        {"x": positions[src, 0], "y": positions[src, 1], "xend": positions[tgt, 0], "yend": positions[tgt, 1]}
    )
df_edges = pd.DataFrame(edge_data)

# Group colors
group_colors = {
    "Marketing": "#306998",  # Python Blue
    "Engineering": "#FFD43B",  # Python Yellow
    "Design": "#27AE60",  # Green
}

# Create plot
plot = (
    ggplot()
    # Draw edges first (behind nodes)
    + geom_segment(aes(x="x", y="y", xend="xend", yend="yend"), data=df_edges, color="#AAAAAA", size=1.2, alpha=0.6)
    # Draw nodes
    + geom_point(aes(x="x", y="y", color="group", size="size"), data=df_nodes, alpha=0.9)
    + scale_size_identity()
    # Draw labels (offset slightly above nodes)
    + geom_text(aes(x="x", y="y", label="label"), data=df_nodes, nudge_y=0.08, size=11, color="#333333")
    + scale_color_manual(values=["#27AE60", "#FFD43B", "#306998"], name="Department")
    + coord_fixed(ratio=1)
    + labs(title="Social Network · network-basic · lets-plot · pyplots.ai")
    + theme_minimal()
    + theme(
        plot_title=element_text(size=28, face="bold"),
        axis_title=element_blank(),
        axis_text=element_blank(),
        axis_ticks=element_blank(),
        panel_grid=element_blank(),
        legend_text=element_text(size=16),
        legend_title=element_text(size=18),
        legend_position="right",
    )
    + ggsize(1600, 900)
)

# Save as PNG (scale 3x to get 4800 x 2700 px)
ggsave(plot, "plot.png", path=".", scale=3)

# Save as HTML for interactive version
ggsave(plot, "plot.html", path=".")
