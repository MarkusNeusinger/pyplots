"""
sankey-basic: Basic Sankey Diagram
Library: highcharts
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


# Data - Energy flow from sources to sectors
# Format: [source, target, value]
flows = [
    # Coal flows
    ["Coal", "Electricity", 150],
    ["Coal", "Industrial", 80],
    # Natural Gas flows
    ["Natural Gas", "Electricity", 120],
    ["Natural Gas", "Residential", 90],
    ["Natural Gas", "Commercial", 60],
    ["Natural Gas", "Industrial", 50],
    # Nuclear flows
    ["Nuclear", "Electricity", 200],
    # Petroleum flows
    ["Petroleum", "Transportation", 280],
    ["Petroleum", "Industrial", 70],
    ["Petroleum", "Residential", 30],
    # Renewable flows
    ["Renewable", "Electricity", 100],
    ["Renewable", "Transportation", 20],
    # Electricity flows to end uses
    ["Electricity", "Residential", 180],
    ["Electricity", "Commercial", 160],
    ["Electricity", "Industrial", 140],
]

# Collect unique nodes
nodes_set = set()
for source, target, _ in flows:
    nodes_set.add(source)
    nodes_set.add(target)
nodes = list(nodes_set)

# Colorblind-safe colors for nodes
node_colors = {
    # Sources (energy sources)
    "Coal": "#306998",  # Python Blue
    "Natural Gas": "#FFD43B",  # Python Yellow
    "Nuclear": "#9467BD",  # Purple
    "Petroleum": "#17BECF",  # Cyan
    "Renewable": "#2CA02C",  # Green
    # Intermediate
    "Electricity": "#8C564B",  # Brown
    # End uses
    "Residential": "#E377C2",  # Pink
    "Commercial": "#7F7F7F",  # Gray
    "Industrial": "#BCBD22",  # Olive
    "Transportation": "#FF7F0E",  # Orange
}

# Create nodes data with colors
nodes_data = [{"id": node, "name": node, "color": node_colors.get(node, "#306998")} for node in nodes]

# Create links data
links_data = [{"from": source, "to": target, "weight": value} for source, target, value in flows]

# Create chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration
chart.options.chart = {"type": "sankey", "width": 4800, "height": 2700, "backgroundColor": "#ffffff"}

# Title
chart.options.title = {
    "text": "Energy Flow · sankey-basic · highcharts · pyplots.ai",
    "style": {"fontSize": "64px", "fontWeight": "bold"},
}

# Tooltip
chart.options.tooltip = {
    "style": {"fontSize": "36px"},
    "nodeFormat": "{point.name}: {point.sum} units",
    "pointFormat": "{point.fromNode.name} → {point.toNode.name}: {point.weight} units",
}

# Sankey series configuration
series_config = {
    "type": "sankey",
    "name": "Energy Flow",
    "keys": ["from", "to", "weight"],
    "nodes": nodes_data,
    "data": links_data,
    "dataLabels": {
        "enabled": True,
        "style": {"fontSize": "32px", "fontWeight": "bold", "textOutline": "2px white"},
        "nodeFormat": "{point.name}",
    },
    "nodeWidth": 40,
    "nodePadding": 30,
    "linkOpacity": 0.5,
    "curveFactor": 0.5,
}

chart.options.series = [series_config]

# Disable legend for sankey (nodes are labeled)
chart.options.legend = {"enabled": False}

# Disable credits
chart.options.credits = {"enabled": False}

# Download Highcharts JS and sankey module
highcharts_url = "https://code.highcharts.com/highcharts.js"
sankey_url = "https://code.highcharts.com/modules/sankey.js"

with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

with urllib.request.urlopen(sankey_url, timeout=30) as response:
    sankey_js = response.read().decode("utf-8")

# Generate HTML with inline scripts
html_str = chart.to_js_literal()
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <script>{sankey_js}</script>
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
