"""
donut-labeled: Donut Chart with Percentage Labels
Library: highcharts
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


# Data - Department budget allocation
categories = ["Marketing", "Engineering", "Operations", "Sales", "HR", "R&D"]
values = [25, 30, 15, 18, 7, 5]

# Colors from style guide palette
colors = ["#306998", "#FFD43B", "#DC2626", "#059669", "#8B5CF6", "#F97316"]

# Create chart with container specified
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration
chart.options.chart = {"type": "pie", "width": 4800, "height": 2700, "backgroundColor": "#ffffff"}

# Title
chart.options.title = {"text": "Department Budget Allocation", "style": {"fontSize": "48px", "fontWeight": "bold"}}

# Tooltip configuration
chart.options.tooltip = {"pointFormat": "<b>{point.percentage:.1f}%</b>", "style": {"fontSize": "32px"}}

# Plot options for donut appearance with labels
chart.options.plot_options = {
    "pie": {
        "innerSize": "55%",  # Creates donut hole (55% inner radius)
        "borderWidth": 3,
        "borderColor": "#ffffff",
        "dataLabels": {
            "enabled": True,
            "format": "{point.percentage:.1f}%",
            "distance": -50,  # Negative distance places labels inside slices
            "style": {"fontSize": "36px", "fontWeight": "bold", "color": "white", "textOutline": "2px black"},
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
    "itemStyle": {"fontSize": "32px"},
    "title": {"text": "Department", "style": {"fontSize": "36px", "fontWeight": "bold"}},
}

# Create pie series with data
series = PieSeries()
series.name = "Budget"
series.data = [{"name": cat, "y": val, "color": col} for cat, val, col in zip(categories, values, colors, strict=True)]

chart.add_series(series)

# Download Highcharts JS for headless Chrome
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

# Also save the HTML for interactive viewing
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)

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
