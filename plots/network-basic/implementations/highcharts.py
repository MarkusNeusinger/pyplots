"""
network-basic: Basic Network Graph
Library: highcharts
"""

import json
import tempfile
import time
import urllib.request
from pathlib import Path

from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.networkgraph import NetworkGraphSeries
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

# Colors for groups (colorblind-safe)
group_colors = ["#306998", "#FFD43B", "#4CAF50", "#FF7043"]
group_names = ["Group A", "Group B", "Group C", "Group D"]

# Calculate node degrees for sizing
degrees = {node["id"]: 0 for node in nodes}
for src, tgt in edges:
    degrees[src] += 1
    degrees[tgt] += 1

# Build nodes config with colors and markers based on degree
nodes_config = []
for node in nodes:
    node_id = node["id"]
    group = node["group"]
    color = group_colors[group]
    # Scale marker radius based on degree (base 35, plus 5 per connection)
    radius = 35 + degrees[node_id] * 5
    nodes_config.append(
        {
            "id": node_id,
            "color": color,
            "marker": {"radius": radius, "fillColor": color, "lineWidth": 2, "lineColor": "#333333"},
        }
    )

# Create network graph series
series = NetworkGraphSeries()
series.name = "Social Network"
series.data = [{"from": src, "to": tgt} for src, tgt in edges]
series.data_labels = {
    "enabled": True,
    "format": "{point.id}",
    "linkFormat": "",
    "style": {"fontSize": "22px", "fontWeight": "bold", "textOutline": "2px white"},
}
series.marker = {"radius": 40}
series.layout_algorithm = {
    "enableSimulation": True,
    "linkLength": 80,
    "gravitationalConstant": 0.15,
    "friction": -0.95,
    "initialPositions": "circle",
    "maxIterations": 200,
}
series.animation = False

# Create chart
chart = Chart(container="container")
chart.options = HighchartsOptions()
chart.options.chart = {
    "type": "networkgraph",
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#ffffff",
    "margin": [100, 200, 200, 200],  # top, right, bottom, left
}
chart.options.title = {
    "text": "Social Network · network-basic · highcharts · pyplots.ai",
    "style": {"fontSize": "48px"},
}
# Disable legend (we use colors to distinguish groups visually)
chart.options.legend = {"enabled": False}
chart.add_series(series)

# Generate JS and inject nodes (highcharts-core doesn't support nodes property directly)
js_literal = chart.to_js_literal()
nodes_js = json.dumps(nodes_config)
js_literal = js_literal.replace("type: 'networkgraph'", f"type: 'networkgraph',\n  nodes: {nodes_js}")

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

# Generate HTML with inline scripts
# Add JS to remove unwanted link labels after chart renders
cleanup_js = """
setTimeout(function() {
    // Remove data labels that contain 'highcharts-' text (internal IDs)
    var labels = document.querySelectorAll('.highcharts-data-label text');
    labels.forEach(function(label) {
        if (label.textContent && label.textContent.indexOf('highcharts-') === 0) {
            label.parentNode.style.display = 'none';
        }
    });
    // Force a redraw to ensure all markers are visible
    if (Highcharts.charts[0]) {
        Highcharts.charts[0].redraw();
    }
}, 5000);
"""

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
chrome_options.add_argument("--window-size=4800,2700")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(12)  # Wait for chart to render, layout to stabilize, and cleanup JS to run
driver.save_screenshot("plot.png")
driver.quit()

# Save HTML
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Clean up temp file
Path(temp_path).unlink()
