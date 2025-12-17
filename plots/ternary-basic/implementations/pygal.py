"""
ternary-basic: Basic Ternary Plot
Library: pygal

Uses pygal's XML filter to add text labels for vertices since pygal lacks native annotation support.
"""

import math

import pygal
from pygal.etree import etree
from pygal.style import Style


# Data - Soil composition samples (sand, silt, clay percentages)
# Each tuple: (sand%, silt%, clay%) - must sum to 100
samples = [
    (40, 40, 20),
    (60, 25, 15),
    (25, 50, 25),
    (70, 20, 10),
    (30, 30, 40),
    (50, 35, 15),
    (20, 45, 35),
    (55, 30, 15),
    (35, 40, 25),
    (45, 25, 30),
    (65, 20, 15),
    (25, 55, 20),
    (40, 30, 30),
    (50, 40, 10),
    (30, 45, 25),
    (60, 15, 25),
    (35, 50, 15),
    (45, 35, 20),
    (55, 25, 20),
    (20, 40, 40),
]

# Chart dimensions
WIDTH = 4800
HEIGHT = 2700

# Triangle dimensions in normalized coordinates (0-1)
triangle_height = math.sqrt(3) / 2


# Convert ternary coordinates to Cartesian (for equilateral triangle)
def ternary_to_cartesian(a, b, c):
    """Convert (a, b, c) ternary coords to (x, y) Cartesian coords.
    a = Sand (top vertex), b = Silt (bottom-left), c = Clay (bottom-right)
    """
    total = a + b + c
    a, b, c = a / total, b / total, c / total
    x = 0.5 * (2 * c + a)
    y = triangle_height * a
    return x, y


# Convert all samples to Cartesian coordinates
points = [ternary_to_cartesian(s[0], s[1], s[2]) for s in samples]

# Triangle vertices and outline
triangle = [
    (0, 0),  # Bottom-left (Silt)
    (1, 0),  # Bottom-right (Clay)
    (0.5, triangle_height),  # Top (Sand)
    (0, 0),  # Close the triangle
]

# Grid lines at 20% intervals (clipped to triangle)
grid_lines = []
for pct in [20, 40, 60, 80]:
    # Lines parallel to bottom edge (constant Sand %)
    p1 = ternary_to_cartesian(pct, 100 - pct, 0)
    p2 = ternary_to_cartesian(pct, 0, 100 - pct)
    grid_lines.append((p1, p2))
    # Lines parallel to left edge (constant Clay %)
    p1 = ternary_to_cartesian(0, 100 - pct, pct)
    p2 = ternary_to_cartesian(100 - pct, 0, pct)
    grid_lines.append((p1, p2))
    # Lines parallel to right edge (constant Silt %)
    p1 = ternary_to_cartesian(0, pct, 100 - pct)
    p2 = ternary_to_cartesian(100 - pct, pct, 0)
    grid_lines.append((p1, p2))

# Custom style for pyplots (4800 x 2700 px)
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#AAAAAA", "#333333"),
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=48,
    value_font_size=36,
    stroke_width=3,
)

# Plot area margins (approximate from pygal default layout)
PLOT_LEFT = 150
PLOT_TOP = 200
PLOT_WIDTH = WIDTH - 300
PLOT_HEIGHT = HEIGHT - 400

# Data range for coordinate conversion
X_MIN, X_MAX = -0.15, 1.15
Y_MIN, Y_MAX = -0.15, triangle_height + 0.15


def data_to_svg(x, y):
    """Convert data coordinates to SVG pixel coordinates."""
    svg_x = PLOT_LEFT + (x - X_MIN) / (X_MAX - X_MIN) * PLOT_WIDTH
    svg_y = PLOT_TOP + (1 - (y - Y_MIN) / (Y_MAX - Y_MIN)) * PLOT_HEIGHT
    return svg_x, svg_y


# Vertex label data (label text, x, y, anchor, baseline)
vertex_labels = [
    ("Sand", 0.5, triangle_height + 0.06, "middle", "auto"),  # Top
    ("Silt", -0.05, -0.05, "end", "auto"),  # Bottom-left
    ("Clay", 1.05, -0.05, "start", "auto"),  # Bottom-right
]


# XML filter to add vertex labels
def add_vertex_labels(root):
    """Add text labels for triangle vertices."""
    g = etree.SubElement(root, "g")
    g.set("class", "vertex-labels")

    for label, x, y, anchor, baseline in vertex_labels:
        svg_x, svg_y = data_to_svg(x, y)

        text = etree.SubElement(g, "text")
        text.set("x", f"{svg_x:.1f}")
        text.set("y", f"{svg_y:.1f}")
        text.set("text-anchor", anchor)
        text.set("dominant-baseline", baseline)
        text.set("fill", "#333333")
        text.set("font-size", "56")
        text.set("font-family", "sans-serif")
        text.set("font-weight", "bold")
        text.text = label

    return root


# Create XY chart
chart = pygal.XY(
    width=WIDTH,
    height=HEIGHT,
    style=custom_style,
    title="Soil Composition · ternary-basic · pygal · pyplots.ai",
    show_legend=True,
    stroke=False,
    show_x_guides=False,
    show_y_guides=False,
    show_x_labels=False,
    show_y_labels=False,
    x_title=None,
    y_title=None,
    range=(Y_MIN, Y_MAX),
    xrange=(X_MIN, X_MAX),
    margin=50,
    explicit_size=True,
)

# Add data points first (so they appear in legend with correct color)
chart.add(
    "Soil Samples",
    [
        {"value": p, "label": f"Sand: {samples[i][0]}%, Silt: {samples[i][1]}%, Clay: {samples[i][2]}%"}
        for i, p in enumerate(points)
    ],
    stroke=False,
    dots_size=18,
)

# Add grid lines (subtle gray, no legend)
for p1, p2 in grid_lines:
    chart.add(
        None,
        [{"value": p1}, {"value": p2}],
        stroke=True,
        show_dots=False,
        stroke_style={"width": 1, "dasharray": "5,5"},
    )

# Add triangle outline (no legend)
chart.add(
    None, [{"value": p, "node": {"r": 0}} for p in triangle], stroke=True, show_dots=False, stroke_style={"width": 4}
)

# Add XML filter for vertex labels
chart.add_xml_filter(add_vertex_labels)

# Save as SVG (for HTML) and PNG
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
