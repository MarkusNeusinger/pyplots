"""pyplots.ai
scatter-basic: Basic Scatter Plot
Library: highcharts 1.10.3 | Python 3.14
Quality: /100 | Updated: 2026-02-14
"""

import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.scatter import ScatterSeries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data — height vs weight with moderate positive correlation (r~0.7)
np.random.seed(42)
height_cm = np.random.normal(170, 10, 100)
weight_kg = height_cm * 0.65 + np.random.normal(0, 8, 100) - 40

# Create chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration
chart.options.chart = {
    "type": "scatter",
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#ffffff",
    "marginBottom": 200,
}

# Title
chart.options.title = {
    "text": "scatter-basic \u00b7 highcharts \u00b7 pyplots.ai",
    "style": {"fontSize": "72px", "fontWeight": "bold"},
}

# Axes
chart.options.x_axis = {
    "title": {"text": "Height (cm)", "style": {"fontSize": "48px"}},
    "labels": {"style": {"fontSize": "36px"}},
    "tickInterval": 5,
    "gridLineWidth": 1,
    "gridLineColor": "rgba(0, 0, 0, 0.15)",
}
chart.options.y_axis = {
    "title": {"text": "Weight (kg)", "style": {"fontSize": "48px"}},
    "labels": {"style": {"fontSize": "36px"}},
    "gridLineWidth": 1,
    "gridLineColor": "rgba(0, 0, 0, 0.15)",
}

# Legend and credits
chart.options.legend = {"enabled": False}
chart.options.credits = {"enabled": False}

# Tooltip for interactive HTML version
chart.options.tooltip = {
    "headerFormat": "",
    "pointFormat": "<b>{point.x:.1f} cm</b>, <b>{point.y:.1f} kg</b>",
    "style": {"fontSize": "28px"},
}

# Scatter series with Python Blue and transparency
series = ScatterSeries()
series.data = [[float(h), float(w)] for h, w in zip(height_cm, weight_kg, strict=True)]
series.name = "Subjects"
series.color = "rgba(48, 105, 152, 0.7)"
series.marker = {"radius": 18, "symbol": "circle", "lineWidth": 2, "lineColor": "#ffffff"}

chart.add_series(series)

# Download Highcharts JS (required for headless Chrome)
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
chrome_options.add_argument("--window-size=4800,2800")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)

# Take screenshot of just the chart container element
container = driver.find_element("id", "container")
container.screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()

# Save HTML for interactive version
with open("plot.html", "w", encoding="utf-8") as f:
    interactive_html = f"""<!DOCTYPE html>
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
    f.write(interactive_html)
