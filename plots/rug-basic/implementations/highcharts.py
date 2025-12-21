""" pyplots.ai
rug-basic: Basic Rug Plot
Library: highcharts 1.10.3 | Python 3.13.11
Quality: 95/100 | Created: 2025-12-17
"""

import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.area import LineSeries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - response times (ms) with realistic clustering and gaps
np.random.seed(42)
values = np.concatenate(
    [
        np.random.normal(50, 8, 40),  # Fast responses cluster
        np.random.normal(120, 15, 35),  # Medium responses cluster
        np.random.normal(250, 20, 15),  # Slow responses cluster
        np.array([380, 420, 510]),  # Outliers (occasional slow requests)
    ]
)
values = np.clip(values, 10, 600)

# Create chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration
chart.options.chart = {
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#ffffff",
    "marginBottom": 200,
    "marginTop": 150,
}

# Title
chart.options.title = {
    "text": "rug-basic · highcharts · pyplots.ai",
    "style": {"fontSize": "72px", "fontWeight": "bold"},
}

# Subtitle
chart.options.subtitle = {"text": "API Response Times (ms)", "style": {"fontSize": "48px"}}

# X-axis - continuous scale for response times
chart.options.x_axis = {
    "title": {"text": "Response Time (ms)", "style": {"fontSize": "48px"}},
    "labels": {"style": {"fontSize": "36px"}},
    "gridLineWidth": 1,
    "gridLineColor": "rgba(0, 0, 0, 0.1)",
    "gridLineDashStyle": "Dash",
    "min": 0,
    "max": 600,
    "tickInterval": 50,
    "lineWidth": 3,
    "lineColor": "#333333",
}

# Y-axis - narrow range for rug plot (ticks extend from bottom)
chart.options.y_axis = {
    "title": {"text": None},
    "labels": {"enabled": False},
    "gridLineWidth": 0,
    "min": 0,
    "max": 100,
    "visible": False,
    "plotLines": [{"value": 0, "width": 3, "color": "#333333", "zIndex": 2}],  # Baseline
}

# Legend and credits
chart.options.legend = {"enabled": False}
chart.options.credits = {"enabled": False}

# Tooltip disabled (too many series)
chart.options.tooltip = {"enabled": False}

# Add each rug tick as an individual vertical line series
# Use transparency (alpha) for overlapping points
# Tick height of 25 gives a subtle rug effect at the bottom
for v in sorted(values):
    tick_series = LineSeries()
    # Vertical line from bottom to tick height (25% of y-range for subtle rug)
    tick_series.data = [[float(v), 0], [float(v), 25]]
    tick_series.color = "rgba(48, 105, 152, 0.6)"  # Python Blue with transparency
    tick_series.line_width = 5  # Visible but thin ticks
    tick_series.marker = {"enabled": False}
    tick_series.enable_mouse_tracking = False
    tick_series.states = {"hover": {"enabled": False}}
    chart.add_series(tick_series)

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
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html, body {{ width: 4800px; height: 2700px; overflow: hidden; }}
        #container {{ width: 4800px; height: 2700px; }}
    </style>
</head>
<body>
    <div id="container"></div>
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
chrome_options.add_argument("--window-size=4900,2800")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)

# Take screenshot of the container element for exact dimensions
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
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html, body {{ width: 100%; height: 100vh; overflow: hidden; }}
        #container {{ width: 100%; height: 100%; }}
    </style>
</head>
<body>
    <div id="container"></div>
    <script>{html_str}</script>
</body>
</html>"""
    f.write(interactive_html)
