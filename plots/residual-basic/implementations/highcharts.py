"""pyplots.ai
residual-basic: Residual Plot
Library: highcharts | Python 3.13
Quality: pending | Created: 2025-12-25
"""

import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.area import LineSeries
from highcharts_core.options.series.scatter import ScatterSeries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - Simulate linear regression residuals
np.random.seed(42)
n_points = 120

# Generate fitted values (predictions from model)
fitted = np.linspace(10, 90, n_points) + np.random.randn(n_points) * 5

# Generate residuals with slight heteroscedasticity to show diagnostic value
# Residuals centered at zero with some variation
base_residuals = np.random.randn(n_points) * 8
# Add slight pattern for realism (mild heteroscedasticity)
residuals = base_residuals * (0.8 + 0.004 * fitted)
# Add a few outliers
residuals[15] = 28
residuals[85] = -25
residuals[100] = 22

# Sort by fitted values for cleaner plotting
sort_idx = np.argsort(fitted)
fitted = fitted[sort_idx]
residuals = residuals[sort_idx]

# Create chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration
chart.options.chart = {
    "type": "scatter",
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#ffffff",
    "marginBottom": 280,
    "marginLeft": 220,
    "marginTop": 180,
    "marginRight": 120,
}

# Title
chart.options.title = {
    "text": "residual-basic \u00b7 highcharts \u00b7 pyplots.ai",
    "style": {"fontSize": "48px", "fontWeight": "bold"},
}

# Subtitle
chart.options.subtitle = {
    "text": "Residuals from Linear Regression Model",
    "style": {"fontSize": "32px", "color": "#666666"},
}

# X-axis
chart.options.x_axis = {
    "title": {"text": "Fitted Values", "style": {"fontSize": "36px", "fontWeight": "bold"}, "margin": 40},
    "labels": {"style": {"fontSize": "28px"}, "y": 40},
    "gridLineWidth": 1,
    "gridLineColor": "#e0e0e0",
    "lineWidth": 2,
    "lineColor": "#333333",
    "tickWidth": 2,
    "tickLength": 10,
}

# Y-axis with symmetric range around zero
y_max = max(abs(residuals.min()), abs(residuals.max())) * 1.15
chart.options.y_axis = {
    "title": {"text": "Residuals", "style": {"fontSize": "36px", "fontWeight": "bold"}, "margin": 30},
    "labels": {"style": {"fontSize": "28px"}},
    "min": -y_max,
    "max": y_max,
    "gridLineWidth": 1,
    "gridLineColor": "#e0e0e0",
    "lineWidth": 2,
    "lineColor": "#333333",
    "plotLines": [
        {
            "value": 0,
            "color": "#306998",
            "width": 4,
            "zIndex": 3,
            "label": {
                "text": "Zero Reference",
                "align": "right",
                "style": {"fontSize": "24px", "color": "#306998", "fontWeight": "bold"},
                "x": -15,
                "y": -10,
            },
        }
    ],
}

# Legend
chart.options.legend = {
    "enabled": True,
    "align": "right",
    "verticalAlign": "top",
    "layout": "vertical",
    "x": -50,
    "y": 80,
    "itemStyle": {"fontSize": "28px"},
}

# Plot options
chart.options.plot_options = {
    "scatter": {
        "marker": {
            "radius": 14,
            "symbol": "circle",
            "fillColor": "rgba(48, 105, 152, 0.6)",
            "lineWidth": 2,
            "lineColor": "#306998",
        },
        "states": {"hover": {"marker": {"radius": 18}}},
    }
}

# Scatter series for residuals
scatter_series = ScatterSeries()
scatter_series.data = [[float(x), float(y)] for x, y in zip(fitted, residuals, strict=False)]
scatter_series.name = "Residuals"
scatter_series.color = "rgba(48, 105, 152, 0.6)"
scatter_series.marker = {
    "radius": 14,
    "symbol": "circle",
    "fillColor": "rgba(48, 105, 152, 0.6)",
    "lineWidth": 2,
    "lineColor": "#306998",
}

chart.add_series(scatter_series)

# Add LOWESS-like smoothed trend line (simple moving average as approximation)
window = 15
smoothed_residuals = np.convolve(residuals, np.ones(window) / window, mode="valid")
smoothed_fitted = fitted[(window - 1) // 2 : -(window - 1) // 2]

# Adjust lengths to match
if len(smoothed_fitted) > len(smoothed_residuals):
    smoothed_fitted = smoothed_fitted[: len(smoothed_residuals)]

trend_series = LineSeries()
trend_series.data = [[float(x), float(y)] for x, y in zip(smoothed_fitted, smoothed_residuals, strict=False)]
trend_series.name = "Trend (Smoothed)"
trend_series.color = "#FFD43B"
trend_series.line_width = 5
trend_series.marker = {"enabled": False}
trend_series.type = "spline"

chart.add_series(trend_series)

# Credits
chart.options.credits = {"enabled": False}

# Download Highcharts JS
highcharts_url = "https://code.highcharts.com/highcharts.js"
with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

# Generate HTML
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

# Save HTML for interactive version
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Take screenshot with Selenium
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

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
