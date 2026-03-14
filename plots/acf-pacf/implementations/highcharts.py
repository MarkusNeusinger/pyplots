"""pyplots.ai
acf-pacf: Autocorrelation and Partial Autocorrelation (ACF/PACF) Plot
Library: highcharts | Python 3.13
Quality: pending | Created: 2026-03-14
"""

import re
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
from statsmodels.tsa.stattools import acf, pacf


# Data - Generate an AR(2) process for clear ACF/PACF patterns
np.random.seed(42)
n_obs = 200
noise = np.random.normal(0, 1, n_obs)
series = np.zeros(n_obs)
series[0] = noise[0]
series[1] = noise[1]
for i in range(2, n_obs):
    series[i] = 0.6 * series[i - 1] - 0.3 * series[i - 2] + noise[i]

# Compute ACF and PACF
n_lags = 35
acf_values = acf(series, nlags=n_lags, fft=True)
pacf_values = pacf(series, nlags=n_lags, method="ywm")
confidence_bound = 1.96 / np.sqrt(n_obs)
lags = list(range(n_lags + 1))
pacf_lags = list(range(1, n_lags + 1))

# Build chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

chart.options.chart = {
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#ffffff",
    "marginTop": 120,
    "marginBottom": 320,
    "marginLeft": 280,
    "marginRight": 120,
    "style": {"fontFamily": "Arial, Helvetica, sans-serif"},
}

# Title
chart.options.title = {
    "text": "acf-pacf \u00b7 highcharts \u00b7 pyplots.ai",
    "style": {"fontSize": "52px", "fontWeight": "bold", "color": "#2c3e50"},
    "margin": 40,
}

chart.options.subtitle = {
    "text": "AR(2) Process \u2014 Exponential ACF Decay with PACF Cutoff at Lag 2",
    "style": {"fontSize": "30px", "color": "#7f8c8d", "fontWeight": "normal"},
}

# Two y-axes stacked vertically
chart.options.y_axis = [
    {
        "title": {"text": "ACF", "style": {"fontSize": "34px", "color": "#306998", "fontWeight": "bold"}, "margin": 20},
        "labels": {"style": {"fontSize": "24px", "color": "#555555"}, "format": "{value:.1f}"},
        "top": "4%",
        "height": "42%",
        "offset": 0,
        "min": -0.5,
        "max": 1.05,
        "endOnTick": False,
        "tickInterval": 0.2,
        "gridLineColor": "#eeeeee",
        "gridLineWidth": 1,
        "plotLines": [
            {"value": 0, "color": "#999999", "width": 2, "zIndex": 3},
            {"value": confidence_bound, "color": "#e74c3c", "width": 2, "dashStyle": "Dash", "zIndex": 3},
            {"value": -confidence_bound, "color": "#e74c3c", "width": 2, "dashStyle": "Dash", "zIndex": 3},
        ],
    },
    {
        "title": {
            "text": "PACF",
            "style": {"fontSize": "34px", "color": "#306998", "fontWeight": "bold"},
            "margin": 20,
        },
        "labels": {"style": {"fontSize": "24px", "color": "#555555"}, "format": "{value:.1f}"},
        "top": "54%",
        "height": "42%",
        "offset": 0,
        "min": -0.5,
        "max": 0.6,
        "endOnTick": False,
        "startOnTick": False,
        "tickInterval": 0.2,
        "gridLineColor": "#eeeeee",
        "gridLineWidth": 1,
        "plotLines": [
            {"value": 0, "color": "#999999", "width": 2, "zIndex": 3},
            {"value": confidence_bound, "color": "#e74c3c", "width": 2, "dashStyle": "Dash", "zIndex": 3},
            {"value": -confidence_bound, "color": "#e74c3c", "width": 2, "dashStyle": "Dash", "zIndex": 3},
        ],
    },
]

# X-axes: top panel hides labels, bottom panel shows Lag labels
chart.options.x_axis = [
    {
        "title": {"text": None},
        "labels": {"enabled": False},
        "lineColor": "#cccccc",
        "lineWidth": 1,
        "tickInterval": 5,
        "min": -0.5,
        "max": n_lags + 0.5,
    },
    {
        "title": {"text": "Lag", "style": {"fontSize": "36px", "color": "#555555"}, "margin": 25},
        "labels": {"style": {"fontSize": "28px", "color": "#555555"}},
        "lineColor": "#cccccc",
        "lineWidth": 1,
        "tickInterval": 5,
        "min": -0.5,
        "max": n_lags + 0.5,
    },
]

# Color bars based on significance
acf_data = []
for i, val in enumerate(acf_values):
    color = "#e74c3c" if abs(val) > confidence_bound and i > 0 else "#306998"
    if i == 0:
        color = "#1a4971"
    acf_data.append({"x": i, "y": round(float(val), 4), "color": color})

pacf_data = []
for i, val in enumerate(pacf_values[1:], start=1):
    color = "#e74c3c" if abs(val) > confidence_bound else "#306998"
    pacf_data.append({"x": i, "y": round(float(val), 4), "color": color})

# ACF series (top panel, yAxis 0, xAxis 0)
acf_series = ColumnSeries.from_dict(
    {
        "data": acf_data,
        "name": "ACF",
        "type": "column",
        "yAxis": 0,
        "xAxis": 0,
        "pointWidth": 22,
        "borderWidth": 0,
        "groupPadding": 0,
        "pointPadding": 0,
    }
)
chart.add_series(acf_series)

# PACF series (bottom panel, yAxis 1, xAxis 1)
pacf_series = ColumnSeries.from_dict(
    {
        "data": pacf_data,
        "name": "PACF",
        "type": "column",
        "yAxis": 1,
        "xAxis": 1,
        "pointWidth": 22,
        "borderWidth": 0,
        "groupPadding": 0,
        "pointPadding": 0,
    }
)
chart.add_series(pacf_series)

# Tooltip
chart.options.tooltip = {
    "headerFormat": '<span style="font-size:22px">Lag {point.x}</span><br/>',
    "pointFormat": '<span style="font-size:20px">{series.name}: <b>{point.y:.4f}</b></span>',
    "backgroundColor": "rgba(255, 255, 255, 0.95)",
    "borderColor": "#306998",
    "borderRadius": 8,
    "borderWidth": 2,
    "style": {"fontSize": "20px"},
}

# Plot options
chart.options.plot_options = {"column": {"borderRadius": 2}}

# Disable legend and credits
chart.options.legend = {"enabled": False}
chart.options.credits = {"enabled": False}

# Download Highcharts JS (try multiple CDNs, fall back to local npm)
highcharts_js = None
for url in ["https://code.highcharts.com/highcharts.js", "https://cdn.jsdelivr.net/npm/highcharts@11/highcharts.js"]:
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            highcharts_js = response.read().decode("utf-8")
            break
    except Exception:
        continue
if highcharts_js is None:
    local_paths = [
        Path(__file__).resolve().parent.parent.parent.parent / "node_modules" / "highcharts" / "highcharts.js",
        Path("node_modules/highcharts/highcharts.js"),
    ]
    for p in local_paths:
        if p.exists():
            highcharts_js = p.read_text(encoding="utf-8")
            break
if highcharts_js is None:
    raise RuntimeError("Failed to download Highcharts JS from CDN or find local copy")

# Generate JS and fix format strings
chart_js = chart.to_js_literal()
chart_js = re.sub(r"format: (\{[^}]+\})", r"format: '\1'", chart_js)

html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
</head>
<body style="margin:0;">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>{chart_js}</script>
</body>
</html>"""

# Write temp HTML
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

# Save HTML for interactive viewing (uses CDN for portability)
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>acf-pacf \u00b7 highcharts \u00b7 pyplots.ai</title>
    <script src="https://code.highcharts.com/highcharts.js"></script>
    <style>
        body {{ margin: 0; padding: 20px; font-family: sans-serif; background: #fff; }}
        #container {{ width: 100%; height: 90vh; min-height: 600px; }}
    </style>
</head>
<body>
    <div id="container"></div>
    <script>{chart_js}</script>
</body>
</html>""")

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

# Clean up
Path(temp_path).unlink()
