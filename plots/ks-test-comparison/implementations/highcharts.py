""" pyplots.ai
ks-test-comparison: Kolmogorov-Smirnov Plot for Distribution Comparison
Library: highcharts unknown | Python 3.14.3
Quality: 78/100 | Created: 2026-02-17
"""

import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.area import LineSeries
from scipy import stats
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - Credit scoring: Good vs Bad customer score distributions
np.random.seed(42)
good_scores = np.random.beta(5, 2, size=300) * 800 + 200
bad_scores = np.random.beta(2, 4, size=300) * 800 + 200

# Compute K-S statistic and p-value
ks_stat, p_value = stats.ks_2samp(good_scores, bad_scores)

# Compute ECDFs for both samples
good_sorted = np.sort(good_scores)
bad_sorted = np.sort(bad_scores)
good_ecdf_y = np.arange(1, len(good_sorted) + 1) / len(good_sorted)
bad_ecdf_y = np.arange(1, len(bad_sorted) + 1) / len(bad_sorted)

# Find the point of maximum divergence
all_values = np.sort(np.concatenate([good_scores, bad_scores]))
good_ecdf_at_all = np.searchsorted(good_sorted, all_values, side="right") / len(good_sorted)
bad_ecdf_at_all = np.searchsorted(bad_sorted, all_values, side="right") / len(bad_sorted)
differences = np.abs(good_ecdf_at_all - bad_ecdf_at_all)
max_idx = np.argmax(differences)
max_x = float(all_values[max_idx])
max_y_good = float(good_ecdf_at_all[max_idx])
max_y_bad = float(bad_ecdf_at_all[max_idx])

# Build step function data
good_step_data = [[float(good_sorted[i]), float(good_ecdf_y[i])] for i in range(len(good_sorted))]
bad_step_data = [[float(bad_sorted[i]), float(bad_ecdf_y[i])] for i in range(len(bad_sorted))]

# Vertical line at max divergence (two points: from one ECDF to the other)
max_distance_data = [[max_x, min(max_y_good, max_y_bad)], [max_x, max(max_y_good, max_y_bad)]]

# Create chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration
chart.options.chart = {
    "type": "line",
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#ffffff",
    "marginBottom": 180,
    "spacingBottom": 40,
    "spacingRight": 80,
}

# Title
chart.options.title = {
    "text": "ks-test-comparison · highcharts · pyplots.ai",
    "style": {"fontSize": "64px", "fontWeight": "bold"},
}

# Subtitle showing K-S statistic and p-value
chart.options.subtitle = {
    "text": f"K-S Statistic = {ks_stat:.4f}   |   p-value = {p_value:.2e}",
    "style": {"fontSize": "44px", "color": "#555555"},
}

# X-axis
chart.options.x_axis = {
    "title": {"text": "Credit Score", "style": {"fontSize": "44px"}},
    "labels": {"style": {"fontSize": "32px"}},
    "gridLineWidth": 0,
}

# Y-axis
chart.options.y_axis = {
    "title": {"text": "Cumulative Proportion", "style": {"fontSize": "44px"}},
    "labels": {"style": {"fontSize": "32px"}},
    "min": 0,
    "max": 1,
    "gridLineWidth": 1,
    "gridLineColor": "rgba(0, 0, 0, 0.12)",
}

# Legend
chart.options.legend = {"enabled": True, "itemStyle": {"fontSize": "36px"}, "symbolWidth": 40}

# Plot options
chart.options.plot_options = {
    "line": {"lineWidth": 5, "marker": {"enabled": False}, "states": {"hover": {"lineWidth": 6}}}
}

# Credits off
chart.options.credits = {"enabled": False}

# Good customers ECDF series
good_series = LineSeries()
good_series.data = good_step_data
good_series.name = "Good Customers"
good_series.color = "#306998"
good_series.step = "left"
chart.add_series(good_series)

# Bad customers ECDF series
bad_series = LineSeries()
bad_series.data = bad_step_data
bad_series.name = "Bad Customers"
bad_series.color = "#C44E52"
bad_series.step = "left"
chart.add_series(bad_series)

# Max distance vertical line
distance_series = LineSeries()
distance_series.data = max_distance_data
distance_series.name = f"Max Distance (D = {ks_stat:.4f})"
distance_series.color = "#333333"
distance_series.dash_style = "Dash"
distance_series.line_width = 4
distance_series.marker = {"enabled": True, "radius": 8, "symbol": "diamond"}
chart.add_series(distance_series)

# Download Highcharts JS (required for headless Chrome)
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

# Save HTML for interactive version
Path("plot.html").write_text(html_content, encoding="utf-8")

# Screenshot with headless Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=4800,2900")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)
driver.save_screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()
