""" pyplots.ai
chord-basic: Basic Chord Diagram
Library: pygal 3.1.0 | Python 3.13.11
Quality: 75/100 | Created: 2025-12-23
"""

import math

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
radius = 3.5
entity_positions = []
for i in range(n_entities):
    angle = 2 * math.pi * i / n_entities - math.pi / 2  # Start from top
    x = center_x + radius * math.cos(angle)
    y = center_y + radius * math.sin(angle)
    entity_positions.append((x, y, angle))

# Calculate total flow for each entity
total_outflow = [0] * n_entities
for src, _tgt, val in flows:
    total_outflow[src] += val

# Build color sequence: one color per chord (based on source) + legend colors
# Each chord gets the color of its source continent
chord_colors = [entity_colors[src] for src, _, _ in flows]
legend_colors = entity_colors  # One per continent for legend entries
all_colors = tuple(chord_colors + legend_colors)

# Custom style with colors matching chord + legend sequence
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=all_colors,
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=44,
    legend_font_size=44,
    value_font_size=36,
    stroke_width=3,
    opacity=0.6,
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

# Draw each individual chord with stroke width proportional to flow magnitude
max_flow = max(val for _, _, val in flows)
min_flow = min(val for _, _, val in flows)
num_bezier_points = 50

# Draw all chords individually for proper stroke width variation
for src, tgt, val in flows:
    src_x, src_y, src_angle = entity_positions[src]
    tgt_x, tgt_y, tgt_angle = entity_positions[tgt]

    # Control point toward center for the Bezier curve
    pull_factor = 0.25
    ctrl_x = center_x + pull_factor * (src_x + tgt_x - 2 * center_x) / 2
    ctrl_y = center_y + pull_factor * (src_y + tgt_y - 2 * center_y) / 2

    # Generate quadratic Bezier curve points inline (KISS - no functions)
    curve_points = []
    for t in np.linspace(0, 1, num_bezier_points):
        bx = (1 - t) ** 2 * src_x + 2 * (1 - t) * t * ctrl_x + t**2 * tgt_x
        by = (1 - t) ** 2 * src_y + 2 * (1 - t) * t * ctrl_y + t**2 * tgt_y
        curve_points.append((bx, by))

    # Stroke width proportional to flow value (range: 4 to 20 for clear differentiation)
    normalized = (val - min_flow) / (max_flow - min_flow) if max_flow > min_flow else 0.5
    stroke_width = 4 + normalized * 16

    # Add chord without label (None hides from legend)
    chart.add(
        None,
        curve_points,
        stroke=True,
        show_dots=False,
        fill=False,
        stroke_style={"width": stroke_width, "linecap": "round"},
    )

# Add legend entries - one marker per continent at the perimeter
# Use formatter to set explicit colors for legend entries
for i, continent in enumerate(continents):
    x, y, _ = entity_positions[i]
    # Single point for clean legend swatch
    chart.add(
        continent,
        [{"value": (x, y), "color": entity_colors[i]}],
        stroke=False,
        show_dots=True,
        dots_size=20,
        formatter=lambda x, c=entity_colors[i]: c,
    )

# Save outputs
chart.render_to_file("plot.svg")
chart.render_to_png("plot.png")

# Also save HTML for interactive version
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
