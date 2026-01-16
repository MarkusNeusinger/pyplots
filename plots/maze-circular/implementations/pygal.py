""" pyplots.ai
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

# Calculate radii
radii = [(i + 1) / num_rings for i in range(num_rings)]

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

# Create custom style with BLACK walls (using stroke property)
custom_style = Style(
    background="#FFFFFF",
    plot_background="#FFFFFF",
    foreground="#000000",
    foreground_strong="#000000",
    foreground_subtle="#000000",
    # Series colors: walls=black, entry=blue, goal=red
    colors=("#1a1a1a", "#306998", "#E74C3C"),
    title_font_size=60,
    label_font_size=1,
    major_label_font_size=1,
    legend_font_size=36,
    value_font_size=1,
    opacity=1.0,
    opacity_hover=1.0,
    stroke_opacity=1.0,
    stroke_opacity_hover=1.0,
)

# Create XY chart
chart = pygal.XY(
    width=3600,
    height=3600,
    style=custom_style,
    title="maze-circular \u00b7 pygal \u00b7 pyplots.ai",
    show_legend=True,
    show_dots=True,
    dots_size=0,
    stroke_style={"width": 6},
    show_x_guides=False,
    show_y_guides=False,
    show_x_labels=False,
    show_y_labels=False,
    xrange=(-1.35, 1.35),
    range=(-1.35, 1.35),
    explicit_size=True,
    fill=False,
)

# Collect wall segments
wall_segments = []

# Draw concentric ring walls (arcs where no radial passage exists)
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
            angles = np.linspace(angle_start, angle_end, 30)
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

# Draw outer circle except for entry gap
angles = np.linspace(entry_angle_end, entry_angle_start + 2 * np.pi, 200)
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

# Add maze walls
chart.add("Walls", walls_data, stroke_style={"width": 6})

# Add entry marker (outside the maze) - arrow pointing inward
entry_angle_mid = (entry_angle_start + entry_angle_end) / 2
entry_x = (outer_radius + 0.15) * np.cos(entry_angle_mid)
entry_y = (outer_radius + 0.15) * np.sin(entry_angle_mid)
# Draw small triangle pointing to entry
arrow_size = 0.08
entry_data = [
    (entry_x, entry_y),
    (entry_x - arrow_size * np.cos(entry_angle_mid - 0.4), entry_y - arrow_size * np.sin(entry_angle_mid - 0.4)),
    (entry_x - arrow_size * np.cos(entry_angle_mid + 0.4), entry_y - arrow_size * np.sin(entry_angle_mid + 0.4)),
    (entry_x, entry_y),
]
chart.add("Entry", entry_data, stroke_style={"width": 4}, show_dots=False)

# Add goal at center - small circle
goal_radius = 0.06
goal_angles = np.linspace(0, 2 * np.pi, 30)
goal_data = [(goal_radius * np.cos(a), goal_radius * np.sin(a)) for a in goal_angles]
chart.add("Goal", goal_data, stroke_style={"width": 4}, show_dots=False)

# Render outputs
chart.render_to_file("plot.svg")
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
