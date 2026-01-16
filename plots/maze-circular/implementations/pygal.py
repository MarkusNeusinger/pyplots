"""pyplots.ai
maze-circular: Circular Maze Puzzle
Library: pygal 3.1.0 | Python 3.13.11
Quality: 72/100 | Created: 2026-01-16
"""

import numpy as np
import pygal
from pygal.style import Style


# Set seed for reproducibility
np.random.seed(42)

# Maze parameters
num_rings = 7
sectors_per_ring = [1, 6, 12, 12, 18, 24, 30]

# Calculate radii - scale up for better visibility
scale = 1.0
radii = [(i + 1) * scale / num_rings for i in range(num_rings)]

# Build all possible edges between cells
# Cell = (ring_index, sector_index)
edges = []
for ring in range(num_rings):
    n_sectors = sectors_per_ring[ring]
    for sector in range(n_sectors):
        # Adjacent sectors in same ring
        if n_sectors > 1:
            next_sector = (sector + 1) % n_sectors
            edges.append(frozenset([(ring, sector), (ring, next_sector)]))
        # Connection to outer ring
        if ring < num_rings - 1:
            outer_sectors = sectors_per_ring[ring + 1]
            for s in range(outer_sectors):
                if int(s * n_sectors / outer_sectors) == sector:
                    edges.append(frozenset([(ring, sector), (ring + 1, s)]))

# Remove duplicate edges
edges = list(set(edges))

# Generate maze using Kruskal's algorithm with union-find
parent = {}
for ring in range(num_rings):
    for sector in range(sectors_per_ring[ring]):
        parent[(ring, sector)] = (ring, sector)

# Shuffle edges for random maze
np.random.shuffle(edges)

# Build spanning tree
passages = set()
for edge in edges:
    cells = list(edge)
    cell_a, cell_b = cells[0], cells[1]

    # Find roots
    root_a = cell_a
    while parent[root_a] != root_a:
        root_a = parent[root_a]
    root_b = cell_b
    while parent[root_b] != root_b:
        root_b = parent[root_b]

    if root_a != root_b:
        # Union
        parent[root_a] = root_b
        passages.add(edge)

# Add extra passages for medium difficulty
extra_count = 5
for edge in edges:
    if edge not in passages and extra_count > 0:
        passages.add(edge)
        extra_count -= 1

# Create custom style with BLACK walls - thicker for print-friendly output
custom_style = Style(
    background="#FFFFFF",
    plot_background="#FFFFFF",
    foreground="#000000",
    foreground_strong="#000000",
    foreground_subtle="#000000",
    # Series colors: walls=black, entry=blue, goal=red
    colors=("#000000", "#1565C0", "#C62828"),
    title_font_size=72,
    label_font_size=1,
    major_label_font_size=1,
    legend_font_size=1,
    value_font_size=1,
    opacity=1.0,
    opacity_hover=1.0,
    stroke_opacity=1.0,
    stroke_opacity_hover=1.0,
    stroke_width=16,
)

# Create XY chart - hide legend as it's not useful for a maze puzzle
chart = pygal.XY(
    width=3600,
    height=3600,
    style=custom_style,
    title="maze-circular \u00b7 pygal \u00b7 pyplots.ai",
    show_legend=False,
    show_dots=False,
    stroke=True,
    show_x_guides=False,
    show_y_guides=False,
    show_x_labels=False,
    show_y_labels=False,
    xrange=(-1.25, 1.25),
    range=(-1.25, 1.25),
    explicit_size=True,
    fill=False,
    margin=50,
)

# Collect wall segments
wall_segments = []

# Draw concentric ring walls (arcs where no radial passage exists)
# Use more points for smoother arcs
arc_points = 50
for ring in range(num_rings - 1):
    radius = radii[ring]
    n_sectors = sectors_per_ring[ring]
    outer_sectors = sectors_per_ring[ring + 1]

    for sector in range(n_sectors):
        # Check if any outer sector connected to this sector has a passage
        has_passage = False
        for os in range(outer_sectors):
            if int(os * n_sectors / outer_sectors) == sector:
                if frozenset([(ring, sector), (ring + 1, os)]) in passages:
                    has_passage = True
                    break

        if not has_passage:
            # Draw arc for this sector
            angle_start = 2 * np.pi * sector / n_sectors
            angle_end = 2 * np.pi * (sector + 1) / n_sectors
            angles = np.linspace(angle_start, angle_end, arc_points)
            for i in range(len(angles) - 1):
                x1 = radius * np.cos(angles[i])
                y1 = radius * np.sin(angles[i])
                x2 = radius * np.cos(angles[i + 1])
                y2 = radius * np.sin(angles[i + 1])
                wall_segments.append(((x1, y1), (x2, y2)))

# Draw radial walls
for ring in range(num_rings):
    n_sectors = sectors_per_ring[ring]
    inner_radius = radii[ring - 1] if ring > 0 else 0
    outer_radius = radii[ring]

    for sector in range(n_sectors):
        prev_sector = (sector - 1) % n_sectors
        # Check if passage exists between this sector and previous
        if n_sectors > 1 and frozenset([(ring, sector), (ring, prev_sector)]) not in passages:
            angle = 2 * np.pi * sector / n_sectors
            x1 = inner_radius * np.cos(angle)
            y1 = inner_radius * np.sin(angle)
            x2 = outer_radius * np.cos(angle)
            y2 = outer_radius * np.sin(angle)
            wall_segments.append(((x1, y1), (x2, y2)))

# Draw outer boundary (with entry gap)
entry_sector = 0
entry_n_sectors = sectors_per_ring[-1]
outer_radius = radii[-1]
entry_angle_start = 2 * np.pi * entry_sector / entry_n_sectors
entry_angle_end = 2 * np.pi * (entry_sector + 1) / entry_n_sectors

# Draw outer circle except for entry gap - use more points for smooth curve
outer_arc_points = 300
angles = np.linspace(entry_angle_end, entry_angle_start + 2 * np.pi, outer_arc_points)
for i in range(len(angles) - 1):
    x1 = outer_radius * np.cos(angles[i])
    y1 = outer_radius * np.sin(angles[i])
    x2 = outer_radius * np.cos(angles[i + 1])
    y2 = outer_radius * np.sin(angles[i + 1])
    wall_segments.append(((x1, y1), (x2, y2)))

# Convert segments to pygal series format
walls_data = []
for (x1, y1), (x2, y2) in wall_segments:
    walls_data.append((x1, y1))
    walls_data.append((x2, y2))
    walls_data.append(None)

# Add maze walls with thick lines for print-friendly output
chart.add("Walls", walls_data)

# Add entry marker - large visible arrow pointing into the maze
entry_angle_mid = (entry_angle_start + entry_angle_end) / 2
# Position arrow tip at the entry gap on outer boundary
arrow_tip_x = (outer_radius + 0.02) * np.cos(entry_angle_mid)
arrow_tip_y = (outer_radius + 0.02) * np.sin(entry_angle_mid)
# Arrow base further out - longer shaft for visibility
arrow_length = 0.25
arrow_base_x = (outer_radius + arrow_length) * np.cos(entry_angle_mid)
arrow_base_y = (outer_radius + arrow_length) * np.sin(entry_angle_mid)
# Arrow wings - larger and wider angle for clear arrow head
arrow_wing = 0.15
wing_angle = 0.7
entry_data = [
    # Arrow shaft
    (arrow_base_x, arrow_base_y),
    (arrow_tip_x, arrow_tip_y),
    None,
    # Left wing
    (arrow_tip_x, arrow_tip_y),
    (
        arrow_tip_x + arrow_wing * np.cos(entry_angle_mid + np.pi - wing_angle),
        arrow_tip_y + arrow_wing * np.sin(entry_angle_mid + np.pi - wing_angle),
    ),
    None,
    # Right wing
    (arrow_tip_x, arrow_tip_y),
    (
        arrow_tip_x + arrow_wing * np.cos(entry_angle_mid + np.pi + wing_angle),
        arrow_tip_y + arrow_wing * np.sin(entry_angle_mid + np.pi + wing_angle),
    ),
]
chart.add("Entry", entry_data)

# Add goal at center - prominent star shape marking the finish
goal_radius_outer = 0.16
goal_radius_inner = 0.07
num_points = 5
goal_data = []
for i in range(num_points * 2 + 1):
    angle = i * np.pi / num_points - np.pi / 2
    r = goal_radius_outer if i % 2 == 0 else goal_radius_inner
    goal_data.append((r * np.cos(angle), r * np.sin(angle)))
chart.add("Goal", goal_data)

# Render outputs
chart.render_to_file("plot.svg")
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
