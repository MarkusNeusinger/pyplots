""" pyplots.ai
pie-basic: Basic Pie Chart
Library: highcharts unknown | Python 3.13.11
Quality: 92/100 | Created: 2025-12-23
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


# Data - Market share distribution (5 categories, realistic business context)
categories = ["Product A", "Product B", "Product C", "Product D", "Product E"]
values = [35, 25, 20, 12, 8]

# Colorblind-safe colors (Python Blue first, then complementary)
colors = ["#306998", "#FFD43B", "#9467BD", "#17BECF", "#8C564B"]

# Create chart with container specified
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration for 3600x3600 square (ideal for pie charts)
chart.options.chart = {
    "type": "pie",
    "width": 3600,
    "height": 3600,
    "backgroundColor": "#ffffff",
    "spacingTop": 80,
    "spacingBottom": 80,
    "spacingLeft": 80,
    "spacingRight": 80,
}

# Title
chart.options.title = {
    "text": "pie-basic · highcharts · pyplots.ai",
    "style": {"fontSize": "48px", "fontWeight": "bold"},
    "margin": 40,
}

# Colors
chart.options.colors = colors

# Plot options for pie with percentage labels and legend
chart.options.plot_options = {
    "pie": {
        "allowPointSelect": True,
        "cursor": "pointer",
        "dataLabels": {
            "enabled": True,
            "format": "<b>{point.name}</b>: {point.percentage:.1f}%",
            "style": {"fontSize": "32px", "textOutline": "none"},
            "distance": 40,
            "connectorWidth": 2,
        },
        "showInLegend": True,
        "slicedOffset": 25,
        "size": "70%",
        "center": ["40%", "50%"],
    }
}

# Legend on the right side
chart.options.legend = {
    "enabled": True,
    "align": "right",
    "verticalAlign": "middle",
    "layout": "vertical",
    "itemStyle": {"fontSize": "36px", "fontWeight": "normal"},
    "itemMarginTop": 20,
    "itemMarginBottom": 20,
    "symbolRadius": 10,
    "symbolHeight": 20,
    "symbolWidth": 20,
    "x": -80,
}

# Create pie series with data - first slice (largest) is exploded for emphasis
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

# Write temp HTML and take screenshot
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

# Also save the HTML for interactive version
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Setup Chrome for screenshot
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=3600,3800")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)  # Wait for chart to render
driver.save_screenshot("plot_raw.png")
driver.quit()

# Crop to exact 3600x3600 dimensions
img = Image.open("plot_raw.png")
img_cropped = img.crop((0, 0, 3600, 3600))
img_cropped.save("plot.png")
Path("plot_raw.png").unlink()

Path(temp_path).unlink()  # Clean up temp file
