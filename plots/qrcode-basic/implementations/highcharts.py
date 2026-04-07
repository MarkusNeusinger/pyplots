""" pyplots.ai
qrcode-basic: Basic QR Code Generator
Library: highcharts 1.10.3 | Python 3.14.3
Quality: 82/100 | Updated: 2026-04-07
"""

import json
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
matrix = qr.get_matrix()
size = len(matrix)

# Convert to heatmap data [x, y, value] with y flipped for correct orientation
heatmap_data = []
for row_idx, row in enumerate(matrix):
    for col_idx, cell in enumerate(row):
        y = size - 1 - row_idx
        heatmap_data.append([col_idx, y, 1 if cell else 0])

# Chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

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

chart.options.title = {
    "text": "qrcode-basic \u00b7 highcharts \u00b7 pyplots.ai",
    "style": {"fontSize": "48px", "fontWeight": "bold"},
}

chart.options.subtitle = {"text": f"Encoded: {content}", "style": {"fontSize": "28px", "color": "#666666"}}

chart.options.x_axis = {"visible": False, "min": -0.5, "max": size - 0.5}
chart.options.y_axis = {"visible": False, "min": -0.5, "max": size - 0.5, "reversed": False}

chart.options.color_axis = {"min": 0, "max": 1, "stops": [[0, "#ffffff"], [1, "#000000"]], "visible": False}

chart.options.legend = {"enabled": False}
chart.options.credits = {"enabled": False}
chart.options.tooltip = {"enabled": False}

chart.options.plot_options = {
    "heatmap": {"borderWidth": 0, "colsize": 1, "rowsize": 1, "dataLabels": {"enabled": False}}
}

# Series
series = HeatmapSeries()
series.data = heatmap_data
series.name = "QR Code"
series.border_width = 0
chart.add_series(series)

# Download Highcharts JS with CDN fallback
cdn_bases = ["https://code.highcharts.com", "https://cdn.jsdelivr.net/npm/highcharts@11"]
js_paths = {"highcharts": "/highcharts.js", "heatmap": "/modules/heatmap.js"}
js_code = {}
for name, path in js_paths.items():
    for base in cdn_bases:
        try:
            req = urllib.request.Request(base + path, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                js_code[name] = resp.read().decode("utf-8")
            break
        except Exception:
            continue

highcharts_js = js_code["highcharts"]
heatmap_js = js_code["heatmap"]

# Render via options dict for clean output
options_json = json.dumps(chart.options.to_dict())

html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <script>{heatmap_js}</script>
</head>
<body style="margin:0; background-color:#ffffff;">
    <div id="container" style="width: 3600px; height: 3600px;"></div>
    <script>Highcharts.chart('container', {options_json});</script>
</body>
</html>"""

# Save interactive HTML
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Render PNG via headless Chrome
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=3600,3600")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)
driver.save_screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()
