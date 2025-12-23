"""pyplots.ai
histogram-basic: Basic Histogram
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
from highcharts_core.options.series.bar import ColumnSeries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data
np.random.seed(42)
values = np.random.normal(loc=65, scale=15, size=500)

# Calculate histogram bins
num_bins = 15
counts, bin_edges = np.histogram(values, bins=num_bins)

# Create bin labels (center of each bin for cleaner display)
bin_labels = [f"{bin_edges[i]:.0f}-{bin_edges[i + 1]:.0f}" for i in range(len(bin_edges) - 1)]

# Create chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart settings
chart.options.chart = {
    "type": "column",
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#ffffff",
    "marginBottom": 250,
    "marginLeft": 150,
}

# Title
chart.options.title = {
    "text": "histogram-basic · highcharts · pyplots.ai",
    "style": {"fontSize": "72px", "fontWeight": "bold"},
}

# X-axis (categories = bin ranges)
chart.options.x_axis = {
    "categories": bin_labels,
    "title": {"text": "Value Range", "style": {"fontSize": "48px"}},
    "labels": {"style": {"fontSize": "32px"}, "rotation": 315},
}

# Y-axis
chart.options.y_axis = {
    "title": {"text": "Frequency", "style": {"fontSize": "48px"}},
    "labels": {"style": {"fontSize": "36px"}},
    "min": 0,
    "gridLineColor": "#e0e0e0",
    "gridLineWidth": 1,
}

# Plot options for histogram appearance (no gaps between bars)
chart.options.plot_options = {
    "column": {"pointPadding": 0, "groupPadding": 0, "borderWidth": 1, "borderColor": "#1a4a6e"}
}

# Legend (hide for single series)
chart.options.legend = {"enabled": False}

# Create series
series = ColumnSeries()
series.name = "Frequency"
series.data = [int(c) for c in counts]
series.color = "#306998"

chart.add_series(series)

# Download Highcharts JS
highcharts_url = "https://code.highcharts.com/highcharts.js"
with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

# Generate HTML with inline script
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
chrome_options.add_argument("--window-size=4800,2700")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)
driver.save_screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()
