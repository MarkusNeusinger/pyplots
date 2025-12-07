"""
scatter-basic: Basic Scatter Plot
Library: highcharts
"""

import tempfile
import time
import urllib.request
from pathlib import Path

from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.scatter import ScatterSeries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data
x = [1, 2, 3, 4, 5, 6, 7, 8]
y = [2.1, 4.3, 3.2, 5.8, 4.9, 7.2, 6.1, 8.5]

# Create chart with container
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration
chart.options.chart = {"type": "scatter", "width": 4800, "height": 2700, "backgroundColor": "#ffffff"}

# Title
chart.options.title = {"text": "Basic Scatter Plot", "style": {"fontSize": "60px"}}

# Axes
chart.options.x_axis = {
    "title": {"text": "X Value", "style": {"fontSize": "48px"}},
    "labels": {"style": {"fontSize": "40px"}},
    "gridLineWidth": 1,
    "gridLineColor": "rgba(0, 0, 0, 0.1)",
}
chart.options.y_axis = {
    "title": {"text": "Y Value", "style": {"fontSize": "48px"}},
    "labels": {"style": {"fontSize": "40px"}},
    "gridLineWidth": 1,
    "gridLineColor": "rgba(0, 0, 0, 0.1)",
}

# Legend (not needed for single series, but kept minimal)
chart.options.legend = {"enabled": False}

# Add series
series = ScatterSeries()
series.data = list(zip(x, y, strict=False))
series.name = "Data"
series.marker = {"radius": 20, "fillColor": "#306998", "lineWidth": 2, "lineColor": "#306998"}
chart.add_series(series)

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

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=5000,3000")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)

# Screenshot the chart container element for exact dimensions
container = driver.find_element("id", "container")
container.screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()
