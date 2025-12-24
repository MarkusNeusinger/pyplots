"""pyplots.ai
hive-basic: Basic Hive Plot
Library: pygal | Python 3.13
Quality: pending | Created: 2025-12-24
"""

import math

import numpy as np
import pygal
from pygal.style import Style


# Set seed for reproducibility
np.random.seed(42)

# Data: Software module dependency network
# Nodes assigned to 3 axes by module type: Core (0), Utility (1), Interface (2)
nodes = [
    # Core modules (axis 0)
    {"id": 0, "label": "kernel", "axis": 0, "degree": 8},
    {"id": 1, "label": "config", "axis": 0, "degree": 6},
    {"id": 2, "label": "database", "axis": 0, "degree": 7},
    {"id": 3, "label": "auth", "axis": 0, "degree": 5},
    {"id": 4, "label": "cache", "axis": 0, "degree": 4},
    {"id": 5, "label": "logger", "axis": 0, "degree": 6},
    {"id": 6, "label": "events", "axis": 0, "degree": 5},
    # Utility modules (axis 1)
    {"id": 7, "label": "helpers", "axis": 1, "degree": 5},
    {"id": 8, "label": "validators", "axis": 1, "degree": 4},
    {"id": 9, "label": "formatters", "axis": 1, "degree": 3},
    {"id": 10, "label": "parsers", "axis": 1, "degree": 4},
    {"id": 11, "label": "converters", "axis": 1, "degree": 3},
    {"id": 12, "label": "crypto", "axis": 1, "degree": 4},
    {"id": 13, "label": "compress", "axis": 1, "degree": 2},
    # Interface modules (axis 2)
    {"id": 14, "label": "rest_api", "axis": 2, "degree": 6},
    {"id": 15, "label": "graphql", "axis": 2, "degree": 5},
    {"id": 16, "label": "websocket", "axis": 2, "degree": 4},
    {"id": 17, "label": "cli", "axis": 2, "degree": 3},
    {"id": 18, "label": "admin_ui", "axis": 2, "degree": 4},
    {"id": 19, "label": "public_ui", "axis": 2, "degree": 5},
]

# Edges: Dependencies between modules
edges = [
    # Core → Core
    (0, 1),
    (0, 2),
    (0, 3),
    (1, 4),
    (1, 5),
    (2, 4),
    (2, 5),
    (3, 6),
    # Core → Utility
    (0, 7),
    (1, 8),
    (2, 10),
    (3, 12),
    (4, 9),
    (5, 9),
    (6, 7),
    # Core → Interface
    (0, 14),
    (0, 15),
    (2, 14),
    (2, 15),
    (3, 14),
    (3, 16),
    (5, 17),
    # Utility → Utility
    (7, 8),
    (8, 10),
    (9, 11),
    (10, 11),
    (12, 13),
    # Utility → Interface
    (7, 14),
    (7, 19),
    (8, 14),
    (8, 15),
    (9, 17),
    (10, 15),
    (12, 16),
    # Interface → Interface
    (14, 18),
    (14, 19),
    (15, 19),
    (16, 18),
]

# Axis configuration (3 radial axes at 120 degrees apart)
n_axes = 3
axis_angles = [2 * math.pi * i / n_axes - math.pi / 2 for i in range(n_axes)]  # Start from top
axis_names = ["Core", "Utility", "Interface"]
axis_colors = ["#306998", "#FFD43B", "#4CAF50"]

# Calculate node positions along each axis
# Position along axis based on degree (higher degree = closer to center)
center_x, center_y = 5.0, 5.0
inner_radius = 1.2
outer_radius = 3.8

# Sort nodes by axis and degree for positioning
axis_nodes = {i: [] for i in range(n_axes)}
for node in nodes:
    axis_nodes[node["axis"]].append(node)

# Sort each axis by degree (descending) for inner-to-outer positioning
for axis_id in axis_nodes:
    axis_nodes[axis_id].sort(key=lambda n: -n["degree"])

# Calculate positions
node_positions = {}
for axis_id in range(n_axes):
    angle = axis_angles[axis_id]
    nodes_on_axis = axis_nodes[axis_id]
    n_nodes = len(nodes_on_axis)

    for i, node in enumerate(nodes_on_axis):
        # Distribute nodes along the axis from inner to outer based on sorted order
        if n_nodes > 1:
            t = i / (n_nodes - 1)
        else:
            t = 0.5
        radius = inner_radius + t * (outer_radius - inner_radius)
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        node_positions[node["id"]] = (x, y, axis_id)

# Custom style - axis lines, edges, then nodes
# Color order: 3 axis lines (gray), 1 edge series (gray), 3 node groups
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#CCCCCC", "#CCCCCC", "#CCCCCC", "#88888866") + tuple(axis_colors),
    title_font_size=72,
    label_font_size=40,
    major_label_font_size=36,
    legend_font_size=44,
    value_font_size=32,
    stroke_width=2,
    opacity=0.9,
    opacity_hover=1.0,
)

# Create XY chart
chart = pygal.XY(
    width=3600,
    height=3600,
    style=custom_style,
    title="hive-basic · pygal · pyplots.ai",
    show_legend=True,
    x_title="",
    y_title="",
    show_x_guides=False,
    show_y_guides=False,
    show_x_labels=False,
    show_y_labels=False,
    stroke=True,
    dots_size=20,
    legend_at_bottom=True,
    legend_at_bottom_columns=3,
    range=(0, 10),
    xrange=(0, 10),
    print_labels=False,
    print_values=False,
)

# Draw axis lines first (as visual guides)
for axis_id in range(n_axes):
    angle = axis_angles[axis_id]
    x1 = center_x + (inner_radius - 0.2) * math.cos(angle)
    y1 = center_y + (inner_radius - 0.2) * math.sin(angle)
    x2 = center_x + (outer_radius + 0.3) * math.cos(angle)
    y2 = center_y + (outer_radius + 0.3) * math.sin(angle)
    # Draw axis line (hidden from legend)
    chart.add(
        None,
        [(x1, y1), (x2, y2)],
        stroke=True,
        show_dots=False,
        fill=False,
        stroke_style={"width": 6, "linecap": "round"},
    )

# Draw edges as curved paths between nodes
# Using quadratic Bezier curves that bend around the center
edge_points = []
for src, tgt in edges:
    src_x, src_y, src_axis = node_positions[src]
    tgt_x, tgt_y, tgt_axis = node_positions[tgt]

    # Control point - pull toward center for curved edges
    # More curve for edges crossing different axes
    if src_axis == tgt_axis:
        # Same axis - slight curve
        pull = 0.7
    else:
        # Different axes - curve through center area
        pull = 0.4

    ctrl_x = center_x + pull * ((src_x + tgt_x) / 2 - center_x)
    ctrl_y = center_y + pull * ((src_y + tgt_y) / 2 - center_y)

    # Generate Bezier curve points
    n_points = 30
    for t_idx in range(n_points + 1):
        t = t_idx / n_points
        bx = (1 - t) ** 2 * src_x + 2 * (1 - t) * t * ctrl_x + t**2 * tgt_x
        by = (1 - t) ** 2 * src_y + 2 * (1 - t) * t * ctrl_y + t**2 * tgt_y
        edge_points.append((bx, by))
    edge_points.append(None)  # Break between edges

# Add all edges as one series
chart.add(None, edge_points, stroke=True, show_dots=False, fill=False, stroke_style={"width": 1.5, "linecap": "round"})

# Add nodes grouped by axis for legend
for axis_id in range(n_axes):
    nodes_on_axis = axis_nodes[axis_id]
    node_points = []
    for node in nodes_on_axis:
        x, y, _ = node_positions[node["id"]]
        # Include module name in tooltip
        node_points.append({"value": (x, y), "label": f"{node['label']} (degree: {node['degree']})"})
    chart.add(f"{axis_names[axis_id]} Modules", node_points, stroke=False)

# Save outputs
chart.render_to_file("plot.svg")
chart.render_to_png("plot.png")

# Save HTML for interactive version
with open("plot.html", "w") as f:
    f.write(
        """<!DOCTYPE html>
<html>
<head>
    <title>hive-basic · pygal · pyplots.ai</title>
    <style>
        body { margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 100%; margin: 0 auto; }
        object { width: 100%; height: auto; }
    </style>
</head>
<body>
    <div class="container">
        <object type="image/svg+xml" data="plot.svg">
            Hive plot not supported
        </object>
    </div>
</body>
</html>"""
    )
