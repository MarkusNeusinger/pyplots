"""
arc-basic: Basic Arc Diagram
Library: pygal
"""

import math

import pygal
from pygal.style import Style


# Data - Character interactions in a story chapter
nodes = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry"]
edges = [
    (0, 1, 3),  # Alice-Bob (weight 3, close characters)
    (0, 3, 2),  # Alice-Diana
    (1, 2, 4),  # Bob-Charlie (strong connection)
    (2, 4, 2),  # Charlie-Eve
    (3, 5, 3),  # Diana-Frank
    (4, 6, 2),  # Eve-Grace
    (0, 7, 1),  # Alice-Henry (long-range, weak)
    (2, 6, 2),  # Charlie-Grace
    (1, 5, 1),  # Bob-Frank
    (5, 7, 3),  # Frank-Henry
]

# Custom style for 4800x2700 px canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#FFD43B", "#4B8BBE", "#FFE873", "#646464"),
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=48,
    legend_font_size=48,
    value_font_size=36,
    stroke_width=4,
    opacity=0.8,
    opacity_hover=0.95,
)

# Create XY chart for arc diagram
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="arc-basic · pygal · pyplots.ai",
    show_legend=True,
    x_title="Characters (Sequential Order)",
    y_title="Arc Height (Connection Distance)",
    show_x_guides=False,
    show_y_guides=True,
    dots_size=20,
    stroke_style={"width": 4},
    show_dots=True,
    fill=False,
    range=(0, 8),
    xrange=(-0.5, len(nodes) - 0.5),
    legend_at_bottom=True,
    legend_at_bottom_columns=5,
)


# Generate points for a semicircular arc between two node positions
def generate_arc_points(start_idx, end_idx, weight, num_points=40):
    x_start = start_idx
    x_end = end_idx
    x_mid = (x_start + x_end) / 2
    radius = abs(x_end - x_start) / 2
    # Height scales with both distance and weight
    height_scale = 0.8 + (weight * 0.2)

    points = []
    for i in range(num_points + 1):
        t = i / num_points
        angle = math.pi * t  # 0 to pi for top arc
        x = x_mid - radius * math.cos(angle)
        y = radius * height_scale * math.sin(angle)
        points.append((x, y))
    return points


# Group edges by weight for legend
weight_groups = {1: [], 2: [], 3: [], 4: []}
for start, end, weight in edges:
    weight_groups[weight].append((start, end))

# Add arcs grouped by weight
weight_labels = {1: "Weak (1)", 2: "Medium (2)", 3: "Strong (3)", 4: "Very Strong (4)"}
for weight, edge_list in weight_groups.items():
    if edge_list:
        for idx, (start, end) in enumerate(edge_list):
            arc_points = generate_arc_points(start, end, weight)
            label = weight_labels[weight] if idx == 0 else None
            chart.add(label, arc_points, show_dots=False, stroke_style={"width": 2 + weight})

# Add nodes on the baseline
node_points = [(i, 0) for i in range(len(nodes))]
chart.add("Nodes", node_points, dots_size=28, stroke=False)

# Set x-axis labels to node names
chart.x_labels = nodes

# Render to files
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
