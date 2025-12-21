""" pyplots.ai
quiver-basic: Basic Quiver Plot
Library: pygal 3.1.0 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-16
"""

import math

import cairosvg
import numpy as np


# Data - 2D rotation flow field: u = -y, v = x (creates circular pattern)
np.random.seed(42)
grid_size = 12
x_range = np.linspace(-3, 3, grid_size)
y_range = np.linspace(-3, 3, grid_size)
X, Y = np.meshgrid(x_range, y_range)

# Vector field: rotation around origin
U = -Y  # Horizontal component
V = X  # Vertical component

# Flatten arrays
x_flat = X.flatten()
y_flat = Y.flatten()
u_flat = U.flatten()
v_flat = V.flatten()

# Compute magnitudes for color mapping
magnitudes = np.sqrt(u_flat**2 + v_flat**2)
max_mag = magnitudes.max()

# Chart dimensions
width = 4800
height = 2700
margin_left = 300
margin_right = 200
margin_top = 250
margin_bottom = 250

plot_width = width - margin_left - margin_right
plot_height = height - margin_top - margin_bottom

# Data ranges
x_min, x_max = -4, 4
y_min, y_max = -4, 4


def data_to_pixel(x, y):
    """Convert data coordinates to pixel coordinates."""
    px = margin_left + (x - x_min) / (x_max - x_min) * plot_width
    py = margin_top + plot_height - (y - y_min) / (y_max - y_min) * plot_height
    return px, py


def magnitude_to_color(mag, max_mag):
    """Map magnitude to color gradient (Python Blue to Python Yellow)."""
    # Normalize magnitude to 0-1
    t = mag / max_mag if max_mag > 0 else 0

    # Interpolate between Python Blue (#306998) and Python Yellow (#FFD43B)
    r1, g1, b1 = 0x30, 0x69, 0x98  # Python Blue
    r2, g2, b2 = 0xFF, 0xD4, 0x3B  # Python Yellow

    r = int(r1 + (r2 - r1) * t)
    g = int(g1 + (g2 - g1) * t)
    b = int(b1 + (b2 - b1) * t)

    return f"#{r:02x}{g:02x}{b:02x}"


def create_arrow_path(x1, y1, x2, y2, head_size=20):
    """Create SVG path for an arrow with arrowhead."""
    # Vector from start to end
    dx = x2 - x1
    dy = y2 - y1
    length = math.sqrt(dx * dx + dy * dy)

    if length < 1:
        return None

    # Unit vector
    ux = dx / length
    uy = dy / length

    # Perpendicular vector
    px = -uy
    py = ux

    # Arrowhead points
    head_x1 = x2 - head_size * ux + head_size * 0.4 * px
    head_y1 = y2 - head_size * uy + head_size * 0.4 * py
    head_x2 = x2 - head_size * ux - head_size * 0.4 * px
    head_y2 = y2 - head_size * uy - head_size * 0.4 * py

    # SVG path: line + arrowhead
    path = f"M {x1} {y1} L {x2} {y2} "
    path += f"M {x2} {y2} L {head_x1} {head_y1} M {x2} {y2} L {head_x2} {head_y2}"

    return path


# Scale factor for arrows
arrow_scale = 80  # pixels per unit vector


# Create base SVG with pygal-style styling
svg_parts = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
    "  <defs>",
    '    <style type="text/css">',
    "      .title { font-family: sans-serif; font-size: 72px; font-weight: bold; fill: #333333; }",
    "      .axis-label { font-family: sans-serif; font-size: 48px; fill: #333333; }",
    "      .tick-label { font-family: sans-serif; font-size: 36px; fill: #666666; }",
    "      .grid { stroke: #cccccc; stroke-width: 1; stroke-dasharray: 5,5; }",
    "      .axis { stroke: #333333; stroke-width: 3; }",
    "    </style>",
    "  </defs>",
    '  <rect width="100%" height="100%" fill="white"/>',
]

# Title
svg_parts.append(
    f'  <text x="{width / 2}" y="100" text-anchor="middle" class="title">'
    "Rotation Flow Field · quiver-basic · pygal · pyplots.ai</text>"
)

# Plot background
svg_parts.append(
    f'  <rect x="{margin_left}" y="{margin_top}" '
    f'width="{plot_width}" height="{plot_height}" fill="white" stroke="#333333" stroke-width="2"/>'
)

# Grid lines
for i in range(9):
    val = x_min + (x_max - x_min) * i / 8
    px, _ = data_to_pixel(val, 0)
    # Vertical grid line
    svg_parts.append(f'  <line x1="{px}" y1="{margin_top}" x2="{px}" y2="{margin_top + plot_height}" class="grid"/>')
    # X tick label
    label = f"{val:.0f}" if val == int(val) else f"{val:.1f}"
    svg_parts.append(
        f'  <text x="{px}" y="{margin_top + plot_height + 50}" text-anchor="middle" class="tick-label">{label}</text>'
    )

for i in range(9):
    val = y_min + (y_max - y_min) * i / 8
    _, py = data_to_pixel(0, val)
    # Horizontal grid line
    svg_parts.append(f'  <line x1="{margin_left}" y1="{py}" x2="{margin_left + plot_width}" y2="{py}" class="grid"/>')
    # Y tick label
    label = f"{val:.0f}" if val == int(val) else f"{val:.1f}"
    svg_parts.append(
        f'  <text x="{margin_left - 20}" y="{py + 10}" text-anchor="end" class="tick-label">{label}</text>'
    )

# Axis labels
svg_parts.append(
    f'  <text x="{width / 2}" y="{height - 80}" text-anchor="middle" class="axis-label">X Coordinate</text>'
)
svg_parts.append(
    f'  <text x="80" y="{height / 2}" text-anchor="middle" class="axis-label" '
    f'transform="rotate(-90, 80, {height / 2})">Y Coordinate</text>'
)

# Draw arrows
for i in range(len(x_flat)):
    mag = magnitudes[i]
    if mag > 0.01:  # Skip near-zero vectors
        # Base point in pixels
        px1, py1 = data_to_pixel(x_flat[i], y_flat[i])

        # Scale vector for display (normalize then scale by magnitude)
        scale = min(mag, max_mag) / max_mag * arrow_scale
        dx_px = u_flat[i] / mag * scale
        dy_px = -v_flat[i] / mag * scale  # Negative because y increases downward in SVG

        # Tip point
        px2 = px1 + dx_px
        py2 = py1 + dy_px

        # Get color based on magnitude
        color = magnitude_to_color(mag, max_mag)

        # Create arrow path
        arrow_path = create_arrow_path(px1, py1, px2, py2, head_size=15)
        if arrow_path:
            svg_parts.append(
                f'  <path d="{arrow_path}" fill="none" stroke="{color}" '
                f'stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
            )

# Add color legend (magnitude scale)
legend_x = width - 180
legend_y = margin_top + 50
legend_height = 300
legend_width = 30

# Gradient for legend
svg_parts.append("  <defs>")
svg_parts.append('    <linearGradient id="magGradient" x1="0%" y1="100%" x2="0%" y2="0%">')
svg_parts.append('      <stop offset="0%" style="stop-color:#306998;stop-opacity:1" />')
svg_parts.append('      <stop offset="100%" style="stop-color:#FFD43B;stop-opacity:1" />')
svg_parts.append("    </linearGradient>")
svg_parts.append("  </defs>")

svg_parts.append(
    f'  <rect x="{legend_x}" y="{legend_y}" width="{legend_width}" height="{legend_height}" '
    f'fill="url(#magGradient)" stroke="#333333" stroke-width="1"/>'
)

# Legend labels
svg_parts.append(
    f'  <text x="{legend_x + legend_width + 15}" y="{legend_y + 10}" class="tick-label" '
    f'font-size="32">{max_mag:.1f}</text>'
)
svg_parts.append(
    f'  <text x="{legend_x + legend_width + 15}" y="{legend_y + legend_height}" class="tick-label" '
    f'font-size="32">0.0</text>'
)
svg_parts.append(
    f'  <text x="{legend_x + legend_width / 2}" y="{legend_y - 20}" text-anchor="middle" class="tick-label" '
    f'font-size="28">Magnitude</text>'
)

# Close SVG
svg_parts.append("</svg>")

svg_content = "\n".join(svg_parts)

# Save as SVG (HTML for interactivity)
with open("plot.html", "w") as f:
    f.write(svg_content)

# Convert to PNG using cairosvg
cairosvg.svg2png(bytestring=svg_content.encode("utf-8"), write_to="plot.png", output_width=4800, output_height=2700)
