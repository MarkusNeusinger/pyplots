"""
line-basic: Basic Line Plot
Library: highcharts
"""

import tempfile
import time
import urllib.request
from pathlib import Path

from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.area import LineSeries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data
time_values = [1, 2, 3, 4, 5, 6, 7]
value_data = [10, 15, 13, 18, 22, 19, 25]

# Create chart with container specified
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration
chart.options.chart = {
    "type": "line",
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#ffffff",
    "spacing": [20, 40, 80, 40],
}

# Title
chart.options.title = {"text": "Basic Line Plot", "style": {"fontSize": "48px"}}

# Axes
chart.options.x_axis = {
    "title": {"text": "Time", "style": {"fontSize": "36px"}},
    "categories": [str(t) for t in time_values],
    "labels": {"style": {"fontSize": "28px"}},
}
chart.options.y_axis = {
    "title": {"text": "Value", "style": {"fontSize": "36px"}},
    "labels": {"style": {"fontSize": "28px"}},
    "gridLineColor": "#e0e0e0",
}

# Legend
chart.options.legend = {"enabled": False}

# Plot options
chart.options.plot_options = {
    "line": {
        "lineWidth": 4,
        "marker": {"enabled": True, "radius": 8, "fillColor": "#306998", "lineWidth": 2, "lineColor": "#ffffff"},
    }
}

# Create series
series = LineSeries()
series.data = value_data
series.name = "Value"
series.color = "#306998"

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
chrome_options.add_argument("--window-size=4900,2800")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)

# Get the chart container element and take screenshot of it
container = driver.find_element("id", "container")
container.screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()
