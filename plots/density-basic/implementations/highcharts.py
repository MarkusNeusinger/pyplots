"""pyplots.ai
density-basic: Basic Density Plot
Library: highcharts | Python 3.13
Quality: pending | Created: 2025-12-23
"""

import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.area import AreaSeries
from highcharts_core.options.series.scatter import ScatterSeries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - simulating heights (cm) with realistic distribution
np.random.seed(42)
# Mix of two normal distributions to show bimodal feature (male/female heights)
n_samples = 500
values_a = np.random.normal(165, 7, n_samples // 2)  # Female heights
values_b = np.random.normal(178, 8, n_samples // 2)  # Male heights
values = np.concatenate([values_a, values_b])

# Kernel Density Estimation (Gaussian kernel) - inline calculation
x_min, x_max = values.min() - 10, values.max() + 10
x_grid = np.linspace(x_min, x_max, 200)

# Silverman's rule of thumb for bandwidth
n = len(values)
bandwidth = 1.06 * np.std(values) * n ** (-1 / 5)

# Compute Gaussian KDE
density = np.zeros_like(x_grid)
for xi in values:
    density += np.exp(-0.5 * ((x_grid - xi) / bandwidth) ** 2)
density /= n * bandwidth * np.sqrt(2 * np.pi)

# Create chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration
chart.options.chart = {
    "type": "area",
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#ffffff",
    "marginBottom": 200,
    "marginLeft": 200,
}

# Title
chart.options.title = {
    "text": "density-basic · highcharts · pyplots.ai",
    "style": {"fontSize": "72px", "fontWeight": "bold"},
}

# X-axis
chart.options.x_axis = {
    "title": {"text": "Height (cm)", "style": {"fontSize": "48px"}},
    "labels": {"style": {"fontSize": "36px"}},
    "gridLineWidth": 1,
    "gridLineColor": "rgba(0, 0, 0, 0.25)",
}

# Y-axis - start at 0 for proper density representation
chart.options.y_axis = {
    "title": {"text": "Density", "style": {"fontSize": "48px"}},
    "labels": {"style": {"fontSize": "36px"}},
    "gridLineWidth": 1,
    "gridLineColor": "rgba(0, 0, 0, 0.25)",
    "min": 0,
}

# Plot options with semi-transparent fill
chart.options.plot_options = {
    "area": {
        "fillColor": {
            "linearGradient": {"x1": 0, "y1": 0, "x2": 0, "y2": 1},
            "stops": [[0, "rgba(48, 105, 152, 0.6)"], [1, "rgba(48, 105, 152, 0.1)"]],
        },
        "lineWidth": 5,
        "marker": {"enabled": False},
        "color": "#306998",
    },
    "scatter": {
        "marker": {"radius": 8, "fillColor": "#FFD43B", "symbol": "diamond", "lineWidth": 2, "lineColor": "#D4AA00"}
    },
}

# Legend - enabled with clear styling
chart.options.legend = {
    "enabled": True,
    "layout": "horizontal",
    "align": "right",
    "verticalAlign": "top",
    "floating": True,
    "x": -50,
    "y": 80,
    "itemStyle": {"fontSize": "36px"},
    "symbolHeight": 24,
    "symbolWidth": 40,
}

# Add density curve as area series
area_series = AreaSeries()
area_series.data = [[float(x), float(y)] for x, y in zip(x_grid, density, strict=True)]
area_series.name = "Density Curve"
chart.add_series(area_series)

# Add rug plot as small vertical tick marks at y=0
# Sample every 5th point to show distribution without overcrowding
rug_sample = values[::5]
rug_y = 0.0005  # Small positive value just above x-axis
rug_data = [[float(v), rug_y] for v in sorted(rug_sample)]

rug_series = ScatterSeries()
rug_series.data = rug_data
rug_series.name = "Observations (Rug)"
rug_series.marker = {"symbol": "diamond", "fillColor": "#FFD43B", "lineColor": "#D4AA00", "lineWidth": 2, "radius": 10}
chart.add_series(rug_series)

# Download Highcharts JS for inline embedding
highcharts_url = "https://code.highcharts.com/highcharts.js"
with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

# Generate HTML with inline scripts
html_str = chart.to_js_literal()
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
</head>
<body style="margin:0;">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>{html_str}</script>
</body>
</html>"""

# Write temp HTML and take screenshot
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

# Also save HTML for interactive version
with open("plot.html", "w", encoding="utf-8") as f:
    # For standalone HTML, use CDN link
    standalone_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://code.highcharts.com/highcharts.js"></script>
</head>
<body style="margin:0;">
    <div id="container" style="width: 100%; height: 100vh;"></div>
    <script>{html_str}</script>
</body>
</html>"""
    f.write(standalone_html)

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=5000,3000")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)  # Wait for chart to render

# Screenshot the chart element specifically for exact 4800x2700
container = driver.find_element("id", "container")
container.screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()  # Clean up temp file
