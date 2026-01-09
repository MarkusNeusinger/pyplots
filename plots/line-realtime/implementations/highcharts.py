"""pyplots.ai
line-realtime: Real-Time Updating Line Chart
Library: highcharts | Python 3.13
Quality: pending | Created: 2025-01-09
"""

import json
import tempfile
import time
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - Simulated CPU usage with realistic patterns
np.random.seed(42)
n_points = 120  # Visible window of data points

# Generate timestamps (100ms intervals, simulating real-time data)
base_time = datetime(2025, 1, 9, 14, 30, 0)
timestamps = [base_time + timedelta(milliseconds=100 * i) for i in range(n_points)]

# Generate CPU usage with realistic patterns: base load + spikes + noise
base_load = 35  # Base CPU usage
trend = np.sin(np.linspace(0, 4 * np.pi, n_points)) * 15  # Oscillating pattern
spikes = np.zeros(n_points)
spike_indices = [20, 45, 78, 95, 110]
for idx in spike_indices:
    spikes[idx : idx + 5] = np.array([25, 35, 20, 10, 5])[: min(5, n_points - idx)]
noise = np.random.normal(0, 3, n_points)
values = np.clip(base_load + trend + spikes + noise, 0, 100)

# Format data for Highcharts (timestamp in milliseconds, value)
data_points = [[int(ts.timestamp() * 1000), round(float(v), 1)] for ts, v in zip(timestamps, values, strict=True)]

# Current value for display
current_value = values[-1]

# Highcharts configuration as Python dict (will be converted to JSON)
chart_config = {
    "chart": {
        "type": "area",
        "width": 4800,
        "height": 2700,
        "backgroundColor": "#ffffff",
        "marginBottom": 250,
        "marginLeft": 200,
        "marginRight": 280,
        "marginTop": 180,
        "animation": {"duration": 500},
    },
    "title": {"text": "line-realtime · highcharts · pyplots.ai", "style": {"fontSize": "72px", "fontWeight": "bold"}},
    "subtitle": {
        "text": f"CPU Usage Monitor — Current: {current_value:.1f}%  ▶",
        "style": {"fontSize": "48px", "color": "#666666"},
    },
    "xAxis": {
        "type": "datetime",
        "title": {"text": "Time (sliding window →)", "style": {"fontSize": "44px"}, "margin": 25},
        "labels": {"style": {"fontSize": "36px"}, "format": "{value:%H:%M:%S}", "y": 50},
        "tickPixelInterval": 500,
        "gridLineWidth": 1,
        "gridLineColor": "#e0e0e0",
        "lineWidth": 3,
        "lineColor": "#333333",
    },
    "yAxis": {
        "title": {"text": "CPU Usage (%)", "style": {"fontSize": "44px"}, "margin": 30},
        "labels": {"style": {"fontSize": "36px"}, "format": "{value}%"},
        "min": 0,
        "max": 100,
        "tickInterval": 20,
        "gridLineWidth": 1,
        "gridLineColor": "#e0e0e0",
        "plotBands": [
            {"from": 0, "to": 50, "color": "rgba(48, 105, 152, 0.05)"},
            {"from": 50, "to": 80, "color": "rgba(255, 212, 59, 0.1)"},
            {"from": 80, "to": 100, "color": "rgba(220, 53, 69, 0.1)"},
        ],
    },
    "legend": {
        "enabled": True,
        "itemStyle": {"fontSize": "36px"},
        "align": "right",
        "verticalAlign": "top",
        "layout": "vertical",
        "x": -50,
        "y": 80,
    },
    "tooltip": {"style": {"fontSize": "28px"}, "xDateFormat": "%H:%M:%S.%L", "valueSuffix": "%"},
    "plotOptions": {
        "area": {
            "lineWidth": 5,
            "marker": {"enabled": False, "radius": 8, "symbol": "circle"},
            "fillColor": {
                "linearGradient": {"x1": 0, "y1": 0, "x2": 0, "y2": 1},
                "stops": [[0, "rgba(48, 105, 152, 0.5)"], [1, "rgba(48, 105, 152, 0.05)"]],
            },
            "states": {"hover": {"lineWidth": 6}},
        }
    },
    "series": [{"name": "CPU Usage", "data": data_points, "color": "#306998"}],
    "annotations": [
        {
            "labels": [
                {
                    "point": {"x": data_points[-1][0], "y": data_points[-1][1], "xAxis": 0, "yAxis": 0},
                    "text": f"Latest: {current_value:.1f}%",
                    "style": {"fontSize": "36px", "fontWeight": "bold", "color": "white"},
                    "backgroundColor": "#306998",
                    "borderColor": "#306998",
                    "borderRadius": 8,
                    "padding": 15,
                }
            ],
            "labelOptions": {"shape": "callout"},
        }
    ],
    "credits": {"enabled": False},
}

# Convert config to JSON
chart_json = json.dumps(chart_config)

# Download Highcharts JS for inline embedding
highcharts_url = "https://code.highcharts.com/highcharts.js"
with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

# Download annotations module for the callout
annotations_url = "https://code.highcharts.com/modules/annotations.js"
with urllib.request.urlopen(annotations_url, timeout=30) as response:
    annotations_js = response.read().decode("utf-8")

# Generate HTML with inline scripts
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <script>{annotations_js}</script>
</head>
<body style="margin:0; background-color: #ffffff;">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            Highcharts.chart('container', {chart_json});
        }});
    </script>
</body>
</html>"""

# Write temp HTML and capture screenshot
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

# Also save HTML for interactive version
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)
