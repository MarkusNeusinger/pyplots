""" pyplots.ai
pp-basic: Probability-Probability (P-P) Plot
Library: highcharts unknown | Python 3.14.3
Quality: 79/100 | Created: 2026-03-15
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
from scipy.stats import norm
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - slightly skewed sample to show P-P plot deviation from diagonal
np.random.seed(42)
n = 200
sample = np.concatenate([np.random.normal(0, 1, 160), np.random.exponential(0.8, 40)])
np.random.shuffle(sample)

# Compute P-P values
sample_sorted = np.sort(sample)
mu, sigma = norm.fit(sample)
empirical_cdf = (np.arange(1, n + 1)) / (n + 1)
theoretical_cdf = norm.cdf(sample_sorted, loc=mu, scale=sigma)

# Chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

chart.options.chart = {
    "type": "scatter",
    "width": 3600,
    "height": 3600,
    "backgroundColor": "#ffffff",
    "marginBottom": 200,
    "spacingBottom": 30,
}

chart.options.title = {
    "text": "pp-basic \u00b7 highcharts \u00b7 pyplots.ai",
    "style": {"fontSize": "68px", "fontWeight": "bold"},
}

chart.options.x_axis = {
    "title": {"text": "Theoretical CDF (Normal)", "style": {"fontSize": "48px"}},
    "labels": {"style": {"fontSize": "36px"}},
    "gridLineWidth": 1,
    "gridLineColor": "rgba(0, 0, 0, 0.15)",
    "gridLineDashStyle": "Dash",
    "min": 0,
    "max": 1,
    "tickInterval": 0.2,
}
chart.options.y_axis = {
    "title": {"text": "Empirical CDF", "style": {"fontSize": "48px"}},
    "labels": {"style": {"fontSize": "36px"}},
    "gridLineWidth": 1,
    "gridLineColor": "rgba(0, 0, 0, 0.15)",
    "gridLineDashStyle": "Dash",
    "min": 0,
    "max": 1,
    "tickInterval": 0.2,
}

chart.options.legend = {
    "enabled": True,
    "itemStyle": {"fontSize": "36px"},
    "align": "right",
    "verticalAlign": "top",
    "layout": "vertical",
    "x": -50,
    "y": 100,
}
chart.options.credits = {"enabled": False}

# Reference line (perfect fit diagonal)
line_series = LineSeries()
line_series.data = [[0.0, 0.0], [1.0, 1.0]]
line_series.name = "Perfect Fit (y=x)"
line_series.color = "#FFD43B"
line_series.line_width = 6
line_series.marker = {"enabled": False}
line_series.enable_mouse_tracking = False
line_series.dash_style = "Dash"

chart.add_series(line_series)

# P-P scatter points
scatter_series = ScatterSeries()
scatter_series.data = [[float(t), float(e)] for t, e in zip(theoretical_cdf, empirical_cdf, strict=True)]
scatter_series.name = "P-P Points (N=200)"
scatter_series.color = "rgba(48, 105, 152, 0.7)"
scatter_series.marker = {"radius": 14, "symbol": "circle"}

chart.add_series(scatter_series)

# Load Highcharts JS for inline embedding
highcharts_js_path = Path(__file__).resolve().parents[3] / "node_modules" / "highcharts" / "highcharts.js"
if highcharts_js_path.exists():
    highcharts_js = highcharts_js_path.read_text(encoding="utf-8")
else:
    highcharts_url = "https://code.highcharts.com/highcharts.js"
    req = urllib.request.Request(highcharts_url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as response:
        highcharts_js = response.read().decode("utf-8")

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

with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=3600,3700")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)

container = driver.find_element("id", "container")
container.screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()

# Save interactive HTML
with open("plot.html", "w", encoding="utf-8") as f:
    interactive_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://code.highcharts.com/highcharts.js"></script>
</head>
<body style="margin:0;">
    <div id="container" style="width: 100%; height: 100vh;"></div>
    <script>{html_str}</script>
</body>
</html>"""
    f.write(interactive_html)
