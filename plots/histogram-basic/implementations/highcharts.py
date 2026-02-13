"""pyplots.ai
histogram-basic: Basic Histogram
Library: highcharts 1.10.3 | Python 3.14.0
Quality: /100 | Updated: 2026-02-13
"""

import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.bar import ColumnSeries
from highcharts_core.options.series.histogram import HistogramSeries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data — university exam scores with realistic slight right skew
np.random.seed(42)
exam_scores = np.concatenate(
    [np.random.normal(loc=72, scale=12, size=400), np.random.normal(loc=88, scale=5, size=100)]
)
exam_scores = np.clip(exam_scores, 0, 100)

# Create chart using native Highcharts histogram series
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart settings
chart.options.chart = {
    "type": "column",
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#ffffff",
    "marginBottom": 260,
    "marginLeft": 200,
    "marginRight": 120,
}

# Title
chart.options.title = {
    "text": "Exam Score Distribution \u00b7 histogram-basic \u00b7 highcharts \u00b7 pyplots.ai",
    "style": {"fontSize": "64px", "fontWeight": "bold", "color": "#333333"},
}

# Subtitle
chart.options.subtitle = {
    "text": "500 students \u2014 Introduction to Statistics, Fall 2024",
    "style": {"fontSize": "40px", "color": "#666666"},
}

# X-axis
chart.options.x_axis = [
    {
        "title": {"text": "Exam Score (points)", "style": {"fontSize": "44px", "color": "#444444"}},
        "labels": {"style": {"fontSize": "36px", "color": "#555555"}},
        "tickInterval": 5,
        "alignTicks": False,
    },
    {"title": {"text": ""}, "opposite": True, "visible": False},
]

# Y-axis
chart.options.y_axis = [
    {
        "title": {"text": "Number of Students", "style": {"fontSize": "44px", "color": "#444444"}},
        "labels": {"style": {"fontSize": "36px", "color": "#555555"}},
        "min": 0,
        "tickInterval": 10,
        "gridLineColor": "#e8e8e8",
        "gridLineWidth": 1,
    },
    {"title": {"text": ""}, "opposite": True, "visible": False},
]

# Plot options for histogram appearance (no gaps between bars)
chart.options.plot_options = {
    "histogram": {
        "pointPadding": 0,
        "groupPadding": 0,
        "borderWidth": 2,
        "borderColor": "#1a4a6e",
        "binsNumber": 20,
        "tooltip": {
            "headerFormat": "",
            "pointFormat": "<b>{point.x:.0f} \u2013 {point.x2:.0f}</b><br/>Students: {point.y}",
        },
    }
}

# Legend (hide for single series)
chart.options.legend = {"enabled": False}

# Credits
chart.options.credits = {"enabled": False}

# Base data series (hidden — provides data for histogram)
base_series = ColumnSeries()
base_series.name = "Raw Scores"
base_series.data = [round(float(v), 1) for v in exam_scores]
base_series.id = "exam-data"
base_series.visible = False
base_series.show_in_legend = False

# Histogram series derived from base data
hist_series = HistogramSeries()
hist_series.name = "Frequency"
hist_series.base_series = "exam-data"
hist_series.color = "#306998"
hist_series.x_axis = 0
hist_series.y_axis = 0
hist_series.bins_number = 20

chart.add_series(base_series)
chart.add_series(hist_series)

# Download Highcharts JS and histogram module
highcharts_url = "https://code.highcharts.com/highcharts.js"
with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

histogram_module_url = "https://code.highcharts.com/modules/histogram-bellcurve.js"
with urllib.request.urlopen(histogram_module_url, timeout=30) as response:
    histogram_module_js = response.read().decode("utf-8")

# Generate HTML with inline scripts
html_str = chart.to_js_literal()
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <script>{histogram_module_js}</script>
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

# Save HTML for interactive version
Path("plot.html").write_text(html_content, encoding="utf-8")

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
