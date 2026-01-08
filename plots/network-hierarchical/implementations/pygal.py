"""pyplots.ai
network-hierarchical: Hierarchical Network Graph with Tree Layout
Library: pygal | Python 3.13
Quality: pending | Created: 2026-01-08
"""

import pygal
from pygal.style import Style


# Define organizational hierarchy (CEO -> VPs -> Directors -> Managers)
# Structure: {node_id: (label, level, parent_id)}
hierarchy = {
    0: ("CEO", 0, None),
    1: ("VP Eng", 1, 0),
    2: ("VP Sales", 1, 0),
    3: ("VP Ops", 1, 0),
    4: ("Dir FE", 2, 1),
    5: ("Dir BE", 2, 1),
    6: ("Dir DevOps", 2, 1),
    7: ("Dir Americas", 2, 2),
    8: ("Dir EMEA", 2, 2),
    9: ("Dir Logistics", 2, 3),
    10: ("Dir HR", 2, 3),
    11: ("Mgr React", 3, 4),
    12: ("Mgr Vue", 3, 4),
    13: ("Mgr API", 3, 5),
    14: ("Mgr DB", 3, 5),
    15: ("Mgr Cloud", 3, 6),
    16: ("Mgr NA", 3, 7),
    17: ("Mgr LATAM", 3, 7),
    18: ("Mgr UK", 3, 8),
    19: ("Mgr DE", 3, 8),
    20: ("Mgr Supply", 3, 9),
    21: ("Mgr Talent", 3, 10),
}

# Group nodes by level
levels = {}
for node_id, (_label, level, _parent) in hierarchy.items():
    if level not in levels:
        levels[level] = []
    levels[level].append(node_id)

# Calculate node positions using tree layout
node_positions = {}
max_level = max(levels.keys())
y_spacing = 70 / (max_level + 1)

for level, nodes in levels.items():
    num_nodes = len(nodes)
    x_spacing = 85 / (num_nodes + 1)
    for i, node_id in enumerate(nodes):
        x = 7 + (i + 1) * x_spacing
        y = 92 - (level * y_spacing + y_spacing / 2)
        node_positions[node_id] = (x, y)

# Level colors: Blue (CEO), Yellow (VPs), Teal (Directors), Coral (Managers)
level_colors = ["#306998", "#FFD43B", "#4ECDC4", "#FF6B6B"]

# Create custom style with grey for edges, then level colors for nodes
# Order: edge color first, then 4 level colors
style_colors = ["#AAAAAA"] + level_colors

custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#888888",
    colors=tuple(style_colors),
    title_font_size=72,
    label_font_size=36,
    major_label_font_size=32,
    legend_font_size=40,
    value_font_size=28,
    tooltip_font_size=28,
    stroke_width=4,
    opacity=0.95,
    opacity_hover=1.0,
)

# Create XY chart
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="network-hierarchical · pygal · pyplots.ai",
    x_title="Organization Width",
    y_title="Hierarchy Level (Top to Bottom)",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=5,
    show_x_guides=False,
    show_y_guides=False,
    stroke=True,
    dots_size=28,
    show_dots=True,
    range=(0, 100),
    xrange=(0, 100),
    explicit_size=True,
    print_values=False,
    truncate_legend=-1,
    margin_bottom=120,
)

# Collect all edges
all_edges = []
for node_id, (_label, _level, parent_id) in hierarchy.items():
    if parent_id is not None:
        parent_pos = node_positions[parent_id]
        child_pos = node_positions[node_id]
        all_edges.append((parent_pos, child_pos))

# Add edges as a single series with discontinuous lines using None
edge_data = []
for start, end in all_edges:
    if edge_data:
        edge_data.append(None)
    edge_data.append(start)
    edge_data.append(end)

chart.add("Edges", edge_data, show_dots=False, stroke=True)

# Add nodes grouped by level
level_names = {0: "CEO", 1: "VPs", 2: "Directors", 3: "Managers"}
for level in sorted(levels.keys()):
    node_ids = levels[level]
    points = []
    for node_id in node_ids:
        pos = node_positions[node_id]
        label = hierarchy[node_id][0]
        points.append({"value": pos, "label": label})
    chart.add(level_names.get(level, f"Level {level}"), points, stroke=False)

# Render to PNG and HTML
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
