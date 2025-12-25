"""pyplots.ai
pie-exploded: Exploded Pie Chart
Library: highcharts | Python 3.13
Quality: pending | Created: 2025-12-25
"""

import tempfile
import time
import urllib.request
from pathlib import Path

from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.pie import PieSeries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - Market share showing exploded leader and runner-up
categories = ["TechCorp", "DataSoft", "CloudNet", "InnoSys", "WebScale", "CoreLogic"]
values = [35, 25, 18, 12, 7, 3]
# Explode the market leader and runner-up to emphasize top performers
explode = [0.12, 0.06, 0, 0, 0, 0]

# Colorblind-safe palette
colors = ["#306998", "#FFD43B", "#9467BD", "#17BECF", "#8C564B", "#E377C2"]

# Build pie data with sliced property for explosion
pie_data = []
for i, (cat, val, exp) in enumerate(zip(categories, values, explode, strict=True)):
    data_point = {"name": cat, "y": val, "sliced": exp > 0, "color": colors[i]}
    if exp > 0:
        data_point["sliced"] = True
    pie_data.append(data_point)

# Create chart - CRITICAL: always specify container
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration for square format (pie charts look best in square)
chart.options.chart = {"type": "pie", "width": 3600, "height": 3600, "backgroundColor": "#ffffff"}

# Title
chart.options.title = {
    "text": "pie-exploded · highcharts · pyplots.ai",
    "style": {"fontSize": "72px", "fontWeight": "bold"},
}

# Subtitle
chart.options.subtitle = {"text": "Market Share by Company", "style": {"fontSize": "48px"}}

# Plot options for pie with explosion and data labels
chart.options.plot_options = {
    "pie": {
        "allowPointSelect": True,
        "cursor": "pointer",
        "slicedOffset": 80,  # Explosion distance in pixels
        "size": "65%",  # Make the pie larger
        "dataLabels": {
            "enabled": True,
            "format": "<b>{point.name}</b>: {point.percentage:.1f}%",
            "style": {"fontSize": "36px", "fontWeight": "normal", "textOutline": "2px white"},
            "distance": 50,
        },
        "showInLegend": True,
    }
}

# Legend configuration
chart.options.legend = {
    "enabled": True,
    "layout": "vertical",
    "align": "right",
    "verticalAlign": "middle",
    "itemStyle": {"fontSize": "36px"},
    "itemMarginBottom": 15,
}

# Credits off
chart.options.credits = {"enabled": False}

# Create and add pie series
series = PieSeries()
series.data = pie_data
series.name = "Market Share"
chart.add_series(series)

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
    <div id="container" style="width: 3600px; height: 3600px;"></div>
    <script>{html_str}</script>
</body>
</html>"""

# Save HTML version
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Write temp HTML and take screenshot
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
time.sleep(5)  # Wait for chart to render
driver.save_screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()  # Clean up temp file
