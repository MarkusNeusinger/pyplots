"""pyplots.ai
network-hierarchical: Hierarchical Network Graph with Tree Layout
Library: bokeh 3.8.2 | Python 3.13.11
Quality: 72/100 | Created: 2026-01-08
"""

import numpy as np
from bokeh.io import export_png
from bokeh.models import ColumnDataSource, HoverTool, LabelSet
from bokeh.plotting import figure


# Data: Software project team hierarchy (25 employees, 4 levels)
np.random.seed(42)

nodes = [
    # Level 0 - CEO
    {"id": 0, "label": "CEO", "level": 0},
    # Level 1 - VPs
    {"id": 1, "label": "VP Engineering", "level": 1},
    {"id": 2, "label": "VP Product", "level": 1},
    {"id": 3, "label": "VP Operations", "level": 1},
    # Level 2 - Directors/Managers
    {"id": 4, "label": "Frontend Dir.", "level": 2},
    {"id": 5, "label": "Backend Dir.", "level": 2},
    {"id": 6, "label": "PM Lead", "level": 2},
    {"id": 7, "label": "UX Lead", "level": 2},
    {"id": 8, "label": "IT Manager", "level": 2},
    {"id": 9, "label": "HR Manager", "level": 2},
    # Level 3 - Team Members
    {"id": 10, "label": "FE Dev 1", "level": 3},
    {"id": 11, "label": "FE Dev 2", "level": 3},
    {"id": 12, "label": "BE Dev 1", "level": 3},
    {"id": 13, "label": "BE Dev 2", "level": 3},
    {"id": 14, "label": "BE Dev 3", "level": 3},
    {"id": 15, "label": "PM 1", "level": 3},
    {"id": 16, "label": "PM 2", "level": 3},
    {"id": 17, "label": "Designer 1", "level": 3},
    {"id": 18, "label": "Designer 2", "level": 3},
    {"id": 19, "label": "IT Support 1", "level": 3},
    {"id": 20, "label": "IT Support 2", "level": 3},
    {"id": 21, "label": "HR Spec 1", "level": 3},
    {"id": 22, "label": "HR Spec 2", "level": 3},
    {"id": 23, "label": "Recruiter", "level": 3},
]

edges = [
    # CEO to VPs
    (0, 1),
    (0, 2),
    (0, 3),
    # VP Engineering to Directors
    (1, 4),
    (1, 5),
    # VP Product to Leads
    (2, 6),
    (2, 7),
    # VP Operations to Managers
    (3, 8),
    (3, 9),
    # Directors to Team Members
    (4, 10),
    (4, 11),
    (5, 12),
    (5, 13),
    (5, 14),
    (6, 15),
    (6, 16),
    (7, 17),
    (7, 18),
    (8, 19),
    (8, 20),
    (9, 21),
    (9, 22),
    (9, 23),
]

# Compute hierarchical layout positions
# Group nodes by level
levels = {}
for node in nodes:
    lvl = node["level"]
    if lvl not in levels:
        levels[lvl] = []
    levels[lvl].append(node)

# Calculate positions: levels spread vertically, nodes at each level spread horizontally
positions = {}
y_spacing = 1.5  # Increased vertical spacing
for lvl in sorted(levels.keys()):
    nodes_at_level = levels[lvl]
    n = len(nodes_at_level)
    # Wider horizontal spread for lower levels
    spread = max(n * 1.2, 8)
    x_positions = np.linspace(-spread / 2, spread / 2, n)
    y_pos = -lvl * y_spacing  # Root at top, children below
    for i, node in enumerate(nodes_at_level):
        positions[node["id"]] = (x_positions[i], y_pos)

# Prepare node data
node_x = [positions[n["id"]][0] for n in nodes]
node_y = [positions[n["id"]][1] for n in nodes]
node_labels = [n["label"] for n in nodes]
node_levels = [n["level"] for n in nodes]

# Color by level - using Python Blue and Yellow as primary
level_colors = ["#306998", "#FFD43B", "#4B8BBE", "#8BC34A"]
node_colors = [level_colors[lvl] for lvl in node_levels]

# Node sizes based on level (higher in hierarchy = larger)
size_map = {0: 70, 1: 58, 2: 50, 3: 45}
node_sizes = [size_map[lvl] for lvl in node_levels]

# Prepare edge data
edge_x0 = [positions[e[0]][0] for e in edges]
edge_y0 = [positions[e[0]][1] for e in edges]
edge_x1 = [positions[e[1]][0] for e in edges]
edge_y1 = [positions[e[1]][1] for e in edges]

# Create figure
p = figure(
    width=4800,
    height=2700,
    title="network-hierarchical · bokeh · pyplots.ai",
    x_axis_label="",
    y_axis_label="",
    tools="",
    toolbar_location=None,
)

# Hide axes for cleaner network visualization
p.xaxis.visible = False
p.yaxis.visible = False
p.xgrid.visible = False
p.ygrid.visible = False

# Draw edges (lines connecting parent to child)
edge_source = ColumnDataSource(data={"x0": edge_x0, "y0": edge_y0, "x1": edge_x1, "y1": edge_y1})
p.segment(x0="x0", y0="y0", x1="x1", y1="y1", source=edge_source, line_width=3, line_color="#666666", line_alpha=0.6)

# Draw nodes
node_source = ColumnDataSource(
    data={
        "x": node_x,
        "y": node_y,
        "labels": node_labels,
        "colors": node_colors,
        "sizes": node_sizes,
        "levels": node_levels,
    }
)
p.scatter(
    x="x", y="y", source=node_source, size="sizes", fill_color="colors", line_color="#333333", line_width=2, alpha=0.9
)

# Add labels to nodes
labels = LabelSet(
    x="x",
    y="y",
    text="labels",
    source=node_source,
    text_font_size="24pt",
    text_color="#222222",
    text_align="center",
    y_offset=45,
)
p.add_layout(labels)

# Add hover tool for interactivity
hover = HoverTool(tooltips=[("Role", "@labels"), ("Level", "@levels")], mode="mouse")
p.add_tools(hover)

# Style title
p.title.text_font_size = "32pt"
p.title.align = "center"

# Add level annotations on the side as legend
level_labels = ["Level 0: CEO", "Level 1: VPs", "Level 2: Directors", "Level 3: Team"]
level_y_positions = [0, -1.5, -3.0, -4.5]
for i, (label, y_pos) in enumerate(zip(level_labels, level_y_positions, strict=True)):
    p.text(x=[-10], y=[y_pos], text=[label], text_font_size="28pt", text_color=level_colors[i], text_align="left")

# Set plot range to include all elements with padding
p.x_range.start = -11
p.x_range.end = 11
p.y_range.start = -5.5
p.y_range.end = 1.0

# Save as PNG
export_png(p, filename="plot.png")
