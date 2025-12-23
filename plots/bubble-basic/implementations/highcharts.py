""" pyplots.ai
bubble-basic: Basic Bubble Chart
Library: highcharts unknown | Python 3.13.11
Quality: 91/100 | Created: 2025-12-23
"""

import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.bubble import BubbleSeries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - Tech companies comparison
np.random.seed(42)
n = 30

# Revenue (billions USD) - x axis
revenue = np.array(
    [
        5,
        12,
        25,
        38,
        45,
        52,
        68,
        75,
        82,
        95,
        110,
        125,
        140,
        155,
        170,
        185,
        200,
        220,
        245,
        270,
        300,
        330,
        360,
        390,
        420,
        460,
        500,
        550,
        600,
        650,
    ]
)

# Growth rate (%) - y axis
growth = np.array(
    [
        45,
        38,
        52,
        28,
        35,
        22,
        42,
        18,
        30,
        25,
        33,
        20,
        28,
        15,
        38,
        12,
        25,
        18,
        22,
        15,
        20,
        12,
        18,
        10,
        15,
        8,
        12,
        6,
        10,
        5,
    ]
)

# Add realistic variation
revenue = revenue + np.random.uniform(-3, 3, n)
growth = growth + np.random.uniform(-3, 3, n)

# Market cap (billions USD) - bubble size
market_cap = revenue * (1 + growth / 100) * np.random.uniform(2, 8, n)

# Scale bubble z values for Highcharts (controls visual size)
min_cap, max_cap = market_cap.min(), market_cap.max()
z_scaled = 20 + (market_cap - min_cap) / (max_cap - min_cap) * 80

# Format data for Highcharts bubble chart
bubble_data = [
    {"x": float(revenue[i]), "y": float(growth[i]), "z": float(z_scaled[i]), "marketCap": float(market_cap[i])}
    for i in range(n)
]

# Create chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

chart.options.chart = {
    "type": "bubble",
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#ffffff",
    "plotBorderWidth": 1,
    "plotBorderColor": "#cccccc",
    "spacingBottom": 120,
    "spacingRight": 100,
}

chart.options.title = {
    "text": "bubble-basic · highcharts · pyplots.ai",
    "style": {"fontSize": "64px", "fontWeight": "bold"},
}

chart.options.subtitle = {
    "text": "Bubble size represents Market Capitalization",
    "style": {"fontSize": "40px", "color": "#666666"},
}

chart.options.x_axis = {
    "title": {"text": "Revenue (Billion USD)", "style": {"fontSize": "48px"}, "margin": 30},
    "labels": {"style": {"fontSize": "36px"}},
    "gridLineWidth": 1,
    "gridLineColor": "#e6e6e6",
    "min": 0,
}

chart.options.y_axis = {
    "title": {"text": "Growth Rate (%)", "style": {"fontSize": "48px"}},
    "labels": {"style": {"fontSize": "36px"}},
    "gridLineWidth": 1,
    "gridLineColor": "#e6e6e6",
    "min": 0,
}

chart.options.legend = {
    "enabled": True,
    "itemStyle": {"fontSize": "36px"},
    "bubbleLegend": {
        "enabled": True,
        "borderColor": "#306998",
        "borderWidth": 2,
        "color": "rgba(48, 105, 152, 0.5)",
        "connectorColor": "#306998",
        "labels": {"style": {"fontSize": "28px"}},
        "legendIndex": 0,
        "ranges": [
            {"value": 20, "borderColor": "#306998", "color": "rgba(48, 105, 152, 0.5)"},
            {"value": 60, "borderColor": "#306998", "color": "rgba(48, 105, 152, 0.5)"},
            {"value": 100, "borderColor": "#306998", "color": "rgba(48, 105, 152, 0.5)"},
        ],
    },
}

chart.options.tooltip = {
    "useHTML": True,
    "headerFormat": "",
    "pointFormat": '<span style="font-size: 28px"><b>Company Data</b></span><br/>'
    '<span style="font-size: 24px">Revenue: ${point.x:.1f}B<br/>'
    "Growth: {point.y:.1f}%<br/>"
    "Market Cap: ${point.marketCap:.0f}B</span>",
}

chart.options.plot_options = {
    "bubble": {
        "minSize": 50,
        "maxSize": 200,
        "color": "#306998",
        "marker": {"fillOpacity": 0.6, "lineWidth": 3, "lineColor": "#1e4f7a"},
        "dataLabels": {"enabled": False},
        "sizeBy": "area",
    }
}

# Create bubble series
series = BubbleSeries()
series.name = "Market Cap"
series.data = bubble_data
series.color = "#306998"

chart.add_series(series)

# Download Highcharts JS and highcharts-more.js for bubble support
highcharts_url = "https://code.highcharts.com/highcharts.js"
highcharts_more_url = "https://code.highcharts.com/highcharts-more.js"

with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

with urllib.request.urlopen(highcharts_more_url, timeout=30) as response:
    highcharts_more_js = response.read().decode("utf-8")

# Generate HTML with inline scripts
html_str = chart.to_js_literal()
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <script>{highcharts_more_js}</script>
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

# Also save interactive HTML
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
time.sleep(5)
driver.save_screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()
