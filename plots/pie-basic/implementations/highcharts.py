"""pyplots.ai
pie-basic: Basic Pie Chart
Library: highcharts 1.10.3 | Python 3.14.0
Quality: 86/100 | Created: 2025-12-23
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
total = sum(values)

# Colorblind-safe palette (Python Blue first, then complementary)
colors = ["#306998", "#FFD43B", "#E07B54", "#17BECF", "#9467BD"]

# Compute top-3 share for annotation
top3_share = sum(values[:3])

# Chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

chart.options.chart = {
    "type": "pie",
    "width": 3600,
    "height": 3600,
    "backgroundColor": "#ffffff",
    "spacingTop": 50,
    "spacingBottom": 30,
    "spacingLeft": 80,
    "spacingRight": 80,
    "style": {"fontFamily": "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"},
}

# Title
chart.options.title = {
    "text": "Cloud Infrastructure Market Share · pie-basic · highcharts · pyplots.ai",
    "style": {"fontSize": "50px", "fontWeight": "bold", "color": "#1a1a2e"},
    "margin": 10,
}

# Subtitle with storytelling context
chart.options.subtitle = {
    "text": (f"Global cloud spending by provider, 2024 — Top 3 providers control {top3_share}% of the market"),
    "style": {"fontSize": "34px", "color": "#555555", "fontWeight": "normal"},
}

# Colors
chart.options.colors = colors

# Credits
chart.options.credits = {"enabled": False}

# Plot options with enhanced visual refinement
chart.options.plot_options = {
    "pie": {
        "allowPointSelect": True,
        "cursor": "pointer",
        "borderWidth": 2,
        "borderColor": "#ffffff",
        "shadow": {"color": "rgba(0,0,0,0.12)", "offsetX": 3, "offsetY": 3, "width": 8},
        "dataLabels": {
            "enabled": True,
            "format": "<b>{point.name}</b><br>{point.percentage:.1f}%",
            "style": {"fontSize": "38px", "textOutline": "none", "fontWeight": "normal", "color": "#333333"},
            "distance": 55,
            "connectorWidth": 2,
            "connectorColor": "#999999",
            "softConnector": True,
            "connectorShape": "crookedLine",
        },
        "showInLegend": True,
        "slicedOffset": 45,
        "size": "75%",
        "center": ["50%", "46%"],
        "startAngle": -20,
        "innerSize": "0%",
        "states": {"hover": {"halo": {"size": 15, "opacity": 0.25}}, "inactive": {"opacity": 0.5}},
    }
}

# Legend — bottom horizontal, refined styling
chart.options.legend = {
    "enabled": True,
    "align": "center",
    "verticalAlign": "bottom",
    "layout": "horizontal",
    "itemStyle": {"fontSize": "36px", "fontWeight": "normal", "color": "#444444"},
    "itemHoverStyle": {"color": "#1a1a2e"},
    "symbolRadius": 8,
    "symbolHeight": 20,
    "symbolWidth": 20,
    "margin": 15,
    "padding": 12,
}

# Tooltip
chart.options.tooltip = {
    "pointFormat": "<b>{point.percentage:.1f}%</b> market share",
    "style": {"fontSize": "28px"},
    "backgroundColor": "rgba(255,255,255,0.95)",
    "borderColor": "#cccccc",
    "borderRadius": 8,
    "shadow": {"color": "rgba(0,0,0,0.08)", "offsetX": 1, "offsetY": 1, "width": 3},
}

# Series — largest slice (AWS) exploded for emphasis
# Use point-level custom styling for the leader slice
series = PieSeries()
series.name = "Market Share"

series_data = []
for i, (cat, val) in enumerate(zip(categories, values, strict=True)):
    point = {"name": cat, "y": val, "sliced": i == 0, "selected": i == 0}
    if i == 0:
        # Highlight leader with slightly brighter variant and thicker border
        point["borderWidth"] = 3
        point["borderColor"] = "#1e4060"
    series_data.append(point)

series.data = series_data
chart.add_series(series)

# Download Highcharts JS for inline embedding
highcharts_url = "https://code.highcharts.com/highcharts.js"
with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

# Callout annotation as an overlay (positioned with CSS for precise control)
callout_html = """
<div style="
    position: absolute;
    bottom: 215px;
    left: 50%;
    transform: translateX(-50%);
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    color: #ffffff;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 34px;
    font-weight: 600;
    padding: 22px 44px;
    border-radius: 12px;
    line-height: 1.5;
    text-align: center;
    box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    letter-spacing: 0.3px;
    border-left: 5px solid #306998;
">
    AWS leads with nearly &frac13; of global cloud revenue
</div>
"""

# Generate HTML with inline scripts
html_str = chart.to_js_literal()
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
</head>
<body style="margin:0; position: relative;">
    <div id="container" style="width: 3600px; height: 3600px;"></div>
    {callout_html}
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
