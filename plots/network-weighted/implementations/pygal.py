"""pyplots.ai
network-weighted: Weighted Network Graph with Edge Thickness
Library: pygal | Python 3.13
Quality: pending | Created: 2026-01-09
"""

import numpy as np
import pygal
from pygal.style import Style


# Set seed for reproducibility
np.random.seed(42)

# Data: Research collaboration network (co-authored papers)
nodes = [
    {"id": 0, "label": "MIT", "group": 0},
    {"id": 1, "label": "Stanford", "group": 0},
    {"id": 2, "label": "Berkeley", "group": 0},
    {"id": 3, "label": "Harvard", "group": 0},
    {"id": 4, "label": "Caltech", "group": 0},
    {"id": 5, "label": "Oxford", "group": 1},
    {"id": 6, "label": "Cambridge", "group": 1},
    {"id": 7, "label": "ETH Zurich", "group": 1},
    {"id": 8, "label": "Imperial", "group": 1},
    {"id": 9, "label": "Tokyo", "group": 2},
    {"id": 10, "label": "Tsinghua", "group": 2},
    {"id": 11, "label": "NUS", "group": 2},
    {"id": 12, "label": "Seoul Nat'l", "group": 2},
]

# Edges with weights (source, target, co-authored papers count)
edges = [
    # Strong US collaborations
    (0, 1, 85),  # MIT-Stanford
    (0, 3, 78),  # MIT-Harvard
    (1, 2, 72),  # Stanford-Berkeley
    (1, 4, 45),  # Stanford-Caltech
    (2, 4, 38),  # Berkeley-Caltech
    (0, 2, 55),  # MIT-Berkeley
    (3, 4, 32),  # Harvard-Caltech
    # Strong UK collaborations
    (5, 6, 92),  # Oxford-Cambridge
    (5, 8, 48),  # Oxford-Imperial
    (6, 8, 42),  # Cambridge-Imperial
    (7, 5, 35),  # ETH-Oxford
    (7, 6, 40),  # ETH-Cambridge
    # Asia collaborations
    (9, 10, 55),  # Tokyo-Tsinghua
    (10, 11, 38),  # Tsinghua-NUS
    (10, 12, 42),  # Tsinghua-Seoul
    (11, 12, 28),  # NUS-Seoul
    (9, 12, 35),  # Tokyo-Seoul
    # Cross-regional bridges
    (0, 5, 65),  # MIT-Oxford
    (1, 6, 58),  # Stanford-Cambridge
    (0, 9, 42),  # MIT-Tokyo
    (1, 10, 38),  # Stanford-Tsinghua
    (6, 9, 30),  # Cambridge-Tokyo
    (5, 10, 28),  # Oxford-Tsinghua
    (7, 9, 25),  # ETH-Tokyo
]

# Calculate weighted degree for node sizing
weighted_degrees = {node["id"]: 0 for node in nodes}
for src, tgt, weight in edges:
    weighted_degrees[src] += weight
    weighted_degrees[tgt] += weight

# Force-directed layout
n = len(nodes)
group_centers = {0: (-0.6, 0.3), 1: (0.0, -0.5), 2: (0.6, 0.3)}
positions = np.zeros((n, 2))
for i, node in enumerate(nodes):
    cx, cy = group_centers[node["group"]]
    positions[i] = [cx + np.random.rand() * 0.4 - 0.2, cy + np.random.rand() * 0.4 - 0.2]

k = 0.4

for iteration in range(250):
    displacement = np.zeros((n, 2))

    # Repulsive forces
    for i in range(n):
        for j in range(i + 1, n):
            diff = positions[i] - positions[j]
            dist = max(np.linalg.norm(diff), 0.01)
            force = (k * k / dist) * (diff / dist)
            displacement[i] += force
            displacement[j] -= force

    # Attractive forces (weighted)
    max_weight = max(w for _, _, w in edges)
    for src, tgt, weight in edges:
        diff = positions[src] - positions[tgt]
        dist = max(np.linalg.norm(diff), 0.01)
        weight_factor = 0.5 + 0.5 * (weight / max_weight)
        force = (dist * dist / k) * (diff / dist) * weight_factor
        displacement[src] -= force
        displacement[tgt] += force

    cooling = 1 - iteration / 250
    for i in range(n):
        disp_norm = np.linalg.norm(displacement[i])
        if disp_norm > 0:
            positions[i] += (displacement[i] / disp_norm) * min(disp_norm, 0.08 * cooling)

# Normalize positions
pos_min = positions.min(axis=0)
pos_max = positions.max(axis=0)
positions = (positions - pos_min) / (pos_max - pos_min + 1e-6)
positions[:, 0] = positions[:, 0] * 7 + 2.5  # X: [2.5, 9.5]
positions[:, 1] = positions[:, 1] * 5 + 2.5  # Y: [2.5, 7.5]
pos = {node["id"]: positions[i] for i, node in enumerate(nodes)}

# Region colors and names
region_names = ["US Universities", "European Universities", "Asian Universities"]

# Edge weight categories with visual styling
# num_lines creates parallel lines to simulate edge thickness
weight_categories = [("Light (< 35)", 0, 35, 1), ("Medium (35-60)", 35, 60, 2), ("Strong (> 60)", 60, float("inf"), 4)]

# Custom style for large canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#222222",
    foreground_subtle="#555555",
    colors=("#AAAAAA", "#666666", "#222222", "#306998", "#4CAF50", "#FFD43B"),
    title_font_size=64,
    label_font_size=36,
    major_label_font_size=32,
    legend_font_size=32,
    value_font_size=24,
    stroke_width=3,
    opacity=0.9,
    opacity_hover=1.0,
)

# Create XY chart for network
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="Research Collaborations · network-weighted · pygal · pyplots.ai",
    show_legend=True,
    show_x_guides=False,
    show_y_guides=False,
    show_x_labels=False,
    show_y_labels=False,
    x_title="",
    y_title="",
    stroke=True,
    dots_size=40,
    legend_at_bottom=True,
    legend_at_bottom_columns=6,
    range=(1, 9),
    xrange=(1, 11),
    print_labels=False,
    print_values=False,
    explicit_size=True,
)

# Draw edges grouped by weight category with parallel lines for thickness
for cat_name, min_w, max_w, num_lines in weight_categories:
    edge_points = []
    for src, tgt, weight in edges:
        if min_w <= weight < max_w:
            x1, y1 = pos[src]
            x2, y2 = pos[tgt]
            if num_lines == 1:
                edge_points.append((x1, y1))
                edge_points.append((x2, y2))
                edge_points.append(None)
            else:
                # Create parallel lines for thickness effect
                dx, dy = x2 - x1, y2 - y1
                length = np.sqrt(dx * dx + dy * dy) + 1e-6
                perp_x, perp_y = -dy / length, dx / length
                spacing = 0.06
                for i in range(num_lines):
                    offset = (i - (num_lines - 1) / 2) * spacing
                    ox, oy = perp_x * offset, perp_y * offset
                    edge_points.append((x1 + ox, y1 + oy))
                    edge_points.append((x2 + ox, y2 + oy))
                    edge_points.append(None)
    if edge_points:
        chart.add(cat_name, edge_points, stroke=True, show_dots=False, fill=False)

# Add nodes by region
for region_idx, region_name in enumerate(region_names):
    region_nodes = [node for node in nodes if node["group"] == region_idx]
    node_data = []
    for node in region_nodes:
        x, y = pos[node["id"]]
        wd = weighted_degrees[node["id"]]
        tooltip = f"{node['label']}: {wd} collaborations"
        node_data.append({"value": (x, y), "label": tooltip})
    chart.add(region_name, node_data, stroke=False, dots_size=50)

# Save outputs
chart.render_to_file("plot.svg")
chart.render_to_png("plot.png")

# Save interactive HTML
with open("plot.html", "w") as f:
    f.write(
        """<!DOCTYPE html>
<html>
<head>
    <title>network-weighted · pygal · pyplots.ai</title>
    <style>
        body { margin: 0; padding: 20px; background: #f5f5f5; font-family: sans-serif; }
        .container { max-width: 100%; margin: 0 auto; }
        object { width: 100%; height: auto; }
        h1 { text-align: center; color: #333; font-size: 1.5em; margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Research Collaboration Network (Weighted by Co-authored Papers)</h1>
        <object type="image/svg+xml" data="plot.svg">
            Weighted network graph visualization
        </object>
    </div>
</body>
</html>"""
    )
