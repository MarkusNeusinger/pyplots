"""pyplots.ai
network-weighted: Weighted Network Graph with Edge Thickness
Library: pygal | Python 3.13
Quality: pending | Created: 2026-01-08
"""

import numpy as np
import pygal
from pygal.style import Style


# Set seed for reproducibility
np.random.seed(42)

# Data: Trade network between 15 countries (billions USD annual trade)
nodes = [
    {"id": 0, "label": "USA", "group": 0},
    {"id": 1, "label": "China", "group": 1},
    {"id": 2, "label": "Germany", "group": 2},
    {"id": 3, "label": "Japan", "group": 1},
    {"id": 4, "label": "UK", "group": 2},
    {"id": 5, "label": "France", "group": 2},
    {"id": 6, "label": "India", "group": 1},
    {"id": 7, "label": "Italy", "group": 2},
    {"id": 8, "label": "Brazil", "group": 0},
    {"id": 9, "label": "Canada", "group": 0},
    {"id": 10, "label": "S. Korea", "group": 1},
    {"id": 11, "label": "Mexico", "group": 0},
    {"id": 12, "label": "Spain", "group": 2},
    {"id": 13, "label": "Australia", "group": 1},
    {"id": 14, "label": "Netherlands", "group": 2},
]

# Edges with weights (source, target, weight in billions USD)
edges = [
    # Major trade partnerships (high volume)
    (0, 1, 650),  # USA-China
    (0, 9, 580),  # USA-Canada
    (0, 11, 520),  # USA-Mexico
    (0, 3, 280),  # USA-Japan
    (0, 2, 250),  # USA-Germany
    (1, 3, 340),  # China-Japan
    (1, 10, 300),  # China-S.Korea
    (1, 2, 220),  # China-Germany
    (1, 6, 180),  # China-India
    # European connections
    (2, 5, 190),  # Germany-France
    (2, 4, 170),  # Germany-UK
    (2, 14, 200),  # Germany-Netherlands
    (2, 7, 130),  # Germany-Italy
    (5, 4, 100),  # France-UK
    (5, 12, 80),  # France-Spain
    (7, 12, 60),  # Italy-Spain
    (4, 14, 90),  # UK-Netherlands
    # Pacific connections
    (3, 10, 110),  # Japan-S.Korea
    (3, 13, 70),  # Japan-Australia
    (10, 13, 50),  # S.Korea-Australia
    (6, 13, 40),  # India-Australia
    # Americas
    (0, 8, 100),  # USA-Brazil
    (9, 11, 50),  # Canada-Mexico
    (8, 11, 30),  # Brazil-Mexico
    # Cross-regional bridges
    (4, 6, 60),  # UK-India
    (0, 4, 130),  # USA-UK
    (1, 13, 180),  # China-Australia
]

# Calculate weighted degree for node sizing
weighted_degrees = {node["id"]: 0 for node in nodes}
for src, tgt, weight in edges:
    weighted_degrees[src] += weight
    weighted_degrees[tgt] += weight

# Force-directed layout with weight-influenced attraction
n = len(nodes)

# Initialize positions by region (Americas=0, Asia=1, Europe=2)
group_centers = {0: (-0.7, 0.0), 1: (0.7, 0.0), 2: (0.0, -0.6)}
positions = np.zeros((n, 2))
for i, node in enumerate(nodes):
    cx, cy = group_centers[node["group"]]
    positions[i] = [cx + np.random.rand() * 0.5 - 0.25, cy + np.random.rand() * 0.5 - 0.25]

k = 0.5  # Optimal distance parameter (larger = more spread out)

for iteration in range(300):
    displacement = np.zeros((n, 2))

    # Repulsive forces between all node pairs
    for i in range(n):
        for j in range(i + 1, n):
            diff = positions[i] - positions[j]
            dist = max(np.linalg.norm(diff), 0.01)
            force = (k * k / dist) * (diff / dist)
            displacement[i] += force
            displacement[j] -= force

    # Attractive forces for edges (weighted - stronger pull for higher weights)
    max_weight = max(w for _, _, w in edges)
    for src, tgt, weight in edges:
        diff = positions[src] - positions[tgt]
        dist = max(np.linalg.norm(diff), 0.01)
        # Scale attraction by weight (normalized)
        weight_factor = 0.5 + 0.5 * (weight / max_weight)
        force = (dist * dist / k) * (diff / dist) * weight_factor
        displacement[src] -= force
        displacement[tgt] += force

    # Apply displacement with cooling
    cooling = 1 - iteration / 300
    for i in range(n):
        disp_norm = np.linalg.norm(displacement[i])
        if disp_norm > 0:
            positions[i] += (displacement[i] / disp_norm) * min(disp_norm, 0.1 * cooling)

# Normalize positions to centered range for pygal
pos_min = positions.min(axis=0)
pos_max = positions.max(axis=0)
positions = (positions - pos_min) / (pos_max - pos_min + 1e-6)
positions[:, 0] = positions[:, 0] * 8 + 2  # X: [2, 10]
positions[:, 1] = positions[:, 1] * 6 + 3  # Y: [3, 9]
pos = {node["id"]: positions[i] for i, node in enumerate(nodes)}

# Region colors
region_colors = ["#306998", "#FFD43B", "#4CAF50"]  # Americas, Asia, Europe
region_names = ["Americas", "Asia", "Europe"]

# Categorize edges by weight for different visual thickness
# Pygal doesn't support per-edge styling, so we create separate series
# Using more parallel lines for thicker visual representation
weight_categories = [
    ("Light (< 100B)", 0, 100, "#BBBBBB", 1),
    ("Medium (100-300B)", 100, 300, "#777777", 3),
    ("Heavy (> 300B)", 300, float("inf"), "#333333", 6),
]

# Custom style
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#BBBBBB", "#777777", "#333333", "#306998", "#FFD43B", "#4CAF50"),
    title_font_size=72,
    label_font_size=40,
    major_label_font_size=36,
    legend_font_size=36,
    value_font_size=28,
    stroke_width=2,
    opacity=0.9,
    opacity_hover=1.0,
)

# Create XY chart
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="Trade Network (Billions USD) · network-weighted · pygal · pyplots.ai",
    show_legend=True,
    x_title="",
    y_title="",
    show_x_guides=False,
    show_y_guides=False,
    show_x_labels=False,
    show_y_labels=False,
    stroke=True,
    dots_size=35,
    stroke_style={"width": 2, "linecap": "round"},
    legend_at_bottom=True,
    legend_at_bottom_columns=6,
    range=(0, 12),
    xrange=(0, 12),
    print_labels=False,
    print_values=False,
)

# Add edges by weight category (creates visual thickness variation)
for cat_name, min_w, max_w, _color, thickness in weight_categories:
    edge_points = []
    for src, tgt, weight in edges:
        if min_w <= weight < max_w:
            x1, y1 = pos[src]
            x2, y2 = pos[tgt]
            # For thicker lines, add multiple parallel traces
            if thickness > 1:
                # Create slightly offset parallel lines to simulate thickness
                dx, dy = x2 - x1, y2 - y1
                length = np.sqrt(dx * dx + dy * dy) + 1e-6
                # Perpendicular offset
                offset_x = -dy / length * 0.03 * thickness
                offset_y = dx / length * 0.03 * thickness
                for i in range(thickness):
                    off = (i - thickness / 2) * 0.5
                    edge_points.append((x1 + offset_x * off, y1 + offset_y * off))
                    edge_points.append((x2 + offset_x * off, y2 + offset_y * off))
                    edge_points.append(None)
            else:
                edge_points.append((x1, y1))
                edge_points.append((x2, y2))
                edge_points.append(None)
    if edge_points:
        chart.add(cat_name, edge_points, stroke=True, show_dots=False, fill=False)

# Add nodes grouped by region
for region_idx, region_name in enumerate(region_names):
    region_nodes = [node for node in nodes if node["group"] == region_idx]
    node_points = []
    for node in region_nodes:
        x, y = pos[node["id"]]
        wd = weighted_degrees[node["id"]]
        label = f"{node['label']}: ${wd}B total trade"
        node_points.append({"value": (x, y), "label": label})
    chart.add(region_name, node_points, stroke=False)

# Save outputs
chart.render_to_file("plot.svg")
chart.render_to_png("plot.png")

# Save HTML for interactive version
with open("plot.html", "w") as f:
    f.write(
        """<!DOCTYPE html>
<html>
<head>
    <title>network-weighted · pygal · pyplots.ai</title>
    <style>
        body { margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 100%; margin: 0 auto; }
        object { width: 100%; height: auto; }
    </style>
</head>
<body>
    <div class="container">
        <object type="image/svg+xml" data="plot.svg">
            Weighted network graph not supported
        </object>
    </div>
</body>
</html>"""
    )
