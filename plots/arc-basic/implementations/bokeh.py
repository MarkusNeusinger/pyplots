"""
arc-basic: Basic Arc Diagram
Library: bokeh
"""

import numpy as np
from bokeh.io import export_png
from bokeh.models import ColumnDataSource, Label
from bokeh.plotting import figure, save


# Data - Character interactions in a story chapter
nodes = ["Alice", "Bob", "Carol", "David", "Eve", "Frank", "Grace", "Henry"]
# Edges as (source_idx, target_idx, weight) - character conversation connections
edges = [
    (0, 1, 3),  # Alice-Bob: frequent
    (0, 2, 2),  # Alice-Carol: moderate
    (1, 3, 1),  # Bob-David: brief
    (2, 4, 2),  # Carol-Eve: moderate
    (0, 5, 1),  # Alice-Frank: brief
    (3, 6, 2),  # David-Grace: moderate
    (4, 7, 1),  # Eve-Henry: brief
    (0, 7, 3),  # Alice-Henry: frequent (long-range)
    (1, 4, 2),  # Bob-Eve: moderate
    (2, 6, 1),  # Carol-Grace: brief
    (5, 7, 2),  # Frank-Henry: moderate
    (1, 2, 1),  # Bob-Carol: brief (short-range)
]

# Node positions along horizontal axis
n_nodes = len(nodes)
x_positions = np.linspace(0, 10, n_nodes)
y_baseline = 0

# Create figure
p = figure(
    width=4800,
    height=2700,
    title="arc-basic \u00b7 bokeh \u00b7 pyplots.ai",
    x_axis_label="Characters",
    y_axis_label="",
    x_range=(-0.5, 10.5),
    y_range=(-1.5, 6),
)

# Style the figure
p.title.text_font_size = "28pt"
p.xaxis.axis_label_text_font_size = "22pt"
p.yaxis.axis_label_text_font_size = "22pt"
p.xaxis.major_label_text_font_size = "18pt"
p.yaxis.major_label_text_font_size = "18pt"

# Hide y-axis (not meaningful for arc diagram)
p.yaxis.visible = False
p.ygrid.visible = False

# Draw arcs as bezier curves
for src_idx, tgt_idx, weight in edges:
    x_src = x_positions[src_idx]
    x_tgt = x_positions[tgt_idx]

    # Arc height proportional to distance between nodes
    distance = abs(x_tgt - x_src)
    arc_height = distance * 0.5

    # Generate arc points using quadratic bezier
    t = np.linspace(0, 1, 50)
    # Control point at midpoint, elevated by arc_height
    cx = (x_src + x_tgt) / 2
    cy = arc_height

    # Quadratic bezier: B(t) = (1-t)^2*P0 + 2*(1-t)*t*P1 + t^2*P2
    arc_x = (1 - t) ** 2 * x_src + 2 * (1 - t) * t * cx + t**2 * x_tgt
    arc_y = (1 - t) ** 2 * y_baseline + 2 * (1 - t) * t * cy + t**2 * y_baseline

    # Line width based on weight
    line_width = weight * 2

    # Color based on connection type (long-range vs short-range)
    if distance > 5:
        color = "#FFD43B"  # Python Yellow for long-range
        alpha = 0.7
    else:
        color = "#306998"  # Python Blue for short-range
        alpha = 0.5

    arc_source = ColumnDataSource(data={"x": arc_x, "y": arc_y})
    p.line(x="x", y="y", source=arc_source, line_width=line_width, line_color=color, line_alpha=alpha)

# Draw nodes along baseline
node_source = ColumnDataSource(data={"x": x_positions, "y": [y_baseline] * n_nodes, "name": nodes})
p.scatter(x="x", y="y", source=node_source, size=25, fill_color="#306998", line_color="white", line_width=2)

# Add node labels below the baseline
for i, name in enumerate(nodes):
    label = Label(x=x_positions[i], y=-0.5, text=name, text_font_size="16pt", text_align="center", text_baseline="top")
    p.add_layout(label)

# Add subtle grid only for x
p.xgrid.grid_line_alpha = 0.3
p.xgrid.grid_line_dash = [6, 4]

# Save outputs
export_png(p, filename="plot.png")
save(p, filename="plot.html", title="arc-basic")
