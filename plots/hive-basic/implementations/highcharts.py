""" pyplots.ai
hive-basic: Basic Hive Plot
Library: highcharts unknown | Python 3.13.11
Quality: 85/100 | Created: 2025-12-24
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

# Hive plot configuration - centered for better canvas utilization
num_axes = 3
axis_angles = [3 * math.pi / 2, math.pi / 6, 5 * math.pi / 6]  # bottom, upper-right, upper-left
inner_radius = 250
outer_radius = 950
center_x = 2400
center_y = 1450

# Axis colors (colorblind-safe) and labels
axis_colors = ["#306998", "#FFD43B", "#9467BD"]
axis_labels = ["Core", "Utility", "Interface"]

# Create node lookup and pre-compute coordinates inline
node_lookup = {n["id"]: n for n in nodes}
node_coords = {}
for node in nodes:
    angle = axis_angles[node["axis"]]
    radius = inner_radius + (outer_radius - inner_radius) * node["position"]
    node_coords[node["id"]] = (center_x + radius * math.cos(angle), center_y + radius * math.sin(angle))

# Download Highcharts JS
highcharts_url = "https://code.highcharts.com/highcharts.js"
with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

# Build Highcharts renderer commands for the hive plot
# Using Highcharts.SVGRenderer API to draw custom elements
renderer_commands = []

# Draw axis lines with labels
for axis_idx in range(num_axes):
    angle = axis_angles[axis_idx]
    x1 = center_x + inner_radius * math.cos(angle)
    y1 = center_y + inner_radius * math.sin(angle)
    x2 = center_x + (outer_radius + 50) * math.cos(angle)
    y2 = center_y + (outer_radius + 50) * math.sin(angle)
    color = axis_colors[axis_idx]

    renderer_commands.append(
        f"chart.renderer.path(['M', {x1:.0f}, {y1:.0f}, 'L', {x2:.0f}, {y2:.0f}])"
        f".attr({{stroke: '{color}', 'stroke-width': 12, 'stroke-linecap': 'round', opacity: 0.8}}).add();"
    )

    label_x = center_x + (outer_radius + 130) * math.cos(angle)
    label_y = center_y + (outer_radius + 130) * math.sin(angle)
    renderer_commands.append(
        f"chart.renderer.text('{axis_labels[axis_idx]}', {label_x:.0f}, {label_y:.0f})"
        f".attr({{align: 'center'}}).css({{fontSize: '42px', fontWeight: 'bold', color: '{color}'}}).add();"
    )

# Draw edges as curved paths using Highcharts renderer
for source_id, target_id in edges:
    source = node_lookup[source_id]
    x1, y1 = node_coords[source_id]
    x2, y2 = node_coords[target_id]

    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2
    ctrl_x = center_x + (mid_x - center_x) * 0.15
    ctrl_y = center_y + (mid_y - center_y) * 0.15
    edge_color = axis_colors[source["axis"]]

    renderer_commands.append(
        f"chart.renderer.path(['M', {x1:.0f}, {y1:.0f}, 'Q', {ctrl_x:.0f}, {ctrl_y:.0f}, {x2:.0f}, {y2:.0f}])"
        f".attr({{stroke: '{edge_color}', 'stroke-width': 5, fill: 'none', opacity: 0.45}}).add();"
    )

# Draw central hub
renderer_commands.append(
    f"chart.renderer.circle({center_x}, {center_y}, 45).attr({{fill: '#666666', opacity: 0.5}}).add();"
)

# Draw nodes and labels
for node in nodes:
    x, y = node_coords[node["id"]]
    color = axis_colors[node["axis"]]

    renderer_commands.append(
        f"chart.renderer.circle({x:.0f}, {y:.0f}, 28).attr({{fill: '{color}', stroke: '#ffffff', 'stroke-width': 4}}).add();"
    )

    label_offset = 55
    if node["axis"] == 0:
        lx, ly, align = x + label_offset, y, "left"
    elif node["axis"] == 1:
        lx, ly, align = x + label_offset * 0.8, y - label_offset * 0.3, "left"
    else:
        lx, ly, align = x - label_offset * 0.8, y - label_offset * 0.3, "right"

    renderer_commands.append(
        f"chart.renderer.text('{node['label']}', {lx:.0f}, {ly:.0f})"
        f".attr({{align: '{align}'}}).css({{fontSize: '32px', fontWeight: '500', color: '#333333'}}).add();"
    )

renderer_js = "\n        ".join(renderer_commands)

# Build legend items - labels match axis labels exactly
legend_items = ""
for i, label in enumerate(axis_labels):
    legend_items += f"""
            <div style="display: flex; align-items: center; margin-bottom: 20px;">
                <div style="width: 40px; height: 40px; border-radius: 50%; background: {axis_colors[i]}; margin-right: 20px;"></div>
                <span>{label}</span>
            </div>"""

# Build complete HTML using Highcharts chart and renderer API
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <style>
        body {{ margin: 0; padding: 0; font-family: Arial, sans-serif; background: #ffffff; }}
    </style>
</head>
<body>
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <div style="position: absolute; top: 180px; right: 200px; font-size: 32px;">
        {legend_items}
    </div>
    <script>
        var chart = Highcharts.chart('container', {{
            chart: {{
                width: 4800,
                height: 2700,
                backgroundColor: '#ffffff',
                events: {{
                    load: function() {{
                        var chart = this;
                        {renderer_js}
                    }}
                }}
            }},
            title: {{
                text: 'hive-basic · highcharts · pyplots.ai',
                style: {{ fontSize: '48px', fontWeight: 'bold', color: '#333333' }},
                y: 80
            }},
            credits: {{ enabled: false }},
            legend: {{ enabled: false }},
            xAxis: {{ visible: false }},
            yAxis: {{ visible: false }},
            series: [{{ type: 'scatter', data: [] }}]
        }});
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
time.sleep(5)
driver.save_screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()
