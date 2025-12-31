"""pyplots.ai
streamline-basic: Basic Streamline Plot
Library: highcharts | Python 3.13
Quality: pending | Created: 2025-12-31
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


# Data: Create a vortex flow field
np.random.seed(42)
grid_size = 30
x = np.linspace(-3, 3, grid_size)
y = np.linspace(-3, 3, grid_size)
X, Y = np.meshgrid(x, y)

# Vortex flow: u = -y, v = x (circular flow around origin)
U = -Y
V = X


# Function to trace a streamline from a starting point
def trace_streamline(x0, y0, u_field, v_field, x_grid, y_grid, max_steps=100, dt=0.05):
    """Trace a streamline using simple Euler integration."""
    points = [(x0, y0)]
    x_curr, y_curr = x0, y0

    x_min, x_max = x_grid.min(), x_grid.max()
    y_min, y_max = y_grid.min(), y_grid.max()

    for _ in range(max_steps):
        # Find grid indices
        xi = int((x_curr - x_min) / (x_max - x_min) * (len(x_grid) - 1))
        yi = int((y_curr - y_min) / (y_max - y_min) * (len(y_grid) - 1))

        # Check bounds
        if xi < 0 or xi >= len(x_grid) - 1 or yi < 0 or yi >= len(y_grid) - 1:
            break

        # Get velocity (bilinear interpolation simplified)
        u = u_field[yi, xi]
        v = v_field[yi, xi]

        # Normalize velocity for consistent step size
        speed = np.sqrt(u**2 + v**2)
        if speed < 1e-6:
            break

        u_norm = u / speed
        v_norm = v / speed

        # Step forward
        x_new = x_curr + u_norm * dt
        y_new = y_curr + v_norm * dt

        # Check if out of bounds
        if x_new < x_min or x_new > x_max or y_new < y_min or y_new > y_max:
            break

        points.append((x_new, y_new))
        x_curr, y_curr = x_new, y_new

    return points


# Generate streamlines from distributed starting points
streamlines = []

# Start from a grid of points
start_points = []
for sx in np.linspace(-2.5, 2.5, 6):
    for sy in np.linspace(-2.5, 2.5, 6):
        # Skip points too close to origin (singularity)
        if np.sqrt(sx**2 + sy**2) > 0.3:
            start_points.append((sx, sy))

for x0, y0 in start_points:
    line = trace_streamline(x0, y0, U, V, x, y, max_steps=150, dt=0.08)
    if len(line) > 5:  # Only keep meaningful streamlines
        streamlines.append(line)

# Create Highcharts chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration
chart.options.chart = {
    "type": "line",
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#ffffff",
    "marginBottom": 250,
    "marginLeft": 220,
    "marginRight": 150,
    "marginTop": 180,
    "spacingBottom": 50,
}

# Title
chart.options.title = {
    "text": "streamline-basic · highcharts · pyplots.ai",
    "style": {"fontSize": "56px", "fontWeight": "bold"},
}

# Subtitle describing the vortex
chart.options.subtitle = {"text": "Vortex Flow Field: u = -y, v = x", "style": {"fontSize": "40px", "color": "#666666"}}

# Axes
chart.options.x_axis = {
    "title": {"text": "X Position", "style": {"fontSize": "42px"}},
    "labels": {"style": {"fontSize": "32px"}},
    "min": -3.5,
    "max": 3.5,
    "tickInterval": 1,
    "gridLineWidth": 1,
    "gridLineColor": "#e0e0e0",
    "lineWidth": 2,
    "lineColor": "#333333",
}

chart.options.y_axis = {
    "title": {"text": "Y Position", "style": {"fontSize": "42px"}},
    "labels": {"style": {"fontSize": "32px"}},
    "min": -3.5,
    "max": 3.5,
    "tickInterval": 1,
    "gridLineWidth": 1,
    "gridLineColor": "#e0e0e0",
    "lineWidth": 2,
    "lineColor": "#333333",
}

# Color palette for streamlines
colors = ["#306998", "#FFD43B", "#9467BD", "#17BECF", "#8C564B", "#E377C2", "#7F7F7F", "#BCBD22"]

# Plot options
chart.options.plot_options = {"line": {"lineWidth": 5, "marker": {"enabled": False}, "enableMouseTracking": False}}

# Legend
chart.options.legend = {"enabled": False}

# Add streamlines as series
for i, streamline in enumerate(streamlines):
    series = LineSeries()
    series.data = [[round(pt[0], 4), round(pt[1], 4)] for pt in streamline]
    series.name = f"Streamline {i + 1}"
    series.color = colors[i % len(colors)]
    series.line_width = 5
    chart.add_series(series)

# Download Highcharts JS
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

# Write temp HTML
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

# Also save as plot.html for interactive version
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Take screenshot with Selenium
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

# Clean up temp file
Path(temp_path).unlink()
