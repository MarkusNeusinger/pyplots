""" pyplots.ai
rose-basic: Basic Rose Chart
Library: pygal 3.1.0 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-17
"""

import math

import cairosvg


# Data - Monthly rainfall (mm) showing natural cyclical pattern
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
rainfall = [78, 62, 55, 42, 38, 52, 65, 72, 85, 98, 102, 89]

# Chart parameters
width, height = 4800, 2700
cx, cy = width // 2, height // 2 + 50  # center of chart, slight offset for title
max_radius = min(width, height) // 2 - 350  # leave margin for labels
max_value = max(rainfall)
n_sectors = len(months)
angle_per_sector = 360 / n_sectors

# Style settings (matching pygal conventions)
color = "#306998"  # Python blue
bg_color = "white"
text_color = "#333333"
grid_color = "#cccccc"
title_font_size = 72
label_font_size = 48
grid_label_size = 36

# Build SVG content
svg_parts = []

# Background
svg_parts.append(f'<rect width="{width}" height="{height}" fill="{bg_color}"/>')

# Title
title = "Monthly Rainfall (mm) · rose-basic · pygal · pyplots.ai"
svg_parts.append(
    f'<text x="{width // 2}" y="100" text-anchor="middle" '
    f'font-family="sans-serif" font-size="{title_font_size}" fill="{text_color}">{title}</text>'
)

# Draw radial gridlines (concentric circles)
grid_values = [20, 40, 60, 80, 100]
for grid_val in grid_values:
    r = (grid_val / max_value) * max_radius
    svg_parts.append(
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{grid_color}" '
        f'stroke-width="1.5" stroke-dasharray="5,5"/>'
    )
    # Grid value labels (positioned to the right of center)
    svg_parts.append(
        f'<text x="{cx + r + 10}" y="{cy + 12}" font-family="sans-serif" '
        f'font-size="{grid_label_size}" fill="#666666">{grid_val}</text>'
    )

# Draw angular gridlines (spokes)
for i in range(n_sectors):
    angle_rad = math.radians(-90 + i * angle_per_sector)
    x_end = cx + (max_radius + 20) * math.cos(angle_rad)
    y_end = cy + (max_radius + 20) * math.sin(angle_rad)
    svg_parts.append(f'<line x1="{cx}" y1="{cy}" x2="{x_end}" y2="{y_end}" stroke="{grid_color}" stroke-width="1"/>')

# Draw sectors (wedges) - core of the rose chart
for i, value in enumerate(rainfall):
    # Calculate angles (starting from top/-90°, going clockwise)
    start_angle = -90 + i * angle_per_sector
    end_angle = start_angle + angle_per_sector

    # Calculate radius proportional to value
    radius = (value / max_value) * max_radius

    # Convert to radians
    start_rad = math.radians(start_angle)
    end_rad = math.radians(end_angle)

    # Calculate arc endpoints
    x1 = cx + radius * math.cos(start_rad)
    y1 = cy + radius * math.sin(start_rad)
    x2 = cx + radius * math.cos(end_rad)
    y2 = cy + radius * math.sin(end_rad)

    # SVG path for sector (arc from center)
    # M = move to center, L = line to arc start, A = arc, Z = close path
    large_arc = 1 if angle_per_sector > 180 else 0
    path = f"M {cx},{cy} L {x1},{y1} A {radius},{radius} 0 {large_arc},1 {x2},{y2} Z"
    svg_parts.append(f'<path d="{path}" fill="{color}" fill-opacity="0.85" stroke="white" stroke-width="3"/>')

# Draw month labels around the chart
for i, month in enumerate(months):
    mid_angle = -90 + i * angle_per_sector + angle_per_sector / 2
    mid_rad = math.radians(mid_angle)
    label_radius = max_radius + 80
    lx = cx + label_radius * math.cos(mid_rad)
    ly = cy + label_radius * math.sin(mid_rad)

    svg_parts.append(
        f'<text x="{lx}" y="{ly}" text-anchor="middle" dominant-baseline="middle" '
        f'font-family="sans-serif" font-size="{label_font_size}" fill="{text_color}">{month}</text>'
    )

# Compose final SVG
svg_content = f"""<?xml version="1.0" encoding="utf-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
{chr(10).join(svg_parts)}
</svg>"""

# Save as HTML (SVG wrapped for browser viewing, like pygal's render_to_file)
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>rose-basic · pygal · pyplots.ai</title>
    <style>body {{ margin: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; background: #f5f5f5; }}</style>
</head>
<body>
{svg_content}
</body>
</html>"""

with open("plot.html", "w") as f:
    f.write(html_content)

# Save as PNG using cairosvg (same as pygal's render_to_png)
cairosvg.svg2png(bytestring=svg_content.encode("utf-8"), write_to="plot.png")
