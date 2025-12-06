"""
line-basic: Basic Line Plot
Library: highcharts
"""

import json
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
time_values = ["1", "2", "3", "4", "5", "6", "7"]
values = [10, 15, 13, 18, 22, 19, 25]

# Create chart with container
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration
chart.options.chart = {
    "type": "line",
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#ffffff",
    "style": {"fontFamily": "Arial, sans-serif"},
}

# Title
chart.options.title = {"text": "Basic Line Plot", "style": {"fontSize": "48px"}}

# Axes
chart.options.x_axis = {
    "title": {"text": "Time", "style": {"fontSize": "40px"}},
    "labels": {"style": {"fontSize": "32px"}, "enabled": True},
    "categories": time_values,
    "gridLineWidth": 1,
    "gridLineColor": "#e0e0e0",
    "lineWidth": 2,
    "tickWidth": 2,
}
chart.options.y_axis = {
    "title": {"text": "Value", "style": {"fontSize": "40px"}},
    "labels": {"style": {"fontSize": "32px"}},
    "gridLineColor": "#e0e0e0",
    "lineWidth": 2,
}

# Legend (not needed for single series)
chart.options.legend = {"enabled": False}

# Disable credits
chart.options.credits = {"enabled": False}

# Create and add series
series = LineSeries()
series.data = values
series.name = "Value"
series.color = "#306998"
series.marker = {"enabled": True, "radius": 8, "fillColor": "#306998"}
series.line_width = 4

chart.add_series(series)

# Download Highcharts JS for inline embedding
highcharts_url = "https://code.highcharts.com/highcharts.js"
with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

# Generate HTML with inline scripts using JSON approach for reliability
opts_json = json.dumps(chart.options.to_dict())
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
</head>
<body style="margin:0;">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>
        Highcharts.chart('container', {opts_json});
    </script>
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
chrome_options.add_argument("--window-size=4800,2800")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)

# Take screenshot of just the chart container element
container = driver.find_element("id", "container")
container.screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()
