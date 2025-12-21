""" pyplots.ai
chord-basic: Basic Chord Diagram
Library: pygal 3.1.0 | Python 3.13.11
Quality: 89/100 | Created: 2025-12-14
"""

import math

import cairosvg


# Data - Migration flows between continents (bidirectional)
# Each tuple: (source, target, flow_value)
flows = [
    ("Europe", "North America", 45),
    ("North America", "Europe", 38),
    ("Europe", "Asia", 32),
    ("Asia", "Europe", 28),
    ("Asia", "North America", 25),
    ("North America", "Asia", 20),
    ("Africa", "Europe", 35),
    ("Europe", "Africa", 12),
    ("South America", "North America", 30),
    ("North America", "South America", 15),
    ("Asia", "Africa", 18),
    ("Africa", "Asia", 14),
    ("Oceania", "Asia", 12),
    ("Asia", "Oceania", 10),
    ("Europe", "Oceania", 8),
    ("Oceania", "Europe", 6),
    ("South America", "Europe", 22),
    ("Europe", "South America", 10),
]

# Entity names (continents)
entities = ["Europe", "North America", "Asia", "Africa", "South America", "Oceania"]

# Colors for each entity - Python colors first, then complementary
entity_colors = {
    "Europe": "#306998",  # Python Blue
    "North America": "#FFD43B",  # Python Yellow
    "Asia": "#4ECDC4",  # Teal
    "Africa": "#FF6B6B",  # Coral
    "South America": "#9B59B6",  # Purple
    "Oceania": "#2ECC71",  # Green
}

# Canvas dimensions (4800x2700 px as per spec)
width = 4800
height = 2700
cx = width / 2
cy = height / 2 + 80  # Slightly offset for title

# Chord diagram parameters
outer_radius = 900
inner_radius = 850
chord_padding = 0.02  # Gap between arc segments (radians)


def polar_to_cartesian(cx, cy, radius, angle_rad):
    """Convert polar coordinates to Cartesian."""
    return cx + radius * math.cos(angle_rad), cy + radius * math.sin(angle_rad)


def arc_path(cx, cy, radius, start_angle, end_angle):
    """Create SVG arc path for outer ring segment."""
    x1, y1 = polar_to_cartesian(cx, cy, radius, start_angle)
    x2, y2 = polar_to_cartesian(cx, cy, radius, end_angle)
    large_arc = 1 if (end_angle - start_angle) > math.pi else 0
    return f"M {x1} {y1} A {radius} {radius} 0 {large_arc} 1 {x2} {y2}"


def chord_path(cx, cy, radius, start1, end1, start2, end2):
    """Create SVG path for a chord connecting two arc segments."""
    # Points on first arc
    x1_start, y1_start = polar_to_cartesian(cx, cy, radius, start1)
    x1_end, y1_end = polar_to_cartesian(cx, cy, radius, end1)

    # Points on second arc
    x2_start, y2_start = polar_to_cartesian(cx, cy, radius, start2)
    x2_end, y2_end = polar_to_cartesian(cx, cy, radius, end2)

    # Bezier control points (through center area)
    ctrl_factor = 0.6  # Controls curve tightness

    # Build path: arc1 -> bezier to arc2 start -> arc2 -> bezier back to arc1 start
    path = f"M {x1_start} {y1_start} "

    # Arc along first segment
    large_arc1 = 1 if (end1 - start1) > math.pi else 0
    path += f"A {radius} {radius} 0 {large_arc1} 1 {x1_end} {y1_end} "

    # Bezier curve to second arc start
    ctrl1_x = cx + (x1_end - cx) * ctrl_factor
    ctrl1_y = cy + (y1_end - cy) * ctrl_factor
    ctrl2_x = cx + (x2_start - cx) * ctrl_factor
    ctrl2_y = cy + (y2_start - cy) * ctrl_factor
    path += f"Q {ctrl1_x} {ctrl1_y} {cx} {cy} "
    path += f"Q {ctrl2_x} {ctrl2_y} {x2_start} {y2_start} "

    # Arc along second segment
    large_arc2 = 1 if (end2 - start2) > math.pi else 0
    path += f"A {radius} {radius} 0 {large_arc2} 1 {x2_end} {y2_end} "

    # Bezier curve back to start
    ctrl3_x = cx + (x2_end - cx) * ctrl_factor
    ctrl3_y = cy + (y2_end - cy) * ctrl_factor
    ctrl4_x = cx + (x1_start - cx) * ctrl_factor
    ctrl4_y = cy + (y1_start - cy) * ctrl_factor
    path += f"Q {ctrl3_x} {ctrl3_y} {cx} {cy} "
    path += f"Q {ctrl4_x} {ctrl4_y} {x1_start} {y1_start} "

    path += "Z"
    return path


# Calculate total flow for each entity
entity_totals = dict.fromkeys(entities, 0)
for src, tgt, val in flows:
    entity_totals[src] += val
    entity_totals[tgt] += val

total_flow = sum(entity_totals.values())

# Calculate arc angles for each entity
arc_angles = {}
current_angle = -math.pi / 2  # Start from top

for entity in entities:
    # Angle span proportional to total connections
    span = (entity_totals[entity] / total_flow) * (2 * math.pi - len(entities) * chord_padding)
    arc_angles[entity] = {
        "start": current_angle,
        "end": current_angle + span,
        "flow_offset": 0,  # Track where next chord starts within this arc
    }
    current_angle += span + chord_padding

# Build SVG content
svg_elements = []

# Title
title = "Migration Flows · chord-basic · pygal · pyplots.ai"
svg_elements.append(
    f'<text x="{cx}" y="80" font-size="72" font-weight="bold" '
    f'text-anchor="middle" fill="#333333" font-family="Arial, sans-serif">{title}</text>'
)

# Draw outer arc segments for each entity
for entity in entities:
    angles = arc_angles[entity]
    color = entity_colors[entity]

    # Outer arc (thicker ring segment)
    x1, y1 = polar_to_cartesian(cx, cy, inner_radius, angles["start"])
    x2, y2 = polar_to_cartesian(cx, cy, inner_radius, angles["end"])
    x3, y3 = polar_to_cartesian(cx, cy, outer_radius, angles["end"])
    x4, y4 = polar_to_cartesian(cx, cy, outer_radius, angles["start"])

    large_arc = 1 if (angles["end"] - angles["start"]) > math.pi else 0

    arc_segment = f"M {x1} {y1} "
    arc_segment += f"A {inner_radius} {inner_radius} 0 {large_arc} 1 {x2} {y2} "
    arc_segment += f"L {x3} {y3} "
    arc_segment += f"A {outer_radius} {outer_radius} 0 {large_arc} 0 {x4} {y4} "
    arc_segment += "Z"

    svg_elements.append(f'<path d="{arc_segment}" fill="{color}" stroke="white" stroke-width="2"/>')

    # Entity label
    mid_angle = (angles["start"] + angles["end"]) / 2
    label_radius = outer_radius + 60
    lx, ly = polar_to_cartesian(cx, cy, label_radius, mid_angle)

    # Adjust text anchor based on position
    if mid_angle < -math.pi / 2 or mid_angle > math.pi / 2:
        text_anchor = "end"
    elif abs(mid_angle + math.pi / 2) < 0.1 or abs(mid_angle - math.pi / 2) < 0.1:
        text_anchor = "middle"
    else:
        text_anchor = "start"

    # Rotate label for readability
    rotation = math.degrees(mid_angle) + 90
    if rotation > 90 and rotation < 270:
        rotation += 180

    svg_elements.append(
        f'<text x="{lx}" y="{ly}" font-size="42" font-weight="bold" '
        f'text-anchor="{text_anchor}" dominant-baseline="middle" '
        f'fill="{color}" font-family="Arial, sans-serif">{entity}</text>'
    )

# Calculate chord positions and draw them
# Track used angles for each entity
entity_used = dict.fromkeys(entities, 0)

for src, tgt, val in flows:
    src_angles = arc_angles[src]
    tgt_angles = arc_angles[tgt]
    color = entity_colors[src]

    # Calculate angle span for this flow
    src_span = (val / entity_totals[src]) * (src_angles["end"] - src_angles["start"])
    tgt_span = (val / entity_totals[tgt]) * (tgt_angles["end"] - tgt_angles["start"])

    # Start positions within each entity's arc
    src_start = src_angles["start"] + entity_used[src]
    src_end = src_start + src_span

    tgt_start = tgt_angles["start"] + entity_used[tgt]
    tgt_end = tgt_start + tgt_span

    # Update used angles
    entity_used[src] += src_span
    entity_used[tgt] += tgt_span

    # Draw chord
    path = chord_path(cx, cy, inner_radius, src_start, src_end, tgt_start, tgt_end)
    svg_elements.append(f'<path d="{path}" fill="{color}" fill-opacity="0.6" stroke="none"/>')

# Add legend
legend_x = 100
legend_y = height - 350
svg_elements.append(
    f'<text x="{legend_x}" y="{legend_y - 50}" font-size="36" font-weight="bold" '
    f'fill="#333333" font-family="Arial, sans-serif">Continents</text>'
)

for i, entity in enumerate(entities):
    y_pos = legend_y + i * 50
    color = entity_colors[entity]
    total = entity_totals[entity] // 2  # Divide by 2 since counted in both directions
    svg_elements.append(f'<rect x="{legend_x}" y="{y_pos - 15}" width="30" height="30" fill="{color}"/>')
    svg_elements.append(
        f'<text x="{legend_x + 45}" y="{y_pos + 5}" font-size="32" '
        f'fill="#333333" font-family="Arial, sans-serif">{entity} ({total}M migrants)</text>'
    )

# Assemble full SVG
svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="white"/>
  {"".join(svg_elements)}
</svg>'''

# Save as HTML for interactive viewing
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>chord-basic · pygal · pyplots.ai</title>
    <style>
        body {{ margin: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; background: #f5f5f5; }}
        svg {{ max-width: 100%; height: auto; background: white; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
    </style>
</head>
<body>
{svg_content}
</body>
</html>"""

with open("plot.html", "w") as f:
    f.write(html_content)

# Convert to PNG using cairosvg
cairosvg.svg2png(bytestring=svg_content.encode("utf-8"), write_to="plot.png", output_width=width, output_height=height)
