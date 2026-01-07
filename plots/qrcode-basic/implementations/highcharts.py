"""pyplots.ai
qrcode-basic: Basic QR Code Generator
Library: highcharts | Python 3.13
Quality: pending | Created: 2026-01-07
"""

import tempfile
import time
import urllib.request
from pathlib import Path

import qrcode
from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.heatmap import HeatmapSeries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data
content = "https://pyplots.ai"
qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=1, border=4)
qr.add_data(content)
qr.make(fit=True)

# Get QR code matrix as 2D list (True = black, False = white)
matrix = qr.get_matrix()
size = len(matrix)

# Convert to heatmap data: [x, y, value] where 1 = black, 0 = white
# Flip y-axis so QR code displays correctly (row 0 at top)
heatmap_data = []
for row_idx, row in enumerate(matrix):
    for col_idx, cell in enumerate(row):
        # Invert y for correct orientation
        y = size - 1 - row_idx
        heatmap_data.append([col_idx, y, 1 if cell else 0])

# Create chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration
chart.options.chart = {
    "type": "heatmap",
    "width": 3600,
    "height": 3600,
    "backgroundColor": "#ffffff",
    "marginTop": 120,
    "marginBottom": 80,
    "marginLeft": 80,
    "marginRight": 80,
}

# Title
chart.options.title = {
    "text": "qrcode-basic · highcharts · pyplots.ai",
    "style": {"fontSize": "48px", "fontWeight": "bold"},
}

chart.options.subtitle = {"text": f"Encoded: {content}", "style": {"fontSize": "28px", "color": "#666666"}}

# Remove axes for clean QR code appearance
chart.options.x_axis = {"visible": False, "min": -0.5, "max": size - 0.5}

chart.options.y_axis = {"visible": False, "min": -0.5, "max": size - 0.5, "reversed": False}

# Color axis - black and white only
chart.options.color_axis = {"min": 0, "max": 1, "stops": [[0, "#ffffff"], [1, "#000000"]], "visible": False}

# Legend off
chart.options.legend = {"enabled": False}

# Credits off
chart.options.credits = {"enabled": False}

# Tooltip
chart.options.tooltip = {"enabled": False}

# Plot options for heatmap
chart.options.plot_options = {
    "heatmap": {"borderWidth": 0, "colsize": 1, "rowsize": 1, "dataLabels": {"enabled": False}}
}

# Add series data
series = HeatmapSeries()
series.data = heatmap_data
series.name = "QR Code"
series.border_width = 0

chart.add_series(series)

# Export to PNG via Selenium
# Download required Highcharts modules
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
<body style="margin:0; background-color:#ffffff;">
    <div id="container" style="width: 3600px; height: 3600px;"></div>
    <script>{html_str}</script>
</body>
</html>"""

# Write temp HTML and take screenshot
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

# Also save the HTML for interactive version
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=3600,3600")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)  # Wait for chart to render
driver.save_screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()  # Clean up temp file
