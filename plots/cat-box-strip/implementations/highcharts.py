"""pyplots.ai
cat-box-strip: Box Plot with Strip Overlay
Library: highcharts | Python 3.13
Quality: pending | Created: 2025-12-30
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


# Data - Plant growth under different light conditions
np.random.seed(42)

categories = ["Low Light", "Medium Light", "High Light", "Full Sun"]

# Generate data with varying distributions for each category
data_by_category = {
    "Low Light": np.random.normal(loc=12, scale=3, size=30),
    "Medium Light": np.random.normal(loc=22, scale=4, size=35),
    "High Light": np.random.normal(loc=35, scale=5, size=28),
    "Full Sun": np.random.normal(loc=45, scale=6, size=32),
}

# Add some outliers to make the boxplot more interesting
data_by_category["Low Light"] = np.append(data_by_category["Low Light"], [2, 24])
data_by_category["High Light"] = np.append(data_by_category["High Light"], [18, 52])

# Calculate boxplot statistics for each category
boxplot_data = []
for cat in categories:
    values = data_by_category[cat]
    q1 = np.percentile(values, 25)
    median = np.percentile(values, 50)
    q3 = np.percentile(values, 75)
    iqr = q3 - q1
    whisker_low = max(values.min(), q1 - 1.5 * iqr)
    whisker_high = min(values.max(), q3 + 1.5 * iqr)
    boxplot_data.append([whisker_low, q1, median, q3, whisker_high])

# Prepare scatter data with jitter for strip overlay
scatter_data = []
for i, cat in enumerate(categories):
    values = data_by_category[cat]
    for val in values:
        # Add horizontal jitter for visibility
        jitter = np.random.uniform(-0.15, 0.15)
        scatter_data.append({"x": i + jitter, "y": float(val)})

# Create chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration
chart.options.chart = {
    "type": "boxplot",
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#ffffff",
    "marginBottom": 200,
    "spacingBottom": 50,
}

# Title
chart.options.title = {
    "text": "cat-box-strip · highcharts · pyplots.ai",
    "style": {"fontSize": "48px", "fontWeight": "bold"},
}

# Subtitle
chart.options.subtitle = {"text": "Plant Growth Height (cm) by Light Condition", "style": {"fontSize": "32px"}}

# X-axis (categories)
chart.options.x_axis = {
    "categories": categories,
    "title": {"text": "Light Condition", "style": {"fontSize": "36px"}},
    "labels": {"style": {"fontSize": "28px"}},
}

# Y-axis
chart.options.y_axis = {
    "title": {"text": "Plant Height (cm)", "style": {"fontSize": "36px"}},
    "labels": {"style": {"fontSize": "28px"}},
    "gridLineColor": "#e0e0e0",
    "gridLineWidth": 1,
}

# Legend
chart.options.legend = {"enabled": True, "itemStyle": {"fontSize": "26px"}}

# Plot options
chart.options.plot_options = {
    "boxplot": {
        "fillColor": "rgba(48, 105, 152, 0.5)",
        "lineWidth": 3,
        "lineColor": "#306998",
        "medianColor": "#FFD43B",
        "medianWidth": 6,
        "stemColor": "#306998",
        "stemWidth": 3,
        "whiskerColor": "#306998",
        "whiskerWidth": 4,
        "whiskerLength": "50%",
    },
    "scatter": {
        "marker": {"radius": 12, "fillColor": "rgba(255, 212, 59, 0.75)", "lineColor": "#306998", "lineWidth": 2}
    },
}

# Add box plot series with explicit styling
boxplot_series = BoxPlotSeries()
boxplot_series.name = "Distribution"
boxplot_series.data = boxplot_data
chart.add_series(boxplot_series)

# Add scatter series (strip overlay)
scatter_series = ScatterSeries()
scatter_series.name = "Data Points"
scatter_series.data = scatter_data
scatter_series.color = "rgba(255, 212, 59, 0.7)"
scatter_series.marker = {"radius": 10, "fillColor": "rgba(255, 212, 59, 0.7)", "lineColor": "#306998", "lineWidth": 2}
chart.add_series(scatter_series)

# Download Highcharts JS files
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

# Save HTML for interactive version
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)
