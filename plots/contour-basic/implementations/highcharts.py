"""
contour-basic: Basic Contour Plot
Library: highcharts
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


# Data - create a 2D scalar field using a mathematical function
np.random.seed(42)
grid_size = 50  # 50x50 grid for smooth contours

x = np.linspace(-3, 3, grid_size)
y = np.linspace(-3, 3, grid_size)
X, Y = np.meshgrid(x, y)

# Create an interesting surface: combination of Gaussian peaks
Z = (
    np.exp(-((X - 1) ** 2 + (Y - 1) ** 2))
    + 0.8 * np.exp(-((X + 1) ** 2 + (Y + 1) ** 2))
    - 0.5 * np.exp(-((X) ** 2 + (Y - 1.5) ** 2) / 0.5)
)

# Normalize Z to 0-100 range for better color mapping
Z_min, Z_max = Z.min(), Z.max()
Z_normalized = ((Z - Z_min) / (Z_max - Z_min) * 100).astype(int)

# Create heatmap data in Highcharts format: [x_index, y_index, value]
# This creates a filled contour-like visualization
heatmap_data = []
for y_idx in range(grid_size):
    for x_idx in range(grid_size):
        heatmap_data.append([x_idx, y_idx, int(Z_normalized[y_idx, x_idx])])

# Create category labels for axes (showing actual coordinate values)
x_labels = [f"{v:.1f}" for v in x]
y_labels = [f"{v:.1f}" for v in y]

# Create chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration
chart.options.chart = {
    "type": "heatmap",
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#ffffff",
    "marginBottom": 300,
    "marginRight": 250,
    "marginLeft": 200,
}

# Title
chart.options.title = {
    "text": "contour-basic · highcharts · pyplots.ai",
    "style": {"fontSize": "64px", "fontWeight": "bold"},
}

# Create sparse category labels (only show at key positions)
x_labels_sparse = ["" for _ in range(grid_size)]
y_labels_sparse = ["" for _ in range(grid_size)]
for i in range(0, grid_size, 8):
    x_labels_sparse[i] = f"{x[i]:.1f}"
    y_labels_sparse[i] = f"{y[i]:.1f}"
x_labels_sparse[-1] = f"{x[-1]:.1f}"
y_labels_sparse[-1] = f"{y[-1]:.1f}"

# X-axis
chart.options.x_axis = {
    "categories": x_labels_sparse,
    "title": {"text": "X", "style": {"fontSize": "48px"}},
    "labels": {"style": {"fontSize": "36px"}, "rotation": 0},
    "lineWidth": 2,
    "tickLength": 10,
}

# Y-axis
chart.options.y_axis = {
    "categories": y_labels_sparse,
    "title": {"text": "Y", "style": {"fontSize": "48px"}},
    "labels": {"style": {"fontSize": "36px"}},
    "reversed": False,
    "lineWidth": 2,
    "tickLength": 10,
}

# Color axis with viridis-like gradient (colorblind-safe)
chart.options.color_axis = {
    "min": 0,
    "max": 100,
    "stops": [
        [0, "#440154"],  # Dark purple
        [0.25, "#3b528b"],  # Blue
        [0.5, "#21918c"],  # Teal
        [0.75, "#5ec962"],  # Green
        [1, "#fde725"],  # Yellow
    ],
    "labels": {"style": {"fontSize": "32px"}, "format": "{value}%"},
}

# Legend configuration (colorbar)
chart.options.legend = {
    "align": "right",
    "layout": "vertical",
    "margin": 30,
    "verticalAlign": "middle",
    "symbolHeight": 800,
    "itemStyle": {"fontSize": "32px"},
    "title": {"text": "Value", "style": {"fontSize": "36px"}},
}

# Tooltip
chart.options.tooltip = {
    "style": {"fontSize": "32px"},
    "headerFormat": "",
    "pointFormat": "X: <b>{series.xAxis.categories.(point.x)}</b><br>"
    "Y: <b>{series.yAxis.categories.(point.y)}</b><br>"
    "Value: <b>{point.value}</b>",
}

# Add heatmap series (creates filled contour effect)
series_config = {
    "name": "Surface",
    "type": "heatmap",
    "data": heatmap_data,
    "borderWidth": 0,  # No borders for smooth contour appearance
    "colsize": 1,
    "rowsize": 1,
    "dataLabels": {"enabled": False},  # No labels for clean look
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
