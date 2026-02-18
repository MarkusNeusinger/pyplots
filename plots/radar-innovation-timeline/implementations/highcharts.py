"""pyplots.ai
radar-innovation-timeline: Innovation Radar with Time-Horizon Rings
Library: highcharts | Python 3.13
Quality: pending | Created: 2026-02-18
"""

import json
import math
import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - Technology innovation radar for a software company
np.random.seed(42)

sectors = ["AI & ML", "Cloud & DevOps", "Security", "Data Engineering"]
rings = ["Adopt", "Trial", "Assess", "Hold"]

innovations = [
    # AI & ML - Adopt
    {"name": "LLM-Powered Code Review", "sector": "AI & ML", "ring": "Adopt"},
    {"name": "ML Feature Stores", "sector": "AI & ML", "ring": "Adopt"},
    {"name": "Automated Testing with AI", "sector": "AI & ML", "ring": "Trial"},
    {"name": "Retrieval-Augmented Gen.", "sector": "AI & ML", "ring": "Trial"},
    {"name": "AI Pair Programming", "sector": "AI & ML", "ring": "Trial"},
    {"name": "Multimodal Foundation Models", "sector": "AI & ML", "ring": "Assess"},
    {"name": "Autonomous AI Agents", "sector": "AI & ML", "ring": "Assess"},
    {"name": "Neuromorphic Computing", "sector": "AI & ML", "ring": "Hold"},
    # Cloud & DevOps - Adopt
    {"name": "Platform Engineering", "sector": "Cloud & DevOps", "ring": "Adopt"},
    {"name": "GitOps Workflows", "sector": "Cloud & DevOps", "ring": "Adopt"},
    {"name": "FinOps Practices", "sector": "Cloud & DevOps", "ring": "Trial"},
    {"name": "WebAssembly Runtimes", "sector": "Cloud & DevOps", "ring": "Trial"},
    {"name": "Internal Developer Portals", "sector": "Cloud & DevOps", "ring": "Assess"},
    {"name": "Edge-Native Applications", "sector": "Cloud & DevOps", "ring": "Assess"},
    {"name": "Serverless Containers", "sector": "Cloud & DevOps", "ring": "Hold"},
    # Security
    {"name": "Zero Trust Architecture", "sector": "Security", "ring": "Adopt"},
    {"name": "Supply Chain Security", "sector": "Security", "ring": "Adopt"},
    {"name": "SBOM Automation", "sector": "Security", "ring": "Trial"},
    {"name": "Confidential Computing", "sector": "Security", "ring": "Trial"},
    {"name": "Post-Quantum Cryptography", "sector": "Security", "ring": "Assess"},
    {"name": "AI Threat Detection", "sector": "Security", "ring": "Assess"},
    {"name": "Homomorphic Encryption", "sector": "Security", "ring": "Hold"},
    # Data Engineering
    {"name": "Data Mesh Architecture", "sector": "Data Engineering", "ring": "Adopt"},
    {"name": "Real-Time Stream Processing", "sector": "Data Engineering", "ring": "Trial"},
    {"name": "Lakehouse Architecture", "sector": "Data Engineering", "ring": "Trial"},
    {"name": "Data Contracts", "sector": "Data Engineering", "ring": "Trial"},
    {"name": "Semantic Layer Platforms", "sector": "Data Engineering", "ring": "Assess"},
    {"name": "Vector Databases", "sector": "Data Engineering", "ring": "Assess"},
    {"name": "Quantum Data Processing", "sector": "Data Engineering", "ring": "Hold"},
]

# Assign angular positions and radial positions
num_sectors = len(sectors)
sector_angle_size = 360.0 / num_sectors
ring_radii = {"Adopt": 1, "Trial": 2, "Assess": 3, "Hold": 4}

sector_colors = {
    "AI & ML": "#306998",
    "Cloud & DevOps": "#D4762C",
    "Security": "#3C9150",
    "Data Engineering": "#8C50A0",
}

# Compute x, y positions for each item
items_by_sector_ring = {}
for item in innovations:
    key = (item["sector"], item["ring"])
    if key not in items_by_sector_ring:
        items_by_sector_ring[key] = []
    items_by_sector_ring[key].append(item)

for item in innovations:
    sector_idx = sectors.index(item["sector"])
    ring_idx = ring_radii[item["ring"]]

    key = (item["sector"], item["ring"])
    group = items_by_sector_ring[key]
    pos_in_group = group.index(item)
    n_in_group = len(group)

    sector_start = sector_idx * sector_angle_size + 5
    sector_end = (sector_idx + 1) * sector_angle_size - 5
    angle_step = (sector_end - sector_start) / max(n_in_group, 1)
    angle_deg = sector_start + angle_step * (pos_in_group + 0.5)

    jitter = np.random.uniform(-0.15, 0.15)
    radius = ring_idx - 0.5 + jitter

    angle_rad = math.radians(angle_deg)
    x = radius * math.cos(angle_rad)
    y = radius * math.sin(angle_rad)
    item["x"] = round(x, 3)
    item["y"] = round(y, 3)
    item["angle_deg"] = angle_deg
    item["radius"] = radius

# Build Highcharts config as raw JS via HTML
series_data = {}
for item in innovations:
    sector = item["sector"]
    if sector not in series_data:
        series_data[sector] = []
    series_data[sector].append({"x": item["x"], "y": item["y"], "name": item["name"], "ring": item["ring"]})

# Build chart config as JSON for Highcharts
chart_series = []
for sector in sectors:
    chart_series.append(
        {
            "type": "scatter",
            "name": sector,
            "color": sector_colors[sector],
            "data": [
                {"x": d["x"], "y": d["y"], "name": d["name"], "custom": {"ring": d["ring"]}}
                for d in series_data[sector]
            ],
            "marker": {"radius": 14, "symbol": "circle", "lineWidth": 3, "lineColor": "#ffffff"},
            "dataLabels": {
                "enabled": True,
                "format": "{point.name}",
                "style": {"fontSize": "20px", "fontWeight": "normal", "color": "#333333", "textOutline": "3px white"},
                "padding": 6,
                "y": -20,
            },
        }
    )

# Ring boundaries for drawing concentric circles
ring_boundaries = [1, 2, 3, 4]

# Build plot bands for rings with subtle fills
plot_bands_x = []
plot_bands_y = []
ring_colors_bg = [
    "rgba(48, 105, 152, 0.06)",
    "rgba(48, 105, 152, 0.04)",
    "rgba(48, 105, 152, 0.02)",
    "rgba(48, 105, 152, 0.01)",
]

# Sector divider lines and ring circles will be drawn via plotLines
plot_lines_x = []
plot_lines_y = []

highcharts_config = {
    "chart": {
        "type": "scatter",
        "width": 4800,
        "height": 2700,
        "backgroundColor": "#fafafa",
        "spacing": [60, 60, 80, 60],
        "style": {"fontFamily": "'Segoe UI', Arial, sans-serif"},
    },
    "title": {
        "text": "radar-innovation-timeline \u00b7 highcharts \u00b7 pyplots.ai",
        "style": {"fontSize": "56px", "fontWeight": "bold", "color": "#2a2a2a"},
    },
    "subtitle": {
        "text": "Technology Innovation Radar \u2014 Items mapped by adoption stage and domain",
        "style": {"fontSize": "36px", "color": "#666666"},
    },
    "xAxis": {
        "min": -5,
        "max": 5,
        "gridLineWidth": 0,
        "lineWidth": 0,
        "tickWidth": 0,
        "labels": {"enabled": False},
        "title": {"text": None},
    },
    "yAxis": {
        "min": -5,
        "max": 5,
        "gridLineWidth": 0,
        "lineWidth": 0,
        "tickWidth": 0,
        "labels": {"enabled": False},
        "title": {"text": None},
    },
    "legend": {
        "enabled": True,
        "align": "right",
        "verticalAlign": "middle",
        "layout": "vertical",
        "x": -40,
        "y": -60,
        "floating": True,
        "backgroundColor": "rgba(255, 255, 255, 0.92)",
        "borderColor": "#dddddd",
        "borderWidth": 1,
        "borderRadius": 12,
        "padding": 24,
        "itemStyle": {"fontSize": "32px", "fontWeight": "normal", "color": "#333333"},
        "itemMarginBottom": 12,
        "symbolRadius": 8,
        "symbolWidth": 28,
        "symbolHeight": 28,
        "title": {"text": "Sectors", "style": {"fontSize": "36px", "fontWeight": "bold", "color": "#333333"}},
    },
    "tooltip": {
        "useHTML": True,
        "headerFormat": "",
        "pointFormat": '<div style="font-size:24px"><b style="color:{series.color}">{point.name}</b><br/>'
        "Sector: {series.name}<br/>"
        "Stage: {point.custom.ring}</div>",
        "backgroundColor": "rgba(255, 255, 255, 0.96)",
        "borderRadius": 8,
        "borderColor": "#cccccc",
    },
    "plotOptions": {"scatter": {"marker": {"radius": 14}, "states": {"hover": {"marker": {"radius": 18}}}}},
    "credits": {"enabled": False},
    "series": chart_series,
}

config_json = json.dumps(highcharts_config)

# Build ring circles, sector lines, and ring labels as SVG-like overlays via Highcharts renderer callback
# We'll use chart.renderer in a callback to draw the concentric rings and sector dividers
ring_labels = ["Adopt", "Trial", "Assess", "Hold"]
ring_label_colors = ["#2a7d3a", "#b8860b", "#cc6600", "#993333"]

# Calculate SVG drawing coordinates (chart area center and scale)
# Chart is 4800x2700, with spacing [60, 60, 80, 60]
# Plot area: x from 60 to 4740, y from 60 to 2620
# Center of plot area
cx = (60 + 4740) / 2
cy = (60 + 2620) / 2 + 20
plot_w = 4740 - 60
plot_h = 2620 - 60
# Scale: data range is -5 to 5 = 10 units, mapped to plot area
scale_x = plot_w / 10
scale_y = plot_h / 10

renderer_js_lines = []

# Draw filled ring backgrounds (from outermost to innermost)
for i in range(len(ring_boundaries) - 1, -1, -1):
    r = ring_boundaries[i]
    rx = r * scale_x
    ry = r * scale_y
    fill = ring_colors_bg[i]
    renderer_js_lines.append(
        f"chart.renderer.circle({cx}, {cy}, {min(rx, ry)}).attr({{fill: '{fill}', stroke: 'rgba(0,0,0,0.12)', 'stroke-width': 2, 'stroke-dasharray': '8,6', zIndex: 0}}).add();"
    )

# Draw sector divider lines
for i in range(num_sectors):
    angle_deg = i * sector_angle_size
    angle_rad = math.radians(angle_deg)
    outer_r = 4
    end_x = cx + outer_r * math.cos(angle_rad) * scale_x
    end_y = cy + outer_r * math.sin(angle_rad) * scale_y
    renderer_js_lines.append(
        f"chart.renderer.path(['M', {cx}, {cy}, 'L', {end_x}, {end_y}]).attr({{stroke: 'rgba(0,0,0,0.10)', 'stroke-width': 2, zIndex: 0}}).add();"
    )

# Draw ring labels along the top (directly above center, stacked vertically)
for i, ring_name in enumerate(ring_labels):
    r = ring_boundaries[i]
    label_x = cx + 12
    label_y = cy - r * scale_y + 22
    color = ring_label_colors[i]
    renderer_js_lines.append(
        f"chart.renderer.text('{ring_name}', {label_x}, {label_y}).attr({{zIndex: 5}}).css({{fontSize: '26px', fontWeight: 'bold', fontStyle: 'italic', color: '{color}', opacity: 0.55}}).add();"
    )

# Draw sector header labels along the outer edge
for i, sector_name in enumerate(sectors):
    mid_angle_deg = (i + 0.5) * sector_angle_size
    mid_angle_rad = math.radians(mid_angle_deg)
    label_r = 4.4
    lx = cx + label_r * math.cos(mid_angle_rad) * scale_x
    ly = cy + label_r * math.sin(mid_angle_rad) * scale_y
    color = sector_colors[sector_name]
    renderer_js_lines.append(
        f"chart.renderer.text('{sector_name}', {lx}, {ly}).attr({{zIndex: 3, align: 'center'}}).css({{fontSize: '34px', fontWeight: 'bold', color: '{color}'}}).add();"
    )

renderer_js = "\n".join(renderer_js_lines)

# Download Highcharts JS
highcharts_url = "https://code.highcharts.com/highcharts.js"
with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

highcharts_more_url = "https://code.highcharts.com/highcharts-more.js"
with urllib.request.urlopen(highcharts_more_url, timeout=30) as response:
    highcharts_more_js = response.read().decode("utf-8")

# Generate HTML with inline scripts and renderer callback
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <script>{highcharts_more_js}</script>
</head>
<body style="margin:0; background: #fafafa;">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>
    var config = {config_json};
    config.chart.events = {{
        load: function() {{
            var chart = this;
            {renderer_js}
        }}
    }};
    Highcharts.chart('container', config);
    </script>
</body>
</html>"""

with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

with open("plot.html", "w", encoding="utf-8") as f:
    interactive_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://code.highcharts.com/highcharts.js"></script>
    <script src="https://code.highcharts.com/highcharts-more.js"></script>
</head>
<body style="margin:0; background: #fafafa;">
    <div id="container" style="width: 100%; height: 100vh;"></div>
    <script>
    var config = {config_json};
    config.chart.width = null;
    config.chart.height = null;
    config.chart.events = {{
        load: function() {{
            var chart = this;
            // Renderer overlays omitted for responsive interactive version
        }}
    }};
    Highcharts.chart('container', config);
    </script>
</body>
</html>"""
    f.write(interactive_html)

# Screenshot with Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=4800,2700")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)

container = driver.find_element("id", "container")
container.screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()
