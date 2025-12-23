""" pyplots.ai
network-basic: Basic Network Graph
Library: highcharts unknown | Python 3.13.11
Quality: 88/100 | Created: 2025-12-23
"""

import json
import math
import tempfile
import time
import urllib.request
from pathlib import Path

from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.networkgraph import NetworkGraphSeries
from highcharts_core.options.series.scatter import ScatterSeries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data: A small social network with 20 people in 4 communities
nodes = [
    {"id": "Alice", "group": 0},
    {"id": "Bob", "group": 0},
    {"id": "Carol", "group": 0},
    {"id": "David", "group": 0},
    {"id": "Eve", "group": 0},
    {"id": "Frank", "group": 1},
    {"id": "Grace", "group": 1},
    {"id": "Henry", "group": 1},
    {"id": "Ivy", "group": 1},
    {"id": "Jack", "group": 1},
    {"id": "Kate", "group": 2},
    {"id": "Leo", "group": 2},
    {"id": "Mia", "group": 2},
    {"id": "Noah", "group": 2},
    {"id": "Olivia", "group": 2},
    {"id": "Paul", "group": 3},
    {"id": "Quinn", "group": 3},
    {"id": "Ryan", "group": 3},
    {"id": "Sara", "group": 3},
    {"id": "Tom", "group": 3},
]

# Edges: Friendship connections (within and between groups)
edges = [
    # Group 0 internal connections
    ("Alice", "Bob"),
    ("Alice", "Carol"),
    ("Bob", "Carol"),
    ("Bob", "David"),
    ("Carol", "Eve"),
    ("David", "Eve"),
    # Group 1 internal connections
    ("Frank", "Grace"),
    ("Frank", "Henry"),
    ("Grace", "Ivy"),
    ("Henry", "Ivy"),
    ("Henry", "Jack"),
    ("Ivy", "Jack"),
    # Group 2 internal connections
    ("Kate", "Leo"),
    ("Kate", "Mia"),
    ("Leo", "Noah"),
    ("Mia", "Noah"),
    ("Mia", "Olivia"),
    ("Noah", "Olivia"),
    # Group 3 internal connections
    ("Paul", "Quinn"),
    ("Paul", "Ryan"),
    ("Quinn", "Sara"),
    ("Ryan", "Sara"),
    ("Ryan", "Tom"),
    ("Sara", "Tom"),
    # Cross-group connections (bridges between communities)
    ("Alice", "Frank"),
    ("Eve", "Kate"),
    ("Jack", "Paul"),
    ("Olivia", "Tom"),
    ("Carol", "Grace"),
    ("Ivy", "Leo"),
    ("Noah", "Quinn"),
]

# Colors for groups (colorblind-safe: Python Blue, Python Yellow, teal, purple)
group_colors = ["#306998", "#FFD43B", "#17BECF", "#9467BD"]

# Calculate node degrees for sizing
degrees = {node["id"]: 0 for node in nodes}
for src, tgt in edges:
    degrees[src] += 1
    degrees[tgt] += 1

# Pre-calculated fixed initial positions for reproducibility (4 groups in quadrants)
# Using deterministic circular positions within each group's quadrant
group_centers = [
    (1800, 900),  # Group 0: top-left quadrant
    (3000, 900),  # Group 1: top-right quadrant
    (1800, 1800),  # Group 2: bottom-left quadrant
    (3000, 1800),  # Group 3: bottom-right quadrant
]

# Build nodes config with colors, markers based on degree, and fixed initial positions
nodes_config = []
group_indices = {0: 0, 1: 0, 2: 0, 3: 0}  # Track index within each group
for node in nodes:
    node_id = node["id"]
    group = node["group"]
    color = group_colors[group]
    # Scale marker radius based on degree (base 55, plus 10 per connection)
    radius = 55 + degrees[node_id] * 10
    # Calculate fixed initial position in a circle around group center
    center_x, center_y = group_centers[group]
    idx = group_indices[group]
    group_indices[group] += 1
    angle = (2 * math.pi * idx) / 5  # 5 nodes per group
    offset = 300
    init_x = center_x + offset * math.cos(angle)
    init_y = center_y + offset * math.sin(angle)
    nodes_config.append(
        {
            "id": node_id,
            "color": color,
            "marker": {"radius": radius, "fillColor": color, "lineWidth": 3, "lineColor": "#333333"},
            "plotX": init_x,
            "plotY": init_y,
        }
    )

# Group names for legend
group_names = ["Community A", "Community B", "Community C", "Community D"]

# Create network graph series
series = NetworkGraphSeries()
series.name = "Network"
series.data = [{"from": src, "to": tgt} for src, tgt in edges]
series.data_labels = {
    "enabled": True,
    "format": "{point.id}",
    "linkFormat": "",
    "style": {"fontSize": "32px", "fontWeight": "bold", "textOutline": "4px white"},
    "y": -5,
}
series.marker = {"radius": 55}
series.layout_algorithm = {
    "enableSimulation": True,
    "linkLength": 500,
    "gravitationalConstant": 0.01,
    "friction": -0.95,
    "initialPositions": "circle",
    "maxIterations": 500,
    "integration": "verlet",
}
series.animation = False
series.link = {"width": 3, "color": "#aaaaaa"}
series.show_in_legend = False

# Create chart
chart = Chart(container="container")
chart.options = HighchartsOptions()
chart.options.chart = {
    "type": "networkgraph",
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#ffffff",
    "margin": [120, 400, 150, 100],
    "spacingTop": 80,
    "spacingBottom": 80,
}
chart.options.title = {
    "text": "network-basic · highcharts · pyplots.ai",
    "style": {"fontSize": "48px", "fontWeight": "bold"},
}
# Hide axes (not needed for network graph)
chart.options.x_axis = {"visible": False}
chart.options.y_axis = {"visible": False}
# Set plot options for networkgraph
chart.options.plot_options = {
    "networkgraph": {"keys": ["from", "to"], "marker": {"radius": 55, "lineWidth": 3, "lineColor": "#333333"}}
}
# Add legend explaining the 4 community groups - positioned inside right margin
chart.options.legend = {
    "enabled": True,
    "align": "right",
    "verticalAlign": "middle",
    "layout": "vertical",
    "x": -100,
    "y": 0,
    "itemStyle": {"fontSize": "28px", "fontWeight": "normal"},
    "symbolRadius": 12,
    "symbolWidth": 24,
    "symbolHeight": 24,
}
chart.add_series(series)

# Add dummy scatter series for legend (to show community colors)
for color, name in zip(group_colors, group_names, strict=True):
    legend_series = ScatterSeries()
    legend_series.name = name
    legend_series.color = color
    legend_series.data = []  # Empty data - just for legend display
    legend_series.marker = {"symbol": "circle", "radius": 12}
    legend_series.show_in_legend = True
    chart.add_series(legend_series)

# Generate JS and inject nodes into the first series (highcharts-core doesn't support nodes property directly)
js_literal = chart.to_js_literal()
nodes_js = json.dumps(nodes_config)
# Inject nodes into the networkgraph series (series[0])
js_literal = js_literal.replace("series: [{", f"series: [{{\n  nodes: {nodes_js},")

# Download Highcharts JS (required for headless Chrome)
highcharts_url = "https://code.highcharts.com/highcharts.js"
with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

# Download highcharts-more.js for networkgraph
highcharts_more_url = "https://code.highcharts.com/highcharts-more.js"
with urllib.request.urlopen(highcharts_more_url, timeout=30) as response:
    highcharts_more_js = response.read().decode("utf-8")

# Download networkgraph module
networkgraph_url = "https://code.highcharts.com/modules/networkgraph.js"
with urllib.request.urlopen(networkgraph_url, timeout=30) as response:
    networkgraph_js = response.read().decode("utf-8")

# Cleanup JS to remove unwanted link labels after chart renders
cleanup_js = """
setTimeout(function() {
    var labels = document.querySelectorAll('.highcharts-data-label text');
    labels.forEach(function(label) {
        if (label.textContent && label.textContent.indexOf('highcharts-') === 0) {
            label.parentNode.style.display = 'none';
        }
    });
    if (Highcharts.charts[0]) {
        Highcharts.charts[0].redraw();
    }
}, 5000);
"""

# Generate HTML with inline scripts
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <script>{highcharts_more_js}</script>
    <script>{networkgraph_js}</script>
</head>
<body style="margin:0;">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>{js_literal}</script>
    <script>{cleanup_js}</script>
</body>
</html>"""

# Write temp HTML
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

# Take screenshot with headless Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=4800,2800")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(15)  # Wait for chart to render, layout to stabilize, and cleanup JS to run
driver.save_screenshot("plot.png")
driver.quit()

# Save HTML
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Clean up temp file
Path(temp_path).unlink()
