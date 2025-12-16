"""
quiver-basic: Basic Quiver Plot
Library: highcharts
"""

import math
import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - Create a 15x15 grid with circular rotation pattern (u = -y, v = x)
np.random.seed(42)
grid_size = 15
x_range = np.linspace(-2, 2, grid_size)
y_range = np.linspace(-2, 2, grid_size)
X, Y = np.meshgrid(x_range, y_range)

# Circular rotation field: u = -y, v = x
U = -Y
V = X

# Flatten for iteration
x_flat = X.flatten()
y_flat = Y.flatten()
u_flat = U.flatten()
v_flat = V.flatten()

# Chart dimensions
chart_width = 4800
chart_height = 2700

# Compute plot area (accounting for margins)
margin_left = 200
margin_right = 100
margin_top = 200
margin_bottom = 150
plot_width = chart_width - margin_left - margin_right
plot_height = chart_height - margin_top - margin_bottom

# Data ranges
x_min, x_max = -2.5, 2.5
y_min, y_max = -2.5, 2.5

# Arrow scaling - scale arrows to be visible but not overlapping
arrow_scale = 60  # Pixels per unit vector magnitude


def data_to_pixel(data_x, data_y):
    """Convert data coordinates to pixel coordinates."""
    px = margin_left + (data_x - x_min) / (x_max - x_min) * plot_width
    # Y is inverted in pixel coordinates
    py = margin_top + (y_max - data_y) / (y_max - y_min) * plot_height
    return px, py


def create_arrow_svg(x, y, u, v, color="#306998", head_size=15, line_width=4):
    """Create SVG path for an arrow from (x,y) with direction (u,v)."""
    # Convert to pixel coordinates
    start_px, start_py = data_to_pixel(x, y)

    # Calculate magnitude for scaling
    mag = math.sqrt(u**2 + v**2)
    if mag < 0.01:
        return ""  # Skip very small vectors

    # Normalize and scale to pixel length
    dx = (u / mag) * mag * arrow_scale
    dy = -(v / mag) * mag * arrow_scale  # Negative because Y is inverted

    end_px = start_px + dx
    end_py = start_py + dy

    # Calculate arrow head
    angle = math.atan2(dy, dx)
    head_angle = math.pi / 6  # 30 degrees

    # Arrow head points
    head_x1 = end_px - head_size * math.cos(angle - head_angle)
    head_y1 = end_py - head_size * math.sin(angle - head_angle)
    head_x2 = end_px - head_size * math.cos(angle + head_angle)
    head_y2 = end_py - head_size * math.sin(angle + head_angle)

    # SVG path for line and arrow head
    path = f'<path d="M{start_px},{start_py} L{end_px},{end_py}" stroke="{color}" stroke-width="{line_width}" fill="none"/>'
    path += f'<polygon points="{end_px},{end_py} {head_x1},{head_y1} {head_x2},{head_y2}" fill="{color}"/>'

    return path


# Generate all arrow SVG elements
arrows_svg = []
for i in range(len(x_flat)):
    arrow = create_arrow_svg(x_flat[i], y_flat[i], u_flat[i], v_flat[i])
    if arrow:
        arrows_svg.append(arrow)

arrows_svg_str = "\n".join(arrows_svg)


# Create tick marks and labels for axes
def create_axis_elements():
    """Create SVG elements for axes, ticks, and labels."""
    svg_parts = []

    # X-axis line
    svg_parts.append(
        f'<line x1="{margin_left}" y1="{margin_top + plot_height}" '
        f'x2="{margin_left + plot_width}" y2="{margin_top + plot_height}" '
        f'stroke="#333" stroke-width="3"/>'
    )

    # Y-axis line
    svg_parts.append(
        f'<line x1="{margin_left}" y1="{margin_top}" '
        f'x2="{margin_left}" y2="{margin_top + plot_height}" '
        f'stroke="#333" stroke-width="3"/>'
    )

    # X-axis ticks and labels
    x_ticks = np.arange(-2, 2.5, 1)
    for tick in x_ticks:
        px, py = data_to_pixel(tick, y_min)
        svg_parts.append(
            f'<line x1="{px}" y1="{margin_top + plot_height}" '
            f'x2="{px}" y2="{margin_top + plot_height + 15}" stroke="#333" stroke-width="2"/>'
        )
        svg_parts.append(
            f'<text x="{px}" y="{margin_top + plot_height + 55}" '
            f'text-anchor="middle" font-size="36" fill="#333">{tick:.1f}</text>'
        )

    # Y-axis ticks and labels
    y_ticks = np.arange(-2, 2.5, 1)
    for tick in y_ticks:
        px, py = data_to_pixel(x_min, tick)
        svg_parts.append(
            f'<line x1="{margin_left - 15}" y1="{py}" x2="{margin_left}" y2="{py}" stroke="#333" stroke-width="2"/>'
        )
        svg_parts.append(
            f'<text x="{margin_left - 25}" y="{py + 12}" text-anchor="end" font-size="36" fill="#333">{tick:.1f}</text>'
        )

    # X-axis label
    svg_parts.append(
        f'<text x="{margin_left + plot_width / 2}" y="{chart_height - 40}" '
        f'text-anchor="middle" font-size="48" font-weight="bold" fill="#333">X Position</text>'
    )

    # Y-axis label (rotated)
    svg_parts.append(
        f'<text x="60" y="{margin_top + plot_height / 2}" '
        f'text-anchor="middle" font-size="48" font-weight="bold" fill="#333" '
        f'transform="rotate(-90, 60, {margin_top + plot_height / 2})">Y Position</text>'
    )

    # Grid lines
    for tick in x_ticks:
        px, _ = data_to_pixel(tick, 0)
        svg_parts.append(
            f'<line x1="{px}" y1="{margin_top}" x2="{px}" y2="{margin_top + plot_height}" '
            f'stroke="rgba(0,0,0,0.15)" stroke-width="1" stroke-dasharray="10,5"/>'
        )

    for tick in y_ticks:
        _, py = data_to_pixel(0, tick)
        svg_parts.append(
            f'<line x1="{margin_left}" y1="{py}" x2="{margin_left + plot_width}" y2="{py}" '
            f'stroke="rgba(0,0,0,0.15)" stroke-width="1" stroke-dasharray="10,5"/>'
        )

    return "\n".join(svg_parts)


axis_svg = create_axis_elements()

# Download Highcharts JS (for consistent styling with other implementations)
highcharts_url = "https://code.highcharts.com/highcharts.js"
with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

# Create full HTML/SVG content
# Using pure SVG approach since Highcharts doesn't have native quiver support
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{ margin: 0; padding: 0; background: white; }}
    </style>
</head>
<body>
    <div id="container" style="width: {chart_width}px; height: {chart_height}px;">
        <svg width="{chart_width}" height="{chart_height}" xmlns="http://www.w3.org/2000/svg">
            <!-- Background -->
            <rect width="100%" height="100%" fill="white"/>

            <!-- Title -->
            <text x="{chart_width / 2}" y="80" text-anchor="middle"
                  font-size="72" font-weight="bold" fill="#333">
                quiver-basic · highcharts · pyplots.ai
            </text>

            <!-- Subtitle -->
            <text x="{chart_width / 2}" y="140" text-anchor="middle"
                  font-size="42" fill="#666">
                Circular Rotation Vector Field
            </text>

            <!-- Plot area background -->
            <rect x="{margin_left}" y="{margin_top}" width="{plot_width}" height="{plot_height}"
                  fill="white" stroke="#ccc" stroke-width="1"/>

            <!-- Axes and grid -->
            {axis_svg}

            <!-- Arrows -->
            {arrows_svg_str}

            <!-- Legend -->
            <g transform="translate({chart_width - 350}, {margin_top + 50})">
                <rect x="0" y="0" width="280" height="100" fill="white" stroke="#ccc" stroke-width="1" rx="5"/>
                <path d="M20,50 L100,50" stroke="#306998" stroke-width="4" fill="none"/>
                <polygon points="100,50 85,42 85,58" fill="#306998"/>
                <text x="120" y="58" font-size="32" fill="#333">Velocity Vector</text>
            </g>
        </svg>
    </div>
</body>
</html>"""

# Write temp HTML and take screenshot
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=5000,3000")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(3)  # Wait for rendering

# Take screenshot of just the chart container element
container = driver.find_element("id", "container")
container.screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()  # Clean up temp file

# Also save HTML for interactive version
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)
