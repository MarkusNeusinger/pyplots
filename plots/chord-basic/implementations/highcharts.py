""" pyplots.ai
chord-basic: Basic Chord Diagram
Library: highcharts 1.10.3 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-14
"""

import tempfile
import time
import urllib.request
from pathlib import Path

from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - Migration flows between continents (in millions)
# Format: [source, target, value]
flows = [
    # From Europe
    ["Europe", "North America", 45],
    ["Europe", "Asia", 28],
    ["Europe", "Africa", 15],
    ["Europe", "South America", 12],
    ["Europe", "Oceania", 8],
    # From Asia
    ["Asia", "North America", 55],
    ["Asia", "Europe", 35],
    ["Asia", "Oceania", 22],
    ["Asia", "Africa", 10],
    ["Asia", "South America", 5],
    # From Africa
    ["Africa", "Europe", 42],
    ["Africa", "North America", 18],
    ["Africa", "Asia", 12],
    ["Africa", "South America", 6],
    ["Africa", "Oceania", 3],
    # From North America
    ["North America", "Europe", 30],
    ["North America", "Asia", 25],
    ["North America", "South America", 15],
    ["North America", "Oceania", 8],
    ["North America", "Africa", 4],
    # From South America
    ["South America", "North America", 38],
    ["South America", "Europe", 25],
    ["South America", "Asia", 8],
    ["South America", "Africa", 3],
    ["South America", "Oceania", 2],
    # From Oceania
    ["Oceania", "Asia", 18],
    ["Oceania", "Europe", 12],
    ["Oceania", "North America", 10],
    ["Oceania", "Africa", 2],
    ["Oceania", "South America", 1],
]

# Collect unique nodes
nodes_set = set()
for source, target, _ in flows:
    nodes_set.add(source)
    nodes_set.add(target)
nodes = list(nodes_set)

# Colorblind-safe colors for continents
node_colors = {
    "Europe": "#306998",  # Python Blue
    "Asia": "#FFD43B",  # Python Yellow
    "Africa": "#9467BD",  # Purple
    "North America": "#17BECF",  # Cyan
    "South America": "#2CA02C",  # Green
    "Oceania": "#FF7F0E",  # Orange
}

# Create nodes data with colors
nodes_data = [{"id": node, "name": node, "color": node_colors.get(node, "#306998")} for node in nodes]

# Create links data
links_data = [{"from": source, "to": target, "weight": value} for source, target, value in flows]

# Create chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration
chart.options.chart = {"type": "dependencywheel", "width": 4800, "height": 2700, "backgroundColor": "#ffffff"}

# Title
chart.options.title = {
    "text": "Migration Flows · chord-basic · highcharts · pyplots.ai",
    "style": {"fontSize": "64px", "fontWeight": "bold"},
}

# Tooltip
chart.options.tooltip = {
    "style": {"fontSize": "36px"},
    "nodeFormat": "{point.name}: {point.sum}M total flow",
    "pointFormat": "{point.fromNode.name} → {point.toNode.name}: {point.weight}M migrants",
}

# Dependency wheel (chord diagram) series configuration
series_config = {
    "type": "dependencywheel",
    "name": "Migration Flow",
    "keys": ["from", "to", "weight"],
    "nodes": nodes_data,
    "data": links_data,
    "dataLabels": {
        "enabled": True,
        "style": {"fontSize": "36px", "fontWeight": "bold", "textOutline": "3px white"},
        "nodeFormat": "{point.name}",  # Only format node labels
        "linkFormat": "",  # Empty format for links (hides them)
        "distance": 20,
    },
    "size": "90%",
    "center": ["50%", "50%"],
    "linkOpacity": 0.6,
    "curveFactor": 0.6,
}

chart.options.series = [series_config]

# Disable legend (nodes are labeled around the wheel)
chart.options.legend = {"enabled": False}

# Disable credits
chart.options.credits = {"enabled": False}

# Download Highcharts JS and sankey module (dependency wheel extends sankey)
highcharts_url = "https://code.highcharts.com/highcharts.js"
sankey_url = "https://code.highcharts.com/modules/sankey.js"
wheel_url = "https://code.highcharts.com/modules/dependency-wheel.js"

with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

with urllib.request.urlopen(sankey_url, timeout=30) as response:
    sankey_js = response.read().decode("utf-8")

with urllib.request.urlopen(wheel_url, timeout=30) as response:
    wheel_js = response.read().decode("utf-8")

# Generate HTML with inline scripts
html_str = chart.to_js_literal()
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <script>{sankey_js}</script>
    <script>{wheel_js}</script>
</head>
<body style="margin:0;">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>{html_str}</script>
</body>
</html>"""

# Save HTML for interactive version (use CDN for standalone)
standalone_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://code.highcharts.com/highcharts.js"></script>
    <script src="https://code.highcharts.com/modules/sankey.js"></script>
    <script src="https://code.highcharts.com/modules/dependency-wheel.js"></script>
</head>
<body style="margin:0;">
    <div id="container" style="width: 100%; height: 100vh;"></div>
    <script>{html_str}</script>
</body>
</html>"""

with open("plot.html", "w", encoding="utf-8") as f:
    f.write(standalone_html)

# Write temp HTML and take screenshot
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=4800,2900")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)  # Wait for chart to render
driver.save_screenshot("plot_raw.png")
driver.quit()

# Crop to exact 4800x2700 dimensions
img = Image.open("plot_raw.png")
img_cropped = img.crop((0, 0, 4800, 2700))
img_cropped.save("plot.png")
Path("plot_raw.png").unlink()

Path(temp_path).unlink()  # Clean up temp file
