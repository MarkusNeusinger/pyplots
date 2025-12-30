""" pyplots.ai
line-interactive: Interactive Line Chart with Hover and Zoom
Library: highcharts unknown | Python 3.13.11
Quality: 91/100 | Created: 2025-12-30
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


# Data - Server CPU usage over 7 days (hourly readings)
np.random.seed(42)
n_points = 168  # 7 days * 24 hours

dates = pd.date_range("2024-01-01", periods=n_points, freq="h")

# Simulate realistic CPU usage pattern with daily cycles and some anomalies
base = 35  # base CPU usage
daily_pattern = 20 * np.sin(np.linspace(0, 7 * 2 * np.pi, n_points))  # daily cycle
weekly_trend = np.linspace(0, 10, n_points)  # slight upward trend
noise = np.random.normal(0, 5, n_points)

# Add some random spikes (anomalies)
spikes = np.zeros(n_points)
spike_indices = [45, 92, 120, 155]
for idx in spike_indices:
    spikes[idx] = np.random.uniform(20, 35)

cpu_usage = base + daily_pattern + weekly_trend + noise + spikes
cpu_usage = np.clip(cpu_usage, 5, 100)  # Keep within 5-100%

# Convert to timestamp milliseconds for Highcharts datetime axis
timestamps = [int(d.timestamp() * 1000) for d in dates]
data_points = [[ts, round(val, 1)] for ts, val in zip(timestamps, cpu_usage, strict=True)]

# Build Highcharts configuration as Python dict, then serialize to JSON
highcharts_config = {
    "chart": {
        "type": "line",
        "width": 4800,
        "height": 2700,
        "backgroundColor": "#ffffff",
        "spacingTop": 60,
        "spacingBottom": 100,
        "spacingLeft": 80,
        "spacingRight": 80,
        "zoomType": "x",
    },
    "title": {
        "text": "line-interactive \u00b7 highcharts \u00b7 pyplots.ai",
        "style": {"fontSize": "56px", "fontWeight": "bold"},
        "margin": 40,
    },
    "subtitle": {
        "text": "Server CPU Usage - Click and drag to zoom (7 Days of Hourly Data)",
        "style": {"fontSize": "36px", "color": "#666666"},
    },
    "xAxis": {
        "type": "datetime",
        "title": {"text": "Date and Time", "style": {"fontSize": "36px"}, "margin": 25},
        "labels": {"style": {"fontSize": "28px"}},
        "gridLineWidth": 1,
        "gridLineColor": "rgba(0, 0, 0, 0.1)",
        "tickInterval": 24 * 3600 * 1000,
        "dateTimeLabelFormats": {"day": "%b %d"},
        "crosshair": {"width": 2, "color": "#306998"},
    },
    "yAxis": {
        "title": {"text": "CPU Usage (%)", "style": {"fontSize": "36px"}, "margin": 25},
        "labels": {"style": {"fontSize": "28px"}, "format": "{value}%"},
        "gridLineWidth": 1,
        "gridLineColor": "rgba(0, 0, 0, 0.1)",
        "min": 0,
        "max": 105,
    },
    "legend": {"enabled": True, "itemStyle": {"fontSize": "32px"}, "margin": 30},
    "tooltip": {
        "xDateFormat": "%A, %b %d, %H:%M",
        "valueSuffix": "%",
        "style": {"fontSize": "28px"},
        "headerFormat": "<b>{point.key}</b><br/>",
        "pointFormat": "CPU: <b>{point.y}%</b>",
    },
    "plotOptions": {
        "line": {
            "lineWidth": 5,
            "marker": {"enabled": False, "radius": 8, "states": {"hover": {"enabled": True, "radius": 10}}},
            "states": {"hover": {"lineWidth": 6}},
        }
    },
    "series": [{"name": "CPU Usage", "data": data_points, "color": "#306998", "type": "line"}],
}

# Convert to JSON string
config_json = json.dumps(highcharts_config)

# Download Highcharts JS for inline embedding
highcharts_url = "https://code.highcharts.com/highcharts.js"
with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

# Generate HTML with proper JSON config
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
</head>
<body style="margin:0;">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            Highcharts.chart('container', {config_json});
        }});
    </script>
</body>
</html>"""

# Save HTML version (interactive)
with open("plot.html", "w", encoding="utf-8") as f:
    cdn_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>line-interactive · highcharts · pyplots.ai</title>
    <script src="https://code.highcharts.com/highcharts.js"></script>
</head>
<body style="margin:0;">
    <div id="container" style="width: 100%; height: 100vh;"></div>
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            Highcharts.chart('container', {config_json});
        }});
    </script>
</body>
</html>"""
    f.write(cdn_html)

# Take screenshot with headless Chrome
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=5000,3000")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)

# Screenshot the chart container element for exact dimensions
container = driver.find_element("id", "container")
container.screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()
