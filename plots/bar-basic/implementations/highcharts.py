"""
bar-basic: Basic Bar Chart
Library: highcharts
"""

import json
import tempfile
import time
import urllib.request
from pathlib import Path

import pandas as pd
from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.bar import ColumnSeries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data
data = pd.DataFrame(
    {"category": ["Product A", "Product B", "Product C", "Product D", "Product E"], "value": [45, 78, 52, 91, 63]}
)

# Create chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration
chart.options.chart = {"type": "column", "width": 4800, "height": 2700, "backgroundColor": "#ffffff"}

# Title
chart.options.title = {"text": "Basic Bar Chart", "style": {"fontSize": "48px", "fontWeight": "bold"}}

# X-axis configuration
chart.options.x_axis = {
    "categories": data["category"].tolist(),
    "title": {"text": "Product Category", "style": {"fontSize": "40px"}},
    "labels": {"style": {"fontSize": "32px"}},
}

# Y-axis configuration
chart.options.y_axis = {
    "title": {"text": "Sales Value", "style": {"fontSize": "40px"}},
    "labels": {"style": {"fontSize": "32px"}},
    "min": 0,
    "gridLineWidth": 1,
    "gridLineDashStyle": "Dot",
    "gridLineColor": "rgba(0, 0, 0, 0.15)",
}

# Create series
series = ColumnSeries()
series.data = data["value"].tolist()
series.name = "Sales Value"
series.color = "#306998"  # Python Blue from style guide

chart.add_series(series)

# Plot options
chart.options.plot_options = {
    "column": {"pointPadding": 0.1, "groupPadding": 0.1, "borderWidth": 1, "borderColor": "#000000"}
}

# Legend (single series, hide)
chart.options.legend = {"enabled": False}

# Credits
chart.options.credits = {"enabled": False}

# Export to PNG via Selenium
highcharts_url = "https://code.highcharts.com/highcharts.js"
with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

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

# Screenshot the chart element specifically for exact dimensions
container = driver.find_element("id", "container")
container.screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()
