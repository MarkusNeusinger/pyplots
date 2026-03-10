""" pyplots.ai
pictogram-basic: Pictogram Chart (Isotype Visualization)
Library: highcharts unknown | Python 3.14.3
Quality: 78/100 | Created: 2026-03-10
"""

import tempfile
import time
import urllib.request
from pathlib import Path

from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.scatter import ScatterSeries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - Annual fruit production (thousands of tons)
categories = ["Apples", "Grapes", "Oranges", "Bananas", "Strawberries"]
production = [35, 28, 22, 18, 12]
unit_value = 5

colors = ["#306998", "#7B68A8", "#E8813B", "#F2C94C", "#E74C3C"]

# Create chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart settings
max_icons = max(v // unit_value + (1 if v % unit_value else 0) for v in production)
chart.options.chart = {
    "type": "scatter",
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#ffffff",
    "marginLeft": 450,
    "marginRight": 300,
    "marginBottom": 150,
    "marginTop": 220,
    "plotBorderWidth": 0,
}

# Title
chart.options.title = {
    "text": "pictogram-basic \u00b7 highcharts \u00b7 pyplots.ai",
    "style": {"fontSize": "48px", "fontWeight": "bold"},
}

# Subtitle with legend note
chart.options.subtitle = {
    "text": f"Annual Fruit Production \u2014 each \u25cf = {unit_value}k tons",
    "style": {"fontSize": "32px", "color": "#666666"},
}

# X-axis (icon positions) - tighter range for compact layout
chart.options.x_axis = {
    "min": -0.5,
    "max": max_icons - 0.3,
    "title": {"text": None},
    "labels": {"enabled": False},
    "gridLineWidth": 0,
    "lineWidth": 0,
    "tickWidth": 0,
    "tickLength": 0,
}

# Y-axis (categories)
chart.options.y_axis = {
    "categories": categories,
    "title": {"text": None},
    "labels": {"style": {"fontSize": "36px", "fontWeight": "bold"}, "x": -15},
    "gridLineWidth": 0,
    "lineWidth": 0,
    "tickWidth": 0,
    "tickLength": 0,
    "reversed": True,
    "startOnTick": False,
    "endOnTick": False,
}

# Legend
chart.options.legend = {"enabled": False}

# Credits
chart.options.credits = {"enabled": False}

# Tooltip
chart.options.tooltip = {
    "headerFormat": "",
    "pointFormat": "<b>{series.name}</b>: {point.total}k tons",
    "style": {"fontSize": "24px"},
}

# Plot options
chart.options.plot_options = {
    "scatter": {
        "jitter": {"x": 0, "y": 0},
        "marker": {"symbol": "circle", "radius": 45, "lineWidth": 3, "lineColor": "#ffffff"},
    }
}

# Create series for each category
for i, (cat, val, color) in enumerate(zip(categories, production, colors, strict=True)):
    n_full = val // unit_value
    remainder = (val % unit_value) / unit_value

    data = []
    for j in range(n_full):
        data.append({"x": j, "y": i, "total": val})

    if remainder > 0:
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        data.append(
            {"x": n_full, "y": i, "total": val, "marker": {"fillColor": f"rgba({r},{g},{b},{round(remainder, 2)})"}}
        )

    series = ScatterSeries()
    series.name = cat
    series.data = data
    series.color = color
    chart.add_series(series)

# Download Highcharts JS
highcharts_url = "https://cdn.jsdelivr.net/npm/highcharts@11/highcharts.js"
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

# Write temp HTML file
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

# Save standalone HTML
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Take screenshot with Selenium
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=4800,2700")
chrome_options.add_argument("--hide-scrollbars")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)

container = driver.find_element("id", "container")
container.screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()
