"""
sunburst-basic: Basic Sunburst Chart
Library: pygal

Note: pygal does not have native sunburst chart support.
This implementation creates a sunburst using custom SVG generation
with cairosvg for PNG export, following pygal's visual style.
"""

import math

import cairosvg


# Data - Company budget breakdown by department, team, and project
# Hierarchical structure: Department > Team > Project
hierarchy = {
    "Engineering": {
        "Backend": {"API": 180, "Database": 120},
        "Frontend": {"Web App": 150, "Mobile": 100},
        "DevOps": {"Cloud": 90, "CI/CD": 60},
    },
    "Sales": {"Enterprise": {"APAC": 100, "EMEA": 85}, "SMB": {"Direct": 65, "Partners": 45}},
    "Marketing": {"Digital": {"SEO": 80, "Social": 70}, "Content": {"Blog": 50, "Video": 60}},
    "Operations": {"Support": {"Tier 1": 70, "Tier 2": 50}, "HR": {"Recruiting": 60, "Training": 40}},
}

# Colors - Python colors as primary, with variations for children
dept_colors = {
    "Engineering": "#306998",  # Python Blue
    "Sales": "#FFD43B",  # Python Yellow
    "Marketing": "#4ECDC4",  # Teal
    "Operations": "#FF6B6B",  # Coral
}


def lighten_color(hex_color, factor=0.3):
    """Lighten a hex color by mixing with white."""
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    r = int(r + (255 - r) * factor)
    g = int(g + (255 - g) * factor)
    b = int(b + (255 - b) * factor)
    return f"#{r:02x}{g:02x}{b:02x}"


# Flatten hierarchy and calculate values for each level
level1_data = []
level2_data = []
level3_data = []

for dept, teams in hierarchy.items():
    dept_total = sum(sum(projects.values()) for projects in teams.values())
    level1_data.append({"name": dept, "value": dept_total, "color": dept_colors[dept]})

    for team, projects in teams.items():
        team_total = sum(projects.values())
        level2_data.append(
            {"name": team, "value": team_total, "parent": dept, "color": lighten_color(dept_colors[dept], 0.25)}
        )

        for project, value in projects.items():
            level3_data.append(
                {
                    "name": project,
                    "value": value,
                    "parent_team": team,
                    "parent_dept": dept,
                    "color": lighten_color(dept_colors[dept], 0.5),
                }
            )

# Calculate totals
total_value = sum(d["value"] for d in level1_data)

# Chart dimensions
width = 4800
height = 2700
cx = width / 2  # Center x
cy = height / 2 + 100  # Center y (offset for title)

# Ring radii
r1_inner, r1_outer = 200, 400  # Level 1 (innermost)
r2_inner, r2_outer = 420, 620  # Level 2 (middle)
r3_inner, r3_outer = 640, 840  # Level 3 (outermost)


def polar_to_cartesian(cx, cy, radius, angle_deg):
    """Convert polar coordinates to Cartesian."""
    angle_rad = math.radians(angle_deg - 90)  # Start from top
    return cx + radius * math.cos(angle_rad), cy + radius * math.sin(angle_rad)


def arc_path(cx, cy, r_inner, r_outer, start_angle, end_angle):
    """Create SVG path for an arc segment (donut slice)."""
    # Handle full circle case
    if abs(end_angle - start_angle) >= 360:
        end_angle = start_angle + 359.99

    large_arc = 1 if (end_angle - start_angle) > 180 else 0

    # Outer arc points
    x1_outer, y1_outer = polar_to_cartesian(cx, cy, r_outer, start_angle)
    x2_outer, y2_outer = polar_to_cartesian(cx, cy, r_outer, end_angle)

    # Inner arc points
    x1_inner, y1_inner = polar_to_cartesian(cx, cy, r_inner, end_angle)
    x2_inner, y2_inner = polar_to_cartesian(cx, cy, r_inner, start_angle)

    # SVG path: outer arc, line to inner, inner arc (reverse), close
    path = f"M {x1_outer} {y1_outer} "
    path += f"A {r_outer} {r_outer} 0 {large_arc} 1 {x2_outer} {y2_outer} "
    path += f"L {x1_inner} {y1_inner} "
    path += f"A {r_inner} {r_inner} 0 {large_arc} 0 {x2_inner} {y2_inner} "
    path += "Z"

    return path


def text_position(cx, cy, r_inner, r_outer, start_angle, end_angle):
    """Calculate text position at center of arc segment."""
    mid_angle = (start_angle + end_angle) / 2
    mid_radius = (r_inner + r_outer) / 2
    x, y = polar_to_cartesian(cx, cy, mid_radius, mid_angle)
    # Calculate rotation for radial text
    rotation = mid_angle if mid_angle <= 180 else mid_angle - 180
    return x, y, rotation


# Create base SVG with pygal-style styling
svg_parts = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
    '  <rect width="100%" height="100%" fill="white"/>',
    f'  <text x="{cx}" y="80" text-anchor="middle" font-size="72" font-weight="bold" fill="#333333">',
    "    sunburst-basic · pygal · pyplots.ai",
    "  </text>",
]

# Draw Level 1 (innermost ring) - Departments
angle_offset = 0
level1_angles = {}
for item in level1_data:
    angle_span = (item["value"] / total_value) * 360
    end_angle = angle_offset + angle_span

    path = arc_path(cx, cy, r1_inner, r1_outer, angle_offset, end_angle)
    svg_parts.append(f'  <path d="{path}" fill="{item["color"]}" stroke="white" stroke-width="3"/>')

    # Store angles for children
    level1_angles[item["name"]] = {"start": angle_offset, "end": end_angle, "total": item["value"]}

    # Add label for level 1 (department names)
    x, y, rotation = text_position(cx, cy, r1_inner, r1_outer, angle_offset, end_angle)
    svg_parts.append(
        f'  <text x="{x}" y="{y}" text-anchor="middle" dominant-baseline="middle" '
        f'font-size="36" font-weight="bold" fill="white">{item["name"]}</text>'
    )

    angle_offset = end_angle

# Draw Level 2 (middle ring) - Teams
level2_angles = {}
for dept_name, dept_angles in level1_angles.items():
    dept_items = [d for d in level2_data if d["parent"] == dept_name]
    current_angle = dept_angles["start"]

    for item in dept_items:
        angle_span = (item["value"] / dept_angles["total"]) * (dept_angles["end"] - dept_angles["start"])
        end_angle = current_angle + angle_span

        path = arc_path(cx, cy, r2_inner, r2_outer, current_angle, end_angle)
        svg_parts.append(f'  <path d="{path}" fill="{item["color"]}" stroke="white" stroke-width="2"/>')

        # Store angles for children
        level2_angles[f"{dept_name}|{item['name']}"] = {
            "start": current_angle,
            "end": end_angle,
            "total": item["value"],
        }

        # Add label for level 2 (only if segment is large enough)
        if angle_span > 20:
            x, y, rotation = text_position(cx, cy, r2_inner, r2_outer, current_angle, end_angle)
            svg_parts.append(
                f'  <text x="{x}" y="{y}" text-anchor="middle" dominant-baseline="middle" '
                f'font-size="28" fill="#333333">{item["name"]}</text>'
            )

        current_angle = end_angle

# Draw Level 3 (outer ring) - Projects
for item in level3_data:
    key = f"{item['parent_dept']}|{item['parent_team']}"
    parent_angles = level2_angles[key]
    angle_span = (item["value"] / parent_angles["total"]) * (parent_angles["end"] - parent_angles["start"])

    if "current" not in parent_angles:
        parent_angles["current"] = parent_angles["start"]

    start_angle = parent_angles["current"]
    end_angle = start_angle + angle_span

    path = arc_path(cx, cy, r3_inner, r3_outer, start_angle, end_angle)
    svg_parts.append(f'  <path d="{path}" fill="{item["color"]}" stroke="white" stroke-width="1.5"/>')

    # Add label for level 3 (only if segment is large enough)
    if angle_span > 15:
        x, y, rotation = text_position(cx, cy, r3_inner, r3_outer, start_angle, end_angle)
        svg_parts.append(
            f'  <text x="{x}" y="{y}" text-anchor="middle" dominant-baseline="middle" '
            f'font-size="22" fill="#555555">{item["name"]}</text>'
        )

    parent_angles["current"] = end_angle

# Add legend
legend_x = width - 400
legend_y = 200
for i, item in enumerate(level1_data):
    y_pos = legend_y + i * 60
    svg_parts.append(f'  <rect x="{legend_x}" y="{y_pos}" width="40" height="40" fill="{item["color"]}"/>')
    svg_parts.append(
        f'  <text x="{legend_x + 55}" y="{y_pos + 28}" font-size="32" fill="#333333">'
        f"{item['name']}: ${item['value']}K</text>"
    )

# Close SVG
svg_parts.append("</svg>")

svg_content = "\n".join(svg_parts)

# Save as SVG (HTML for interactivity)
with open("plot.html", "w") as f:
    f.write(svg_content)

# Convert to PNG using cairosvg
cairosvg.svg2png(bytestring=svg_content.encode("utf-8"), write_to="plot.png", output_width=4800, output_height=2700)
