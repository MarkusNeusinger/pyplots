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

# Compute boxplot statistics for each group
groups = ["A", "B", "C", "D"]
boxplot_data = []
outliers_data = []

for i, group in enumerate(groups):
    values = data[data["group"] == group]["value"].values
    q1 = np.percentile(values, 25)
    median = np.percentile(values, 50)
    q3 = np.percentile(values, 75)
    iqr = q3 - q1
    whisker_low = q1 - 1.5 * iqr
    whisker_high = q3 + 1.5 * iqr

    # Actual whisker ends are the most extreme data within bounds
    low = values[values >= whisker_low].min()
    high = values[values <= whisker_high].max()

    boxplot_data.append([low, q1, median, q3, high])

    # Outliers
    outlier_values = values[(values < whisker_low) | (values > whisker_high)]
    for val in outlier_values:
        outliers_data.append([i, val])

# Create chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

chart.options.chart = {"type": "boxplot", "width": 4800, "height": 2700, "backgroundColor": "#ffffff"}

chart.options.title = {"text": "Basic Box Plot", "style": {"fontSize": "48px"}}

chart.options.x_axis = {
    "categories": groups,
    "title": {"text": "Group", "style": {"fontSize": "40px"}},
    "labels": {"style": {"fontSize": "32px"}},
}

chart.options.y_axis = {
    "title": {"text": "Value", "style": {"fontSize": "40px"}},
    "labels": {"style": {"fontSize": "32px"}},
}

chart.options.legend = {"enabled": False}

# Boxplot series
boxplot_series = BoxPlotSeries()
boxplot_series.name = "Distribution"
boxplot_series.data = boxplot_data
boxplot_series.color = "#306998"
boxplot_series.fillColor = "rgba(48, 105, 152, 0.4)"
boxplot_series.lineWidth = 3
boxplot_series.medianWidth = 4
boxplot_series.medianColor = "#DC2626"
boxplot_series.whiskerLength = "60%"
boxplot_series.whiskerWidth = 3

chart.add_series(boxplot_series)

# Outliers as scatter series
if outliers_data:
    from highcharts_core.options.series.scatter import ScatterSeries

    outlier_series = ScatterSeries()
    outlier_series.name = "Outliers"
    outlier_series.data = outliers_data
    outlier_series.color = "#DC2626"
    outlier_series.marker = {"radius": 6, "symbol": "circle"}

    chart.add_series(outlier_series)

# Download Highcharts JS and highcharts-more.js (needed for boxplot)
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
chrome_options.add_argument("--window-size=4900,2800")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)

# Take screenshot of the container element to get exact dimensions
container = driver.find_element("id", "container")
container.screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()
