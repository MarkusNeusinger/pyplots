"""pyplots.ai
pie-basic: Basic Pie Chart
Library: highcharts 1.10.3 | Python 3.14.0
Quality: /100 | Updated: 2026-02-14
"""

import tempfile
import time
import urllib.request
from pathlib import Path

from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.pie import PieSeries
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data — Cloud infrastructure market share (5 categories, realistic business context)
# No random data — fully deterministic
categories = ["AWS", "Azure", "Google Cloud", "Alibaba", "Others"]
values = [31, 25, 11, 4, 29]

# Colorblind-safe palette (Python Blue first, then complementary)
colors = ["#306998", "#FFD43B", "#E07B54", "#17BECF", "#9467BD"]

# Chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

chart.options.chart = {
    "type": "pie",
    "width": 3600,
    "height": 3600,
    "backgroundColor": "#ffffff",
    "spacingTop": 60,
    "spacingBottom": 40,
    "spacingLeft": 100,
    "spacingRight": 100,
}

# Title
chart.options.title = {
    "text": "Cloud Infrastructure Market Share · pie-basic · highcharts · pyplots.ai",
    "style": {"fontSize": "52px", "fontWeight": "bold"},
    "margin": 20,
}

# Subtitle
chart.options.subtitle = {
    "text": "Global cloud spending by provider, 2024",
    "style": {"fontSize": "36px", "color": "#666666"},
}

# Colors
chart.options.colors = colors

# Credits
chart.options.credits = {"enabled": False}

# Plot options
chart.options.plot_options = {
    "pie": {
        "allowPointSelect": True,
        "cursor": "pointer",
        "dataLabels": {
            "enabled": True,
            "format": "<b>{point.name}</b>: {point.percentage:.1f}%",
            "style": {"fontSize": "38px", "textOutline": "none", "fontWeight": "normal"},
            "distance": 50,
            "connectorWidth": 3,
            "connectorColor": "#aaaaaa",
            "softConnector": True,
        },
        "showInLegend": True,
        "slicedOffset": 35,
        "size": "70%",
        "center": ["50%", "50%"],
        "startAngle": -20,
    }
}

# Legend — bottom horizontal
chart.options.legend = {
    "enabled": True,
    "align": "center",
    "verticalAlign": "bottom",
    "layout": "horizontal",
    "itemStyle": {"fontSize": "38px", "fontWeight": "normal"},
    "symbolRadius": 10,
    "symbolHeight": 22,
    "symbolWidth": 22,
    "margin": 20,
}

# Tooltip
chart.options.tooltip = {"pointFormat": "<b>{point.percentage:.1f}%</b> market share", "style": {"fontSize": "28px"}}

# Series — largest slice (AWS) exploded for emphasis
series = PieSeries()
series.name = "Market Share"
series.data = [
    {"name": cat, "y": val, "sliced": i == 0, "selected": i == 0}
    for i, (cat, val) in enumerate(zip(categories, values, strict=True))
]

chart.add_series(series)

# Download Highcharts JS for inline embedding (required for headless Chrome)
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
    <div id="container" style="width: 3600px; height: 3600px;"></div>
    <script>{html_str}</script>
</body>
</html>"""

# Write temp HTML and save interactive version
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Screenshot via headless Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=3600,3800")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)
driver.save_screenshot("plot_raw.png")
driver.quit()

# Crop to exact 3600x3600
img = Image.open("plot_raw.png")
img_cropped = img.crop((0, 0, 3600, 3600))
img_cropped.save("plot.png")
Path("plot_raw.png").unlink()

Path(temp_path).unlink()
