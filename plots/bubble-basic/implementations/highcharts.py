""" pyplots.ai
bubble-basic: Basic Bubble Chart
Library: highcharts 1.10.3 | Python 3.13.11
Quality: 87/100 | Created: 2025-12-14
"""

import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.bubble import BubbleSeries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data
np.random.seed(42)
n = 50
x = np.random.uniform(10, 90, n)
y = x * 0.6 + np.random.uniform(-15, 15, n)
# Size variable - represents a third dimension
size = np.random.uniform(100, 2000, n)

# Scale bubble sizes for visualization (area proportional to value)
# z value controls bubble size in Highcharts
min_size, max_size = size.min(), size.max()
z_scaled = 10 + (size - min_size) / (max_size - min_size) * 90

# Format data for Highcharts bubble chart: [x, y, z] where z controls bubble size
bubble_data = [
    {"x": float(x[i]), "y": float(y[i]), "z": float(z_scaled[i]), "name": f"Point {i + 1}"} for i in range(n)
]

# Create chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

chart.options.chart = {
    "type": "bubble",
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#ffffff",
    "plotBorderWidth": 1,
    "plotBorderColor": "#cccccc",
    "spacingBottom": 100,
}

chart.options.title = {
    "text": "bubble-basic · highcharts · pyplots.ai",
    "style": {"fontSize": "64px", "fontWeight": "bold"},
}

chart.options.x_axis = {
    "title": {"text": "X Value", "style": {"fontSize": "48px"}, "margin": 30},
    "labels": {"style": {"fontSize": "36px"}},
    "gridLineWidth": 1,
    "gridLineColor": "#e0e0e0",
}

chart.options.y_axis = {
    "title": {"text": "Y Value", "style": {"fontSize": "48px"}},
    "labels": {"style": {"fontSize": "36px"}},
    "gridLineWidth": 1,
    "gridLineColor": "#e0e0e0",
}

chart.options.legend = {"enabled": True, "itemStyle": {"fontSize": "36px"}}

chart.options.tooltip = {
    "useHTML": True,
    "headerFormat": '<span style="font-size: 28px">{point.key}</span><br/>',
    "pointFormat": '<span style="font-size: 24px">X: {point.x:.1f}<br/>Y: {point.y:.1f}<br/>Size: {point.z:.0f}</span>',
}

chart.options.plot_options = {
    "bubble": {
        "minSize": 40,
        "maxSize": 180,
        "color": "#306998",
        "marker": {"fillOpacity": 0.6, "lineWidth": 3, "lineColor": "#1e4f7a"},
        "dataLabels": {"enabled": False},
    }
}

# Create bubble series
series = BubbleSeries()
series.name = "Size Value"
series.data = bubble_data
series.color = "#306998"

chart.add_series(series)

# Download Highcharts JS and highcharts-more.js for bubble support
highcharts_url = "https://code.highcharts.com/highcharts.js"
highcharts_more_url = "https://code.highcharts.com/highcharts-more.js"

with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

with urllib.request.urlopen(highcharts_more_url, timeout=30) as response:
    highcharts_more_js = response.read().decode("utf-8")

# Generate HTML with inline scripts
html_str = chart.to_js_literal()
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <script>{highcharts_more_js}</script>
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

# Also save interactive HTML
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)

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
