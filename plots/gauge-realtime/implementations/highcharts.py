"""pyplots.ai
gauge-realtime: Real-Time Updating Gauge
Library: highcharts | Python 3.13
Quality: pending | Created: 2025-01-19
"""

import tempfile
import time
import urllib.request
from pathlib import Path

from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - simulated CPU usage with thresholds
current_value = 67  # Current CPU usage percentage
min_value = 0
max_value = 100
thresholds = [50, 80]  # Green < 50, Yellow 50-80, Red > 80

# Create chart with container
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration for gauge
chart.options.chart = {
    "type": "gauge",
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#ffffff",
    "plotBackgroundColor": None,
    "plotBorderWidth": 0,
    "plotShadow": False,
}

# Title
chart.options.title = {
    "text": "gauge-realtime · highcharts · pyplots.ai",
    "style": {"fontSize": "72px", "fontWeight": "bold"},
    "y": 80,
}

# Subtitle showing current metric context
chart.options.subtitle = {
    "text": "CPU Usage Monitor - Live Dashboard Simulation",
    "style": {"fontSize": "48px", "color": "#666666"},
    "y": 160,
}

# Pane configuration for gauge background
chart.options.pane = {
    "startAngle": -150,
    "endAngle": 150,
    "background": [
        {
            "backgroundColor": {
                "linearGradient": {"x1": 0, "y1": 0, "x2": 0, "y2": 1},
                "stops": [[0, "#FFF"], [1, "#333"]],
            },
            "borderWidth": 0,
            "outerRadius": "109%",
        },
        {
            "backgroundColor": {
                "linearGradient": {"x1": 0, "y1": 0, "x2": 0, "y2": 1},
                "stops": [[0, "#333"], [1, "#FFF"]],
            },
            "borderWidth": 1,
            "outerRadius": "107%",
        },
        {"backgroundColor": "#DDD", "borderWidth": 0, "outerRadius": "105%", "innerRadius": "103%"},
    ],
}

# Y-axis configuration with color zones for thresholds
chart.options.y_axis = {
    "min": min_value,
    "max": max_value,
    "minorTickInterval": "auto",
    "minorTickWidth": 2,
    "minorTickLength": 15,
    "minorTickPosition": "inside",
    "minorTickColor": "#666",
    "tickPixelInterval": 50,
    "tickWidth": 4,
    "tickPosition": "inside",
    "tickLength": 25,
    "tickColor": "#666",
    "labels": {"step": 2, "style": {"fontSize": "36px", "fontWeight": "bold"}},
    "title": {"text": "%", "style": {"fontSize": "48px", "fontWeight": "bold"}, "y": 40},
    "plotBands": [
        {"from": min_value, "to": thresholds[0], "color": "#55BF3B", "thickness": 40},  # Green zone
        {"from": thresholds[0], "to": thresholds[1], "color": "#DDDF0D", "thickness": 40},  # Yellow zone
        {"from": thresholds[1], "to": max_value, "color": "#DF5353", "thickness": 40},  # Red zone
    ],
}

# Tooltip configuration
chart.options.tooltip = {"enabled": False}

# Plot options for gauge
chart.options.plot_options = {
    "gauge": {
        "dataLabels": {
            "enabled": True,
            "format": "{y}%",
            "style": {"fontSize": "96px", "fontWeight": "bold", "color": "#306998"},
            "borderWidth": 0,
            "y": 120,
        },
        "dial": {
            "radius": "80%",
            "backgroundColor": "#306998",
            "baseWidth": 20,
            "topWidth": 1,
            "baseLength": "0%",
            "rearLength": "0%",
        },
        "pivot": {"backgroundColor": "#306998", "radius": 15},
    }
}

# Add gauge series with current value
chart.add_series({"type": "gauge", "name": "CPU Usage", "data": [current_value]})

# Credits
chart.options.credits = {"enabled": False}

# Download Highcharts JS and highcharts-more for gauge support
highcharts_url = "https://code.highcharts.com/highcharts.js"
with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

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
<body style="margin:0; display:flex; justify-content:center; align-items:center; min-height:2700px; background:#ffffff;">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>{html_str}</script>
</body>
</html>"""

# Save HTML for interactive version
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)

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
time.sleep(5)  # Wait for chart to render
driver.save_screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()  # Clean up temp file
