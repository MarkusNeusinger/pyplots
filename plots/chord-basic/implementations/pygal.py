"""pyplots.ai
chord-basic: Basic Chord Diagram
Library: pygal 3.1.0 | Python 3.13.11
Quality: 72/100 | Created: 2025-12-23
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

# Group flows by source for coloring
flows_by_source = {i: [] for i in range(n_entities)}
for src, tgt, val in flows:
    flows_by_source[src].append((tgt, val))

# Custom style for the chart - only 6 colors for 6 continents
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=tuple(entity_colors),
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=44,
    legend_font_size=44,
    value_font_size=36,
    stroke_width=3,
    opacity=0.55,
    opacity_hover=0.9,
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
    range=(0, 10),
    xrange=(0, 10),
)

# Draw chords grouped by source (each source gets its color based on index)
max_flow = max(val for _, _, val in flows)
num_bezier_points = 50

for src in range(n_entities):
    src_x, src_y, src_angle = entity_positions[src]

    # Collect all chord points for this source into one series
    # This way we get one legend entry per continent
    all_chord_points = []

    for tgt, _val in flows_by_source[src]:
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

        # Add a break point (None) between chords, then append this chord
        if all_chord_points:
            all_chord_points.append(None)
        all_chord_points.extend(curve_points)

    # Calculate average stroke width for this source's chords
    avg_flow = sum(val for _, val in flows_by_source[src]) / len(flows_by_source[src])
    stroke_width = 3 + (avg_flow / max_flow) * 12

    # Add all chords from this source as one series with the continent name
    chart.add(
        continents[src],
        all_chord_points,
        stroke=True,
        show_dots=False,
        fill=False,
        stroke_style={"width": stroke_width, "linecap": "round"},
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
