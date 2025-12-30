"""pyplots.ai
polar-line: Polar Line Plot
Library: highcharts | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import tempfile
import time
import urllib.request
from pathlib import Path

from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data: Simulated seasonal temperature pattern (monthly averages in °C)
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# City A: Temperate climate with summer peak
city_a_temps = [2, 4, 9, 14, 18, 22, 25, 24, 19, 13, 7, 3]
# City B: Southern hemisphere with opposite seasons
city_b_temps = [23, 22, 19, 14, 10, 7, 6, 8, 12, 16, 19, 22]

# Create chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration for polar
chart.options.chart = {"polar": True, "width": 3600, "height": 3600, "backgroundColor": "#ffffff", "spacingBottom": 120}

# Title
chart.options.title = {
    "text": "polar-line · highcharts · pyplots.ai",
    "style": {"fontSize": "48px", "fontWeight": "bold"},
}

chart.options.subtitle = {"text": "Monthly Temperature Pattern (°C)", "style": {"fontSize": "32px"}}

# Pane (polar chart configuration)
chart.options.pane = {"startAngle": 0, "endAngle": 360, "size": "85%", "center": ["50%", "48%"]}

# Y-axis (radial) - temperature values
chart.options.y_axis = {
    "min": 0,
    "max": 30,
    "tickInterval": 5,
    "labels": {"style": {"fontSize": "24px"}, "format": "{value}°C"},
    "gridLineWidth": 2,
    "gridLineColor": "rgba(0, 0, 0, 0.15)",
    "gridLineInterpolation": "circle",
}

# X-axis (angular) - categories for months
chart.options.x_axis = {
    "categories": months,
    "tickmarkPlacement": "on",
    "lineWidth": 0,
    "labels": {"style": {"fontSize": "28px"}},
    "gridLineWidth": 2,
    "gridLineColor": "rgba(0, 0, 0, 0.1)",
}

# Plot options for line styling with connectEnds to close the polar loop
chart.options.plot_options = {
    "line": {
        "lineWidth": 5,
        "connectEnds": True,
        "marker": {"enabled": True, "radius": 10, "symbol": "circle"},
        "dataLabels": {"enabled": False},
    }
}

# Legend - positioned below the chart
chart.options.legend = {
    "enabled": True,
    "itemStyle": {"fontSize": "32px"},
    "align": "center",
    "verticalAlign": "bottom",
    "layout": "horizontal",
    "y": -20,
}

# Series data
chart.options.series = [
    {
        "type": "line",
        "name": "City A (Northern Hemisphere)",
        "data": city_a_temps,
        "color": "#306998",
        "marker": {"fillColor": "#306998"},
    },
    {
        "type": "line",
        "name": "City B (Southern Hemisphere)",
        "data": city_b_temps,
        "color": "#FFD43B",
        "marker": {"fillColor": "#FFD43B"},
    },
]

# Credits
chart.options.credits = {"enabled": False}

# Download Highcharts JS and highcharts-more for polar support
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
<body style="margin:0; background-color: #ffffff;">
    <div id="container" style="width: 3600px; height: 3600px;"></div>
    <script>{html_str}</script>
</body>
</html>"""

# Write temp HTML and take screenshot
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

# Also save HTML for interactive version
with open("plot.html", "w", encoding="utf-8") as f:
    # For standalone HTML, use CDN links
    standalone_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>polar-line · highcharts · pyplots.ai</title>
    <script src="https://code.highcharts.com/highcharts.js"></script>
    <script src="https://code.highcharts.com/highcharts-more.js"></script>
</head>
<body style="margin:0; background-color: #ffffff; display: flex; justify-content: center; align-items: center; min-height: 100vh;">
    <div id="container" style="width: 90vmin; height: 90vmin; max-width: 1200px; max-height: 1200px;"></div>
    <script>{html_str}</script>
</body>
</html>"""
    f.write(standalone_html)

# Configure Chrome for headless screenshot
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=3600,3600")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)  # Wait for chart to render
driver.save_screenshot("plot.png")
driver.quit()

# Clean up temp file
Path(temp_path).unlink()
