"""pyplots.ai
circos-basic: Circos Plot
Library: highcharts | Python 3.13
Quality: pending | Created: 2025-12-31
"""

import json
import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - Simulating trade flows between 8 regions
np.random.seed(42)

regions = ["North America", "South America", "Europe", "Africa", "Middle East", "South Asia", "East Asia", "Oceania"]

# Generate flow matrix - inter-regional trade flows
n_regions = len(regions)
flow_matrix = np.zeros((n_regions, n_regions))

# Create realistic flow patterns with some regions having stronger connections
for i in range(n_regions):
    for j in range(n_regions):
        if i != j:
            base_flow = np.random.exponential(50)
            # Some regional pairs have stronger trade relationships
            if (i == 0 and j == 6) or (i == 6 and j == 0):  # North America - East Asia
                base_flow *= 3
            elif (i == 2 and j == 6) or (i == 6 and j == 2):  # Europe - East Asia
                base_flow *= 2.5
            elif (i == 0 and j == 2) or (i == 2 and j == 0):  # North America - Europe
                base_flow *= 2
            flow_matrix[i, j] = base_flow

# Prepare data for Highcharts dependency wheel (circular chord-like visualization)
# Format: [from, to, weight] arrays
connections = []
for i in range(n_regions):
    for j in range(n_regions):
        if i != j and flow_matrix[i, j] > 20:  # Filter small connections
            connections.append([regions[i], regions[j], float(round(flow_matrix[i, j], 1))])

# Colorblind-safe colors for each region
colors = [
    "#306998",  # Python Blue - North America
    "#FFD43B",  # Python Yellow - South America
    "#9467BD",  # Purple - Europe
    "#17BECF",  # Cyan - Africa
    "#8C564B",  # Brown - Middle East
    "#E377C2",  # Pink - South Asia
    "#7F7F7F",  # Gray - East Asia
    "#BCBD22",  # Olive - Oceania
]

# Create nodes with colors
nodes = [{"id": regions[i], "color": colors[i]} for i in range(n_regions)]

# Create Highcharts configuration directly
chart_config = {
    "chart": {"type": "dependencywheel", "width": 3600, "height": 3600, "backgroundColor": "#ffffff"},
    "title": {"text": "circos-basic · highcharts · pyplots.ai", "style": {"fontSize": "48px", "fontWeight": "bold"}},
    "subtitle": {"text": "Global Trade Flows Between Regions", "style": {"fontSize": "32px"}},
    "accessibility": {"enabled": False},
    "credits": {"enabled": False},
    "tooltip": {"style": {"fontSize": "24px"}},
    "series": [
        {
            "type": "dependencywheel",
            "name": "Trade Flow",
            "keys": ["from", "to", "weight"],
            "data": connections,
            "nodes": nodes,
            "size": "90%",
            "dataLabels": {
                "enabled": True,
                "style": {"fontSize": "28px", "fontWeight": "bold", "textOutline": "2px white"},
                "distance": 20,
            },
            "nodeWidth": 30,
        }
    ],
}

# Download Highcharts JS and sankey module (dependency wheel requires sankey)
highcharts_url = "https://code.highcharts.com/highcharts.js"
sankey_url = "https://code.highcharts.com/modules/sankey.js"
dependency_wheel_url = "https://code.highcharts.com/modules/dependency-wheel.js"

with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

with urllib.request.urlopen(sankey_url, timeout=30) as response:
    sankey_js = response.read().decode("utf-8")

with urllib.request.urlopen(dependency_wheel_url, timeout=30) as response:
    dependency_wheel_js = response.read().decode("utf-8")

# Generate HTML with inline scripts
chart_config_json = json.dumps(chart_config)
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <script>{sankey_js}</script>
    <script>{dependency_wheel_js}</script>
</head>
<body style="margin:0; background-color: #ffffff;">
    <div id="container" style="width: 3600px; height: 3600px;"></div>
    <script>
        Highcharts.chart('container', {chart_config_json});
    </script>
</body>
</html>"""

# Write temp HTML and take screenshot
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

# Also save HTML for interactive version
interactive_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>circos-basic · highcharts · pyplots.ai</title>
    <script src="https://code.highcharts.com/highcharts.js"></script>
    <script src="https://code.highcharts.com/modules/sankey.js"></script>
    <script src="https://code.highcharts.com/modules/dependency-wheel.js"></script>
</head>
<body style="margin:0; background-color: #ffffff;">
    <div id="container" style="width: 100%; height: 100vh;"></div>
    <script>
        Highcharts.chart('container', {chart_config_json});
    </script>
</body>
</html>"""
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(interactive_html)

# Setup Chrome for screenshot
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=3600,3600")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)  # Wait for chart to render
driver.save_screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()  # Clean up temp file
