""" pyplots.ai
network-basic: Basic Network Graph
Library: bokeh 3.8.1 | Python 3.13.11
Quality: 94/100 | Created: 2025-12-17
"""

import numpy as np
from bokeh.io import export_png, output_file, save
from bokeh.models import ColumnDataSource, HoverTool, Legend, LegendItem
from bokeh.plotting import figure


# Set seed for reproducibility
np.random.seed(42)

# Data: A small social network with 20 people in 4 communities
nodes = [
    {"id": 0, "label": "Alice", "group": 0},
    {"id": 1, "label": "Bob", "group": 0},
    {"id": 2, "label": "Carol", "group": 0},
    {"id": 3, "label": "David", "group": 0},
    {"id": 4, "label": "Eve", "group": 0},
    {"id": 5, "label": "Frank", "group": 1},
    {"id": 6, "label": "Grace", "group": 1},
    {"id": 7, "label": "Henry", "group": 1},
    {"id": 8, "label": "Ivy", "group": 1},
    {"id": 9, "label": "Jack", "group": 1},
    {"id": 10, "label": "Kate", "group": 2},
    {"id": 11, "label": "Leo", "group": 2},
    {"id": 12, "label": "Mia", "group": 2},
    {"id": 13, "label": "Noah", "group": 2},
    {"id": 14, "label": "Olivia", "group": 2},
    {"id": 15, "label": "Paul", "group": 3},
    {"id": 16, "label": "Quinn", "group": 3},
    {"id": 17, "label": "Ryan", "group": 3},
    {"id": 18, "label": "Sara", "group": 3},
    {"id": 19, "label": "Tom", "group": 3},
]

# Edges: Friendship connections (within and between groups)
edges = [
    # Group 0 internal connections
    (0, 1),
    (0, 2),
    (1, 2),
    (1, 3),
    (2, 4),
    (3, 4),
    # Group 1 internal connections
    (5, 6),
    (5, 7),
    (6, 8),
    (7, 8),
    (7, 9),
    (8, 9),
    # Group 2 internal connections
    (10, 11),
    (10, 12),
    (11, 13),
    (12, 13),
    (12, 14),
    (13, 14),
    # Group 3 internal connections
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

# Colors for groups
group_colors = ["#306998", "#FFD43B", "#4CAF50", "#FF7043"]
group_names = ["Group A", "Group B", "Group C", "Group D"]

# Create figure
p = figure(
    width=4800,
    height=2700,
    title="Social Network · network-basic · bokeh · pyplots.ai",
    x_range=(-0.05, 1.05),
    y_range=(-0.05, 1.05),
    tools="pan,wheel_zoom,box_zoom,reset,save",
)

# Style title and hide axes
p.title.text_font_size = "28pt"
p.title.align = "center"
p.axis.visible = False
p.grid.visible = False
p.outline_line_color = None

# Draw edges
for src, tgt in edges:
    x0, y0 = pos[src]
    x1, y1 = pos[tgt]
    p.line([x0, x1], [y0, y1], line_width=4, line_color="#888888", line_alpha=0.5)

# Draw nodes by group (for legend)
legend_items = []
for group_id, (color, name) in enumerate(zip(group_colors, group_names, strict=True)):
    group_nodes = [node for node in nodes if node["group"] == group_id]
    node_x = [pos[node["id"]][0] for node in group_nodes]
    node_y = [pos[node["id"]][1] for node in group_nodes]
    node_sizes = [45 + degrees[node["id"]] * 10 for node in group_nodes]
    node_labels = [node["label"] for node in group_nodes]
    node_degrees = [degrees[node["id"]] for node in group_nodes]

    source = ColumnDataSource(
        data={"x": node_x, "y": node_y, "size": node_sizes, "label": node_labels, "connections": node_degrees}
    )

    renderer = p.scatter(
        x="x", y="y", size="size", source=source, fill_color=color, line_color="#333333", line_width=2, fill_alpha=0.9
    )
    legend_items.append(LegendItem(label=name, renderers=[renderer]))

# Add node labels
for node in nodes:
    x, y = pos[node["id"]]
    p.text(
        x=[x],
        y=[y],
        text=[node["label"]],
        text_font_size="18pt",
        text_font_style="bold",
        text_color="#222222",
        text_align="center",
        text_baseline="middle",
    )

# Add hover tool
hover = HoverTool(
    tooltips=[("Name", "@label"), ("Connections", "@connections")],
    renderers=[r for item in legend_items for r in item.renderers],
)
p.add_tools(hover)

# Add legend
legend = Legend(items=legend_items, location="top_left", title="Communities", title_text_font_size="20pt")
legend.label_text_font_size = "16pt"
legend.background_fill_alpha = 0.9
p.add_layout(legend, "left")

# Save outputs
export_png(p, filename="plot.png")
output_file("plot.html")
save(p)
