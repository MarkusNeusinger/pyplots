""" pyplots.ai
cat-strip: Categorical Strip Plot
Library: highcharts unknown | Python 3.13.11
Quality: 91/100 | Created: 2025-12-30
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


# Data - Plant growth measurements across different fertilizer types
np.random.seed(42)
categories = ["Control", "Fertilizer A", "Fertilizer B", "Fertilizer C"]
n_per_category = 25

data_by_category = {}
# Control: lower growth, moderate spread
data_by_category["Control"] = np.random.normal(loc=15, scale=3, size=n_per_category)
# Fertilizer A: moderate growth, tight spread
data_by_category["Fertilizer A"] = np.random.normal(loc=22, scale=2, size=n_per_category)
# Fertilizer B: high growth, wider spread with some outliers
data_by_category["Fertilizer B"] = np.concatenate(
    [
        np.random.normal(loc=28, scale=4, size=n_per_category - 3),
        np.array([38, 40, 12]),  # outliers
    ]
)
# Fertilizer C: moderate-high growth, bimodal distribution
data_by_category["Fertilizer C"] = np.concatenate(
    [
        np.random.normal(loc=20, scale=2, size=n_per_category // 2),
        np.random.normal(loc=30, scale=2, size=n_per_category - n_per_category // 2),
    ]
)

# Colors for each category
colors = ["#306998", "#FFD43B", "#9467BD", "#17BECF"]

# Create chart
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

# X-axis (categories)
chart.options.x_axis = {
    "categories": categories,
    "title": {"text": "Treatment Group", "style": {"fontSize": "36px"}},
    "labels": {"style": {"fontSize": "28px"}},
    "gridLineWidth": 1,
    "gridLineColor": "rgba(0, 0, 0, 0.1)",
}

# Y-axis (values)
chart.options.y_axis = {
    "title": {"text": "Plant Height (cm)", "style": {"fontSize": "36px"}},
    "labels": {"style": {"fontSize": "28px"}},
    "gridLineWidth": 1,
    "gridLineColor": "rgba(0, 0, 0, 0.1)",
}

# Legend - position at top right for better visibility
chart.options.legend = {
    "enabled": True,
    "itemStyle": {"fontSize": "32px"},
    "symbolHeight": 20,
    "symbolWidth": 20,
    "symbolRadius": 10,
    "layout": "vertical",
    "align": "right",
    "verticalAlign": "top",
    "x": -50,
    "y": 80,
    "borderWidth": 1,
    "borderColor": "#cccccc",
    "backgroundColor": "#ffffff",
    "padding": 15,
}

# Plot options
chart.options.plot_options = {
    "scatter": {
        "marker": {"radius": 14, "symbol": "circle"},
        "jitter": {"x": 0.2, "y": 0},  # Highcharts built-in jitter
    }
}

# Add series for each category
for i, (cat, values) in enumerate(data_by_category.items()):
    series = ScatterSeries()
    # For jitter to work with categories, we use category index as x
    series.data = [[i, float(v)] for v in values]
    series.name = cat
    series.color = colors[i]
    series.marker = {"fillColor": colors[i], "lineWidth": 2, "lineColor": "#ffffff"}
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
