""" pyplots.ai
network-directed: Directed Network Graph
Library: altair 6.0.0 | Python 3.13.11
Quality: 87/100 | Created: 2025-12-30
"""

import altair as alt
import numpy as np
import pandas as pd


np.random.seed(42)

# Data: Software package dependency graph
nodes = [
    {"id": "app", "label": "App", "group": "main"},
    {"id": "api", "label": "API", "group": "core"},
    {"id": "auth", "label": "Auth", "group": "core"},
    {"id": "database", "label": "Database", "group": "core"},
    {"id": "cache", "label": "Cache", "group": "service"},
    {"id": "logger", "label": "Logger", "group": "util"},
    {"id": "config", "label": "Config", "group": "util"},
    {"id": "utils", "label": "Utils", "group": "util"},
    {"id": "models", "label": "Models", "group": "data"},
    {"id": "schemas", "label": "Schemas", "group": "data"},
    {"id": "router", "label": "Router", "group": "core"},
    {"id": "middleware", "label": "Middleware", "group": "core"},
]

# Directed edges: (source, target) - arrows point from source to target
edges = [
    ("app", "api"),
    ("app", "auth"),
    ("app", "router"),
    ("api", "database"),
    ("api", "cache"),
    ("api", "models"),
    ("auth", "database"),
    ("auth", "cache"),
    ("auth", "logger"),
    ("database", "config"),
    ("database", "logger"),
    ("cache", "config"),
    ("cache", "logger"),
    ("router", "middleware"),
    ("router", "api"),
    ("middleware", "auth"),
    ("middleware", "logger"),
    ("models", "schemas"),
    ("models", "utils"),
    ("schemas", "utils"),
    ("logger", "config"),
    ("utils", "config"),
]

# Node positions using hierarchical layout based on dependency depth
# Calculate depth for each node (topological sort-like approach)
depths = {"app": 0}
for _ in range(len(nodes)):
    for source, target in edges:
        if source in depths:
            current_depth = depths.get(target, -1)
            depths[target] = max(current_depth, depths[source] + 1)

# Assign default depth for any disconnected nodes
for node in nodes:
    if node["id"] not in depths:
        depths[node["id"]] = 0

# Group nodes by depth for horizontal positioning
depth_groups = {}
for node_id, depth in depths.items():
    if depth not in depth_groups:
        depth_groups[depth] = []
    depth_groups[depth].append(node_id)

# Calculate positions
positions = {}
max_depth = max(depths.values()) if depths else 0
for depth, node_ids in depth_groups.items():
    n_nodes = len(node_ids)
    for i, node_id in enumerate(node_ids):
        x = depth / max(max_depth, 1)  # Normalize x to [0, 1]
        y = (i + 0.5) / n_nodes  # Distribute vertically
        positions[node_id] = (x, y)

# Create node DataFrame
node_df = pd.DataFrame(
    [
        {
            "id": n["id"],
            "label": n["label"],
            "group": n["group"],
            "x": positions[n["id"]][0],
            "y": positions[n["id"]][1],
        }
        for n in nodes
    ]
)

# Create edge DataFrame with arrow coordinates
edge_data = []
for source, target in edges:
    sx, sy = positions[source]
    tx, ty = positions[target]

    # Shorten edge slightly so arrows don't overlap nodes
    dx, dy = tx - sx, ty - sy
    length = np.sqrt(dx**2 + dy**2)
    if length > 0:
        # Move endpoints slightly inward
        offset = 0.03
        sx_adj = sx + dx / length * offset
        sy_adj = sy + dy / length * offset
        tx_adj = tx - dx / length * offset
        ty_adj = ty - dy / length * offset
    else:
        sx_adj, sy_adj = sx, sy
        tx_adj, ty_adj = tx, ty

    edge_data.append({"source": source, "target": target, "x": sx_adj, "y": sy_adj, "x2": tx_adj, "y2": ty_adj})

edge_df = pd.DataFrame(edge_data)

# Create arrow head data (triangular markers at edge endpoints)
arrow_data = []
for source, target in edges:
    sx, sy = positions[source]
    tx, ty = positions[target]

    dx, dy = tx - sx, ty - sy
    length = np.sqrt(dx**2 + dy**2)
    if length > 0:
        # Arrow tip position (slightly before target node)
        offset = 0.04
        ax = tx - dx / length * offset
        ay = ty - dy / length * offset

        # Calculate arrow direction angle
        angle = np.degrees(np.arctan2(dy, dx))

        arrow_data.append({"x": ax, "y": ay, "angle": angle})

arrow_df = pd.DataFrame(arrow_data)

# Color palette for groups
group_colors = {
    "main": "#306998",  # Python Blue
    "core": "#FFD43B",  # Python Yellow
    "service": "#4ECDC4",
    "util": "#95A5A6",
    "data": "#E74C3C",
}

# Add colors to node dataframe
node_df["color"] = node_df["group"].map(group_colors)

# Create the visualization
# Edges as rules (lines)
edges_chart = (
    alt.Chart(edge_df)
    .mark_rule(strokeWidth=2, opacity=0.6, color="#666666")
    .encode(
        x=alt.X("x:Q", scale=alt.Scale(domain=[-0.1, 1.1]), axis=None),
        y=alt.Y("y:Q", scale=alt.Scale(domain=[-0.05, 1.05]), axis=None),
        x2="x2:Q",
        y2="y2:Q",
    )
)

# Arrow heads as triangular points
arrows_chart = (
    alt.Chart(arrow_df)
    .mark_point(shape="triangle", size=150, filled=True, color="#666666", opacity=0.8)
    .encode(
        x=alt.X("x:Q", scale=alt.Scale(domain=[-0.1, 1.1])),
        y=alt.Y("y:Q", scale=alt.Scale(domain=[-0.05, 1.05])),
        angle=alt.Angle("angle:Q"),
    )
)

# Nodes as circles
nodes_chart = (
    alt.Chart(node_df)
    .mark_circle(size=800, stroke="#ffffff", strokeWidth=2)
    .encode(
        x=alt.X("x:Q", scale=alt.Scale(domain=[-0.1, 1.1])),
        y=alt.Y("y:Q", scale=alt.Scale(domain=[-0.05, 1.05])),
        color=alt.Color(
            "group:N",
            scale=alt.Scale(domain=list(group_colors.keys()), range=list(group_colors.values())),
            legend=alt.Legend(title="Module Type", titleFontSize=18, labelFontSize=16, orient="right"),
        ),
        tooltip=["label:N", "group:N"],
    )
)

# Node labels
labels_chart = (
    alt.Chart(node_df)
    .mark_text(fontSize=14, fontWeight="bold", dy=-25)
    .encode(
        x=alt.X("x:Q", scale=alt.Scale(domain=[-0.1, 1.1])),
        y=alt.Y("y:Q", scale=alt.Scale(domain=[-0.05, 1.05])),
        text="label:N",
    )
)

# Combine all layers
chart = (
    (edges_chart + arrows_chart + nodes_chart + labels_chart)
    .properties(
        width=1600,
        height=900,
        title=alt.Title(
            text="network-directed · altair · pyplots.ai",
            subtitle="Software Package Dependencies",
            fontSize=28,
            subtitleFontSize=18,
            anchor="middle",
        ),
    )
    .configure_view(strokeWidth=0)
)

# Save as PNG and HTML
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
