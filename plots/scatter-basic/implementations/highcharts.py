""" pyplots.ai
scatter-basic: Basic Scatter Plot
Library: highcharts 1.10.3 | Python 3.14.2
Quality: /100 | Updated: 2026-02-10
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


# Data - Daily temperature vs iced coffee sales at a cafe
np.random.seed(42)
temperature = np.random.normal(22, 8, 120).clip(2, 40)  # Daily temp in Celsius
iced_sales = temperature * 2.8 + np.random.normal(0, 8, 120)  # Iced drinks sold
iced_sales = iced_sales.clip(5, None)

# Create chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration
chart.options.chart = {
    "type": "scatter",
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#FAFBFC",
    "marginBottom": 220,
    "marginLeft": 200,
    "marginTop": 200,
    "style": {"fontFamily": "'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif"},
}

# Title
chart.options.title = {
    "text": "scatter-basic \u00b7 highcharts \u00b7 pyplots.ai",
    "style": {"fontSize": "64px", "fontWeight": "600", "color": "#2D3748", "letterSpacing": "1px"},
    "margin": 60,
}

# Subtitle for context
chart.options.subtitle = {
    "text": "Daily Temperature vs Iced Coffee Sales \u2014 120 days observed",
    "style": {"fontSize": "40px", "color": "#718096", "fontWeight": "400"},
}

# X-axis
chart.options.x_axis = {
    "title": {
        "text": "Daily Temperature (\u00b0C)",
        "style": {"fontSize": "44px", "color": "#4A5568", "fontWeight": "500"},
        "margin": 30,
    },
    "labels": {"style": {"fontSize": "34px", "color": "#718096"}},
    "gridLineWidth": 1,
    "gridLineColor": "rgba(203, 213, 224, 0.5)",
    "gridLineDashStyle": "Dot",
    "lineColor": "#CBD5E0",
    "lineWidth": 2,
    "tickColor": "#CBD5E0",
    "tickWidth": 2,
    "tickLength": 10,
}

# Y-axis
chart.options.y_axis = {
    "title": {
        "text": "Iced Drinks Sold",
        "style": {"fontSize": "44px", "color": "#4A5568", "fontWeight": "500"},
        "margin": 30,
    },
    "labels": {"style": {"fontSize": "34px", "color": "#718096"}},
    "gridLineWidth": 1,
    "gridLineColor": "rgba(203, 213, 224, 0.5)",
    "gridLineDashStyle": "Dot",
    "lineColor": "#CBD5E0",
    "lineWidth": 2,
    "tickColor": "#CBD5E0",
    "tickWidth": 2,
    "tickLength": 10,
}

# Legend and credits
chart.options.legend = {"enabled": False}
chart.options.credits = {"enabled": False}

# Tooltip styling for interactive HTML version
chart.options.tooltip = {
    "headerFormat": "",
    "pointFormat": "<b>{point.x:.1f}\u00b0C</b> \u2192 <b>{point.y:.0f}</b> drinks",
    "style": {"fontSize": "28px"},
    "backgroundColor": "rgba(255, 255, 255, 0.95)",
    "borderColor": "#306998",
    "borderRadius": 8,
    "shadow": {"color": "rgba(0,0,0,0.1)", "offsetX": 2, "offsetY": 2, "width": 4},
}

# Split data into warm and cool groups for visual interest
cool_mask = temperature < 18
warm_mask = ~cool_mask

# Cool days series (blue tones)
series_cool = ScatterSeries()
series_cool.data = [
    [float(xi), float(yi)] for xi, yi in zip(temperature[cool_mask], iced_sales[cool_mask], strict=True)
]
series_cool.name = "Cool Days (< 18\u00b0C)"
series_cool.color = "rgba(48, 105, 152, 0.75)"
series_cool.marker = {"radius": 16, "symbol": "circle", "lineWidth": 2, "lineColor": "rgba(48, 105, 152, 0.9)"}

# Warm days series (amber/gold tones)
series_warm = ScatterSeries()
series_warm.data = [
    [float(xi), float(yi)] for xi, yi in zip(temperature[warm_mask], iced_sales[warm_mask], strict=True)
]
series_warm.name = "Warm Days (\u2265 18\u00b0C)"
series_warm.color = "rgba(255, 179, 25, 0.75)"
series_warm.marker = {"radius": 16, "symbol": "circle", "lineWidth": 2, "lineColor": "rgba(214, 138, 0, 0.9)"}

chart.add_series(series_cool)
chart.add_series(series_warm)

# Enable legend for two series - positioned inside top-left
chart.options.legend = {
    "enabled": True,
    "layout": "vertical",
    "align": "left",
    "verticalAlign": "top",
    "x": 180,
    "y": 120,
    "floating": True,
    "backgroundColor": "rgba(255, 255, 255, 0.85)",
    "borderColor": "#E2E8F0",
    "borderWidth": 2,
    "borderRadius": 8,
    "padding": 20,
    "itemStyle": {"fontSize": "34px", "fontWeight": "500", "color": "#4A5568"},
    "symbolRadius": 8,
    "itemMarginBottom": 10,
}

# Download Highcharts JS (required for headless Chrome)
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

# Take screenshot of just the chart container element
container = driver.find_element("id", "container")
container.screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()

# Also save HTML for interactive version
with open("plot.html", "w", encoding="utf-8") as f:
    interactive_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://code.highcharts.com/highcharts.js"></script>
</head>
<body style="margin:0;">
    <div id="container" style="width: 100%; height: 100vh;"></div>
    <script>{html_str}</script>
</body>
</html>"""
    f.write(interactive_html)
