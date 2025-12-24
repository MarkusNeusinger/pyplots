""" pyplots.ai
ternary-basic: Basic Ternary Plot
Library: pygal 3.1.0 | Python 3.13.11
Quality: 72/100 | Created: 2025-12-24
"""

import math

import cairosvg
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

# Tick marks along each edge at 20% intervals
tick_marks = []
tick_len = 0.03  # Length of tick marks

for pct in [0.2, 0.4, 0.6, 0.8]:
    # Ticks on left edge (Clay-Sand): perpendicular outward
    x_left = 0.5 * pct
    y_left = H * pct
    tick_marks.extend([(x_left, y_left), (x_left - tick_len, y_left), (None, None)])

    # Ticks on right edge (Sand-Silt): perpendicular outward
    x_right = 0.5 * (2 - pct)
    y_right = H * pct
    tick_marks.extend([(x_right, y_right), (x_right + tick_len, y_right), (None, None)])

    # Ticks on base (Clay-Silt): perpendicular downward
    x_base = pct
    y_base = 0.0
    tick_marks.extend([(x_base, y_base), (x_base, y_base - tick_len), (None, None)])

# Custom style for 3600x3600 px canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#333333", "#AAAAAA", "#306998", "#333333"),  # Boundary, Grid, Data, Ticks
    title_font_size=80,
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
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=4,
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
    yrange=(-0.20, 1.05),
    explicit_size=True,
    margin=50,
    margin_bottom=120,
)

# Triangle outline
chart.add(
    "Triangle Boundary",
    [vertex_clay, vertex_silt, vertex_sand, vertex_clay],
    stroke=True,
    show_dots=False,
    stroke_style={"width": 5},
)

# Grid lines (20% intervals)
chart.add("Grid (20%)", grid_lines, stroke=True, show_dots=False, stroke_style={"width": 2, "dasharray": "8,5"})

# Data points (soil samples)
chart.add("Soil Samples", data_points, stroke=False, dots_size=22)

# Tick marks along edges
chart.add("Tick Marks", tick_marks, stroke=True, show_dots=False, stroke_style={"width": 3})

# Render to SVG string first
svg_content = chart.render().decode("utf-8")

# Calculate pixel positions for vertex labels
# The chart has xrange=(-0.15, 1.15) = 1.30 range and yrange=(-0.20, 1.05) = 1.25 range
# With 3600px width and margins, we need to calculate positions
# Approximate: plot area starts after margin and title
plot_x_start = 150
plot_x_end = 3450
plot_y_start = 250  # After title
plot_y_end = 3350  # Before legend

x_range = 1.30  # -0.15 to 1.15
y_range = 1.25  # -0.20 to 1.05


def data_to_pixel(x, y):
    """Convert data coordinates to pixel coordinates."""
    px = plot_x_start + (x + 0.15) / x_range * (plot_x_end - plot_x_start)
    # Y is inverted in SVG (0 at top)
    py = plot_y_start + (1.05 - y) / y_range * (plot_y_end - plot_y_start)
    return px, py


# Get pixel positions for labels (offset slightly from vertices)
sand_px, sand_py = data_to_pixel(0.5, H + 0.06)
silt_px, silt_py = data_to_pixel(1.07, -0.03)
clay_px, clay_py = data_to_pixel(-0.07, -0.03)

# Create SVG text elements for vertex labels
vertex_labels_svg = f"""
  <text x="{sand_px}" y="{sand_py}" text-anchor="middle" font-size="60" font-weight="bold" fill="#333333" font-family="sans-serif">SAND</text>
  <text x="{silt_px}" y="{silt_py}" text-anchor="start" font-size="60" font-weight="bold" fill="#333333" font-family="sans-serif">SILT</text>
  <text x="{clay_px}" y="{clay_py}" text-anchor="end" font-size="60" font-weight="bold" fill="#333333" font-family="sans-serif">CLAY</text>
"""

# Insert labels before the closing </svg> tag
svg_content = svg_content.replace("</svg>", vertex_labels_svg + "</svg>")

# Save as SVG for HTML output
with open("plot.html", "w") as f:
    f.write(svg_content)

# Convert to PNG
cairosvg.svg2png(bytestring=svg_content.encode("utf-8"), write_to="plot.png")
