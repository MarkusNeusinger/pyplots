"""
area-stacked: Stacked Area Chart
Library: highcharts
"""

import tempfile
import time
import urllib.request
from pathlib import Path

from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.area import AreaSeries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - monthly revenue by product line over 2 years
months = [
    "Jan 23",
    "Feb 23",
    "Mar 23",
    "Apr 23",
    "May 23",
    "Jun 23",
    "Jul 23",
    "Aug 23",
    "Sep 23",
    "Oct 23",
    "Nov 23",
    "Dec 23",
    "Jan 24",
    "Feb 24",
    "Mar 24",
    "Apr 24",
    "May 24",
    "Jun 24",
    "Jul 24",
    "Aug 24",
    "Sep 24",
    "Oct 24",
    "Nov 24",
    "Dec 24",
]

# Product line revenues (in thousands)
product_a = [45, 48, 52, 55, 60, 58, 62, 65, 68, 72, 78, 85, 88, 92, 95, 98, 102, 105, 108, 112, 115, 118, 125, 130]
product_b = [30, 32, 35, 38, 42, 45, 48, 50, 52, 55, 58, 62, 65, 68, 70, 72, 75, 78, 80, 82, 85, 88, 90, 95]
product_c = [20, 22, 25, 28, 30, 32, 35, 38, 40, 42, 45, 48, 50, 52, 55, 58, 60, 62, 65, 68, 70, 72, 75, 78]
product_d = [15, 16, 18, 20, 22, 24, 26, 28, 30, 32, 35, 38, 40, 42, 45, 48, 50, 52, 55, 58, 60, 62, 65, 68]

# Color palette from style guide
colors = ["#306998", "#FFD43B", "#DC2626", "#059669"]

# Create chart with container (required for headless export)
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration
chart.options.chart = {
    "type": "area",
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#ffffff",
    "style": {"fontFamily": "Arial, sans-serif"},
}

# Title
chart.options.title = {"text": "Monthly Revenue by Product Line", "style": {"fontSize": "48px"}}

# X-axis with categories
chart.options.x_axis = {
    "categories": months,
    "title": {"text": "Month", "style": {"fontSize": "40px"}},
    "labels": {"style": {"fontSize": "28px"}},
    "lineWidth": 2,
}

# Y-axis
chart.options.y_axis = {
    "title": {"text": "Revenue (Thousands $)", "style": {"fontSize": "40px"}},
    "labels": {"style": {"fontSize": "32px"}},
    "gridLineColor": "#e0e0e0",
    "gridLineWidth": 1,
}

# Enable stacking
chart.options.plot_options = {
    "area": {"stacking": "normal", "fillOpacity": 0.75, "lineWidth": 2, "marker": {"enabled": False}}
}

# Legend
chart.options.legend = {
    "enabled": True,
    "itemStyle": {"fontSize": "32px"},
    "align": "center",
    "verticalAlign": "bottom",
}

# Create series for each product line (largest at bottom for stability)
series_data = [
    ("Product A", product_a, colors[0]),
    ("Product B", product_b, colors[1]),
    ("Product C", product_c, colors[2]),
    ("Product D", product_d, colors[3]),
]

for name, data, color in series_data:
    series = AreaSeries()
    series.data = data
    series.name = name
    series.color = color
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
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>{html_str}</script>
</body>
</html>"""

# Save HTML for interactive viewing
with open("plot.html", "w", encoding="utf-8") as f:
    # For standalone HTML, use CDN instead of inline
    standalone_html = (
        """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://code.highcharts.com/highcharts.js"></script>
</head>
<body style="margin:0;">
    <div id="container" style="width: 100%; height: 600px;"></div>
    <script>"""
        + html_str
        + """</script>
</body>
</html>"""
    )
    f.write(standalone_html)

# Write temp HTML and take screenshot
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=4900,2800")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)
driver.save_screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()
