"""pyplots.ai
line-realtime: Real-Time Updating Line Chart
Library: highcharts | Python 3.13
Quality: pending | Created: 2026-01-09
"""

import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.area import AreaSeries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - Simulated CPU usage with sliding window (last 60 seconds visible)
np.random.seed(42)
n_points = 60

# Generate realistic CPU usage pattern (fluctuating around 45% with spikes)
base_usage = 45
noise = np.random.randn(n_points) * 8
trend = np.sin(np.linspace(0, 2 * np.pi, n_points)) * 15
spikes = np.zeros(n_points)
spike_indices = [15, 35, 50]
for idx in spike_indices:
    if idx + 3 <= n_points:
        spikes[idx : idx + 3] = np.array([20, 30, 15])

cpu_values = base_usage + noise + trend + spikes
cpu_values = np.clip(cpu_values, 0, 100).tolist()

# Time labels (showing seconds in sliding window)
time_labels = [f"{i}s" for i in range(n_points)]

# Current value for display
current_value = cpu_values[-1]

# Create chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration with large canvas
chart.options.chart = {
    "type": "area",
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#ffffff",
    "marginBottom": 300,
    "marginLeft": 250,
    "marginRight": 100,
    "spacingTop": 80,
}

# Title with current value indicator
chart.options.title = {
    "text": f"CPU Usage Monitor (Current: {current_value:.1f}%) · line-realtime · highcharts · pyplots.ai",
    "style": {"fontSize": "64px", "fontWeight": "bold"},
}

chart.options.subtitle = {
    "text": "Sliding window showing last 60 seconds of data ◀ older data scrolls off",
    "style": {"fontSize": "40px", "color": "#666666"},
}

# X-axis (time as categories)
chart.options.x_axis = {
    "categories": time_labels,
    "title": {"text": "Time (sliding window)", "style": {"fontSize": "48px"}, "margin": 30},
    "labels": {"style": {"fontSize": "28px"}, "y": 40, "step": 5},
    "lineWidth": 2,
    "gridLineWidth": 1,
    "gridLineColor": "#e0e0e0",
}

# Y-axis (CPU percentage)
chart.options.y_axis = {
    "title": {"text": "CPU Usage (%)", "style": {"fontSize": "48px"}, "margin": 30},
    "labels": {"style": {"fontSize": "36px"}, "x": -15},
    "min": 0,
    "max": 100,
    "gridLineWidth": 1,
    "gridLineColor": "#e0e0e0",
    "gridLineDashStyle": "Dash",
    "plotBands": [
        {
            "from": 80,
            "to": 100,
            "color": "rgba(255, 212, 59, 0.15)",
            "label": {
                "text": "High Usage Zone",
                "style": {"fontSize": "32px", "color": "#999999"},
                "align": "right",
                "x": -20,
            },
        }
    ],
}

# Series data - area chart for visual appeal
series = AreaSeries()
series.data = cpu_values
series.name = "CPU Usage"
series.color = "#306998"
series.fill_color = {
    "linearGradient": {"x1": 0, "y1": 0, "x2": 0, "y2": 1},
    "stops": [[0, "rgba(48, 105, 152, 0.6)"], [1, "rgba(48, 105, 152, 0.05)"]],
}

chart.add_series(series)

# Legend
chart.options.legend = {"enabled": True, "itemStyle": {"fontSize": "40px"}}

# Credits off
chart.options.credits = {"enabled": False}

# Plot options for line styling
chart.options.plot_options = {
    "area": {
        "lineWidth": 6,
        "marker": {"enabled": True, "radius": 10, "symbol": "circle"},
        "states": {"hover": {"lineWidth": 8}},
        "threshold": None,
    }
}

# Download Highcharts JS for inline embedding
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

# Write temp HTML and take screenshot
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

# Also save HTML for interactive viewing
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)

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
time.sleep(6)
driver.save_screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()
