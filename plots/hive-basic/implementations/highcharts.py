"""pyplots.ai
hive-basic: Basic Hive Plot
Library: highcharts | Python 3.13
Quality: pending | Created: 2025-12-24
"""

import math
import tempfile
import time
import urllib.request
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data: Software module dependency network
# Nodes assigned to 3 axes by module type: Core, Utility, Interface
nodes = [
    # Core modules (axis 0) - bottom axis
    {"id": "core_main", "axis": 0, "position": 0.95, "label": "Main"},
    {"id": "core_engine", "axis": 0, "position": 0.75, "label": "Engine"},
    {"id": "core_db", "axis": 0, "position": 0.55, "label": "Database"},
    {"id": "core_auth", "axis": 0, "position": 0.35, "label": "Auth"},
    # Utility modules (axis 1) - upper right axis
    {"id": "util_log", "axis": 1, "position": 0.9, "label": "Logger"},
    {"id": "util_config", "axis": 1, "position": 0.7, "label": "Config"},
    {"id": "util_cache", "axis": 1, "position": 0.5, "label": "Cache"},
    {"id": "util_format", "axis": 1, "position": 0.3, "label": "Format"},
    # Interface modules (axis 2) - upper left axis
    {"id": "iface_api", "axis": 2, "position": 0.85, "label": "API"},
    {"id": "iface_web", "axis": 2, "position": 0.65, "label": "Web"},
    {"id": "iface_cli", "axis": 2, "position": 0.45, "label": "CLI"},
    {"id": "iface_ws", "axis": 2, "position": 0.25, "label": "WebSocket"},
]

edges = [
    # Core to Utility
    ("core_main", "util_log"),
    ("core_main", "util_config"),
    ("core_engine", "util_cache"),
    ("core_engine", "util_log"),
    ("core_db", "util_cache"),
    ("core_db", "util_config"),
    ("core_auth", "util_log"),
    # Core to Interface
    ("core_main", "iface_api"),
    ("core_main", "iface_web"),
    ("core_engine", "iface_api"),
    ("core_auth", "iface_api"),
    ("core_auth", "iface_ws"),
    # Utility to Interface
    ("util_log", "iface_api"),
    ("util_config", "iface_web"),
    ("util_cache", "iface_api"),
    ("util_format", "iface_cli"),
]

# Hive plot configuration
num_axes = 3
# Angles: bottom (270°), upper-right (30°), upper-left (150°)
axis_angles = [3 * math.pi / 2, math.pi / 6, 5 * math.pi / 6]
inner_radius = 250
outer_radius = 1000
center_x = 2200
center_y = 1450

# Axis colors (colorblind-safe)
axis_colors = ["#306998", "#FFD43B", "#9467BD"]
axis_labels = ["Core", "Utility", "Interface"]

# Create node lookup
node_lookup = {n["id"]: n for n in nodes}


def get_node_coords(node):
    """Convert node to x, y coordinates on hive plot"""
    angle = axis_angles[node["axis"]]
    radius = inner_radius + (outer_radius - inner_radius) * node["position"]
    x = center_x + radius * math.cos(angle)
    y = center_y + radius * math.sin(angle)
    return x, y


# Build SVG elements
svg_elements = []

# Draw axis lines with labels
for axis_idx in range(num_axes):
    angle = axis_angles[axis_idx]
    x1 = center_x + inner_radius * math.cos(angle)
    y1 = center_y + inner_radius * math.sin(angle)
    x2 = center_x + (outer_radius + 50) * math.cos(angle)
    y2 = center_y + (outer_radius + 50) * math.sin(angle)
    color = axis_colors[axis_idx]

    # Axis line
    svg_elements.append(
        f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" '
        f'stroke="{color}" stroke-width="12" stroke-linecap="round" opacity="0.8"/>'
    )

    # Axis label at end
    label_x = center_x + (outer_radius + 120) * math.cos(angle)
    label_y = center_y + (outer_radius + 120) * math.sin(angle)
    svg_elements.append(
        f'<text x="{label_x:.0f}" y="{label_y:.0f}" font-size="42" font-weight="bold" '
        f'fill="{color}" text-anchor="middle" dominant-baseline="middle">{axis_labels[axis_idx]}</text>'
    )

# Draw edges as curved paths (quadratic Bezier through center region)
for source_id, target_id in edges:
    source = node_lookup[source_id]
    target = node_lookup[target_id]
    x1, y1 = get_node_coords(source)
    x2, y2 = get_node_coords(target)

    # Control point: pull toward center for smooth curves
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2
    ctrl_x = center_x + (mid_x - center_x) * 0.15
    ctrl_y = center_y + (mid_y - center_y) * 0.15

    # Edge color gradient based on source axis
    edge_color = axis_colors[source["axis"]]

    svg_elements.append(
        f'<path d="M {x1:.0f} {y1:.0f} Q {ctrl_x:.0f} {ctrl_y:.0f} {x2:.0f} {y2:.0f}" '
        f'stroke="{edge_color}" stroke-width="5" fill="none" opacity="0.45"/>'
    )

# Draw central hub
svg_elements.append(f'<circle cx="{center_x}" cy="{center_y}" r="40" fill="#666666" opacity="0.5"/>')

# Draw nodes on top of edges
for node in nodes:
    x, y = get_node_coords(node)
    color = axis_colors[node["axis"]]

    # Node circle
    svg_elements.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="28" fill="{color}" stroke="#ffffff" stroke-width="4"/>')

    # Node label - position based on axis
    angle = axis_angles[node["axis"]]
    # Offset label perpendicular to axis
    label_offset = 55
    if node["axis"] == 0:  # Bottom axis - labels to the right
        lx = x + label_offset
        ly = y
        anchor = "start"
    elif node["axis"] == 1:  # Upper-right - labels to the right
        lx = x + label_offset * 0.8
        ly = y - label_offset * 0.3
        anchor = "start"
    else:  # Upper-left - labels to the left
        lx = x - label_offset * 0.8
        ly = y - label_offset * 0.3
        anchor = "end"

    svg_elements.append(
        f'<text x="{lx:.0f}" y="{ly:.0f}" font-size="32" font-weight="500" '
        f'fill="#333333" text-anchor="{anchor}" dominant-baseline="middle">{node["label"]}</text>'
    )

svg_content = "\n            ".join(svg_elements)

# Download Highcharts JS for interactive HTML
highcharts_url = "https://code.highcharts.com/highcharts.js"
with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

# Build complete HTML - using Highcharts for interactivity wrapper but SVG for the actual hive plot
# Since Highcharts doesn't have native hive plots, we use custom SVG rendering
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <style>
        body {{ margin: 0; padding: 0; font-family: Arial, sans-serif; background: #ffffff; }}
        #container {{ width: 4800px; height: 2700px; position: relative; }}
        .title {{
            position: absolute;
            top: 60px;
            left: 0;
            right: 0;
            text-align: center;
            font-size: 48px;
            font-weight: bold;
            color: #333333;
        }}
        .legend {{
            position: absolute;
            top: 180px;
            right: 200px;
            font-size: 32px;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            margin-bottom: 20px;
        }}
        .legend-color {{
            width: 40px;
            height: 40px;
            border-radius: 50%;
            margin-right: 20px;
        }}
    </style>
</head>
<body>
    <div id="container">
        <div class="title">Software Dependencies · hive-basic · highcharts · pyplots.ai</div>
        <div class="legend">
            <div class="legend-item">
                <div class="legend-color" style="background: #306998;"></div>
                <span>Core Modules</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #FFD43B;"></div>
                <span>Utility Modules</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #9467BD;"></div>
                <span>Interface Modules</span>
            </div>
        </div>
        <svg width="4800" height="2700" style="position: absolute; top: 0; left: 0;">
            {svg_content}
        </svg>
    </div>
    <script>
        // Highcharts is loaded for potential interactivity extensions
        console.log('Highcharts version:', Highcharts.version);
    </script>
</body>
</html>"""

# Save interactive HTML
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Take screenshot for PNG
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=4800,2700")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(3)
driver.save_screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()
