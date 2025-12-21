""" pyplots.ai
box-basic: Basic Box Plot
Library: highcharts 1.10.3 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-14
"""

import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.boxplot import BoxPlotSeries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - generate sample data for 5 categories
np.random.seed(42)
categories = ["Group A", "Group B", "Group C", "Group D", "Group E"]
colors = ["#306998", "#FFD43B", "#9467BD", "#17BECF", "#8C564B"]

# Generate data for each category (100 points each)
raw_data = {
    "Group A": np.random.normal(50, 10, 100),
    "Group B": np.random.normal(65, 15, 100),
    "Group C": np.random.normal(45, 8, 100),
    "Group D": np.random.normal(70, 12, 100),
    "Group E": np.random.normal(55, 20, 100),
}


# Calculate box plot statistics for each category
def calc_boxplot_stats(data):
    q1 = np.percentile(data, 25)
    median = np.percentile(data, 50)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1
    whisker_low = max(data.min(), q1 - 1.5 * iqr)
    whisker_high = min(data.max(), q3 + 1.5 * iqr)

    # Find outliers
    outliers = data[(data < whisker_low) | (data > whisker_high)]

    return {
        "low": float(whisker_low),
        "q1": float(q1),
        "median": float(median),
        "q3": float(q3),
        "high": float(whisker_high),
        "outliers": outliers.tolist(),
    }


box_data = []
outlier_data = []
for i, cat in enumerate(categories):
    stats = calc_boxplot_stats(raw_data[cat])
    box_data.append([stats["low"], stats["q1"], stats["median"], stats["q3"], stats["high"]])
    # Add outliers with x-index
    for outlier in stats["outliers"]:
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
    "marginBottom": 300,
    "spacingBottom": 80,
}

# Title
chart.options.title = {
    "text": "box-basic · highcharts · pyplots.ai",
    "style": {"fontSize": "72px", "fontWeight": "bold"},
}

# X-axis
chart.options.x_axis = {
    "categories": categories,
    "title": {"text": "Category", "style": {"fontSize": "48px"}},
    "labels": {"style": {"fontSize": "36px"}},
}

# Y-axis
chart.options.y_axis = {
    "title": {"text": "Value", "style": {"fontSize": "48px"}},
    "labels": {"style": {"fontSize": "36px"}},
    "gridLineWidth": 1,
    "gridLineColor": "#e0e0e0",
}

# Legend
chart.options.legend = {"enabled": True, "itemStyle": {"fontSize": "36px"}}

# Plot options for styling
chart.options.plot_options = {
    "boxplot": {
        "fillColor": "#306998",
        "lineWidth": 4,
        "medianWidth": 6,
        "medianColor": "#FFD43B",
        "stemWidth": 3,
        "whiskerWidth": 4,
        "whiskerLength": "50%",
        "colorByPoint": True,
    }
}

# Box plot series
box_series = BoxPlotSeries()
box_series.name = "Distribution"
box_series.data = box_data
box_series.colors = colors

chart.add_series(box_series)

# Outliers as scatter series
if outlier_data:
    from highcharts_core.options.series.scatter import ScatterSeries

    outlier_series = ScatterSeries()
    outlier_series.name = "Outliers"
    outlier_series.data = outlier_data
    outlier_series.marker = {
        "fillColor": "#E74C3C",
        "lineWidth": 2,
        "lineColor": "#C0392B",
        "radius": 10,
        "symbol": "circle",
    }
    chart.add_series(outlier_series)

# Download Highcharts JS files (required for headless Chrome)
highcharts_url = "https://code.highcharts.com/highcharts.js"
with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

# BoxPlot requires highcharts-more.js
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

# Write temp HTML file
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

# Save HTML file for interactive viewing
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Take screenshot with Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=4800,2700")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)  # Wait for chart to render
driver.save_screenshot("plot.png")
driver.quit()

# Clean up temp file
Path(temp_path).unlink()
