""" pyplots.ai
box-basic: Basic Box Plot
Library: highcharts 1.10.3 | Python 3.14
Quality: 79/100 | Created: 2025-12-23
"""

import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.boxplot import BoxPlotSeries
from highcharts_core.options.series.scatter import ScatterSeries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - employee performance scores across 5 departments
np.random.seed(42)
departments = ["Engineering", "Marketing", "Sales", "Design", "Finance"]
colors = ["#306998", "#FFD43B", "#9467BD", "#17BECF", "#8C564B"]

scores = [
    np.random.normal(78, 8, 80),  # Engineering: high, tight
    np.random.normal(72, 14, 60),  # Marketing: moderate, wide spread
    np.random.normal(68, 9, 90),  # Sales: lower mean, moderate
    np.random.normal(82, 7, 50),  # Design: highest, tight
    np.random.normal(75, 18, 70),  # Finance: moderate, widest spread
]

# Calculate box plot statistics
box_stats = []
outlier_data = []

for i, data in enumerate(scores):
    data = np.clip(data, 0, 100)
    q1 = float(np.percentile(data, 25))
    median = float(np.percentile(data, 50))
    q3 = float(np.percentile(data, 75))
    iqr = q3 - q1
    whisker_low = float(max(data[data >= q1 - 1.5 * iqr].min(), data.min()))
    whisker_high = float(min(data[data <= q3 + 1.5 * iqr].max(), data.max()))

    box_stats.append(
        {
            "low": round(whisker_low, 1),
            "q1": round(q1, 1),
            "median": round(median, 1),
            "q3": round(q3, 1),
            "high": round(whisker_high, 1),
        }
    )

    outliers = data[(data < q1 - 1.5 * iqr) | (data > q3 + 1.5 * iqr)]
    for val in outliers:
        outlier_data.append({"x": i, "y": round(float(val), 1)})

# Build fill colors (75% opacity)
fill_colors = []
for c in colors:
    r, g, b = int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16)
    fill_colors.append(f"rgba({r}, {g}, {b}, 0.75)")

# Create chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

chart.options.chart = {
    "type": "boxplot",
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#ffffff",
    "marginBottom": 260,
    "spacingBottom": 60,
    "spacingLeft": 40,
    "style": {"fontFamily": "Arial, Helvetica, sans-serif"},
}

chart.options.title = {
    "text": "box-basic \u00b7 highcharts \u00b7 pyplots.ai",
    "style": {"fontSize": "64px", "fontWeight": "600", "color": "#2c3e50"},
    "margin": 60,
}

chart.options.subtitle = {
    "text": "Annual Performance Review Scores by Department",
    "style": {"fontSize": "42px", "color": "#7f8c8d"},
}

chart.options.x_axis = {
    "categories": departments,
    "title": {"text": "Department", "style": {"fontSize": "44px", "color": "#34495e"}},
    "labels": {"style": {"fontSize": "38px", "color": "#34495e"}},
    "lineColor": "#bdc3c7",
    "lineWidth": 2,
    "tickWidth": 0,
}

chart.options.y_axis = {
    "title": {"text": "Score (out of 100)", "style": {"fontSize": "44px", "color": "#34495e"}},
    "labels": {"style": {"fontSize": "34px", "color": "#7f8c8d"}},
    "gridLineWidth": 1,
    "gridLineColor": "rgba(0, 0, 0, 0.06)",
    "tickInterval": 5,
}

chart.options.legend = {"enabled": False}
chart.options.credits = {"enabled": False}

chart.options.plot_options = {
    "boxplot": {
        "lineWidth": 4,
        "medianWidth": 6,
        "medianColor": "#1a1a1a",
        "stemWidth": 3,
        "stemDashStyle": "Solid",
        "whiskerWidth": 4,
        "whiskerLength": "50%",
        "whiskerColor": "#555555",
        "pointWidth": 350,
        "tooltip": {
            "headerFormat": "<b>{point.key}</b><br/>",
            "pointFormat": (
                "Max: {point.high}<br/>"
                "Q3: {point.q3}<br/>"
                "Median: {point.median}<br/>"
                "Q1: {point.q1}<br/>"
                "Min: {point.low}<br/>"
            ),
        },
    }
}

# One series per department for distinct colors
for i, dept in enumerate(departments):
    series = BoxPlotSeries()
    series.name = dept
    series.data = [
        {
            "x": i,
            "low": box_stats[i]["low"],
            "q1": box_stats[i]["q1"],
            "median": box_stats[i]["median"],
            "q3": box_stats[i]["q3"],
            "high": box_stats[i]["high"],
        }
    ]
    series.color = colors[i]
    chart.add_series(series)

# Outlier series
if outlier_data:
    outlier_series = ScatterSeries()
    outlier_series.name = "Outliers"
    outlier_series.data = outlier_data
    outlier_series.marker = {
        "fillColor": "rgba(231, 76, 60, 0.7)",
        "lineWidth": 2,
        "lineColor": "#c0392b",
        "radius": 10,
        "symbol": "circle",
    }
    outlier_series.tooltip = {"pointFormat": "Score: {point.y}"}
    chart.add_series(outlier_series)

# Download Highcharts JS files (required for headless Chrome)
highcharts_url = "https://code.highcharts.com/highcharts.js"
with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

highcharts_more_url = "https://code.highcharts.com/highcharts-more.js"
with urllib.request.urlopen(highcharts_more_url, timeout=30) as response:
    highcharts_more_js = response.read().decode("utf-8")

# Generate JS and inject properties not supported by highcharts-core API
html_str = chart.to_js_literal()

# Inject stemColor into plotOptions (stripped by Python API)
html_str = html_str.replace("stemDashStyle: 'Solid'", "stemColor: '#555555',\n  stemDashStyle: 'Solid'")

# Inject fillColor per series
for i in range(len(departments)):
    html_str = html_str.replace(
        f"color: '{colors[i]}',\n  type: 'boxplot'",
        f"color: '{colors[i]}',\n  fillColor: '{fill_colors[i]}',\n  type: 'boxplot'",
    )

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

# Write temp HTML file
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

# Take screenshot with Selenium
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

# Clean up
Path(temp_path).unlink()
