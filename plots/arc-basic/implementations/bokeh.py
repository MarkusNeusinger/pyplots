"""
arc-basic: Basic Arc Diagram
Library: bokeh
"""

import numpy as np
from bokeh.io import export_png, save
from bokeh.models import ColumnDataSource, Label
from bokeh.plotting import figure
from bokeh.resources import CDN


# Data - Character interactions from a story
nodes = ["Alice", "Bob", "Carol", "Dave", "Eve", "Frank", "Grace", "Heidi", "Ivan", "Judy"]

# Edges as pairs of node indices with varying distances
edges = [
    (0, 1),  # Alice-Bob (short range)
    (0, 3),  # Alice-Dave (medium range)
    (1, 2),  # Bob-Carol (short range)
    (2, 4),  # Carol-Eve (short range)
    (0, 7),  # Alice-Heidi (long range)
    (3, 5),  # Dave-Frank (short range)
    (4, 6),  # Eve-Grace (short range)
    (5, 8),  # Frank-Ivan (medium range)
    (6, 9),  # Grace-Judy (medium range)
    (1, 6),  # Bob-Grace (long range)
    (2, 8),  # Carol-Ivan (long range)
    (7, 9),  # Heidi-Judy (short range)
]

# Node positions along horizontal axis
np.random.seed(42)
node_x = list(range(len(nodes)))
node_y = [0] * len(nodes)

# Create figure
p = figure(
    width=4800,
    height=2700,
    title="arc-basic · bokeh · pyplots.ai",
    x_axis_label="",
    y_axis_label="",
    x_range=(-1, len(nodes)),
    y_range=(-0.8, 5.5),
    tools="",  # Remove toolbar
)

# Draw arcs for each edge
for start_idx, end_idx in edges:
    x1, x2 = node_x[start_idx], node_x[end_idx]
    # Arc height proportional to distance between nodes
    distance = abs(x2 - x1)
    height = distance * 0.5

    # Generate arc points using a semi-circle
    t = np.linspace(0, np.pi, 50)
    mid_x = (x1 + x2) / 2
    radius_x = abs(x2 - x1) / 2
    arc_x = mid_x + radius_x * np.cos(np.pi - t)
    arc_y = height * np.sin(t)

    # Color based on distance (longer = darker blue)
    alpha = 0.3 + 0.4 * (distance / (len(nodes) - 1))

    source = ColumnDataSource(data={"x": arc_x, "y": arc_y})
    p.line(x="x", y="y", source=source, line_width=3, line_color="#306998", line_alpha=alpha)

# Draw nodes
node_source = ColumnDataSource(data={"x": node_x, "y": node_y})
p.scatter(x="x", y="y", source=node_source, size=25, color="#FFD43B", line_color="#306998", line_width=3)

# Add node labels below the nodes
for i, name in enumerate(nodes):
    label = Label(
        x=node_x[i],
        y=-0.15,
        text=name,
        text_align="center",
        text_baseline="top",
        text_font_size="18pt",
        text_color="#333333",
    )
    p.add_layout(label)

# Draw baseline
p.line(x=[-0.5, len(nodes) - 0.5], y=[0, 0], line_width=2, line_color="#666666", line_alpha=0.5)

# Styling
p.title.text_font_size = "28pt"
p.xaxis.visible = False
p.yaxis.visible = False
p.xgrid.visible = False
p.ygrid.visible = False
p.outline_line_color = None
p.background_fill_color = "#ffffff"
p.border_fill_color = "#ffffff"

# Save
export_png(p, filename="plot.png")
save(p, filename="plot.html", resources=CDN, title="arc-basic · bokeh · pyplots.ai")
