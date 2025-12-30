"""pyplots.ai
bar-sorted: Sorted Bar Chart
Library: highcharts | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import tempfile
import time
import urllib.request
from pathlib import Path

from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.bar import BarSeries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - Monthly sales by product category (in thousands $)
categories = [
    "Electronics",
    "Clothing",
    "Home & Garden",
    "Sports Equipment",
    "Books & Media",
    "Toys & Games",
    "Automotive",
    "Health & Beauty",
    "Office Supplies",
    "Pet Supplies",
]
values = [145, 98, 76, 62, 54, 48, 42, 38, 31, 25]

# Sort by value (descending) - largest at top for horizontal bar chart
sorted_pairs = sorted(zip(categories, values, strict=True), key=lambda x: x[1], reverse=False)
categories = [p[0] for p in sorted_pairs]
values = [p[1] for p in sorted_pairs]

# Create chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart settings (horizontal bar chart)
chart.options.chart = {
    "type": "bar",
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#ffffff",
    "marginLeft": 300,
    "marginRight": 150,
    "marginBottom": 150,
    "marginTop": 180,
}

# Title
chart.options.title = {
    "text": "bar-sorted \u00b7 highcharts \u00b7 pyplots.ai",
    "style": {"fontSize": "48px", "fontWeight": "bold"},
}

# Subtitle with context
chart.options.subtitle = {
    "text": "Monthly Sales by Product Category",
    "style": {"fontSize": "32px", "color": "#666666"},
}

# X-axis (categories on y-axis for horizontal bar)
chart.options.x_axis = {
    "categories": categories,
    "title": {"text": None},
    "labels": {"style": {"fontSize": "28px"}},
    "lineWidth": 0,
}

# Y-axis (values - appears at bottom for bar chart)
chart.options.y_axis = {
    "min": 0,
    "title": {"text": "Sales (thousands USD)", "style": {"fontSize": "32px"}, "margin": 30},
    "labels": {"style": {"fontSize": "24px"}, "format": "{value}K"},
    "gridLineWidth": 1,
    "gridLineColor": "#e0e0e0",
    "gridLineDashStyle": "Dash",
}

# Plot options
chart.options.plot_options = {
    "bar": {
        "dataLabels": {
            "enabled": True,
            "format": "{y}K",
            "style": {"fontSize": "24px", "fontWeight": "bold", "color": "#333333"},
            "align": "left",
            "x": 10,
        },
        "pointPadding": 0.1,
        "groupPadding": 0.1,
        "borderWidth": 0,
        "borderRadius": 4,
        "colorByPoint": False,
    }
}

# Legend
chart.options.legend = {"enabled": False}

# Credits
chart.options.credits = {"enabled": False}

# Series
series = BarSeries()
series.name = "Sales"
series.data = values
series.color = "#306998"

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

# Write temp HTML file
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

# Save standalone HTML
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Take screenshot with Selenium
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=4800,2700")
chrome_options.add_argument("--hide-scrollbars")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)

# Screenshot the chart container element directly for exact dimensions
container = driver.find_element("id", "container")
container.screenshot("plot.png")
driver.quit()

# Clean up temp file
Path(temp_path).unlink()
