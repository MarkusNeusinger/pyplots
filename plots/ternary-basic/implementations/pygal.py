"""
ternary-basic: Basic Ternary Plot
Library: pygal

Pygal lacks native ternary support, so we render the triangle and grid
as XY series, then add vertex labels using PIL for PNG output.
"""

import math

import pygal
from PIL import Image, ImageDraw, ImageFont
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

# Triangle geometry
TRIANGLE_HEIGHT = math.sqrt(3) / 2

# Convert ternary coordinates to Cartesian
# a = Sand (top vertex), b = Silt (bottom-left), c = Clay (bottom-right)
points = []
for sand, silt, clay in samples:
    total = sand + silt + clay
    a, b, c = sand / total, silt / total, clay / total
    x = 0.5 * (2 * c + a)
    y = TRIANGLE_HEIGHT * a
    points.append((x, y))

# Triangle vertices and outline
triangle = [
    (0, 0),  # Bottom-left (Silt)
    (1, 0),  # Bottom-right (Clay)
    (0.5, TRIANGLE_HEIGHT),  # Top (Sand)
    (0, 0),  # Close the triangle
]

# Grid lines at 20% intervals
grid_lines = []
for pct in [20, 40, 60, 80]:
    frac = pct / 100
    # Lines parallel to bottom edge (constant Sand %)
    p1_a, p1_b, p1_c = frac, 1 - frac, 0
    p2_a, p2_b, p2_c = frac, 0, 1 - frac
    p1 = (0.5 * (2 * p1_c + p1_a), TRIANGLE_HEIGHT * p1_a)
    p2 = (0.5 * (2 * p2_c + p2_a), TRIANGLE_HEIGHT * p2_a)
    grid_lines.append((p1, p2))
    # Lines parallel to left edge (constant Clay %)
    p1_a, p1_b, p1_c = 0, 1 - frac, frac
    p2_a, p2_b, p2_c = 1 - frac, 0, frac
    p1 = (0.5 * (2 * p1_c + p1_a), TRIANGLE_HEIGHT * p1_a)
    p2 = (0.5 * (2 * p2_c + p2_a), TRIANGLE_HEIGHT * p2_a)
    grid_lines.append((p1, p2))
    # Lines parallel to right edge (constant Silt %)
    p1_a, p1_b, p1_c = 0, frac, 1 - frac
    p2_a, p2_b, p2_c = 1 - frac, frac, 0
    p1 = (0.5 * (2 * p1_c + p1_a), TRIANGLE_HEIGHT * p1_a)
    p2 = (0.5 * (2 * p2_c + p2_a), TRIANGLE_HEIGHT * p2_a)
    grid_lines.append((p1, p2))

# Custom style for 4800 x 2700 px
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

# Data range for coordinate conversion (with padding)
X_MIN, X_MAX = -0.15, 1.15
Y_MIN, Y_MAX = -0.15, TRIANGLE_HEIGHT + 0.15

# Create XY chart
chart = pygal.XY(
    width=WIDTH,
    height=HEIGHT,
    style=custom_style,
    title="ternary-basic · pygal · pyplots.ai",
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

# Add data points with tooltips
chart.add(
    "Soil Samples",
    [
        {"value": points[i], "label": f"Sand: {samples[i][0]}%, Silt: {samples[i][1]}%, Clay: {samples[i][2]}%"}
        for i in range(len(samples))
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

# Save as SVG (for HTML) and PNG
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")

# Add vertex labels using PIL
img = Image.open("plot.png")
draw = ImageDraw.Draw(img)

# Calculate plot area (approximate from pygal layout)
PLOT_LEFT = 150
PLOT_TOP = 200
PLOT_WIDTH = WIDTH - 300
PLOT_HEIGHT = HEIGHT - 400

# Map data coordinates to pixel coordinates
# Y is inverted in SVG/image coordinates
sand_x = PLOT_LEFT + (0.5 - X_MIN) / (X_MAX - X_MIN) * PLOT_WIDTH
sand_y = PLOT_TOP + (1 - (TRIANGLE_HEIGHT + 0.08 - Y_MIN) / (Y_MAX - Y_MIN)) * PLOT_HEIGHT
silt_x = PLOT_LEFT + (-0.08 - X_MIN) / (X_MAX - X_MIN) * PLOT_WIDTH
silt_y = PLOT_TOP + (1 - (-0.06 - Y_MIN) / (Y_MAX - Y_MIN)) * PLOT_HEIGHT
clay_x = PLOT_LEFT + (1.08 - X_MIN) / (X_MAX - X_MIN) * PLOT_WIDTH
clay_y = PLOT_TOP + (1 - (-0.06 - Y_MIN) / (Y_MAX - Y_MIN)) * PLOT_HEIGHT

# Try to load a font, fall back to default
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 56)
except OSError:
    font = ImageFont.load_default()

# Draw vertex labels
draw.text((sand_x, sand_y), "Sand", fill="#333333", font=font, anchor="mm")
draw.text((silt_x, silt_y), "Silt", fill="#333333", font=font, anchor="rm")
draw.text((clay_x, clay_y), "Clay", fill="#333333", font=font, anchor="lm")

# Save final image
img.save("plot.png")
