"""
ecdf-basic: Basic ECDF Plot
Library: highcharts
"""

import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.area import LineSeries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - Generate sample from normal distribution
np.random.seed(42)
values = np.random.normal(loc=50, scale=15, size=150)

# Compute ECDF
sorted_values = np.sort(values)
n = len(sorted_values)
ecdf_y = np.arange(1, n + 1) / n

# Build step function data for ECDF
# For each point, we need a horizontal line then a vertical step
step_data = []
for i in range(n):
    if i == 0:
        # Start from (min_value, 0)
        step_data.append([float(sorted_values[i]), 0.0])
    step_data.append([float(sorted_values[i]), float(ecdf_y[i])])
    if i < n - 1:
        # Horizontal line to next point
        step_data.append([float(sorted_values[i + 1]), float(ecdf_y[i])])

# Create chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration
chart.options.chart = {
    "type": "line",
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#ffffff",
    "marginBottom": 200,
    "spacingBottom": 50,
}

# Title
chart.options.title = {
    "text": "ecdf-basic \u00b7 highcharts \u00b7 pyplots.ai",
    "style": {"fontSize": "72px", "fontWeight": "bold"},
}

# X-axis
chart.options.x_axis = {
    "title": {"text": "Value", "style": {"fontSize": "48px"}},
    "labels": {"style": {"fontSize": "36px"}},
    "gridLineWidth": 1,
    "gridLineColor": "#e0e0e0",
    "gridLineDashStyle": "Dash",
}

# Y-axis (0 to 1 for cumulative proportion)
chart.options.y_axis = {
    "title": {"text": "Cumulative Proportion", "style": {"fontSize": "48px"}},
    "labels": {"style": {"fontSize": "36px"}},
    "min": 0,
    "max": 1,
    "gridLineWidth": 1,
    "gridLineColor": "#e0e0e0",
    "gridLineDashStyle": "Dash",
}

# Legend
chart.options.legend = {"enabled": True, "itemStyle": {"fontSize": "36px"}}

# Plot options for line
chart.options.plot_options = {
    "line": {
        "lineWidth": 6,
        "marker": {"enabled": False},
        "step": False,  # We manually created step data
    }
}

# Create series
series = LineSeries()
series.data = step_data
series.name = "ECDF"
series.color = "#306998"  # Python Blue

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

# Also save HTML for interactive version
Path("plot.html").write_text(html_content, encoding="utf-8")

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=4800,2900")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)  # Wait for chart to render
driver.save_screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()  # Clean up temp file
