"""pyplots.ai
cat-strip: Categorical Strip Plot
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
from highcharts_core.options.series.scatter import ScatterSeries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - Test scores across different study methods
np.random.seed(42)
categories = ["Online Course", "Textbook", "Tutor", "Group Study", "Self-Study"]
n_per_category = 25

data_by_category = {}
# Generate different distributions for each category
data_by_category["Online Course"] = np.random.normal(72, 8, n_per_category)
data_by_category["Textbook"] = np.random.normal(68, 12, n_per_category)
data_by_category["Tutor"] = np.random.normal(82, 6, n_per_category)
data_by_category["Group Study"] = np.random.normal(75, 10, n_per_category)
data_by_category["Self-Study"] = np.random.normal(65, 15, n_per_category)

# Clip scores to realistic range (0-100)
for cat in categories:
    data_by_category[cat] = np.clip(data_by_category[cat], 30, 100)

# Create chart with container
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration
chart.options.chart = {
    "type": "scatter",
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#ffffff",
    "marginBottom": 250,
    "spacingBottom": 50,
}

# Title
chart.options.title = {
    "text": "cat-strip · highcharts · pyplots.ai",
    "style": {"fontSize": "48px", "fontWeight": "bold"},
}

# Subtitle
chart.options.subtitle = {"text": "Test Scores by Study Method", "style": {"fontSize": "32px"}}

# X-axis (categories)
chart.options.x_axis = {
    "categories": categories,
    "title": {"text": "Study Method", "style": {"fontSize": "36px"}},
    "labels": {"style": {"fontSize": "28px"}},
    "gridLineWidth": 1,
    "gridLineColor": "#e0e0e0",
}

# Y-axis (values)
chart.options.y_axis = {
    "title": {"text": "Test Score (points)", "style": {"fontSize": "36px"}},
    "labels": {"style": {"fontSize": "28px"}},
    "min": 40,
    "max": 105,
    "gridLineWidth": 1,
    "gridLineColor": "#e0e0e0",
    "gridLineDashStyle": "Dash",
}

# Plot options for scatter with jitter
chart.options.plot_options = {
    "scatter": {
        "marker": {"radius": 14, "symbol": "circle"},
        "jitter": {"x": 0.25, "y": 0},  # Horizontal jitter to prevent overlap
    }
}

# Legend
chart.options.legend = {
    "enabled": True,
    "itemStyle": {"fontSize": "26px"},
    "align": "right",
    "verticalAlign": "middle",
    "layout": "vertical",
}

# Colors - colorblind-safe palette
colors = ["#306998", "#FFD43B", "#9467BD", "#17BECF", "#8C564B"]

# Add series for each category
for i, category in enumerate(categories):
    series = ScatterSeries()
    # Data format: [[x_index, y_value], ...]
    series.data = [[i, float(val)] for val in data_by_category[category]]
    series.name = category
    series.color = colors[i]
    chart.add_series(series)

# Download Highcharts JS
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
chrome_options.add_argument("--window-size=4800,2800")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)
driver.save_screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()

# Also save HTML for interactive version
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)
