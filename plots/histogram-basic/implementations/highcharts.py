"""
histogram-basic: Basic Histogram
Library: highcharts
"""

import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.bar import ColumnSeries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data
np.random.seed(42)
values = np.random.normal(100, 15, 500)  # 500 values, mean=100, std=15

# Calculate histogram bins
bins = 30
counts, bin_edges = np.histogram(values, bins=bins)

# Create bin labels (center of each bin)
bin_centers = [(bin_edges[i] + bin_edges[i + 1]) / 2 for i in range(len(counts))]
bin_labels = [f"{bin_edges[i]:.1f}-{bin_edges[i + 1]:.1f}" for i in range(len(counts))]

# Create chart with container ID
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration
chart.options.chart = {
    "type": "column",
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#ffffff",
    "spacingBottom": 120,  # Add space for x-axis title
}

# Title
chart.options.title = {"text": "Basic Histogram", "style": {"fontSize": "48px", "fontWeight": "bold"}}

# X-axis configuration
chart.options.x_axis = {
    "categories": bin_labels,
    "title": {"text": "Value", "style": {"fontSize": "40px"}},
    "labels": {
        "rotation": 315,  # 315 degrees = -45 degrees
        "style": {"fontSize": "28px"},
        "step": 3,  # Show every 3rd label to avoid overlap
    },
}

# Y-axis configuration
chart.options.y_axis = {
    "title": {"text": "Frequency", "style": {"fontSize": "40px"}},
    "min": 0,
    "gridLineWidth": 1,
    "gridLineDashStyle": "Dot",
    "gridLineColor": "rgba(0, 0, 0, 0.15)",
    "labels": {"style": {"fontSize": "32px"}},
}

# Create series with histogram data
series = ColumnSeries()
series.data = counts.tolist()
series.name = "Frequency"
series.color = "#306998"  # Python Blue
series.border_color = "white"
series.border_width = 1

# Plot options for histogram appearance
chart.options.plot_options = {"column": {"pointPadding": 0, "groupPadding": 0, "borderWidth": 1, "opacity": 0.8}}

chart.add_series(series)

# Legend (single series, hide)
chart.options.legend = {"enabled": False}

# Credits
chart.options.credits = {"enabled": False}

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
chrome_options.add_argument("--window-size=4800,2800")  # Slightly larger to capture full chart

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)  # Wait for chart to render
driver.save_screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()  # Clean up temp file
