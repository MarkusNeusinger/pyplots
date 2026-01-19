""" pyplots.ai
scatter-streaming: Streaming Scatter Plot
Library: highcharts unknown | Python 3.13.11
Quality: 86/100 | Created: 2026-01-19
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


# Data - Simulated sensor readings arriving over time
# x: temperature readings, y: humidity readings
np.random.seed(42)
n_points = 150

# Simulate streaming data with timestamps
timestamps = np.arange(n_points)  # Arrival order (0 = oldest, n-1 = newest)

# Temperature: random walk around 22C
temperature = 22 + np.cumsum(np.random.randn(n_points) * 0.3)
temperature = np.clip(temperature, 15, 30)

# Humidity: correlated with temperature (inverse relationship) plus noise
humidity = 60 - (temperature - 22) * 2 + np.random.randn(n_points) * 5
humidity = np.clip(humidity, 30, 80)

# Calculate opacity based on recency (newer = more opaque)
# Oldest points start at 0.2, newest at 1.0
opacities = 0.2 + 0.8 * (timestamps / (n_points - 1))

# Group points by opacity ranges to create visual layers
opacity_groups = [
    (0.2, 0.4, "#306998", "Oldest readings"),
    (0.4, 0.6, "#306998", "Older readings"),
    (0.6, 0.8, "#306998", "Recent readings"),
    (0.8, 1.01, "#306998", "Latest readings"),
]

# Create chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration
chart.options.chart = {
    "type": "scatter",
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#ffffff",
    "marginBottom": 300,
    "spacingBottom": 120,
}

# Title
chart.options.title = {
    "text": "scatter-streaming \u00b7 highcharts \u00b7 pyplots.ai",
    "style": {"fontSize": "48px", "fontWeight": "bold"},
}

chart.options.subtitle = {
    "text": "Sensor readings stream (opacity indicates data recency)",
    "style": {"fontSize": "32px"},
}

# X-axis (Temperature)
chart.options.x_axis = {
    "title": {"text": "Temperature (\u00b0C)", "style": {"fontSize": "32px"}},
    "labels": {"style": {"fontSize": "24px"}},
    "gridLineWidth": 1,
    "gridLineColor": "#e0e0e0",
}

# Y-axis (Humidity)
chart.options.y_axis = {
    "title": {"text": "Humidity (%)", "style": {"fontSize": "32px"}},
    "labels": {"style": {"fontSize": "24px"}},
    "gridLineWidth": 1,
    "gridLineColor": "#e0e0e0",
}

# Legend
chart.options.legend = {
    "enabled": True,
    "itemStyle": {"fontSize": "28px"},
    "layout": "vertical",
    "align": "right",
    "verticalAlign": "top",
    "x": -100,
    "y": 100,
    "floating": True,
    "backgroundColor": "rgba(255, 255, 255, 0.85)",
    "borderWidth": 1,
    "borderColor": "#e0e0e0",
    "symbolRadius": 0,
}

# Tooltip
chart.options.tooltip = {
    "headerFormat": "<b>{series.name}</b><br>",
    "pointFormat": "Temperature: {point.x:.1f}\u00b0C<br>Humidity: {point.y:.1f}%",
    "style": {"fontSize": "20px"},
}

# Add series for each opacity group
for min_op, max_op, _color, name in opacity_groups:
    mask = (opacities >= min_op) & (opacities < max_op)
    if not np.any(mask):
        continue

    x_vals = temperature[mask]
    y_vals = humidity[mask]
    avg_opacity = (min_op + max_op) / 2

    series = ScatterSeries()
    series.data = [{"x": float(x), "y": float(y)} for x, y in zip(x_vals, y_vals, strict=True)]
    series.name = name
    series.marker = {
        "symbol": "circle",
        "radius": 14,
        "fillColor": f"rgba(48, 105, 152, {avg_opacity})",
        "lineWidth": 2,
        "lineColor": "#306998",
    }

    chart.add_series(series)

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

# Save interactive HTML version
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Write temp HTML and take screenshot for PNG
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
