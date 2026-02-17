""" pyplots.ai
line-pca-variance-cumulative: Cumulative Explained Variance for PCA Component Selection
Library: highcharts unknown | Python 3.14.3
Quality: 81/100 | Created: 2026-02-17
"""

import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.area import LineSeries
from highcharts_core.options.series.bar import ColumnSeries
from highcharts_core.options.series.scatter import ScatterSeries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - Simulate sensor data (12 features) and compute PCA via eigendecomposition
np.random.seed(42)
n_samples = 200
n_features = 12

# Create correlated features simulating industrial sensor readings
# A few latent factors drive most of the variance
latent = np.random.randn(n_samples, 3)
mixing = np.random.randn(3, n_features)
noise = np.random.randn(n_samples, n_features) * 0.5
X_raw = latent @ mixing + noise

# Standardize
X = (X_raw - X_raw.mean(axis=0)) / X_raw.std(axis=0)

# PCA via eigendecomposition of covariance matrix
cov_matrix = np.cov(X, rowvar=False)
eigenvalues, _ = np.linalg.eigh(cov_matrix)
eigenvalues = eigenvalues[::-1]  # Sort descending

explained_variance_ratio = eigenvalues / eigenvalues.sum()
n_components = list(range(1, n_features + 1))
individual_variance = explained_variance_ratio * 100
cumulative_variance = np.cumsum(individual_variance)

# Find threshold crossings
threshold_90 = next(i for i, v in enumerate(cumulative_variance) if v >= 90) + 1
threshold_95 = next(i for i, v in enumerate(cumulative_variance) if v >= 95) + 1

# Create chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration
chart.options.chart = {
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#ffffff",
    "marginBottom": 300,
    "marginLeft": 250,
    "marginTop": 140,
    "marginRight": 200,
}

# Title
chart.options.title = {
    "text": "PCA Component Selection · line-pca-variance-cumulative · highcharts · pyplots.ai",
    "style": {"fontSize": "44px", "fontWeight": "bold"},
}

# Subtitle
chart.options.subtitle = {
    "text": "Industrial Sensor Data (12 features → explained variance by principal components)",
    "style": {"fontSize": "30px", "color": "#666666"},
}

# X-axis
chart.options.x_axis = {
    "title": {"text": "Number of Components", "style": {"fontSize": "38px"}, "margin": 30},
    "labels": {"style": {"fontSize": "30px"}, "y": 40},
    "categories": [str(n) for n in n_components],
    "tickInterval": 1,
}

# Y-axis
chart.options.y_axis = {
    "title": {"text": "Explained Variance (%)", "style": {"fontSize": "38px"}, "margin": 40},
    "labels": {"style": {"fontSize": "30px"}, "x": -15},
    "min": 0,
    "max": 105,
    "tickInterval": 10,
    "gridLineWidth": 1,
    "gridLineColor": "#e8e8e8",
    "plotLines": [
        {
            "value": 90,
            "color": "#E67E22",
            "width": 3,
            "dashStyle": "Dash",
            "label": {
                "text": "90% Threshold",
                "align": "right",
                "style": {"fontSize": "26px", "color": "#E67E22", "fontWeight": "bold"},
                "x": -20,
                "y": -12,
            },
            "zIndex": 4,
        },
        {
            "value": 95,
            "color": "#8E44AD",
            "width": 3,
            "dashStyle": "Dash",
            "label": {
                "text": "95% Threshold",
                "align": "right",
                "style": {"fontSize": "26px", "color": "#8E44AD", "fontWeight": "bold"},
                "x": -20,
                "y": -12,
            },
            "zIndex": 4,
        },
    ],
}

# Legend
chart.options.legend = {
    "enabled": True,
    "itemStyle": {"fontSize": "28px", "fontWeight": "normal"},
    "align": "right",
    "verticalAlign": "top",
    "layout": "vertical",
    "x": -40,
    "y": 100,
    "symbolWidth": 40,
    "symbolHeight": 18,
    "itemMarginBottom": 12,
}

# Plot options
chart.options.plot_options = {
    "line": {"lineWidth": 5, "marker": {"enabled": True, "radius": 12, "symbol": "circle"}},
    "column": {"borderWidth": 0, "pointPadding": 0.15, "groupPadding": 0.1},
}

# Tooltip
chart.options.tooltip = {
    "shared": True,
    "style": {"fontSize": "24px"},
    "headerFormat": "<b>Component {point.key}</b><br/>",
    "pointFormat": "{series.name}: <b>{point.y:.1f}%</b><br/>",
}

# Individual variance as column series (subtle background)
col_series = ColumnSeries()
col_series.name = "Individual Variance"
col_series.data = [round(float(v), 2) for v in individual_variance]
col_series.color = "rgba(48, 105, 152, 0.3)"
chart.add_series(col_series)

# Cumulative variance as line series (main focus)
line_series = LineSeries()
line_series.name = "Cumulative Variance"
line_series.data = [round(float(v), 2) for v in cumulative_variance]
line_series.color = "#306998"
line_series.marker = {"fillColor": "#306998", "lineWidth": 3, "lineColor": "#ffffff"}
chart.add_series(line_series)

# Mark 90% threshold point
marker_90 = ScatterSeries()
marker_90.name = f"90% at {threshold_90} components"
marker_90.data = [[threshold_90 - 1, round(float(cumulative_variance[threshold_90 - 1]), 2)]]
marker_90.color = "#E67E22"
marker_90.marker = {"radius": 18, "symbol": "diamond", "fillColor": "#E67E22", "lineWidth": 3, "lineColor": "#ffffff"}
chart.add_series(marker_90)

# Mark 95% threshold point
marker_95 = ScatterSeries()
marker_95.name = f"95% at {threshold_95} components"
marker_95.data = [[threshold_95 - 1, round(float(cumulative_variance[threshold_95 - 1]), 2)]]
marker_95.color = "#8E44AD"
marker_95.marker = {"radius": 18, "symbol": "diamond", "fillColor": "#8E44AD", "lineWidth": 3, "lineColor": "#ffffff"}
chart.add_series(marker_95)

# Download Highcharts JS
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

# Write temp HTML and take screenshot
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

# Save interactive HTML
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
