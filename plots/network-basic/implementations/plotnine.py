"""
network-basic: Basic Network Graph
Library: plotnine
"""

import networkx as nx
import numpy as np
import pandas as pd
from plotnine import (
    aes,
    coord_fixed,
    element_rect,
    element_text,
    geom_point,
    geom_segment,
    geom_text,
    ggplot,
    labs,
    scale_color_manual,
    scale_size_continuous,
    theme,
    theme_void,
)


# Data: Small social network with 20 people
np.random.seed(42)

# Create nodes with groups (departments)
nodes = [
    {"id": 0, "label": "Alice", "group": "Engineering"},
    {"id": 1, "label": "Bob", "group": "Engineering"},
    {"id": 2, "label": "Carol", "group": "Engineering"},
    {"id": 3, "label": "David", "group": "Engineering"},
    {"id": 4, "label": "Eve", "group": "Engineering"},
    {"id": 5, "label": "Frank", "group": "Marketing"},
    {"id": 6, "label": "Grace", "group": "Marketing"},
    {"id": 7, "label": "Henry", "group": "Marketing"},
    {"id": 8, "label": "Ivy", "group": "Marketing"},
    {"id": 9, "label": "Jack", "group": "Sales"},
    {"id": 10, "label": "Kate", "group": "Sales"},
    {"id": 11, "label": "Leo", "group": "Sales"},
    {"id": 12, "label": "Mia", "group": "Sales"},
    {"id": 13, "label": "Noah", "group": "Design"},
    {"id": 14, "label": "Olivia", "group": "Design"},
    {"id": 15, "label": "Paul", "group": "Design"},
    {"id": 16, "label": "Quinn", "group": "HR"},
    {"id": 17, "label": "Ryan", "group": "HR"},
    {"id": 18, "label": "Sara", "group": "HR"},
    {"id": 19, "label": "Tom", "group": "HR"},
]

# Create edges (friendships) - more connections within groups, some across
edges = [
    # Engineering internal
    (0, 1),
    (0, 2),
    (1, 2),
    (1, 3),
    (2, 4),
    (3, 4),
    # Marketing internal
    (5, 6),
    (5, 7),
    (6, 8),
    (7, 8),
    # Sales internal
    (9, 10),
    (9, 11),
    (10, 12),
    (11, 12),
    # Design internal
    (13, 14),
    (13, 15),
    (14, 15),
    # HR internal
    (16, 17),
    (16, 18),
    (17, 19),
    (18, 19),
    # Cross-department connections
    (0, 5),
    (1, 9),
    (2, 13),
    (3, 16),  # Engineering bridges
    (5, 9),
    (6, 14),  # Marketing bridges
    (10, 17),
    (12, 15),  # Sales/Design/HR bridges
    (7, 18),
    (4, 19),  # More cross connections
]

# Build networkx graph for layout computation
G = nx.Graph()
G.add_nodes_from([n["id"] for n in nodes])
G.add_edges_from(edges)

# Compute layout using spring algorithm
pos = nx.spring_layout(G, k=2.5, iterations=100, seed=42)

# Build node dataframe with positions and attributes
node_df = pd.DataFrame(nodes)
node_df["x"] = [pos[i][0] for i in node_df["id"]]
node_df["y"] = [pos[i][1] for i in node_df["id"]]
node_df["degree"] = [G.degree(i) for i in node_df["id"]]

# Build edge dataframe
edge_data = []
for source, target in edges:
    edge_data.append({"x": pos[source][0], "y": pos[source][1], "xend": pos[target][0], "yend": pos[target][1]})
edge_df = pd.DataFrame(edge_data)

# Color palette for groups (colorblind-safe)
group_colors = {
    "Engineering": "#306998",  # Python Blue
    "Marketing": "#FFD43B",  # Python Yellow
    "Sales": "#2CA02C",  # Green
    "Design": "#9467BD",  # Purple
    "HR": "#E377C2",  # Pink
}

# Create plot
plot = (
    ggplot()
    # Draw edges first (underneath nodes)
    + geom_segment(
        data=edge_df, mapping=aes(x="x", y="y", xend="xend", yend="yend"), color="#CCCCCC", size=0.8, alpha=0.6
    )
    # Draw nodes (size encodes degree/connections)
    + geom_point(data=node_df, mapping=aes(x="x", y="y", color="group", size="degree"), alpha=0.9)
    # Add labels
    + geom_text(data=node_df, mapping=aes(x="x", y="y", label="label"), size=10, nudge_y=0.08, color="#333333")
    # Custom colors
    + scale_color_manual(values=group_colors)
    # Node size based on degree
    + scale_size_continuous(range=(8, 16))
    # Labels
    + labs(title="network-basic \u00b7 plotnine \u00b7 pyplots.ai", color="Department", size="Connections")
    # Clean theme for network visualization
    + theme_void()
    + theme(
        figure_size=(16, 9),
        plot_title=element_text(size=24, ha="center", weight="bold"),
        legend_title=element_text(size=18),
        legend_text=element_text(size=14),
        legend_position="right",
        plot_background=element_rect(fill="white", color="white"),
    )
    + coord_fixed(ratio=1)
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
