""" pyplots.ai
maze-circular: Circular Maze Puzzle
Library: pygal 3.1.0 | Python 3.13.11
Quality: 58/100 | Created: 2026-01-16
"""

import numpy as np
import pygal
from pygal.style import Style


# Set seed for reproducibility
np.random.seed(42)

# Maze parameters - balanced for visual clarity
num_rings = 6
num_sectors = 10

# Calculate radii
inner_radius = 0.12
outer_radius = 0.88
radii = np.linspace(inner_radius, outer_radius, num_rings + 1)[1:]

# Build cells: each cell is (ring, sector)
all_cells = [(r, s) for r in range(num_rings) for s in range(num_sectors)]

# Build edges between adjacent cells
edges = []
for ring in range(num_rings):
    for sector in range(num_sectors):
        # Circumferential neighbor
        next_s = (sector + 1) % num_sectors
        edges.append(frozenset([(ring, sector), (ring, next_s)]))
        # Radial neighbor
        if ring < num_rings - 1:
            edges.append(frozenset([(ring, sector), (ring + 1, sector)]))

edges = list(set(edges))

# Kruskal's algorithm for maze generation
parent = {cell: cell for cell in all_cells}


def find(c):
    while parent[c] != c:
        parent[c] = parent[parent[c]]
        c = parent[c]
    return c


def union(a, b):
    ra, rb = find(a), find(b)
    if ra != rb:
        parent[ra] = rb
        return True
    return False


np.random.shuffle(edges)
passages = set()
for edge in edges:
    cells = list(edge)
    if union(cells[0], cells[1]):
        passages.add(edge)

# Entry at sector 0
entry_sector = 0

# Colors
wall_color = "#000000"
entry_color = "#1565C0"
goal_color = "#D32F2F"

custom_style = Style(
    background="#FFFFFF",
    plot_background="#FFFFFF",
    foreground="#333333",
    foreground_strong="#000000",
    foreground_subtle="#666666",
    colors=(wall_color,),
    title_font_size=84,
    stroke_width=8,
)

chart = pygal.XY(
    width=3600,
    height=3600,
    style=custom_style,
    title="maze-circular · pygal · pyplots.ai",
    show_legend=False,
    show_dots=False,
    stroke=True,
    show_x_guides=False,
    show_y_guides=False,
    show_x_labels=False,
    show_y_labels=False,
    xrange=(-1.15, 1.15),
    range=(-1.15, 1.15),
    explicit_size=True,
    fill=False,
    margin=100,
)


def arc_pts(radius, a1, a2, n=25):
    """Generate arc points."""
    angles = np.linspace(a1, a2, n)
    return [(radius * np.cos(a), radius * np.sin(a)) for a in angles]


# Entry angles
entry_a1 = 2 * np.pi * entry_sector / num_sectors
entry_a2 = 2 * np.pi * (entry_sector + 1) / num_sectors

# Wall stroke width
wall_width = 10

# 1. Outer boundary (with entry gap)
chart.add("", arc_pts(radii[-1], entry_a2, entry_a1 + 2 * np.pi, 120), stroke_style={"width": wall_width})

# 2. Inner circle (goal area boundary)
inner_arc = arc_pts(inner_radius, 0, 2 * np.pi, 50)
inner_arc.append(inner_arc[0])
chart.add("", inner_arc, stroke_style={"width": wall_width})

# 3. Ring walls (arcs where no radial passage)
for ring in range(num_rings - 1):
    r = radii[ring]
    for sector in range(num_sectors):
        if frozenset([(ring, sector), (ring + 1, sector)]) not in passages:
            a1 = 2 * np.pi * sector / num_sectors
            a2 = 2 * np.pi * (sector + 1) / num_sectors
            chart.add("", arc_pts(r, a1, a2, 12), stroke_style={"width": wall_width})

# 4. Radial walls
for ring in range(num_rings):
    r_in = radii[ring - 1] if ring > 0 else inner_radius
    r_out = radii[ring]
    for sector in range(num_sectors):
        prev_s = (sector - 1) % num_sectors
        if frozenset([(ring, sector), (ring, prev_s)]) not in passages:
            angle = 2 * np.pi * sector / num_sectors
            x1, y1 = r_in * np.cos(angle), r_in * np.sin(angle)
            x2, y2 = r_out * np.cos(angle), r_out * np.sin(angle)
            chart.add("", [(x1, y1), (x2, y2)], stroke_style={"width": wall_width})

# Entry arrow - blue, prominent
mid_angle = (entry_a1 + entry_a2) / 2
tip_x = (radii[-1] + 0.03) * np.cos(mid_angle)
tip_y = (radii[-1] + 0.03) * np.sin(mid_angle)
base_x = (radii[-1] + 0.22) * np.cos(mid_angle)
base_y = (radii[-1] + 0.22) * np.sin(mid_angle)
wing = 0.09
spread = 0.55

# Arrow shaft
chart.add("", [(base_x, base_y), (tip_x, tip_y)], stroke_style={"width": 12, "color": entry_color})
# Arrow wings
chart.add(
    "",
    [
        (tip_x, tip_y),
        (tip_x + wing * np.cos(mid_angle + np.pi - spread), tip_y + wing * np.sin(mid_angle + np.pi - spread)),
    ],
    stroke_style={"width": 12, "color": entry_color},
)
chart.add(
    "",
    [
        (tip_x, tip_y),
        (tip_x + wing * np.cos(mid_angle + np.pi + spread), tip_y + wing * np.sin(mid_angle + np.pi + spread)),
    ],
    stroke_style={"width": 12, "color": entry_color},
)

# Goal star - red, at center
sr1, sr2 = 0.10, 0.04
goal_data = []
for i in range(11):
    a = i * np.pi / 5 - np.pi / 2
    r = sr1 if i % 2 == 0 else sr2
    goal_data.append((r * np.cos(a), r * np.sin(a)))
chart.add("", goal_data, stroke_style={"width": 8, "color": goal_color})

# Render outputs
chart.render_to_file("plot.svg")
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
