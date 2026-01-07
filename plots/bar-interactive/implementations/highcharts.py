"""pyplots.ai
bar-interactive: Interactive Bar Chart with Hover and Click
Library: highcharts | Python 3.13
Quality: pending | Created: 2026-01-07
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


# Data - Monthly product sales with regional breakdown info
categories = ["Electronics", "Clothing", "Home & Garden", "Sports", "Books", "Toys", "Food & Beverage", "Health"]
values = [87500, 65200, 54800, 48300, 42100, 38700, 71200, 56400]
percentages = [18.8, 14.0, 11.8, 10.4, 9.0, 8.3, 15.3, 12.1]  # Market share percentages
growth = ["+12%", "+8%", "-3%", "+15%", "+2%", "+21%", "+5%", "+9%"]  # Year-over-year growth

# Create chart with container
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration
chart.options.chart = {
    "type": "column",
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#ffffff",
    "marginBottom": 250,
    "spacingBottom": 50,
}

# Title with pyplots.ai branding
chart.options.title = {
    "text": "bar-interactive · highcharts · pyplots.ai",
    "style": {"fontSize": "48px", "fontWeight": "bold", "color": "#333333"},
}

chart.options.subtitle = {
    "text": "Click bars to view details • Hover for tooltips",
    "style": {"fontSize": "28px", "color": "#666666"},
}

# X-axis configuration
chart.options.x_axis = {
    "categories": categories,
    "title": {"text": "Product Category", "style": {"fontSize": "32px", "color": "#333333"}},
    "labels": {"style": {"fontSize": "24px", "color": "#444444"}, "rotation": 0},
    "lineColor": "#cccccc",
    "tickColor": "#cccccc",
}

# Y-axis configuration
chart.options.y_axis = {
    "title": {"text": "Sales Revenue ($)", "style": {"fontSize": "32px", "color": "#333333"}},
    "labels": {"style": {"fontSize": "22px", "color": "#444444"}, "format": "${value:,.0f}"},
    "gridLineColor": "#e6e6e6",
    "gridLineWidth": 1,
}

# Tooltip configuration with detailed hover information
chart.options.tooltip = {
    "headerFormat": '<span style="font-size: 24px; font-weight: bold;">{point.key}</span><br/>',
    "pointFormat": '<span style="font-size: 20px;">Revenue: <b>${point.y:,.0f}</b></span><br/>'
    '<span style="font-size: 18px;">Market Share: <b>{point.percentage:.1f}%</b></span><br/>'
    '<span style="font-size: 18px;">YoY Growth: <b>{point.growth}</b></span>',
    "backgroundColor": "rgba(255, 255, 255, 0.95)",
    "borderColor": "#306998",
    "borderRadius": 8,
    "borderWidth": 2,
    "style": {"fontSize": "18px"},
}

# Plot options with interactive features
chart.options.plot_options = {
    "column": {
        "borderRadius": 6,
        "borderWidth": 0,
        "cursor": "pointer",
        "dataLabels": {
            "enabled": True,
            "format": "${y:,.0f}",
            "style": {"fontSize": "18px", "fontWeight": "bold", "color": "#333333", "textOutline": "none"},
        },
        "states": {
            "hover": {"brightness": 0.15, "borderColor": "#306998", "borderWidth": 3},
            "select": {"color": "#FFD43B", "borderColor": "#306998", "borderWidth": 3},
        },
        "allowPointSelect": True,
        "point": {"events": {"click": None}},  # Click handler placeholder
    },
    "series": {"animation": {"duration": 1000}},
}

# Legend configuration
chart.options.legend = {
    "enabled": True,
    "align": "center",
    "verticalAlign": "bottom",
    "layout": "horizontal",
    "itemStyle": {"fontSize": "22px", "fontWeight": "normal", "color": "#333333"},
    "y": 20,
}

# Create series with data including tooltip extra info
series = ColumnSeries()
series.name = "2024 Sales"
series.color = "#306998"  # Python Blue
series.data = [
    {"y": values[i], "percentage": percentages[i], "growth": growth[i], "drilldown": categories[i].lower()}
    for i in range(len(categories))
]

chart.add_series(series)

# Credits
chart.options.credits = {"enabled": False}

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
<body style="margin:0; padding:0; background-color: #ffffff;">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>{html_str}</script>
</body>
</html>"""

# Write temp HTML file
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

# Save interactive HTML version
with open("plot.html", "w", encoding="utf-8") as f:
    # Create standalone HTML with CDN for actual interactivity
    interactive_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>bar-interactive · highcharts · pyplots.ai</title>
    <script src="https://code.highcharts.com/highcharts.js"></script>
</head>
<body style="margin:0; padding:20px; background-color: #ffffff;">
    <div id="container" style="width: 100%; height: 90vh; min-height: 600px;"></div>
    <script>{html_str}</script>
</body>
</html>"""
    f.write(interactive_html)

# Configure Chrome for headless screenshot
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=4800,2700")

# Take screenshot
driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)  # Wait for chart to render
driver.save_screenshot("plot.png")
driver.quit()

# Clean up temp file
Path(temp_path).unlink()
