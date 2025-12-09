"""
box-basic: Basic Box Plot
Library: highcharts
"""

import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd
from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.boxplot import BoxPlotSeries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data
np.random.seed(42)
data = pd.DataFrame(
    {
        "group": ["A"] * 50 + ["B"] * 50 + ["C"] * 50 + ["D"] * 50,
        "value": np.concatenate(
            [
                np.random.normal(50, 10, 50),
                np.random.normal(60, 15, 50),
                np.random.normal(45, 8, 50),
                np.random.normal(70, 20, 50),
            ]
        ),
    }
)

# Calculate box plot statistics for each group
groups = data["group"].unique()
box_data = []
outlier_data = []

for i, group in enumerate(groups):
    values = data[data["group"] == group]["value"].values
    q1 = np.percentile(values, 25)
    median = np.percentile(values, 50)
    q3 = np.percentile(values, 75)
    iqr = q3 - q1
    whisker_low = max(values.min(), q1 - 1.5 * iqr)
    whisker_high = min(values.max(), q3 + 1.5 * iqr)

    # Find actual whisker values (closest data points within IQR range)
    lower_whisker = values[values >= q1 - 1.5 * iqr].min()
    upper_whisker = values[values <= q3 + 1.5 * iqr].max()

    box_data.append([lower_whisker, q1, median, q3, upper_whisker])

    # Collect outliers
    outliers = values[(values < q1 - 1.5 * iqr) | (values > q3 + 1.5 * iqr)]
    for outlier in outliers:
        outlier_data.append([i, outlier])

# Create chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration
chart.options.chart = {
    "type": "boxplot",
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#ffffff",
    "style": {"fontFamily": "sans-serif"},
}

# Title
chart.options.title = {"text": "Basic Box Plot", "style": {"fontSize": "60px", "fontWeight": "bold"}}

# X-axis
chart.options.x_axis = {
    "categories": list(groups),
    "title": {"text": "Group", "style": {"fontSize": "48px"}},
    "labels": {"style": {"fontSize": "40px"}},
}

# Y-axis
chart.options.y_axis = {
    "title": {"text": "Value", "style": {"fontSize": "48px"}},
    "labels": {"style": {"fontSize": "40px"}},
    "gridLineColor": "#e0e0e0",
    "gridLineWidth": 1,
}

# Legend
chart.options.legend = {"enabled": True, "itemStyle": {"fontSize": "40px"}}

# Colors from style guide
colors = ["#306998", "#FFD43B", "#DC2626", "#059669", "#8B5CF6", "#F97316"]

# Box plot series
box_series = BoxPlotSeries()
box_series.name = "Distribution"
box_series.data = box_data
box_series.color = colors[0]
box_series.fillColor = "#306998"
box_series.medianColor = "#ffffff"
box_series.medianWidth = 4
box_series.stemWidth = 3
box_series.whiskerWidth = 3
box_series.whiskerLength = "50%"

chart.add_series(box_series)

# Outliers series (if any)
if outlier_data:
    from highcharts_core.options.series.scatter import ScatterSeries

    outlier_series = ScatterSeries()
    outlier_series.name = "Outliers"
    outlier_series.data = outlier_data
    outlier_series.color = colors[2]
    outlier_series.marker = {"symbol": "circle", "radius": 8, "fillColor": colors[2]}
    chart.add_series(outlier_series)

# Plot options
chart.options.plot_options = {"boxplot": {"colorByPoint": True, "colors": colors[:4]}}

# Download Highcharts JS files (required for headless Chrome)
highcharts_url = "https://code.highcharts.com/highcharts.js"
with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

highcharts_more_url = "https://code.highcharts.com/highcharts-more.js"
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
