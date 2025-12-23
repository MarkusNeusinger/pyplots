""" pyplots.ai
chord-basic: Basic Chord Diagram
Library: pygal 3.1.0 | Python 3.13.11
Quality: 78/100 | Created: 2025-12-23
"""

import math

import cairosvg
import numpy as np
import pygal
from pygal.style import Style


# Set seed for reproducibility
np.random.seed(42)

# Data: Migration flows between 6 continents (bidirectional)
continents = ["Africa", "Asia", "Europe", "N. America", "S. America", "Oceania"]
n_entities = len(continents)

# Migration flows as (source, target, value) - asymmetric/bidirectional
flows = [
    # From Africa
    (0, 1, 8),  # Africa → Asia
    (0, 2, 25),  # Africa → Europe
    (0, 3, 12),  # Africa → North America
    (0, 4, 5),  # Africa → South America
    (0, 5, 3),  # Africa → Oceania
    # From Asia
    (1, 0, 6),  # Asia → Africa
    (1, 2, 20),  # Asia → Europe
    (1, 3, 35),  # Asia → North America
    (1, 4, 8),  # Asia → South America
    (1, 5, 18),  # Asia → Oceania
    # From Europe
    (2, 0, 4),  # Europe → Africa
    (2, 1, 12),  # Europe → Asia
    (2, 3, 22),  # Europe → North America
    (2, 4, 15),  # Europe → South America
    (2, 5, 10),  # Europe → Oceania
    # From North America
    (3, 0, 2),  # North America → Africa
    (3, 1, 10),  # North America → Asia
    (3, 2, 18),  # North America → Europe
    (3, 4, 14),  # North America → South America
    (3, 5, 6),  # North America → Oceania
    # From South America
    (4, 0, 3),  # South America → Africa
    (4, 1, 7),  # South America → Asia
    (4, 2, 28),  # South America → Europe
    (4, 3, 20),  # South America → North America
    (4, 5, 4),  # South America → Oceania
    # From Oceania
    (5, 0, 2),  # Oceania → Africa
    (5, 1, 15),  # Oceania → Asia
    (5, 2, 12),  # Oceania → Europe
    (5, 3, 8),  # Oceania → North America
    (5, 4, 3),  # Oceania → South America
]

# Colors for each continent (colorblind-safe palette)
entity_colors = [
    "#306998",  # Africa - Python Blue
    "#FFD43B",  # Asia - Python Yellow
    "#4CAF50",  # Europe - Green
    "#FF7043",  # N. America - Orange
    "#9C27B0",  # S. America - Purple
    "#00BCD4",  # Oceania - Cyan
]

# Calculate positions around a circle
center_x, center_y = 5.0, 5.0
radius = 3.2
label_radius = 4.2  # Labels positioned outside the circle
entity_positions = []
for i in range(n_entities):
    angle = 2 * math.pi * i / n_entities - math.pi / 2  # Start from top
    x = center_x + radius * math.cos(angle)
    y = center_y + radius * math.sin(angle)
    lx = center_x + label_radius * math.cos(angle)
    ly = center_y + label_radius * math.sin(angle)
    entity_positions.append((x, y, lx, ly, angle))

# Build color sequence: one color per chord (based on source) followed by legend colors
# Each series in pygal takes the next color from the sequence
chord_colors = [entity_colors[src] for src, _, _ in flows]
all_colors = tuple(chord_colors + entity_colors)

# Custom style with precise color sequence
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=all_colors,  # First 30 colors for chords, last 6 for legend entries
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=44,
    legend_font_size=44,
    value_font_size=36,
    stroke_width=3,
    opacity=0.7,
    opacity_hover=0.95,
)

# Create XY chart (square format for circular diagram)
chart = pygal.XY(
    width=3600,
    height=3600,
    style=custom_style,
    title="chord-basic · pygal · pyplots.ai",
    show_legend=True,
    x_title="",
    y_title="",
    show_x_guides=False,
    show_y_guides=False,
    show_x_labels=False,
    show_y_labels=False,
    stroke=True,
    dots_size=0,
    legend_at_bottom=True,
    legend_at_bottom_columns=6,
    legend_box_size=24,
    range=(0, 10),
    xrange=(0, 10),
    truncate_legend=-1,
)

# Calculate flow stats
max_flow = max(val for _, _, val in flows)
min_flow = min(val for _, _, val in flows)
num_bezier_points = 50

# Draw each chord as a separate series (colors cycle through style.colors)
for src, tgt, val in flows:
    src_x, src_y, _, _, _ = entity_positions[src]
    tgt_x, tgt_y, _, _, _ = entity_positions[tgt]

    # Control point toward center for the Bezier curve
    pull_factor = 0.25
    ctrl_x = center_x + pull_factor * (src_x + tgt_x - 2 * center_x) / 2
    ctrl_y = center_y + pull_factor * (src_y + tgt_y - 2 * center_y) / 2

    # Generate quadratic Bezier curve points
    curve_points = []
    for t in np.linspace(0, 1, num_bezier_points):
        bx = (1 - t) ** 2 * src_x + 2 * (1 - t) * t * ctrl_x + t**2 * tgt_x
        by = (1 - t) ** 2 * src_y + 2 * (1 - t) * t * ctrl_y + t**2 * tgt_y
        curve_points.append((bx, by))

    # Stroke width proportional to flow value (range: 4 to 18)
    normalized = (val - min_flow) / (max_flow - min_flow) if max_flow > min_flow else 0.5
    stroke_width = 4 + normalized * 14

    # Add chord (None hides from legend, color comes from style sequence)
    chart.add(
        None,
        curve_points,
        stroke=True,
        show_dots=False,
        fill=False,
        stroke_style={"width": stroke_width, "linecap": "round"},
    )

# Add legend entries with node markers on the perimeter
# These use colors 30-35 from the style (entity_colors)
for i, continent in enumerate(continents):
    x, y, lx, ly, angle = entity_positions[i]

    # Create a small arc/node at the entity position for visibility
    node_points = []
    arc_span = 0.15
    for t in np.linspace(-arc_span, arc_span, 10):
        nx = center_x + (radius + 0.1) * math.cos(angle + t)
        ny = center_y + (radius + 0.1) * math.sin(angle + t)
        node_points.append((nx, ny))

    # Add continent as legend entry
    chart.add(
        continent, node_points, stroke=True, show_dots=False, fill=False, stroke_style={"width": 12, "linecap": "round"}
    )

# Save outputs
chart.render_to_file("plot.svg")
chart.render_to_png("plot.png")

# Read SVG and inject text labels directly near each node
with open("plot.svg", "r") as f:
    svg_content = f.read()

# Find the closing </svg> tag and inject labels before it
label_svg = ""
for i, continent in enumerate(continents):
    x, y, lx, ly, angle = entity_positions[i]

    # Pygal SVG has a specific coordinate system - map our 0-10 range
    # viewBox is typically "0 0 3600 3600" for width/height 3600
    # The plot area starts after some padding (title, etc.)
    # Approximate: chart area is roughly 400-3200 in both dimensions
    padding = 550
    plot_size = 2500
    svg_x = padding + (lx / 10) * plot_size
    svg_y = padding + ((10 - ly) / 10) * plot_size  # Y is inverted

    # Text anchor based on position around circle
    angle_deg = math.degrees(angle)
    if -60 <= angle_deg <= 60:  # Right side
        anchor = "start"
        svg_x += 30
    elif angle_deg > 120 or angle_deg < -120:  # Left side
        anchor = "end"
        svg_x -= 30
    else:  # Top or bottom
        anchor = "middle"

    # Adjust Y for better centering
    if -30 <= angle_deg <= 30:  # Right
        svg_y += 15
    elif angle_deg > 150 or angle_deg < -150:  # Left
        svg_y += 15

    label_svg += f'''
  <text x="{svg_x:.0f}" y="{svg_y:.0f}" fill="{entity_colors[i]}"
        font-size="48" font-weight="bold" text-anchor="{anchor}"
        font-family="DejaVu Sans, sans-serif">{continent}</text>'''

# Insert labels before closing </svg>
svg_with_labels = svg_content.replace("</svg>", f"{label_svg}\n</svg>")

# Save modified SVG
with open("plot.svg", "w") as f:
    f.write(svg_with_labels)

# Re-render PNG from modified SVG
cairosvg.svg2png(bytestring=svg_with_labels.encode("utf-8"), write_to="plot.png")

# Save HTML for interactive version
with open("plot.html", "w") as f:
    f.write(
        """<!DOCTYPE html>
<html>
<head>
    <title>chord-basic · pygal · pyplots.ai</title>
    <style>
        body { margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 100%; margin: 0 auto; }
        object { width: 100%; height: auto; }
    </style>
</head>
<body>
    <div class="container">
        <object type="image/svg+xml" data="plot.svg">
            Chord diagram not supported
        </object>
    </div>
</body>
</html>"""
    )
