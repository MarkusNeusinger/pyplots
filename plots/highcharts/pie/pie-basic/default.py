"""
pie-basic: Basic Pie Chart
Library: highcharts
"""

import tempfile
import time
import urllib.request
from pathlib import Path

import pandas as pd
from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.pie import PieSeries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data (from spec)
data = pd.DataFrame(
    {"category": ["Product A", "Product B", "Product C", "Product D", "Other"], "value": [35, 25, 20, 15, 5]}
)

# Style guide colors
COLORS = [
    "#306998",  # Python Blue
    "#FFD43B",  # Python Yellow
    "#DC2626",  # Signal Red
    "#059669",  # Teal Green
    "#8B5CF6",  # Violet
    "#F97316",  # Orange
]

# Create chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration (4800 x 2700 px per style guide)
chart.options.chart = {"type": "pie", "width": 4800, "height": 2700, "backgroundColor": "#ffffff"}

# Title
chart.options.title = {"text": "Market Share Distribution", "style": {"fontSize": "48px", "fontWeight": "600"}}

# Build pie data with colors
pie_data = []
for i, row in data.iterrows():
    pie_data.append({"name": row["category"], "y": row["value"], "color": COLORS[i % len(COLORS)]})

# Create pie series
series = PieSeries()
series.data = pie_data
series.name = "Market Share"
series.show_in_legend = True

# Data labels with percentages
series.data_labels = {
    "enabled": True,
    "format": "{point.name}: {point.percentage:.1f}%",
    "distance": 40,
    "style": {"fontSize": "32px", "fontWeight": "normal", "textOutline": "3px white"},
}

chart.add_series(series)

# Plot options for pie
chart.options.plot_options = {
    "pie": {
        "allowPointSelect": True,
        "cursor": "pointer",
        "showInLegend": True,
        "center": ["50%", "50%"],
        "size": "70%",
    }
}

# Legend configuration
chart.options.legend = {
    "enabled": True,
    "align": "right",
    "verticalAlign": "middle",
    "layout": "vertical",
    "itemStyle": {"fontSize": "32px"},
}

# Tooltip
chart.options.tooltip = {
    "pointFormat": "<b>{point.percentage:.1f}%</b><br/>Value: {point.y}",
    "style": {"fontSize": "28px"},
}

# Disable credits
chart.options.credits = {"enabled": False}

# Download Highcharts JS (required for headless Chrome)
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

# Take screenshot with Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=5000,3000")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)  # Wait for chart to render

# Screenshot the chart container element for exact dimensions
container = driver.find_element("id", "container")
container.screenshot("plot.png")
driver.quit()

# Clean up temp file
Path(temp_path).unlink()
