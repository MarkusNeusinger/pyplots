""" pyplots.ai
line-animated-progressive: Animated Line Plot Over Time
Library: highcharts unknown | Python 3.13.11
Quality: 91/100 | Created: 2026-01-07
"""

import json
import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - Monthly temperature readings over 5 years (60 data points)
np.random.seed(42)
dates = pd.date_range("2019-01-01", periods=60, freq="MS")

# Create realistic temperature pattern with seasonal variation and slight warming trend
months = np.arange(60)
seasonal = 15 * np.sin(2 * np.pi * months / 12)  # Seasonal cycle
trend = 0.02 * months  # Slight warming trend
noise = np.random.normal(0, 1.5, 60)
temperatures = 12 + seasonal + trend + noise  # Base temp around 12°C

# Create data as list of [timestamp_ms, value] for Highcharts
data_points = [[int(d.timestamp() * 1000), round(t, 1)] for d, t in zip(dates, temperatures, strict=True)]

# Highcharts configuration as Python dict
chart_config = {
    "chart": {
        "type": "line",
        "width": 4800,
        "height": 2700,
        "backgroundColor": "#ffffff",
        "marginBottom": 200,
        "marginTop": 150,
        "marginLeft": 200,
        "marginRight": 100,
        "animation": {"duration": 2000},
    },
    "title": {
        "text": "line-animated-progressive · highcharts · pyplots.ai",
        "style": {"fontSize": "56px", "fontWeight": "bold", "color": "#333333"},
        "y": 60,
    },
    "subtitle": {
        "text": "Monthly Average Temperature (2019-2023) - Progressive Line Animation",
        "style": {"fontSize": "36px", "color": "#666666"},
        "y": 110,
    },
    "xAxis": {
        "type": "datetime",
        "title": {"text": "Date", "style": {"fontSize": "40px", "color": "#333333"}, "margin": 30},
        "labels": {"style": {"fontSize": "28px", "color": "#333333"}, "format": "{value:%b %Y}", "step": 3},
        "gridLineWidth": 1,
        "gridLineColor": "#e0e0e0",
        "lineWidth": 3,
        "lineColor": "#333333",
        "tickWidth": 3,
        "tickLength": 10,
        "tickInterval": 3 * 30 * 24 * 3600 * 1000,  # 3 months in milliseconds
    },
    "yAxis": {
        "title": {"text": "Temperature (°C)", "style": {"fontSize": "40px", "color": "#333333"}, "margin": 30},
        "labels": {"style": {"fontSize": "32px", "color": "#333333"}, "format": "{value}°C"},
        "gridLineWidth": 1,
        "gridLineColor": "#e0e0e0",
        "lineWidth": 3,
        "lineColor": "#333333",
    },
    "plotOptions": {
        "line": {
            "lineWidth": 6,
            "marker": {
                "enabled": True,
                "radius": 10,
                "fillColor": "#FFD43B",
                "lineWidth": 3,
                "lineColor": "#306998",
                "symbol": "circle",
            },
            "animation": {"duration": 2000},
        },
        "series": {"animation": {"duration": 2000}},
    },
    "legend": {"enabled": True, "itemStyle": {"fontSize": "32px", "fontWeight": "normal", "color": "#333333"}, "y": 30},
    "credits": {"enabled": False},
    "series": [
        {
            "name": "Temperature",
            "color": "#306998",
            "data": data_points,
            "marker": {
                "enabled": True,
                "radius": 10,
                "fillColor": "#FFD43B",
                "lineWidth": 3,
                "lineColor": "#306998",
                "symbol": "circle",
            },
        }
    ],
}

# Convert config to JSON for JavaScript
chart_json = json.dumps(chart_config)

# Download Highcharts JS for inline embedding
highcharts_url = "https://code.highcharts.com/highcharts.js"
with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

# HTML with inline scripts - use window.onload for reliable rendering
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
</head>
<body style="margin:0; padding:0; background:#ffffff;">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>
        window.onload = function() {{
            Highcharts.chart('container', {chart_json});
        }};
    </script>
</body>
</html>"""

# Interactive HTML version for web viewing
html_interactive_config = {
    "chart": {"type": "line", "animation": {"duration": 2000}},
    "title": {"text": "line-animated-progressive · highcharts · pyplots.ai"},
    "subtitle": {"text": "Monthly Average Temperature (2019-2023) - Progressive Line Animation"},
    "xAxis": {"type": "datetime", "title": {"text": "Date"}, "labels": {"format": "{value:%Y-%m}"}},
    "yAxis": {"title": {"text": "Temperature (°C)"}, "labels": {"format": "{value}°C"}},
    "legend": {"enabled": True},
    "credits": {"enabled": False},
    "plotOptions": {
        "line": {
            "lineWidth": 3,
            "marker": {"enabled": True, "radius": 5, "fillColor": "#FFD43B", "lineWidth": 2, "lineColor": "#306998"},
            "animation": {"duration": 2000},
        }
    },
    "series": [{"name": "Temperature", "color": "#306998", "data": data_points}],
}

html_interactive = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://code.highcharts.com/highcharts.js"></script>
    <style>
        body {{ margin: 0; padding: 20px; background: #ffffff; font-family: sans-serif; }}
        #container {{ width: 100%; max-width: 1200px; height: 675px; margin: 0 auto; }}
    </style>
</head>
<body>
    <div id="container"></div>
    <script>
        Highcharts.chart('container', {json.dumps(html_interactive_config)});
    </script>
</body>
</html>"""

with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_interactive)

# Write temp HTML and take screenshot for PNG
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

# Configure Chrome for headless screenshot
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=4800,2700")
chrome_options.add_argument("--force-device-scale-factor=1")

driver = webdriver.Chrome(options=chrome_options)
driver.set_window_size(4800, 2700)
driver.get(f"file://{temp_path}")
time.sleep(5)  # Wait for animation to complete

# Save full page screenshot
driver.save_screenshot("plot.png")
driver.quit()

# Clean up temp file
Path(temp_path).unlink()
