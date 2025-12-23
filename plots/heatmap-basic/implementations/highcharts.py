""" pyplots.ai
heatmap-basic: Basic Heatmap
Library: highcharts unknown | Python 3.13.11
Quality: 91/100 | Created: 2025-12-23
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


# Data - 8x6 matrix with meaningful patterns
np.random.seed(42)
x_categories = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun", "Avg"]
y_categories = ["Morning", "Midday", "Afternoon", "Evening", "Night", "Total"]

# Generate sample activity data (e.g., website traffic by day and time)
base_data = np.random.randint(10, 90, size=(len(y_categories), len(x_categories)))
# Add some patterns - weekends have different traffic
base_data[:, 5:7] = base_data[:, 5:7] * 0.7  # Lower weekend traffic
base_data[1:3, :] = base_data[1:3, :] * 1.3  # Higher midday/afternoon
base_data = np.clip(base_data, 0, 100).astype(int)

# Create heatmap data in Highcharts format: [x_index, y_index, value]
heatmap_data = []
for y_idx in range(len(y_categories)):
    for x_idx in range(len(x_categories)):
        heatmap_data.append([x_idx, y_idx, int(base_data[y_idx, x_idx])])

# Create chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration
chart.options.chart = {
    "type": "heatmap",
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#ffffff",
    "marginBottom": 280,
    "marginRight": 200,
}

# Title
chart.options.title = {
    "text": "heatmap-basic · highcharts · pyplots.ai",
    "style": {"fontSize": "64px", "fontWeight": "bold"},
}

# X-axis (days)
chart.options.x_axis = {
    "categories": x_categories,
    "title": {"text": "Day of Week", "style": {"fontSize": "48px"}},
    "labels": {"style": {"fontSize": "36px"}},
}

# Y-axis (time periods)
chart.options.y_axis = {
    "categories": y_categories,
    "title": {"text": "Time Period", "style": {"fontSize": "48px"}},
    "labels": {"style": {"fontSize": "36px"}},
    "reversed": True,
}

# Colorbar/legend
chart.options.color_axis = {
    "min": 0,
    "max": 100,
    "minColor": "#FFFFFF",
    "maxColor": "#306998",
    "labels": {"style": {"fontSize": "32px"}},
}

# Legend configuration
chart.options.legend = {
    "align": "right",
    "layout": "vertical",
    "margin": 20,
    "verticalAlign": "middle",
    "symbolHeight": 800,
    "itemStyle": {"fontSize": "32px"},
}

# Tooltip
chart.options.tooltip = {
    "style": {"fontSize": "32px"},
    "format": "<b>{series.xAxis.categories.(point.x)}</b><br>"
    "<b>{series.yAxis.categories.(point.y)}</b><br>"
    "Value: <b>{point.value}</b>",
}

# Add heatmap series
series_config = {
    "name": "Activity",
    "type": "heatmap",
    "data": heatmap_data,
    "borderWidth": 2,
    "borderColor": "#ffffff",
    "dataLabels": {
        "enabled": True,
        "color": "#000000",
        "style": {"fontSize": "28px", "fontWeight": "bold", "textOutline": "none"},
    },
}

chart.options.series = [series_config]

# Download Highcharts JS and heatmap module
highcharts_url = "https://code.highcharts.com/highcharts.js"
heatmap_url = "https://code.highcharts.com/modules/heatmap.js"

with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

with urllib.request.urlopen(heatmap_url, timeout=30) as response:
    heatmap_js = response.read().decode("utf-8")

# Generate HTML with inline scripts
html_str = chart.to_js_literal()
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <script>{heatmap_js}</script>
</head>
<body style="margin:0;">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>{html_str}</script>
</body>
</html>"""

# Save HTML for interactive version
with open("plot.html", "w", encoding="utf-8") as f:
    # Use CDN for standalone HTML
    standalone_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://code.highcharts.com/highcharts.js"></script>
    <script src="https://code.highcharts.com/modules/heatmap.js"></script>
</head>
<body style="margin:0;">
    <div id="container" style="width: 100%; height: 100vh;"></div>
    <script>{html_str}</script>
</body>
</html>"""
    f.write(standalone_html)

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
