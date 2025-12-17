"""
network-basic: Basic Network Graph
Library: plotnine
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    element_blank,
    element_text,
    geom_point,
    geom_segment,
    geom_text,
    ggplot,
    labs,
    scale_color_manual,
    scale_size_continuous,
    theme,
    xlim,
    ylim,
)


# Set seed for reproducibility
np.random.seed(42)

# Data: A small social network with 20 people in 4 communities
nodes = [
    {"id": 0, "label": "Alice", "group": "A"},
    {"id": 1, "label": "Bob", "group": "A"},
    {"id": 2, "label": "Carol", "group": "A"},
    {"id": 3, "label": "David", "group": "A"},
    {"id": 4, "label": "Eve", "group": "A"},
    {"id": 5, "label": "Frank", "group": "B"},
    {"id": 6, "label": "Grace", "group": "B"},
    {"id": 7, "label": "Henry", "group": "B"},
    {"id": 8, "label": "Ivy", "group": "B"},
    {"id": 9, "label": "Jack", "group": "B"},
    {"id": 10, "label": "Kate", "group": "C"},
    {"id": 11, "label": "Leo", "group": "C"},
    {"id": 12, "label": "Mia", "group": "C"},
    {"id": 13, "label": "Noah", "group": "C"},
    {"id": 14, "label": "Olivia", "group": "C"},
    {"id": 15, "label": "Paul", "group": "D"},
    {"id": 16, "label": "Quinn", "group": "D"},
    {"id": 17, "label": "Ryan", "group": "D"},
    {"id": 18, "label": "Sara", "group": "D"},
    {"id": 19, "label": "Tom", "group": "D"},
]

# Edges: Friendship connections (within and between groups)
edges = [
    # Group A internal connections
    (0, 1),
    (0, 2),
    (1, 2),
    (1, 3),
    (2, 4),
    (3, 4),
    # Group B internal connections
    (5, 6),
    (5, 7),
    (6, 8),
    (7, 8),
    (7, 9),
    (8, 9),
    # Group C internal connections
    (10, 11),
    (10, 12),
    (11, 13),
    (12, 13),
    (12, 14),
    (13, 14),
    # Group D internal connections
    (15, 16),
    (15, 17),
    (16, 18),
    (17, 18),
    (17, 19),
    (18, 19),
    # Cross-group connections (bridges between communities)
    (0, 5),
    (4, 10),
    (9, 15),
    (14, 19),
    (2, 6),
    (8, 11),
    (13, 16),
]

# Calculate spring layout (force-directed algorithm)
n = len(nodes)
positions = np.random.rand(n, 2) * 2 - 1
k = 0.4  # Optimal distance parameter

for iteration in range(150):
    displacement = np.zeros((n, 2))

    # Repulsive forces between all node pairs
    for i in range(n):
        for j in range(i + 1, n):
            diff = positions[i] - positions[j]
            dist = max(np.linalg.norm(diff), 0.01)
            force = (k * k / dist) * (diff / dist)
            displacement[i] += force
            displacement[j] -= force

    # Attractive forces for edges
    for src, tgt in edges:
        diff = positions[src] - positions[tgt]
        dist = max(np.linalg.norm(diff), 0.01)
        force = (dist * dist / k) * (diff / dist)
        displacement[src] -= force
        displacement[tgt] += force

    # Apply displacement with cooling
    cooling = 1 - iteration / 150
    for i in range(n):
        disp_norm = np.linalg.norm(displacement[i])
        if disp_norm > 0:
            positions[i] += (displacement[i] / disp_norm) * min(disp_norm, 0.1 * cooling)

# Normalize positions to [0.1, 0.9] range
pos_min = positions.min(axis=0)
pos_max = positions.max(axis=0)
positions = (positions - pos_min) / (pos_max - pos_min + 1e-6) * 0.8 + 0.1
pos = {node["id"]: positions[i] for i, node in enumerate(nodes)}

# Calculate node degrees for sizing
degrees = {node["id"]: 0 for node in nodes}
for src, tgt in edges:
    degrees[src] += 1
    degrees[tgt] += 1

# Create nodes DataFrame
nodes_df = pd.DataFrame(
    {
        "x": [pos[node["id"]][0] for node in nodes],
        "y": [pos[node["id"]][1] for node in nodes],
        "label": [node["label"] for node in nodes],
        "group": [node["group"] for node in nodes],
        "degree": [degrees[node["id"]] for node in nodes],
    }
)

# Create edges DataFrame
edges_df = pd.DataFrame(
    {
        "x": [pos[src][0] for src, tgt in edges],
        "y": [pos[src][1] for src, tgt in edges],
        "xend": [pos[tgt][0] for src, tgt in edges],
        "yend": [pos[tgt][1] for src, tgt in edges],
    }
)

# Color palette for groups
group_colors = {"A": "#306998", "B": "#FFD43B", "C": "#4CAF50", "D": "#FF7043"}

# Create plot using grammar of graphics
plot = (
    ggplot()
    # Draw edges first (underneath nodes)
    + geom_segment(
        data=edges_df, mapping=aes(x="x", y="y", xend="xend", yend="yend"), color="#888888", size=1.5, alpha=0.5
    )
    # Draw nodes colored by group, sized by degree
    + geom_point(data=nodes_df, mapping=aes(x="x", y="y", color="group", size="degree"), alpha=0.9, stroke=0.5)
    # Draw labels on top
    + geom_text(data=nodes_df, mapping=aes(x="x", y="y", label="label"), size=10, color="#222222", fontweight="bold")
    # Color scale for groups
    + scale_color_manual(values=group_colors, name="Community")
    # Size scale for node degrees
    + scale_size_continuous(range=(8, 18), name="Connections")
    # Axis limits
    + xlim(-0.05, 1.05)
    + ylim(-0.05, 1.05)
    # Labels and title
    + labs(title="Social Network · network-basic · plotnine · pyplots.ai")
    # Theme for clean network visualization
    + theme(
        figure_size=(16, 9),
        plot_title=element_text(size=24),
        legend_title=element_text(size=16),
        legend_text=element_text(size=14),
        # Remove axes for network graph
        axis_title=element_blank(),
        axis_text=element_blank(),
        axis_ticks=element_blank(),
        panel_grid=element_blank(),
        panel_background=element_blank(),
    )
)

# Save plot
plot.save("plot.png", dpi=300, verbose=False)
