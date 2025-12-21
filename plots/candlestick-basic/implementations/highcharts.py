""" pyplots.ai
candlestick-basic: Basic Candlestick Chart
Library: highcharts 1.10.3 | Python 3.13.11
Quality: 89/100 | Created: 2025-12-14
"""

import json
import tempfile
import time
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - 30 trading days of simulated stock prices
np.random.seed(42)

# Start price and generate OHLC data
start_price = 150.0
n_days = 30

# Generate realistic stock movements
opens = [start_price]
highs = []
lows = []
closes = []

for i in range(n_days):
    open_price = opens[i] if i == 0 else closes[i - 1] + np.random.randn() * 0.5
    if i > 0:
        opens.append(open_price)

    # Daily volatility
    daily_range = abs(np.random.randn() * 2) + 1
    direction = np.random.choice([-1, 1], p=[0.45, 0.55])  # Slight bullish bias

    close_price = open_price + direction * np.random.rand() * daily_range
    high_price = max(open_price, close_price) + abs(np.random.randn() * 0.5)
    low_price = min(open_price, close_price) - abs(np.random.randn() * 0.5)

    highs.append(round(high_price, 2))
    lows.append(round(low_price, 2))
    closes.append(round(close_price, 2))

opens = [round(o, 2) for o in opens]

# Generate dates (trading days, skip weekends)
start_date = datetime(2024, 10, 1)
dates = []
current_date = start_date
while len(dates) < n_days:
    if current_date.weekday() < 5:  # Monday to Friday
        dates.append(current_date)
    current_date += timedelta(days=1)

# Format data for Highcharts: [timestamp, open, high, low, close]
ohlc_data = []
for i in range(n_days):
    timestamp = int(dates[i].timestamp() * 1000)  # JavaScript timestamp in ms
    ohlc_data.append([timestamp, opens[i], highs[i], lows[i], closes[i]])

# Chart options for Highcharts Stock candlestick
chart_options = {
    "chart": {
        "type": "candlestick",
        "width": 4800,
        "height": 2700,
        "backgroundColor": "#ffffff",
        "marginBottom": 250,
        "marginLeft": 200,
        "marginRight": 100,
        "spacingTop": 80,
        "style": {"fontFamily": "Arial, sans-serif"},
    },
    "title": {
        "text": "Stock Price Movement · candlestick-basic · highcharts · pyplots.ai",
        "style": {"fontSize": "64px", "fontWeight": "bold"},
    },
    "xAxis": {
        "type": "datetime",
        "title": {"text": "Date", "style": {"fontSize": "48px"}, "margin": 40},
        "labels": {"style": {"fontSize": "32px"}, "format": "{value:%b %d}", "y": 40},
        "gridLineWidth": 1,
        "gridLineColor": "#e0e0e0",
        "gridLineDashStyle": "Dash",
        "lineWidth": 2,
        "tickWidth": 2,
    },
    "yAxis": {
        "title": {"text": "Price ($)", "style": {"fontSize": "48px"}, "margin": 40},
        "labels": {"style": {"fontSize": "32px"}, "format": "${value:.0f}", "x": -15},
        "gridLineWidth": 1,
        "gridLineColor": "#e0e0e0",
        "gridLineDashStyle": "Dash",
    },
    "legend": {"enabled": False},
    "tooltip": {
        "split": False,
        "style": {"fontSize": "24px"},
        "headerFormat": "<b>{point.x:%b %d, %Y}</b><br/>",
        "pointFormat": "Open: ${point.open:.2f}<br/>"
        + "High: ${point.high:.2f}<br/>"
        + "Low: ${point.low:.2f}<br/>"
        + "Close: ${point.close:.2f}",
    },
    "plotOptions": {
        "candlestick": {
            "color": "#DC2626",  # Red for bearish (close < open)
            "upColor": "#22C55E",  # Green for bullish (close > open)
            "lineColor": "#DC2626",  # Wick color for bearish
            "upLineColor": "#22C55E",  # Wick color for bullish
            "lineWidth": 3,  # Wick line width
            "pointWidth": 60,  # Candle body width
        }
    },
    "rangeSelector": {"enabled": False},
    "navigator": {"enabled": False},
    "scrollbar": {"enabled": False},
    "series": [{"type": "candlestick", "name": "Stock Price", "data": ohlc_data}],
}

# Download Highstock JS (includes candlestick support)
highstock_url = "https://code.highcharts.com/stock/highstock.js"
with urllib.request.urlopen(highstock_url, timeout=30) as response:
    highstock_js = response.read().decode("utf-8")

# Generate chart options JSON
chart_options_json = json.dumps(chart_options)

# Generate HTML with inline scripts
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highstock_js}</script>
</head>
<body style="margin:0;">
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
    f.write(html_content)

# Take screenshot with headless Chrome
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

# Clean up temp file
Path(temp_path).unlink()
