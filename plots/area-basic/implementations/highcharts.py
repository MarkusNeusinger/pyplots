"""
area-basic: Basic Area Chart
Library: highcharts
"""

import tempfile
import time
import urllib.request
from pathlib import Path

from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.area import AreaSeries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
sales = [120, 135, 148, 162, 175, 195, 210, 198, 185, 170, 158, 190]

# Create chart with container (required for headless export)
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration
chart.options.chart = {"type": "area", "width": 4800, "height": 2700, "backgroundColor": "#ffffff"}

# Title
chart.options.title = {"text": "Monthly Sales", "style": {"fontSize": "48px"}}

# X-axis with categories
chart.options.x_axis = {
    "categories": months,
    "title": {"text": "Month", "style": {"fontSize": "40px"}},
    "labels": {"style": {"fontSize": "32px"}},
}

# Y-axis
chart.options.y_axis = {
    "title": {"text": "Sales", "style": {"fontSize": "40px"}},
    "labels": {"style": {"fontSize": "32px"}},
    "gridLineColor": "#e0e0e0",
}

# Legend
chart.options.legend = {"enabled": False}

# Create area series
series = AreaSeries()
series.data = sales
series.name = "Sales"
series.color = "#306998"
series.fill_opacity = 0.6
series.line_width = 3
series.marker = {"enabled": True, "radius": 6, "fillColor": "#306998"}

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
chrome_options.add_argument("--window-size=4800,2700")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)
driver.save_screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()
