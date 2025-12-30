"""pyplots.ai
polar-bar: Polar Bar Chart (Wind Rose)
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
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - Wind direction frequency (typical wind rose data)
np.random.seed(42)
directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]

# Generate realistic wind data with varying frequencies
# Higher frequencies for prevailing wind directions (SW, W typical for many locations)
base_frequencies = [12, 8, 10, 6, 9, 18, 22, 15]
frequencies = [f + np.random.randint(-2, 3) for f in base_frequencies]

# Create chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration for polar bar
chart.options.chart = {
    "polar": True,
    "type": "column",
    "width": 3600,
    "height": 3600,
    "backgroundColor": "#ffffff",
    "marginTop": 200,
    "marginBottom": 250,
}

# Title
chart.options.title = {
    "text": "polar-bar · highcharts · pyplots.ai",
    "style": {"fontSize": "48px", "fontWeight": "bold"},
    "y": 60,
}

# Subtitle
chart.options.subtitle = {"text": "Wind Direction Distribution", "style": {"fontSize": "32px"}, "y": 110}

# Pane configuration for polar chart
chart.options.pane = {"size": "65%", "center": ["50%", "48%"]}

# X-axis (angular axis with directions)
chart.options.x_axis = {
    "categories": directions,
    "tickmarkPlacement": "on",
    "lineWidth": 0,
    "labels": {"style": {"fontSize": "28px", "fontWeight": "bold"}, "distance": 25},
    "gridLineWidth": 2,
    "gridLineColor": "#e0e0e0",
}

# Y-axis (radial axis for frequency)
chart.options.y_axis = {
    "min": 0,
    "max": 30,
    "tickInterval": 10,
    "gridLineInterpolation": "polygon",
    "gridLineWidth": 2,
    "gridLineColor": "#e0e0e0",
    "labels": {"style": {"fontSize": "22px"}, "format": "{value}%"},
    "title": {"text": "Frequency (%)", "style": {"fontSize": "24px"}, "x": -10},
}

# Plot options
chart.options.plot_options = {
    "column": {
        "pointPadding": 0,
        "groupPadding": 0,
        "borderWidth": 2,
        "borderColor": "#ffffff",
        "dataLabels": {
            "enabled": True,
            "format": "{y}%",
            "style": {"fontSize": "20px", "fontWeight": "bold", "textOutline": "2px white"},
        },
    },
    "series": {"pointPlacement": "on"},
}

# Legend
chart.options.legend = {
    "enabled": True,
    "align": "center",
    "verticalAlign": "bottom",
    "layout": "horizontal",
    "itemStyle": {"fontSize": "32px"},
    "symbolRadius": 0,
    "symbolHeight": 24,
    "symbolWidth": 24,
    "y": -50,
}

# Add series data
chart.options.series = [
    {"type": "column", "name": "Wind Frequency", "data": frequencies, "color": "#306998", "borderRadius": 3}
]

# Credits
chart.options.credits = {"enabled": False}

# Download Highcharts JS files for inline embedding (required for headless Chrome)
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
<body style="margin:0; padding:0; background-color:#ffffff;">
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
    # For HTML output, use CDN links (works in browser)
    html_output = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://code.highcharts.com/highcharts.js"></script>
    <script src="https://code.highcharts.com/highcharts-more.js"></script>
</head>
<body style="margin:0; padding:0; background-color:#ffffff;">
    <div id="container" style="width: 100%; height: 100vh;"></div>
    <script>{html_str}</script>
</body>
</html>"""
    f.write(html_output)

# Setup Chrome for screenshot
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
