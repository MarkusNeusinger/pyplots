""" pyplots.ai
bar-categorical: Categorical Count Bar Chart
Library: highcharts unknown | Python 3.13.11
Quality: 91/100 | Created: 2025-12-30
"""

import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd
from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.bar import ColumnSeries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - simulated product category purchases
np.random.seed(42)
categories = ["Electronics", "Clothing", "Books", "Home & Garden", "Sports", "Toys"]
# Create raw categorical data with different frequencies
raw_data = np.random.choice(
    categories,
    size=500,
    p=[0.25, 0.20, 0.18, 0.15, 0.12, 0.10],  # Different probabilities for variety
)

# Count occurrences
counts = pd.Series(raw_data).value_counts().sort_values(ascending=False)
category_names = counts.index.tolist()
category_counts = counts.values.tolist()

# Create chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration
chart.options.chart = {
    "type": "column",
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#ffffff",
    "marginBottom": 250,
    "spacingBottom": 50,
}

# Title
chart.options.title = {
    "text": "bar-categorical · highcharts · pyplots.ai",
    "style": {"fontSize": "48px", "fontWeight": "bold"},
}

# Subtitle
chart.options.subtitle = {"text": "Product Category Purchase Frequency", "style": {"fontSize": "32px"}}

# X-axis (categories)
chart.options.x_axis = {
    "categories": category_names,
    "title": {"text": "Product Category", "style": {"fontSize": "36px"}, "margin": 20},
    "labels": {"style": {"fontSize": "32px"}},
}

# Y-axis (counts)
chart.options.y_axis = {
    "title": {"text": "Count", "style": {"fontSize": "36px"}},
    "labels": {"style": {"fontSize": "28px"}},
    "gridLineWidth": 1,
    "gridLineColor": "#e0e0e0",
}

# Series
series = ColumnSeries()
series.name = "Purchases"
series.data = category_counts
series.color = "#306998"

chart.add_series(series)

# Plot options
chart.options.plot_options = {
    "column": {
        "borderRadius": 4,
        "dataLabels": {"enabled": True, "format": "{y}", "style": {"fontSize": "24px", "fontWeight": "bold"}},
    }
}

# Legend
chart.options.legend = {"enabled": False}

# Credits
chart.options.credits = {"enabled": False}

# Download Highcharts JS for headless Chrome
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

# Also save interactive HTML
with open("plot.html", "w", encoding="utf-8") as f:
    # For standalone HTML, include CDN link
    standalone_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://code.highcharts.com/highcharts.js"></script>
</head>
<body style="margin:0;">
    <div id="container" style="width: 100%; height: 600px;"></div>
    <script>{html_str}</script>
</body>
</html>"""
    f.write(standalone_html)

# Capture PNG with Selenium
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
