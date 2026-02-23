""" pyplots.ai
arc-basic: Basic Arc Diagram
Library: pygal 3.1.0 | Python 3.14.3
Quality: 79/100 | Created: 2026-02-23
"""

import math

import numpy as np
import pygal
from pygal.style import Style


# Set seed for reproducibility
np.random.seed(42)

# Data: Character interactions in a story chapter
nodes = ["Alice", "Bob", "Carol", "David", "Eve", "Frank", "Grace", "Henry", "Iris", "Jack"]
n_nodes = len(nodes)

# Edges: pairs of connected nodes with weights (source, target, weight)
edges = [
    (0, 1, 3),  # Alice-Bob (strong connection)
    (0, 3, 2),  # Alice-David
    (1, 2, 2),  # Bob-Carol
    (2, 4, 1),  # Carol-Eve
    (3, 5, 2),  # David-Frank
    (4, 6, 1),  # Eve-Grace
    (0, 7, 1),  # Alice-Henry (long-range)
    (1, 5, 2),  # Bob-Frank
    (2, 3, 3),  # Carol-David (strong)
    (5, 8, 1),  # Frank-Iris
    (6, 9, 2),  # Grace-Jack
    (0, 9, 1),  # Alice-Jack (longest range)
    (3, 7, 2),  # David-Henry
    (7, 8, 1),  # Henry-Iris
    (8, 9, 2),  # Iris-Jack
]

# Node positions along x-axis (1 to 10 range)
x_positions = np.linspace(1, 10, n_nodes)
y_baseline = 0.5

# Color palette: weight-based blue shades for arcs (lighter=weak, darker=strong)
arc_blues = {1: "#7BA7C9", 2: "#306998", 3: "#1B3F5C"}

# Build colors tuple: one entry per edge series + node series
n_edges = len(edges)
colors = tuple([arc_blues[w] for _, _, w in edges] + ["#FFD43B"])

# Custom style
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#306998",
    foreground_subtle="#666666",
    colors=colors,
    title_font_size=72,
    label_font_size=40,
    major_label_font_size=40,
    legend_font_size=40,
    value_font_size=32,
    stroke_width=3,
    opacity=0.7,
    opacity_hover=1.0,
)

# Create XY chart
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="Character Interactions · arc-basic · pygal · pyplots.ai",
    show_legend=False,
    x_title="",
    y_title="",
    show_x_guides=False,
    show_y_guides=False,
    show_x_labels=True,
    show_y_labels=False,
    stroke=True,
    dots_size=0,
    stroke_style={"width": 3, "linecap": "round"},
    range=(0, 4.6),
    xrange=(0, 11),
    x_labels=[{"value": float(x_positions[i]), "label": nodes[i]} for i in range(n_nodes)],
    truncate_label=-1,
)

# Generate arc points for each edge
arc_resolution = 40

for start_idx, end_idx, weight in edges:
    x_start = x_positions[start_idx]
    x_end = x_positions[end_idx]

    # Arc center and radius
    x_center = (x_start + x_end) / 2
    arc_radius = abs(x_end - x_start) / 2

    # Arc height proportional to node distance
    distance = abs(end_idx - start_idx)
    height_scale = 0.4 * distance

    # Generate arc points (semi-circle above baseline)
    arc_points = []
    for i in range(arc_resolution + 1):
        theta = math.pi * i / arc_resolution
        x = x_center - arc_radius * math.cos(theta)
        y = y_baseline + height_scale * math.sin(theta)
        arc_points.append((x, y))

    chart.add(
        f"Arc {start_idx}-{end_idx}",
        arc_points,
        stroke=True,
        show_dots=False,
        fill=False,
        stroke_style={"width": 2 + weight * 2, "linecap": "round"},
    )

# Add nodes as a separate series (last, uses Python Yellow)
node_points = [{"value": (float(x_positions[i]), y_baseline), "label": nodes[i]} for i in range(n_nodes)]
chart.add("Characters", node_points, stroke=False, dots_size=35)

# Save outputs
chart.render_to_file("plot.svg")
chart.render_to_png("plot.png")

# Save HTML for interactive version
with open("plot.html", "w") as f:
    f.write(
        """<!DOCTYPE html>
<html>
<head>
    <title>Character Interactions · arc-basic · pygal · pyplots.ai</title>
    <style>
        body { margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 100%; margin: 0 auto; }
        object { width: 100%; height: auto; }
    </style>
</head>
<body>
    <div class="container">
        <object type="image/svg+xml" data="plot.svg">
            Arc diagram not supported
        </object>
    </div>
</body>
</html>"""
    )
