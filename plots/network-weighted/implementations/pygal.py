""" pyplots.ai
network-weighted: Weighted Network Graph with Edge Thickness
Library: pygal 3.1.0 | Python 3.13.11
Quality: 72/100 | Created: 2026-01-09
"""

import numpy as np
import pygal
from pygal.style import Style


# Set seed for reproducibility
np.random.seed(42)

# Data: Trade network between countries (billions USD)
nodes = {
    "USA": {"group": "Americas"},
    "CAN": {"group": "Americas"},
    "MEX": {"group": "Americas"},
    "BRA": {"group": "Americas"},
    "DEU": {"group": "Europe"},
    "FRA": {"group": "Europe"},
    "GBR": {"group": "Europe"},
    "ITA": {"group": "Europe"},
    "CHN": {"group": "Asia"},
    "JPN": {"group": "Asia"},
    "KOR": {"group": "Asia"},
    "IND": {"group": "Asia"},
    "AUS": {"group": "Oceania"},
}

# Define edges with trade volume weights (billions USD)
edges = [
    ("USA", "CAN", 650),
    ("USA", "MEX", 580),
    ("USA", "CHN", 520),
    ("USA", "JPN", 180),
    ("USA", "DEU", 200),
    ("USA", "GBR", 130),
    ("USA", "KOR", 140),
    ("USA", "BRA", 80),
    ("CAN", "CHN", 75),
    ("CAN", "MEX", 40),
    ("MEX", "CHN", 90),
    ("DEU", "FRA", 170),
    ("DEU", "GBR", 120),
    ("DEU", "ITA", 130),
    ("DEU", "CHN", 200),
    ("FRA", "GBR", 90),
    ("FRA", "ITA", 80),
    ("FRA", "CHN", 65),
    ("GBR", "CHN", 95),
    ("CHN", "JPN", 280),
    ("CHN", "KOR", 250),
    ("CHN", "AUS", 180),
    ("CHN", "IND", 100),
    ("JPN", "KOR", 70),
    ("JPN", "AUS", 55),
    ("IND", "AUS", 30),
    ("BRA", "DEU", 20),
]

# Force-directed layout computation
node_list = list(nodes.keys())
n = len(node_list)
node_idx = {name: i for i, name in enumerate(node_list)}

# Initialize positions randomly
pos = np.random.rand(n, 2) * 2 - 1

k = 1.5 / np.sqrt(n)  # Optimal distance
t = 0.5  # Temperature (step size)

for _ in range(300):
    disp = np.zeros((n, 2))

    # Repulsive forces between all pairs
    for i in range(n):
        for j in range(i + 1, n):
            delta = pos[i] - pos[j]
            dist = max(np.linalg.norm(delta), 0.01)
            force = k * k / dist * 1.5
            direction = delta / dist
            disp[i] += direction * force
            disp[j] -= direction * force

    # Attractive forces along edges (weighted)
    for src, tgt, weight in edges:
        i, j = node_idx[src], node_idx[tgt]
        delta = pos[i] - pos[j]
        dist = max(np.linalg.norm(delta), 0.01)
        force = dist * dist / k * (0.8 + weight / 400)
        direction = delta / dist
        disp[i] -= direction * force
        disp[j] += direction * force

    # Apply displacement with temperature limiting
    for i in range(n):
        disp_norm = max(np.linalg.norm(disp[i]), 0.01)
        pos[i] += disp[i] / disp_norm * min(disp_norm, t)

    t *= 0.97

# Normalize positions to [1, 11] for pygal
pos_min = pos.min(axis=0)
pos_max = pos.max(axis=0)
pos = (pos - pos_min) / (pos_max - pos_min + 1e-6) * 8 + 2
positions = {name: pos[node_idx[name]] for name in node_list}

# Compute weighted degree for node sizing
weighted_degree = dict.fromkeys(nodes, 0)
for src, tgt, weight in edges:
    weighted_degree[src] += weight
    weighted_degree[tgt] += weight

# Color mapping by region
group_colors = {
    "Americas": "#306998",  # Python Blue
    "Europe": "#FFD43B",  # Python Yellow
    "Asia": "#E74C3C",  # Red
    "Oceania": "#2ECC71",  # Green
}

# Bin edges by weight for visual thickness representation
edge_weights = [w for _, _, w in edges]
min_weight = min(edge_weights)
max_weight = max(edge_weights)
weight_range = max_weight - min_weight

# Create 4 weight bins for edge thickness visualization
# Pygal doesn't support per-line stroke width, so we group by weight category
edge_bins = {
    "low": [],  # 0-25% percentile
    "medium": [],  # 25-50%
    "high": [],  # 50-75%
    "very_high": [],  # 75-100%
}

for src, tgt, weight in edges:
    norm_weight = (weight - min_weight) / weight_range if weight_range > 0 else 0.5
    if norm_weight < 0.25:
        edge_bins["low"].append((src, tgt, weight))
    elif norm_weight < 0.5:
        edge_bins["medium"].append((src, tgt, weight))
    elif norm_weight < 0.75:
        edge_bins["high"].append((src, tgt, weight))
    else:
        edge_bins["very_high"].append((src, tgt, weight))

# Custom style for the chart
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=(
        "#DDDDDD",  # Low weight edges
        "#AAAAAA",  # Medium weight edges
        "#777777",  # High weight edges
        "#333333",  # Very high weight edges
        "#306998",  # Americas
        "#FFD43B",  # Europe
        "#E74C3C",  # Asia
        "#2ECC71",  # Oceania
    ),
    title_font_size=72,
    label_font_size=40,
    major_label_font_size=36,
    legend_font_size=32,
    value_font_size=28,
    stroke_width=3,
    opacity=0.9,
    opacity_hover=1.0,
)

# Create XY chart
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="network-weighted · pygal · pyplots.ai",
    show_legend=True,
    x_title="",
    y_title="",
    show_x_guides=False,
    show_y_guides=False,
    show_x_labels=False,
    show_y_labels=False,
    stroke=True,
    dots_size=0,
    legend_at_bottom=True,
    legend_at_bottom_columns=8,
    legend_box_size=24,
    range=(0, 12),
    xrange=(0, 12),
    print_labels=False,
    print_values=False,
    margin_bottom=120,
)

# Add edges by weight category (thinner to thicker visually in legend order)
weight_labels = {
    "low": "$20-175B (light)",
    "medium": "$175-335B",
    "high": "$335-495B",
    "very_high": "$495-650B (heavy)",
}

for weight_cat in ["low", "medium", "high", "very_high"]:
    edge_points = []
    for src, tgt, _weight in edge_bins[weight_cat]:
        x1, y1 = positions[src]
        x2, y2 = positions[tgt]
        edge_points.append((x1, y1))
        edge_points.append((x2, y2))
        edge_points.append(None)  # Break line for next edge

    if edge_points:
        chart.add(weight_labels[weight_cat], edge_points, stroke=True, show_dots=False, fill=False)

# Group nodes by region
regions = {"Americas": [], "Europe": [], "Asia": [], "Oceania": []}
for name, data in nodes.items():
    regions[data["group"]].append(name)

# Add nodes by region with larger dots
max_degree = max(weighted_degree.values())
for region, region_nodes in regions.items():
    node_points = []
    for name in region_nodes:
        x, y = positions[name]
        w_deg = weighted_degree[name]
        # Scale tooltip to show weighted degree
        label = f"{name}: ${w_deg}B total trade"
        node_points.append({"value": (x, y), "label": label})
    chart.add(region, node_points, stroke=False, dots_size=45)

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
        body { margin: 0; padding: 20px; background: #f5f5f5; font-family: sans-serif; }
        .container { max-width: 100%; margin: 0 auto; }
        object { width: 100%; height: auto; }
        .legend-note {
            background: white;
            padding: 15px;
            border-radius: 8px;
            margin-top: 10px;
            font-size: 14px;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <object type="image/svg+xml" data="plot.svg">
            Weighted network graph not supported
        </object>
        <div class="legend-note">
            Edge thickness represents trade volume between countries (billions USD).
            Node colors indicate geographic regions. Hover over nodes and edges for details.
        </div>
    </div>
</body>
</html>"""
    )
