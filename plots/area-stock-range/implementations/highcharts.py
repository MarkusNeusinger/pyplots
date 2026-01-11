"""pyplots.ai
area-stock-range: Stock Area Chart with Range Selector
Library: highcharts | Python 3.13
Quality: pending | Created: 2026-01-11
"""

import json
import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Generate 3 years of stock price data (about 750 trading days)
np.random.seed(42)
n_days = 750
dates = pd.date_range(start="2023-01-03", periods=n_days, freq="B")  # Business days

# Generate realistic stock price movement using geometric random walk
initial_price = 150.0
daily_returns = np.random.normal(0.0003, 0.018, n_days)

# Add some market cycles and trends
trend = np.sin(np.linspace(0, 4 * np.pi, n_days)) * 0.003
daily_returns = daily_returns + trend

# Generate price series
prices = initial_price * np.cumprod(1 + daily_returns)

# Add a correction period and recovery for visual interest
correction_start = 200
correction_end = 280
prices[correction_start:correction_end] *= np.linspace(1, 0.85, correction_end - correction_start)
prices[correction_end:] *= 0.85

# Recovery rally
recovery_start = 400
prices[recovery_start:] *= np.linspace(1, 1.35, n_days - recovery_start)

# Convert to timestamps for Highcharts (milliseconds since epoch)
timestamps = [int(d.timestamp() * 1000) for d in dates]

# Prepare data as [timestamp, price] pairs
price_data = [[t, round(p, 2)] for t, p in zip(timestamps, prices, strict=True)]

# Chart options for Highcharts Stock with range selector
chart_options = {
    "chart": {
        "type": "area",
        "width": 4800,
        "height": 2700,
        "backgroundColor": "#ffffff",
        "marginBottom": 150,
        "marginLeft": 220,
        "marginRight": 80,
        "marginTop": 160,
        "style": {"fontFamily": "Arial, sans-serif"},
    },
    "title": {
        "text": "area-stock-range · highcharts · pyplots.ai",
        "style": {"fontSize": "64px", "fontWeight": "bold", "color": "#333333"},
        "y": 60,
    },
    "subtitle": {
        "text": "Stock Price with Interactive Range Selector",
        "style": {"fontSize": "36px", "color": "#666666"},
        "y": 120,
    },
    "xAxis": {
        "type": "datetime",
        "title": {"text": "Date", "style": {"fontSize": "44px", "color": "#333333"}, "margin": 25},
        "labels": {"style": {"fontSize": "32px", "color": "#333333"}, "format": "{value:%b %Y}", "y": 40},
        "gridLineWidth": 1,
        "gridLineColor": "rgba(0, 0, 0, 0.1)",
        "lineWidth": 2,
        "lineColor": "#333333",
        "tickWidth": 2,
        "tickColor": "#333333",
        "tickLength": 12,
    },
    "yAxis": {
        "title": {"text": "Price (USD)", "style": {"fontSize": "44px", "color": "#333333"}, "margin": 25},
        "labels": {"style": {"fontSize": "32px", "color": "#333333"}, "format": "${value:.0f}", "x": -15},
        "gridLineWidth": 1,
        "gridLineColor": "rgba(0, 0, 0, 0.1)",
        "lineWidth": 2,
        "lineColor": "#333333",
        "opposite": False,
    },
    "legend": {"enabled": False},
    "tooltip": {
        "shared": True,
        "valueDecimals": 2,
        "valuePrefix": "$",
        "headerFormat": '<span style="font-size: 26px">{point.key:%b %d, %Y}</span><br/>',
        "pointFormat": '<span style="font-size: 24px; color:{series.color}">\u25cf</span> '
        + '<span style="font-size: 24px">{series.name}: <b>${point.y:.2f}</b></span><br/>',
        "style": {"fontSize": "24px"},
    },
    "plotOptions": {
        "area": {
            "fillColor": {
                "linearGradient": {"x1": 0, "y1": 0, "x2": 0, "y2": 1},
                "stops": [[0, "rgba(48, 105, 152, 0.5)"], [1, "rgba(48, 105, 152, 0.05)"]],
            },
            "lineWidth": 4,
            "lineColor": "#306998",
            "marker": {"enabled": False, "radius": 6, "fillColor": "#306998"},
            "states": {"hover": {"lineWidth": 5}},
            "threshold": None,
        }
    },
    "rangeSelector": {
        "enabled": True,
        "selected": 4,  # Default to 1Y view
        "inputEnabled": True,
        "inputStyle": {"fontSize": "24px", "color": "#333333"},
        "inputBoxBorderColor": "#cccccc",
        "inputBoxWidth": 140,
        "inputBoxHeight": 30,
        "labelStyle": {"fontSize": "24px", "color": "#666666"},
        "buttons": [
            {"type": "month", "count": 1, "text": "1M"},
            {"type": "month", "count": 3, "text": "3M"},
            {"type": "month", "count": 6, "text": "6M"},
            {"type": "year", "count": 1, "text": "1Y"},
            {"type": "ytd", "text": "YTD"},
            {"type": "all", "text": "All"},
        ],
        "buttonTheme": {
            "width": 80,
            "height": 36,
            "style": {"fontSize": "24px", "color": "#333333"},
            "states": {"select": {"fill": "#306998", "style": {"color": "#ffffff"}}, "hover": {"fill": "#e6e6e6"}},
        },
        "floating": False,
        "y": 0,
        "height": 50,
    },
    "navigator": {
        "enabled": True,
        "height": 120,
        "margin": 30,
        "series": {"color": "#306998", "fillOpacity": 0.3, "lineWidth": 2},
        "xAxis": {"labels": {"style": {"fontSize": "20px", "color": "#666666"}}},
        "handles": {"width": 20, "height": 30, "backgroundColor": "#306998", "borderColor": "#1a3a5c"},
        "maskFill": "rgba(48, 105, 152, 0.15)",
        "outlineWidth": 2,
        "outlineColor": "#cccccc",
    },
    "scrollbar": {
        "enabled": True,
        "height": 20,
        "barBackgroundColor": "#306998",
        "barBorderRadius": 5,
        "barBorderWidth": 0,
        "buttonBackgroundColor": "#e6e6e6",
        "buttonBorderWidth": 0,
        "rifleColor": "#ffffff",
        "trackBackgroundColor": "#f2f2f2",
        "trackBorderWidth": 1,
        "trackBorderColor": "#cccccc",
    },
    "credits": {"enabled": False},
    "series": [{"type": "area", "name": "Stock Price", "data": price_data, "color": "#306998"}],
}

# Download Highstock JS (required for range selector and navigator)
highstock_url = "https://code.highcharts.com/stock/highstock.js"
with urllib.request.urlopen(highstock_url, timeout=30) as response:
    highstock_js = response.read().decode("utf-8")

# Generate chart options JSON
chart_options_json = json.dumps(chart_options)

# Generate HTML with inline scripts for headless Chrome
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highstock_js}</script>
</head>
<body style="margin:0; background-color: #ffffff;">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            Highcharts.stockChart('container', {chart_options_json});
        }});
    </script>
</body>
</html>"""

# Write temp HTML file
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

# Also save the HTML for interactive viewing
with open("plot.html", "w", encoding="utf-8") as f:
    standalone_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://code.highcharts.com/stock/highstock.js"></script>
</head>
<body style="margin:0; background-color: #ffffff;">
    <div id="container" style="width: 100%; height: 100vh;"></div>
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            Highcharts.stockChart('container', {chart_options_json});
        }});
    </script>
</body>
</html>"""
    f.write(standalone_html)

# Take screenshot with headless Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=5000,3000")  # Larger window to capture full chart

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)  # Wait for chart to render

# Screenshot the chart container for exact dimensions
container = driver.find_element("id", "container")
container.screenshot("plot.png")
driver.quit()

# Clean up temp file
Path(temp_path).unlink()
