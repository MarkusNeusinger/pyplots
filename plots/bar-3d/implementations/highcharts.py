"""pyplots.ai
bar-3d: 3D Bar Chart
Library: highcharts | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.bar import ColumnSeries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - Sales performance across products and quarters
np.random.seed(42)
products = ["Laptop", "Tablet", "Phone", "Monitor", "Keyboard"]
quarters = ["Q1", "Q2", "Q3", "Q4"]

# Generate realistic sales revenue data (in thousands)
sales_data = []
base_values = [150, 80, 200, 60, 30]  # Base sales for each product
for i, _product in enumerate(products):
    product_series = []
    for j, _quarter in enumerate(quarters):
        # Seasonal variation + some randomness
        seasonal = 1 + 0.2 * np.sin(j * np.pi / 2)
        value = base_values[i] * seasonal + np.random.normal(0, 10)
        product_series.append(round(max(10, value), 1))
    sales_data.append(product_series)

# Create chart with container
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration with 3D options
chart.options.chart = {
    "type": "column",
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#ffffff",
    "marginBottom": 180,
    "marginRight": 100,
    "options3d": {
        "enabled": True,
        "alpha": 15,
        "beta": 20,
        "depth": 400,
        "viewDistance": 25,
        "frame": {"bottom": {"size": 1, "color": "rgba(0,0,0,0.02)"}},
    },
}

# Title
chart.options.title = {
    "text": "bar-3d \u00b7 highcharts \u00b7 pyplots.ai",
    "style": {"fontSize": "48px", "fontWeight": "bold"},
}

chart.options.subtitle = {"text": "Quarterly Sales Revenue by Product Category (in $K)", "style": {"fontSize": "32px"}}

# X-axis (products)
chart.options.x_axis = {
    "categories": products,
    "title": {"text": "Product Category", "style": {"fontSize": "28px"}},
    "labels": {"style": {"fontSize": "24px"}, "rotation": 0},
    "gridLineWidth": 0,
}

# Y-axis (revenue)
chart.options.y_axis = {
    "title": {"text": "Revenue ($K)", "style": {"fontSize": "28px"}},
    "labels": {"style": {"fontSize": "24px"}},
    "gridLineColor": "rgba(0,0,0,0.1)",
    "min": 0,
}

# Z-axis (depth for quarters)
chart.options.z_axis = {
    "min": 0,
    "max": len(quarters) - 1,
    "categories": quarters,
    "title": {"text": "Quarter", "style": {"fontSize": "28px"}},
    "labels": {"style": {"fontSize": "24px"}},
}

# Plot options for 3D columns
chart.options.plot_options = {
    "column": {
        "depth": 80,
        "groupZPadding": 20,
        "grouping": False,
        "colorByPoint": False,
        "borderWidth": 1,
        "borderColor": "rgba(0,0,0,0.3)",
    },
    "series": {"dataLabels": {"enabled": False}},
}

# Colorblind-safe colors for quarters
colors = ["#306998", "#FFD43B", "#9467BD", "#17BECF"]

# Legend - positioned at top right for better visibility with 3D chart
chart.options.legend = {
    "enabled": True,
    "layout": "vertical",
    "align": "right",
    "verticalAlign": "top",
    "x": -50,
    "y": 100,
    "itemStyle": {"fontSize": "28px"},
    "symbolHeight": 24,
    "symbolWidth": 36,
    "itemMarginTop": 10,
    "itemMarginBottom": 10,
    "backgroundColor": "rgba(255,255,255,0.9)",
    "borderWidth": 1,
    "borderColor": "#cccccc",
    "padding": 15,
}

# Create series for each quarter (z-depth position)
series_list = []
for q_idx in range(len(quarters)):
    series_data = []
    for p_idx in range(len(products)):
        series_data.append({"x": p_idx, "y": sales_data[p_idx][q_idx], "z": q_idx})
    series_list.append(
        {
            "name": quarters[q_idx],
            "data": series_data,
            "color": colors[q_idx % len(colors)],
            "pointPadding": 0,
            "pointPlacement": -0.1 + q_idx * 0.07,
        }
    )

# Add series using from_dict to properly set type
for s in series_list:
    series = ColumnSeries.from_dict(s)
    chart.add_series(series)

# Download Highcharts JS and 3D module
highcharts_url = "https://code.highcharts.com/highcharts.js"
highcharts_3d_url = "https://code.highcharts.com/highcharts-3d.js"

with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

with urllib.request.urlopen(highcharts_3d_url, timeout=30) as response:
    highcharts_3d_js = response.read().decode("utf-8")

# Generate HTML with inline scripts
html_str = chart.to_js_literal()
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <script>{highcharts_3d_js}</script>
</head>
<body style="margin:0; padding:0; background:#ffffff;">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>{html_str}</script>
</body>
</html>"""

# Write temp HTML and take screenshot
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

# Also save HTML for interactive version
with open("plot.html", "w", encoding="utf-8") as f:
    # For the saved HTML, use CDN links for portability
    html_portable = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://code.highcharts.com/highcharts.js"></script>
    <script src="https://code.highcharts.com/highcharts-3d.js"></script>
    <style>
        body {{ margin: 0; padding: 20px; font-family: Arial, sans-serif; }}
        #container {{ width: 100%; max-width: 1600px; height: 900px; margin: 0 auto; }}
    </style>
</head>
<body>
    <div id="container"></div>
    <script>{html_str}</script>
</body>
</html>"""
    f.write(html_portable)

# Take screenshot with Selenium
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

# Clean up temp file
Path(temp_path).unlink()
