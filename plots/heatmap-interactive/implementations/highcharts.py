"""pyplots.ai
heatmap-interactive: Interactive Heatmap with Hover and Zoom
Library: highcharts | Python 3.13
Quality: pending | Created: 2025-01-09
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


# Data - Monthly website traffic by hour and day (20x24 matrix)
np.random.seed(42)
days = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
    "Week 2 Mon",
    "Week 2 Tue",
    "Week 2 Wed",
    "Week 2 Thu",
    "Week 2 Fri",
    "Week 2 Sat",
    "Week 2 Sun",
    "Week 3 Mon",
    "Week 3 Tue",
    "Week 3 Wed",
    "Week 3 Thu",
    "Week 3 Fri",
    "Week 3 Sat",
]
hours = [f"{h:02d}:00" for h in range(24)]

# Generate realistic traffic patterns
base_traffic = np.zeros((len(days), len(hours)))
for i, day in enumerate(days):
    for j in range(len(hours)):
        # Peak hours 9-17 on weekdays
        is_weekend = "Sat" in day or "Sun" in day
        hour_factor = 1.0
        if 9 <= j <= 17:
            hour_factor = 2.5 if not is_weekend else 1.5
        elif 6 <= j <= 8 or 18 <= j <= 21:
            hour_factor = 1.8 if not is_weekend else 1.3
        elif 0 <= j <= 5:
            hour_factor = 0.3

        day_factor = 0.6 if is_weekend else 1.0
        base_value = 500 * day_factor * hour_factor
        noise = np.random.normal(0, base_value * 0.2)
        base_traffic[i, j] = max(0, base_value + noise)

# Convert to heatmap data format for Highcharts
heatmap_data = []
for i, _day in enumerate(days):
    for j, _hour in enumerate(hours):
        heatmap_data.append([j, i, round(base_traffic[i, j], 1)])

# Download Highcharts JS and heatmap module
highcharts_url = "https://code.highcharts.com/highcharts.js"
heatmap_url = "https://code.highcharts.com/modules/heatmap.js"
boost_url = "https://code.highcharts.com/modules/boost.js"

with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")
with urllib.request.urlopen(heatmap_url, timeout=30) as response:
    heatmap_js = response.read().decode("utf-8")
with urllib.request.urlopen(boost_url, timeout=30) as response:
    boost_js = response.read().decode("utf-8")

# Create chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration with zooming
chart.options.chart = {
    "type": "heatmap",
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#ffffff",
    "zoomType": "xy",
    "panning": {"enabled": True, "type": "xy"},
    "panKey": "shift",
    "marginBottom": 180,
    "resetZoomButton": {
        "position": {"align": "right", "verticalAlign": "top", "x": -60, "y": 60},
        "theme": {"fill": "#306998", "stroke": "#306998", "style": {"color": "#ffffff", "fontSize": "20px"}},
    },
}

# Title
chart.options.title = {
    "text": "Website Traffic by Hour · heatmap-interactive · highcharts · pyplots.ai",
    "style": {"fontSize": "48px", "fontWeight": "bold"},
}

chart.options.subtitle = {
    "text": "Drag to zoom, Shift+drag to pan, click reset button to restore view",
    "style": {"fontSize": "28px", "color": "#666666"},
}

# X-axis (hours)
chart.options.x_axis = {
    "categories": hours,
    "title": {"text": "Hour of Day", "style": {"fontSize": "32px"}},
    "labels": {"style": {"fontSize": "22px"}, "rotation": 315},
    "tickLength": 0,
    "gridLineWidth": 0,
}

# Y-axis (days)
chart.options.y_axis = {
    "categories": days,
    "title": {"text": "Day", "style": {"fontSize": "32px"}},
    "labels": {"style": {"fontSize": "22px"}},
    "reversed": True,
    "gridLineWidth": 0,
}

# Color axis (legend)
chart.options.color_axis = {
    "min": 0,
    "max": float(np.max(base_traffic)),
    "stops": [[0, "#f7fbff"], [0.2, "#c6dbef"], [0.4, "#6baed6"], [0.6, "#2171b5"], [0.8, "#08519c"], [1, "#08306b"]],
    "labels": {"style": {"fontSize": "22px"}},
}

# Legend
chart.options.legend = {
    "align": "right",
    "layout": "vertical",
    "verticalAlign": "middle",
    "symbolHeight": 600,
    "itemStyle": {"fontSize": "22px"},
    "title": {"text": "Visitors", "style": {"fontSize": "26px"}},
}

# Tooltip
chart.options.tooltip = {
    "useHTML": True,
    "headerFormat": "",
    "pointFormat": '<div style="font-size: 24px; padding: 12px;"><b>{series.xAxis.categories.(point.x)}</b> on <b>{series.yAxis.categories.(point.y)}</b><br/>Visitors: <b>{point.value:.0f}</b></div>',
    "backgroundColor": "rgba(255, 255, 255, 0.95)",
    "borderWidth": 2,
    "borderColor": "#306998",
}

# Plot options for heatmap
chart.options.plot_options = {
    "heatmap": {
        "borderWidth": 1,
        "borderColor": "#ffffff",
        "dataLabels": {"enabled": False},
        "cursor": "pointer",
        "states": {"hover": {"brightness": 0.2, "borderColor": "#000000", "borderWidth": 3}},
    }
}

# Add series
chart.add_series({"name": "Traffic", "type": "heatmap", "data": heatmap_data, "turboThreshold": 10000})

# Generate HTML with inline scripts
html_str = chart.to_js_literal()
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <script>{heatmap_js}</script>
    <script>{boost_js}</script>
</head>
<body style="margin:0;">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>{html_str}</script>
</body>
</html>"""

# Save interactive HTML
with open("plot.html", "w", encoding="utf-8") as f:
    # Generate standalone HTML with CDN links for the interactive version
    interactive_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>heatmap-interactive · highcharts · pyplots.ai</title>
    <script src="https://code.highcharts.com/highcharts.js"></script>
    <script src="https://code.highcharts.com/modules/heatmap.js"></script>
    <script src="https://code.highcharts.com/modules/boost.js"></script>
</head>
<body style="margin:0;">
    <div id="container" style="width: 100%; height: 100vh;"></div>
    <script>{html_str}</script>
</body>
</html>"""
    f.write(interactive_html)

# Write temp HTML and take screenshot
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=4800,2900")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)
driver.save_screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()
