"""
box-basic: Basic Box Plot
Library: highcharts

Note: Highcharts requires a license for commercial use.
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
from highcharts_core.options.series.scatter import ScatterSeries
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
groups = sorted(data["group"].unique())
box_data = []
outliers_data = []

for i, group in enumerate(groups):
    group_values = data[data["group"] == group]["value"].dropna()

    q1 = float(group_values.quantile(0.25))
    median = float(group_values.quantile(0.5))
    q3 = float(group_values.quantile(0.75))
    iqr = q3 - q1
    lower_whisker = max(float(group_values.min()), q1 - 1.5 * iqr)
    upper_whisker = min(float(group_values.max()), q3 + 1.5 * iqr)

    # Box plot data format: [low, q1, median, q3, high]
    box_data.append([lower_whisker, q1, median, q3, upper_whisker])

    # Find outliers
    outliers = group_values[(group_values < lower_whisker) | (group_values > upper_whisker)]
    for outlier in outliers:
        outliers_data.append([i, float(outlier)])

# Create chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration
chart.options.chart = {"type": "boxplot", "width": 4800, "height": 2700, "backgroundColor": "#ffffff"}

# Title
chart.options.title = {"text": "Basic Box Plot", "style": {"fontSize": "60px", "fontWeight": "bold"}}

# X-axis
chart.options.x_axis = {
    "categories": groups,
    "title": {"text": "Group", "style": {"fontSize": "60px"}},
    "labels": {"style": {"fontSize": "48px"}},
}

# Y-axis
chart.options.y_axis = {
    "title": {"text": "Value", "style": {"fontSize": "60px"}},
    "labels": {"style": {"fontSize": "48px"}},
    "gridLineWidth": 1,
    "gridLineDashStyle": "Dot",
    "gridLineColor": "rgba(0, 0, 0, 0.3)",
}

# Colors (using palette from style guide)
colors = ["#306998", "#FFD43B", "#059669", "#8B5CF6"]

# Plot options
chart.options.plot_options = {
    "boxplot": {
        "fillColor": None,
        "lineWidth": 4,
        "medianWidth": 6,
        "medianColor": "#DC2626",
        "stemWidth": 2,
        "whiskerWidth": 4,
        "whiskerLength": "50%",
        "colorByPoint": True,
    }
}

# Tooltip
chart.options.tooltip = {
    "shared": False,
    "useHTML": True,
    "headerFormat": "<b>{point.key}</b><br/>",
    "pointFormat": (
        "<span>Max: {point.high:.1f}</span><br/>"
        "<span>Q3: {point.q3:.1f}</span><br/>"
        '<span style="color: #DC2626; font-weight: bold;">Median: {point.median:.1f}</span><br/>'
        "<span>Q1: {point.q1:.1f}</span><br/>"
        "<span>Min: {point.low:.1f}</span><br/>"
    ),
    "style": {"fontSize": "36px"},
}

# Add box plot series
box_series = BoxPlotSeries()
box_series.data = box_data
box_series.name = "Distribution"
chart.options.colors = colors
chart.add_series(box_series)

# Add outliers as scatter series if any exist
if outliers_data:
    scatter_series = ScatterSeries()
    scatter_series.data = outliers_data
    scatter_series.name = "Outliers"
    scatter_series.color = "#DC2626"
    scatter_series.marker = {
        "fillColor": "#DC2626",
        "lineWidth": 2,
        "lineColor": "#000000",
        "radius": 8,
        "symbol": "circle",
    }
    scatter_series.tooltip = {"pointFormat": "Outlier: <b>{point.y:.1f}</b>"}
    chart.add_series(scatter_series)

# Legend
chart.options.legend = {"enabled": False}

# Credits
chart.options.credits = {"enabled": False}

# Download Highcharts JS (required for headless Chrome)
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
