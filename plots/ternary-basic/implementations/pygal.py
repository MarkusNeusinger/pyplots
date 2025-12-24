"""pyplots.ai
ternary-basic: Basic Ternary Plot
Library: pygal | Python 3.13
Quality: pending | Created: 2025-12-24
"""

import math

import pygal
from pygal.style import Style


# Triangle height for equilateral triangle with base = 1
H = math.sqrt(3) / 2

# Sample soil composition data (Sand%, Silt%, Clay%) - all sum to 100
# Ternary coordinates: Top=Sand, Bottom-right=Silt, Bottom-left=Clay
compositions = [
    (65, 25, 10),  # Sandy Loam
    (10, 45, 45),  # Silty Clay
    (30, 35, 35),  # Clay Loam
    (40, 40, 20),  # Loam
    (50, 10, 40),  # Sandy Clay
    (20, 65, 15),  # Silt Loam
    (90, 5, 5),  # Pure Sand
    (5, 90, 5),  # Pure Silt
    (5, 5, 90),  # Pure Clay
    (33, 34, 33),  # Balanced
    (45, 45, 10),  # Sandy Silt
    (55, 35, 10),  # Silty Sand
    (15, 20, 65),  # Clay
    (10, 15, 75),  # Heavy Clay
    (50, 30, 20),  # Light Loam
]

# Convert ternary (sand, silt, clay) to cartesian (x, y)
# Formula: x = 0.5 * (2 * silt/100 + sand/100), y = H * sand/100
data_points = [(0.5 * (2 * s[1] + s[0]) / 100, H * s[0] / 100) for s in compositions]

# Triangle vertices
vertex_sand = (0.5, H)  # Top - 100% Sand
vertex_silt = (1.0, 0.0)  # Bottom-right - 100% Silt
vertex_clay = (0.0, 0.0)  # Bottom-left - 100% Clay

# Grid lines at 20%, 40%, 60%, 80% intervals
# Each line connects two edges of the triangle
grid_lines = []
for pct in [0.2, 0.4, 0.6, 0.8]:
    # Parallel to base (constant Sand %) - from left edge to right edge
    p1 = (0.5 * (2 * (1 - pct) + pct), H * pct)
    p2 = (0.5 * pct, H * pct)
    grid_lines.extend([p1, p2, (None, None)])

    # Parallel to left side (constant Silt %) - from base to right edge
    p1 = (0.5 * (2 * pct + (1 - pct)), H * (1 - pct))
    p2 = (pct, 0.0)
    grid_lines.extend([p1, p2, (None, None)])

    # Parallel to right side (constant Clay %) - from base to left edge
    p1 = (0.5 * (1 - pct), H * (1 - pct))
    p2 = (0.5 * (2 * (1 - pct)), 0.0)
    grid_lines.extend([p1, p2, (None, None)])

# Custom style for 3600x3600 px canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#333333", "#AAAAAA", "#306998"),  # Triangle, Grid, Data
    title_font_size=68,
    label_font_size=48,
    major_label_font_size=44,
    legend_font_size=44,
    value_font_size=40,
    opacity=0.85,
)

# Create XY chart (square format for ternary plot)
chart = pygal.XY(
    width=3600,
    height=3600,
    style=custom_style,
    show_legend=False,
    show_x_guides=False,
    show_y_guides=False,
    show_x_labels=False,
    show_y_labels=False,
    x_title="",
    y_title="",
    title="Soil Composition · ternary-basic · pygal · pyplots.ai",
    dots_size=20,
    stroke=False,
    include_x_axis=False,
    xrange=(-0.15, 1.15),
    yrange=(-0.15, 1.05),
    explicit_size=True,
)

# Triangle outline
chart.add(
    "Boundary",
    [vertex_clay, vertex_silt, vertex_sand, vertex_clay],
    stroke=True,
    show_dots=False,
    stroke_style={"width": 5},
)

# Grid lines (20% intervals)
chart.add("Grid", grid_lines, stroke=True, show_dots=False, stroke_style={"width": 2, "dasharray": "8,5"})

# Data points (soil samples)
chart.add("Samples", data_points, stroke=False, dots_size=22)

# Save outputs
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
