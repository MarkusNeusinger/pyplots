""" pyplots.ai
band-basic: Basic Band Plot
Library: highcharts 1.10.3 | Python 3.14
Quality: 88/100 | Updated: 2026-02-23
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


# Data - Daily temperature forecast with 95% prediction interval
np.random.seed(42)
days = np.arange(1, 31)
# Central forecast: warming trend with daily variation
temp_center = 12 + 0.3 * days + 4 * np.sin(days * 0.4)
# Prediction uncertainty widens over the forecast horizon
uncertainty = 1.5 + 0.08 * days
temp_lower = temp_center - 1.96 * uncertainty
temp_upper = temp_center + 1.96 * uncertainty

# Prepare data for Highcharts
# arearange series expects [[x, low, high], ...]
band_data = [
    [int(d), round(float(lo), 1), round(float(hi), 1)] for d, lo, hi in zip(days, temp_lower, temp_upper, strict=True)
]
# line series expects [[x, y], ...]
line_data = [[int(d), round(float(t), 1)] for d, t in zip(days, temp_center, strict=True)]

# Font stack
font_family = "'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif"

# Chart options using arearange for band and line for center
chart_options = {
    "chart": {
        "width": 4800,
        "height": 2700,
        "backgroundColor": "#ffffff",
        "marginBottom": 180,
        "marginLeft": 220,
        "marginRight": 100,
        "spacing": [40, 40, 40, 40],
        "style": {"fontFamily": font_family},
    },
    "title": {
        "text": "30-Day Temperature Forecast \u00b7 band-basic \u00b7 highcharts \u00b7 pyplots.ai",
        "style": {"fontSize": "48px", "fontWeight": "bold", "fontFamily": font_family},
    },
    "subtitle": {
        "text": "Daily forecast with 95% prediction interval",
        "style": {"fontSize": "30px", "color": "#555555", "fontFamily": font_family},
    },
    "xAxis": {
        "title": {"text": "Forecast Day", "style": {"fontSize": "36px", "fontFamily": font_family}, "margin": 20},
        "labels": {"style": {"fontSize": "28px", "fontFamily": font_family}},
        "gridLineWidth": 0,
        "tickInterval": 5,
        "lineColor": "#cccccc",
        "tickColor": "#cccccc",
    },
    "yAxis": {
        "title": {
            "text": "Temperature (\u00b0C)",
            "style": {"fontSize": "36px", "fontFamily": font_family},
            "margin": 20,
        },
        "labels": {"format": "{value}\u00b0", "style": {"fontSize": "28px", "fontFamily": font_family}},
        "gridLineWidth": 1,
        "gridLineColor": "rgba(0, 0, 0, 0.08)",
        "gridLineDashStyle": "Dot",
        "lineColor": "#cccccc",
        "lineWidth": 1,
    },
    "legend": {
        "enabled": True,
        "align": "right",
        "verticalAlign": "top",
        "layout": "vertical",
        "x": -40,
        "y": 80,
        "itemStyle": {"fontSize": "28px", "fontFamily": font_family},
    },
    "plotOptions": {
        "arearange": {"fillOpacity": 0.25, "lineWidth": 0, "marker": {"enabled": False}},
        "line": {"lineWidth": 5, "marker": {"enabled": False}},
    },
    "series": [
        {
            "name": "95% Prediction Interval",
            "type": "arearange",
            "data": band_data,
            "color": "#306998",
            "fillOpacity": 0.25,
            "zIndex": 0,
        },
        {"name": "Forecast", "type": "line", "data": line_data, "color": "#FFD43B", "lineWidth": 5, "zIndex": 1},
    ],
    "credits": {"enabled": False},
}

# Download Highcharts JS files (jsDelivr CDN with version pin)
cdn_base = "https://cdn.jsdelivr.net/npm/highcharts@11.4"
js_urls = {"highcharts": f"{cdn_base}/highcharts.js", "highcharts_more": f"{cdn_base}/highcharts-more.js"}
js_modules = {}
for name, url in js_urls.items():
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as response:
        js_modules[name] = response.read().decode("utf-8")

# Generate HTML with inline scripts
chart_options_json = json.dumps(chart_options)
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{js_modules["highcharts"]}</script>
    <script>{js_modules["highcharts_more"]}</script>
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

# Save HTML for interactive viewing
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Take screenshot with headless Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=4800,2900")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)
driver.save_screenshot("plot_raw.png")
driver.quit()

# Crop to exact 4800x2700 dimensions
img = Image.open("plot_raw.png")
img_cropped = img.crop((0, 0, 4800, 2700))
img_cropped.save("plot.png")
Path("plot_raw.png").unlink()

Path(temp_path).unlink()
