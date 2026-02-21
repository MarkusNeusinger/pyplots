""" pyplots.ai
hexbin-basic: Basic Hexbin Plot
Library: highcharts 1.10.3 | Python 3.14.3
Quality: 80/100 | Created: 2026-02-21
"""

import json
import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - seismic sensor readings: 10,000 measurements across a monitoring grid
np.random.seed(42)
n_points = 10000

# Three activity zones with different intensities
zone_a = np.column_stack([np.random.randn(n_points // 3) * 1.2 + 2, np.random.randn(n_points // 3) * 1.0 + 3])
zone_b = np.column_stack([np.random.randn(n_points // 3) * 1.5 - 1, np.random.randn(n_points // 3) * 1.5 - 1])
zone_c = np.column_stack([np.random.randn(n_points // 3) * 0.8 + 4, np.random.randn(n_points // 3) * 0.9 - 2])
points = np.vstack([zone_a, zone_b, zone_c])

# Hexagonal binning
gridsize = 20
x_min, x_max = points[:, 0].min() - 0.5, points[:, 0].max() + 0.5
y_min, y_max = points[:, 1].min() - 0.5, points[:, 1].max() + 0.5

hex_width = (x_max - x_min) / gridsize
hex_height = hex_width * 2 / np.sqrt(3)
vert_spacing = hex_height * 0.75

hex_bins = {}
for px, py in points:
    row = int((py - y_min) / vert_spacing)
    col_offset = (row % 2) * hex_width * 0.5
    col = int((px - x_min - col_offset) / hex_width)
    key = (col, row)
    hex_bins[key] = hex_bins.get(key, 0) + 1

# Build tilemap data: grid coordinates + count values
tilemap_data = []
for (col, row), count in hex_bins.items():
    tilemap_data.append({"x": col, "y": row, "value": count})

max_count = max(v["value"] for v in tilemap_data)

# Chart options using Highcharts tilemap with hexagonal tiles
chart_options = {
    "chart": {
        "type": "tilemap",
        "width": 4800,
        "height": 2700,
        "backgroundColor": "#ffffff",
        "marginTop": 130,
        "marginBottom": 120,
        "marginLeft": 140,
        "marginRight": 220,
        "animation": False,
    },
    "title": {
        "text": "Seismic Activity Density \u00b7 hexbin-basic \u00b7 highcharts \u00b7 pyplots.ai",
        "style": {"fontSize": "44px", "fontWeight": "500"},
    },
    "xAxis": {"visible": False},
    "yAxis": {"visible": False},
    "colorAxis": {
        "min": 0,
        "max": int(max_count),
        "stops": [[0, "#440154"], [0.25, "#3b528b"], [0.5, "#21918c"], [0.75, "#5ec962"], [1, "#fde725"]],
        "labels": {"style": {"fontSize": "24px"}},
    },
    "legend": {
        "align": "right",
        "layout": "vertical",
        "verticalAlign": "middle",
        "symbolHeight": 600,
        "symbolWidth": 40,
        "title": {"text": "Event Count", "style": {"fontSize": "28px", "fontWeight": "bold"}},
        "itemStyle": {"fontSize": "24px"},
    },
    "tooltip": {"enabled": False},
    "credits": {"enabled": False},
    "plotOptions": {
        "tilemap": {
            "tileShape": "hexagon",
            "colsize": 1,
            "rowsize": 1,
            "borderWidth": 1,
            "borderColor": "rgba(255,255,255,0.3)",
            "animation": False,
            "states": {"hover": {"enabled": False}, "inactive": {"enabled": False}},
        }
    },
    "series": [
        {
            "type": "tilemap",
            "name": "Density",
            "data": tilemap_data,
            "tileShape": "hexagon",
            "dataLabels": {"enabled": False},
        }
    ],
}

# Download Highcharts JS and required modules
highcharts_url = "https://code.highcharts.com/highcharts.js"
heatmap_url = "https://code.highcharts.com/modules/heatmap.js"
tilemap_url = "https://code.highcharts.com/modules/tilemap.js"

with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

with urllib.request.urlopen(heatmap_url, timeout=30) as response:
    heatmap_js = response.read().decode("utf-8")

with urllib.request.urlopen(tilemap_url, timeout=30) as response:
    tilemap_js = response.read().decode("utf-8")

# Convert options to JSON
options_json = json.dumps(chart_options)

# Generate HTML with inline scripts
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <script>{heatmap_js}</script>
    <script>{tilemap_js}</script>
</head>
<body style="margin:0;">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>
        Highcharts.chart('container', {options_json});
    </script>
</body>
</html>"""

# Save interactive HTML
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Take screenshot with headless Chrome
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
