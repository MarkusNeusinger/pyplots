"""pyplots.ai
timeseries-decomposition: Time Series Decomposition Plot
Library: highcharts | Python 3.13
Quality: pending | Created: 2025-12-31
"""

import base64
import json
import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from statsmodels.tsa.seasonal import seasonal_decompose


# Data - Monthly airline passengers (classic time series dataset)
np.random.seed(42)
dates = pd.date_range(start="2018-01-01", periods=120, freq="MS")  # 10 years monthly

# Generate realistic airline passenger data with trend, seasonality, and noise
trend = np.linspace(100, 300, 120)  # Upward trend over time
seasonal = 40 * np.sin(2 * np.pi * np.arange(120) / 12)  # Annual seasonality
noise = np.random.normal(0, 15, 120)  # Random noise
passengers = trend + seasonal + noise

# Create time series and decompose
ts = pd.Series(passengers, index=dates)
decomposition = seasonal_decompose(ts, model="additive", period=12)

# Extract components
observed = decomposition.observed
trend_comp = decomposition.trend
seasonal_comp = decomposition.seasonal
residual = decomposition.resid

# Convert to lists for Highcharts (handle NaN values in trend/residual)
timestamps = [int(d.timestamp() * 1000) for d in dates]
observed_data = [[t, float(v)] for t, v in zip(timestamps, observed, strict=True)]
trend_data = [[t, float(v) if not np.isnan(v) else None] for t, v in zip(timestamps, trend_comp, strict=True)]
seasonal_data = [[t, float(v)] for t, v in zip(timestamps, seasonal_comp, strict=True)]
residual_data = [[t, float(v) if not np.isnan(v) else None] for t, v in zip(timestamps, residual, strict=True)]

# Colors
primary_blue = "#306998"
secondary_yellow = "#FFD43B"
purple = "#9467BD"
teal = "#17BECF"

# Chart dimensions - single output image
chart_width = 4800
total_height = 2700
subplot_height = total_height // 4  # 675px each

# Download Highcharts JS
highcharts_url = "https://code.highcharts.com/highcharts.js"
with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

# Build chart configurations as dictionaries (native Python, not using highcharts-core)
chart_configs = []

# Chart 1: Observed (Original) - with main title
chart_configs.append(
    {
        "container": "container1",
        "options": {
            "chart": {
                "type": "line",
                "width": chart_width,
                "height": subplot_height,
                "backgroundColor": "#ffffff",
                "marginLeft": 150,
                "marginRight": 100,
                "marginTop": 80,
                "marginBottom": 50,
            },
            "title": {
                "text": "timeseries-decomposition · highcharts · pyplots.ai",
                "style": {"fontSize": "36px", "fontWeight": "bold"},
            },
            "subtitle": {"text": "Original Series", "style": {"fontSize": "28px"}},
            "xAxis": {
                "type": "datetime",
                "labels": {"style": {"fontSize": "20px"}, "format": "{value:%Y-%m}"},
                "title": {"text": None},
                "gridLineWidth": 1,
                "gridLineColor": "rgba(0,0,0,0.1)",
                "lineWidth": 2,
            },
            "yAxis": {
                "title": {"text": "Passengers (thousands)", "style": {"fontSize": "24px", "fontWeight": "bold"}},
                "labels": {"style": {"fontSize": "20px"}},
                "gridLineWidth": 1,
                "gridLineColor": "rgba(0,0,0,0.15)",
                "lineWidth": 2,
            },
            "legend": {"enabled": False},
            "credits": {"enabled": False},
            "series": [
                {
                    "name": "Observed",
                    "data": observed_data,
                    "color": primary_blue,
                    "lineWidth": 4,
                    "marker": {"enabled": False},
                }
            ],
        },
    }
)

# Chart 2: Trend
chart_configs.append(
    {
        "container": "container2",
        "options": {
            "chart": {
                "type": "line",
                "width": chart_width,
                "height": subplot_height,
                "backgroundColor": "#ffffff",
                "marginLeft": 150,
                "marginRight": 100,
                "marginTop": 50,
                "marginBottom": 50,
            },
            "title": {"text": "Trend Component", "style": {"fontSize": "28px", "fontWeight": "bold"}},
            "xAxis": {
                "type": "datetime",
                "labels": {"style": {"fontSize": "20px"}, "format": "{value:%Y-%m}"},
                "title": {"text": None},
                "gridLineWidth": 1,
                "gridLineColor": "rgba(0,0,0,0.1)",
                "lineWidth": 2,
            },
            "yAxis": {
                "title": {"text": "Trend", "style": {"fontSize": "24px", "fontWeight": "bold"}},
                "labels": {"style": {"fontSize": "20px"}},
                "gridLineWidth": 1,
                "gridLineColor": "rgba(0,0,0,0.15)",
                "lineWidth": 2,
            },
            "legend": {"enabled": False},
            "credits": {"enabled": False},
            "series": [
                {
                    "name": "Trend",
                    "data": trend_data,
                    "color": secondary_yellow,
                    "lineWidth": 5,
                    "marker": {"enabled": False},
                }
            ],
        },
    }
)

# Chart 3: Seasonal
chart_configs.append(
    {
        "container": "container3",
        "options": {
            "chart": {
                "type": "line",
                "width": chart_width,
                "height": subplot_height,
                "backgroundColor": "#ffffff",
                "marginLeft": 150,
                "marginRight": 100,
                "marginTop": 50,
                "marginBottom": 50,
            },
            "title": {"text": "Seasonal Component", "style": {"fontSize": "28px", "fontWeight": "bold"}},
            "xAxis": {
                "type": "datetime",
                "labels": {"style": {"fontSize": "20px"}, "format": "{value:%Y-%m}"},
                "title": {"text": None},
                "gridLineWidth": 1,
                "gridLineColor": "rgba(0,0,0,0.1)",
                "lineWidth": 2,
            },
            "yAxis": {
                "title": {"text": "Seasonal", "style": {"fontSize": "24px", "fontWeight": "bold"}},
                "labels": {"style": {"fontSize": "20px"}},
                "gridLineWidth": 1,
                "gridLineColor": "rgba(0,0,0,0.15)",
                "lineWidth": 2,
            },
            "legend": {"enabled": False},
            "credits": {"enabled": False},
            "series": [
                {
                    "name": "Seasonal",
                    "data": seasonal_data,
                    "color": purple,
                    "lineWidth": 4,
                    "marker": {"enabled": False},
                }
            ],
        },
    }
)

# Chart 4: Residual - with x-axis title
chart_configs.append(
    {
        "container": "container4",
        "options": {
            "chart": {
                "type": "line",
                "width": chart_width,
                "height": subplot_height,
                "backgroundColor": "#ffffff",
                "marginLeft": 150,
                "marginRight": 100,
                "marginTop": 50,
                "marginBottom": 80,
            },
            "title": {"text": "Residual Component", "style": {"fontSize": "28px", "fontWeight": "bold"}},
            "xAxis": {
                "type": "datetime",
                "labels": {"style": {"fontSize": "20px"}, "format": "{value:%Y-%m}"},
                "title": {"text": "Date", "style": {"fontSize": "24px", "fontWeight": "bold"}},
                "gridLineWidth": 1,
                "gridLineColor": "rgba(0,0,0,0.1)",
                "lineWidth": 2,
            },
            "yAxis": {
                "title": {"text": "Residual", "style": {"fontSize": "24px", "fontWeight": "bold"}},
                "labels": {"style": {"fontSize": "20px"}},
                "gridLineWidth": 1,
                "gridLineColor": "rgba(0,0,0,0.15)",
                "lineWidth": 2,
            },
            "legend": {"enabled": False},
            "credits": {"enabled": False},
            "series": [
                {"name": "Residual", "data": residual_data, "color": teal, "lineWidth": 3, "marker": {"enabled": False}}
            ],
        },
    }
)

# Build HTML with all 4 charts stacked vertically
containers_html = "\n".join(
    [
        f'<div id="{cfg["container"]}" style="width: {chart_width}px; height: {subplot_height}px;"></div>'
        for cfg in chart_configs
    ]
)

# Build direct JavaScript calls (no DOMContentLoaded wrapper)
scripts_js = "\n".join(
    [f"Highcharts.chart('{cfg['container']}', {json.dumps(cfg['options'])});" for cfg in chart_configs]
)

html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html, body {{ width: {chart_width}px; height: {total_height}px; background-color: #ffffff; overflow: hidden; }}
    </style>
</head>
<body>
    {containers_html}
    <script>
    {scripts_js}
    </script>
</body>
</html>"""

# Save and screenshot using CDP for full page capture
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--hide-scrollbars")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(6)  # Wait for all charts to render

# Use CDP to capture full page screenshot at exact dimensions
screenshot_config = {
    "captureBeyondViewport": True,
    "clip": {"x": 0, "y": 0, "width": chart_width, "height": total_height, "scale": 1},
}
result = driver.execute_cdp_cmd("Page.captureScreenshot", screenshot_config)
screenshot_data = base64.b64decode(result["data"])

with open("plot.png", "wb") as f:
    f.write(screenshot_data)

driver.quit()
Path(temp_path).unlink()

# Also save interactive HTML
with open("plot.html", "w", encoding="utf-8") as f:
    html_portable = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://code.highcharts.com/highcharts.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ background-color: #ffffff; }}
    </style>
</head>
<body>
    {containers_html}
    <script>
    {scripts_js}
    </script>
</body>
</html>"""
    f.write(html_portable)
