"""
network-basic: Basic Network Graph
Library: pygal
"""

import math
import random

import pygal
from pygal.style import Style


# Data - Small social network with 20 people and friendships
random.seed(42)

# Node definitions with groups (communities)
nodes = [
    {"id": 0, "label": "Alice", "group": 0},
    {"id": 1, "label": "Bob", "group": 0},
    {"id": 2, "label": "Carol", "group": 0},
    {"id": 3, "label": "Dave", "group": 0},
    {"id": 4, "label": "Eve", "group": 0},
    {"id": 5, "label": "Frank", "group": 1},
    {"id": 6, "label": "Grace", "group": 1},
    {"id": 7, "label": "Henry", "group": 1},
    {"id": 8, "label": "Iris", "group": 1},
    {"id": 9, "label": "Jack", "group": 2},
    {"id": 10, "label": "Kate", "group": 2},
    {"id": 11, "label": "Leo", "group": 2},
    {"id": 12, "label": "Mia", "group": 2},
    {"id": 13, "label": "Nick", "group": 3},
    {"id": 14, "label": "Olivia", "group": 3},
    {"id": 15, "label": "Peter", "group": 3},
    {"id": 16, "label": "Quinn", "group": 3},
    {"id": 17, "label": "Rose", "group": 3},
    {"id": 18, "label": "Sam", "group": 0},
    {"id": 19, "label": "Tina", "group": 2},
]

# Edges (friendships) - connections within and between groups
edges = [
    # Group 0 connections (Alice's circle)
    (0, 1),
    (0, 2),
    (0, 3),
    (1, 2),
    (2, 4),
    (3, 4),
    (4, 18),
    (0, 18),
    # Group 1 connections (Frank's circle)
    (5, 6),
    (5, 7),
    (6, 7),
    (6, 8),
    (7, 8),
    # Group 2 connections (Jack's circle)
    (9, 10),
    (9, 11),
    (10, 11),
    (10, 12),
    (11, 12),
    (9, 19),
    (12, 19),
    # Group 3 connections (Nick's circle)
    (13, 14),
    (13, 15),
    (14, 15),
    (14, 16),
    (15, 16),
    (16, 17),
    (13, 17),
    # Cross-group connections (bridges between communities)
    (2, 5),  # Carol knows Frank
    (4, 9),  # Eve knows Jack
    (8, 13),  # Iris knows Nick
    (11, 15),  # Leo knows Peter
    (18, 6),  # Sam knows Grace
]

# Calculate node degrees (number of connections)
node_degrees = dict.fromkeys(range(len(nodes)), 0)
for source, target in edges:
    node_degrees[source] += 1
    node_degrees[target] += 1

# Layout - Position nodes in circular clusters with some spacing
# Each group positioned in a different area
group_centers = {
    0: (3, 7),  # Top-left
    1: (7, 7),  # Top-right
    2: (7, 3),  # Bottom-right
    3: (3, 3),  # Bottom-left
}

positions = {}
for node in nodes:
    nid = node["id"]
    group = node["group"]
    cx, cy = group_centers[group]
    # Spread nodes in a small circle around group center
    group_nodes = [n for n in nodes if n["group"] == group]
    idx = next(i for i, n in enumerate(group_nodes) if n["id"] == nid)
    angle = 2 * math.pi * idx / len(group_nodes)
    radius = 1.2
    x = cx + radius * math.cos(angle) + random.uniform(-0.2, 0.2)
    y = cy + radius * math.sin(angle) + random.uniform(-0.2, 0.2)
    positions[nid] = (x, y)

# Custom style for pygal
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#999999",
    colors=("#888888", "#306998", "#FFD43B", "#2E8B57", "#DC143C"),
    title_font_size=72,
    label_font_size=36,
    major_label_font_size=32,
    legend_font_size=40,
    value_font_size=28,
    stroke_width=3,
    opacity=0.9,
)

# Create XY chart to simulate network graph
chart = pygal.XY(
    style=custom_style,
    width=4800,
    height=2700,
    title="network-basic · pygal · pyplots.ai",
    x_title="",
    y_title="",
    show_legend=True,
    legend_at_bottom=True,
    legend_box_size=24,
    show_x_guides=False,
    show_y_guides=False,
    show_x_labels=False,
    show_y_labels=False,
    stroke=True,
    show_dots=True,
    dots_size=12,
    explicit_size=True,
    print_values=False,
    print_labels=False,
    range=(0, 10),
    xrange=(0, 10),
    margin=50,
)

# Draw all edges as a single series with None separators
edge_points = []
for source, target in edges:
    x1, y1 = positions[source]
    x2, y2 = positions[target]
    edge_points.append({"value": (x1, y1), "label": ""})
    edge_points.append({"value": (x2, y2), "label": ""})
    edge_points.append(None)  # Break the line

chart.add("Connections", edge_points, stroke=True, show_dots=False)

# Group names for legend
group_names = {0: "Team Alpha", 1: "Team Beta", 2: "Team Gamma", 3: "Team Delta"}

# Add nodes by group with labels
for group_id in range(4):
    group_nodes = [n for n in nodes if n["group"] == group_id]
    node_points = []
    for node in group_nodes:
        nid = node["id"]
        x, y = positions[nid]
        node_points.append({"value": (x, y), "label": node["label"]})
    # Size based on average degree of group
    avg_degree = sum(node_degrees[n["id"]] for n in group_nodes) / len(group_nodes)
    chart.add(group_names[group_id], node_points, stroke=False, dots_size=18 + int(avg_degree * 2))

# Render to files
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
