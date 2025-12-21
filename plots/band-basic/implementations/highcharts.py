""" pyplots.ai
band-basic: Basic Band Plot
Library: highcharts 1.10.3 | Python 3.13.11
Quality: 94/100 | Created: 2025-12-17
"""

import json
import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - Time series with 95% confidence interval
np.random.seed(42)
x = np.linspace(0, 10, 50)
# Central trend with sinusoidal pattern
y_center = 50 + 20 * np.sin(x) + x * 2
# Uncertainty increases with x (heteroscedastic)
uncertainty = 3 + 0.5 * x
# Upper and lower bounds
y_lower = y_center - 1.96 * uncertainty
y_upper = y_center + 1.96 * uncertainty

# Prepare data for Highcharts
# arearange series expects [[x, low, high], ...]
band_data = [[float(xi), float(lo), float(hi)] for xi, lo, hi in zip(x, y_lower, y_upper, strict=True)]
# line series expects [[x, y], ...]
line_data = [[float(xi), float(yi)] for xi, yi in zip(x, y_center, strict=True)]

# Chart options using arearange for band and line for center
chart_options = {
    "chart": {
        "width": 4800,
        "height": 2700,
        "backgroundColor": "#ffffff",
        "marginBottom": 180,
        "marginLeft": 200,
        "marginRight": 100,
        "style": {"fontFamily": "Arial, sans-serif"},
    },
    "title": {"text": "band-basic · highcharts · pyplots.ai", "style": {"fontSize": "64px", "fontWeight": "bold"}},
    "subtitle": {"text": "Time series with 95% confidence interval", "style": {"fontSize": "38px", "color": "#666666"}},
    "xAxis": {
        "title": {"text": "Time", "style": {"fontSize": "48px"}, "margin": 20},
        "labels": {"style": {"fontSize": "36px"}},
        "gridLineWidth": 1,
        "gridLineColor": "rgba(0, 0, 0, 0.1)",
        "gridLineDashStyle": "Dash",
        "tickInterval": 1,
    },
    "yAxis": {
        "title": {"text": "Value", "style": {"fontSize": "48px"}, "margin": 20},
        "labels": {"style": {"fontSize": "36px"}},
        "gridLineWidth": 1,
        "gridLineColor": "rgba(0, 0, 0, 0.1)",
        "gridLineDashStyle": "Dash",
    },
    "legend": {
        "enabled": True,
        "align": "right",
        "verticalAlign": "top",
        "layout": "vertical",
        "x": -50,
        "y": 100,
        "itemStyle": {"fontSize": "36px"},
    },
    "plotOptions": {
        "arearange": {"fillOpacity": 0.3, "lineWidth": 0, "marker": {"enabled": False}},
        "line": {"lineWidth": 6, "marker": {"enabled": False}},
    },
    "series": [
        {
            "name": "95% Confidence Interval",
            "type": "arearange",
            "data": band_data,
            "color": "#306998",
            "fillOpacity": 0.3,
            "zIndex": 0,
        },
        {"name": "Mean Value", "type": "line", "data": line_data, "color": "#FFD43B", "lineWidth": 6, "zIndex": 1},
    ],
}

# Download Highcharts JS and highcharts-more (needed for arearange)
highcharts_url = "https://code.highcharts.com/highcharts.js"
highcharts_more_url = "https://code.highcharts.com/highcharts-more.js"

with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")
with urllib.request.urlopen(highcharts_more_url, timeout=30) as response:
    highcharts_more_js = response.read().decode("utf-8")

# Generate HTML with inline scripts
chart_options_json = json.dumps(chart_options)
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <script>{highcharts_more_js}</script>
</head>
<body style="margin:0;">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            Highcharts.chart('container', {chart_options_json});
        }});
    </script>
</body>
</html>"""

# Write temp HTML file
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

# Also save the HTML for interactive viewing
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Take screenshot with headless Chrome
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--force-device-scale-factor=1")

driver = webdriver.Chrome(options=chrome_options)
driver.set_window_size(4900, 2900)
driver.get(f"file://{temp_path}")
time.sleep(5)

# Take screenshot
driver.save_screenshot("plot_raw.png")
driver.quit()

# Crop/resize to exact 4800x2700 using PIL
img = Image.open("plot_raw.png")
final_img = Image.new("RGB", (4800, 2700), (255, 255, 255))
final_img.paste(img.crop((0, 0, min(img.width, 4800), min(img.height, 2700))), (0, 0))
final_img.save("plot.png")

# Clean up
Path("plot_raw.png").unlink()
Path(temp_path).unlink()
