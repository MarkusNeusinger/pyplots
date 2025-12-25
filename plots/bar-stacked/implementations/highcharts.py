"""pyplots.ai
bar-stacked: Stacked Bar Chart
Library: highcharts | Python 3.13
Quality: pending | Created: 2025-12-25
"""

import tempfile
import time
import urllib.request
from pathlib import Path

from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.bar import ColumnSeries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data: Quarterly revenue by product category (in thousands)
categories = ["Q1", "Q2", "Q3", "Q4"]
components = {
    "Software": [320, 380, 420, 480],
    "Hardware": [180, 200, 190, 220],
    "Services": [150, 180, 210, 250],
    "Licensing": [90, 110, 130, 160],
}

# Colors: Python Blue, Python Yellow, then colorblind-safe additions
colors = ["#306998", "#FFD43B", "#9467BD", "#17BECF"]

# Create chart with container (CRITICAL for headless rendering)
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration
chart.options.chart = {
    "type": "column",
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#ffffff",
    "marginBottom": 200,
    "marginTop": 120,
    "spacingBottom": 50,
}

# Title
chart.options.title = {
    "text": "bar-stacked \u00b7 highcharts \u00b7 pyplots.ai",
    "style": {"fontSize": "48px", "fontWeight": "bold"},
}

# Subtitle
chart.options.subtitle = {"text": "Quarterly Revenue by Product Category", "style": {"fontSize": "32px"}}

# X-axis (categories)
chart.options.x_axis = {
    "categories": categories,
    "title": {"text": "Quarter", "style": {"fontSize": "32px"}},
    "labels": {"style": {"fontSize": "28px"}},
}

# Y-axis
chart.options.y_axis = {
    "title": {"text": "Revenue ($ thousands)", "style": {"fontSize": "32px"}},
    "labels": {"style": {"fontSize": "28px"}},
    "gridLineWidth": 1,
    "gridLineColor": "#cccccc",
    "stackLabels": {"enabled": True, "style": {"fontSize": "24px", "fontWeight": "bold", "color": "#333333"}},
}

# Legend
chart.options.legend = {
    "enabled": True,
    "itemStyle": {"fontSize": "28px"},
    "layout": "horizontal",
    "align": "center",
    "verticalAlign": "bottom",
    "y": -30,
}

# Plot options for stacking
chart.options.plot_options = {
    "column": {
        "stacking": "normal",
        "borderWidth": 2,
        "borderColor": "#ffffff",
        "dataLabels": {
            "enabled": True,
            "style": {"fontSize": "22px", "fontWeight": "normal", "color": "#333333"},
            "format": "{y}",
        },
    }
}

# Tooltip
chart.options.tooltip = {
    "style": {"fontSize": "24px"},
    "headerFormat": "<b>{point.x}</b><br/>",
    "pointFormat": "{series.name}: ${point.y}k<br/>Total: ${point.stackTotal}k",
}

# Add series for each component
for i, (component_name, values) in enumerate(components.items()):
    series = ColumnSeries()
    series.name = component_name
    series.data = values
    series.color = colors[i % len(colors)]
    chart.add_series(series)

# Download Highcharts JS for inline embedding (required for headless Chrome)
highcharts_url = "https://code.highcharts.com/highcharts.js"
with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

# Generate HTML with inline script
html_str = chart.to_js_literal()
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
</head>
<body style="margin:0; padding:0; background:#ffffff;">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>{html_str}</script>
</body>
</html>"""

# Save HTML file
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Create temp file for screenshot
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

# Screenshot using Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=5000,3000")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)

# Screenshot the container element for exact 4800x2700 dimensions
container = driver.find_element("id", "container")
container.screenshot("plot.png")
driver.quit()

# Clean up temp file
Path(temp_path).unlink()
