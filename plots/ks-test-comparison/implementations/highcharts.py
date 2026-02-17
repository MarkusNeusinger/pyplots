"""pyplots.ai
ks-test-comparison: Kolmogorov-Smirnov Plot for Distribution Comparison
Library: highcharts unknown | Python 3.14.3
Quality: 84/100 | Created: 2026-02-17
"""

import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.annotations import Annotation
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

# Build step function data for Highcharts
good_step_data = [[float(x), float(y)] for x, y in zip(good_sorted, good_ecdf_y, strict=True)]
bad_step_data = [[float(x), float(y)] for x, y in zip(bad_sorted, bad_ecdf_y, strict=True)]

# Vertical line at max divergence
max_distance_data = [[max_x, min(max_y_good, max_y_bad)], [max_x, max(max_y_good, max_y_bad)]]

# Create chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration with balanced margins for good canvas utilization
chart.options.chart = {
    "type": "line",
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#f5f6f8",
    "marginBottom": 260,
    "marginTop": 220,
    "marginLeft": 160,
    "marginRight": 100,
    "spacingTop": 30,
    "spacingBottom": 20,
    "style": {"fontFamily": "'Segoe UI', 'Helvetica Neue', Arial, sans-serif"},
}

# Title with refined typography
chart.options.title = {
    "text": "ks-test-comparison \u00b7 highcharts \u00b7 pyplots.ai",
    "style": {"fontSize": "60px", "fontWeight": "700", "color": "#1a1a2e", "letterSpacing": "0.5px"},
    "y": 50,
}

# Subtitle showing K-S statistic and p-value with interpretation
chart.options.subtitle = {
    "text": f"K-S Statistic = {ks_stat:.4f}  \u2502  p-value = {p_value:.2e}  \u2502  Distributions are significantly different",
    "style": {"fontSize": "40px", "color": "#666666", "fontWeight": "400"},
    "y": 115,
}

# X-axis with clean styling
chart.options.x_axis = {
    "title": {"text": "Credit Score", "style": {"fontSize": "42px", "color": "#444444", "fontWeight": "600"}, "y": 16},
    "labels": {"style": {"fontSize": "32px", "color": "#666666"}},
    "tickInterval": 100,
    "gridLineWidth": 0,
    "lineColor": "#cccccc",
    "lineWidth": 1,
    "tickColor": "#cccccc",
    "tickLength": 8,
    "plotBands": [{"from": max_x - 10, "to": max_x + 10, "color": "rgba(44, 62, 80, 0.06)", "zIndex": 0}],
}

# Y-axis with subtle grid
chart.options.y_axis = {
    "title": {"text": "Cumulative Proportion", "style": {"fontSize": "42px", "color": "#444444", "fontWeight": "600"}},
    "labels": {"style": {"fontSize": "32px", "color": "#666666"}},
    "min": 0,
    "max": 1,
    "tickInterval": 0.2,
    "gridLineWidth": 1,
    "gridLineColor": "rgba(0, 0, 0, 0.06)",
    "gridLineDashStyle": "Dash",
    "lineColor": "#cccccc",
    "lineWidth": 1,
}

# Legend positioned below chart, close to plot area
chart.options.legend = {
    "enabled": True,
    "align": "center",
    "verticalAlign": "bottom",
    "layout": "horizontal",
    "itemStyle": {"fontSize": "36px", "color": "#333333", "fontWeight": "normal"},
    "symbolWidth": 60,
    "symbolHeight": 18,
    "itemDistance": 80,
    "y": -10,
}

# Plot options
chart.options.plot_options = {
    "line": {"lineWidth": 6, "marker": {"enabled": False}, "states": {"hover": {"lineWidth": 8}}}
}

# Tooltip for interactive HTML version
chart.options.tooltip = {
    "headerFormat": '<span style="font-size:24px;font-weight:bold">Credit Score: {point.x:.0f}</span><br/>',
    "pointFormat": '<span style="font-size:22px">{series.name}: <b>{point.y:.3f}</b></span>',
    "backgroundColor": "rgba(255, 255, 255, 0.95)",
    "borderColor": "#306998",
    "borderRadius": 8,
}

# Credits off
chart.options.credits = {"enabled": False}

# Good customers ECDF series
good_series = LineSeries()
good_series.data = good_step_data
good_series.name = "Good Customers"
good_series.color = "#306998"
good_series.step = "left"
good_series.z_index = 2
chart.add_series(good_series)

# Bad customers ECDF series
bad_series = LineSeries()
bad_series.data = bad_step_data
bad_series.name = "Bad Customers"
bad_series.color = "#e67e22"
bad_series.step = "left"
bad_series.z_index = 2
chart.add_series(bad_series)

# Max distance vertical line — clear focal point
distance_series = LineSeries()
distance_series.data = max_distance_data
distance_series.name = f"Max Distance (D = {ks_stat:.4f})"
distance_series.color = "#34495e"
distance_series.dash_style = "LongDash"
distance_series.line_width = 5
distance_series.marker = {
    "enabled": True,
    "radius": 12,
    "symbol": "diamond",
    "fillColor": "#34495e",
    "lineColor": "#ffffff",
    "lineWidth": 3,
}
distance_series.z_index = 5
chart.add_series(distance_series)

# Annotation callout with enhanced styling for data storytelling
mid_y = (max_y_good + max_y_bad) / 2
chart.options.annotations = [
    Annotation.from_dict(
        {
            "labels": [
                {
                    "point": {"x": max_x, "y": mid_y, "xAxis": 0, "yAxis": 0},
                    "text": f"D = {ks_stat:.4f}<br/>Strong separation",
                    "x": 160,
                    "style": {"fontSize": "36px", "fontWeight": "bold", "color": "#1a1a2e", "textAlign": "center"},
                }
            ],
            "labelOptions": {
                "backgroundColor": "rgba(255, 255, 255, 0.92)",
                "borderColor": "#34495e",
                "borderWidth": 2,
                "borderRadius": 10,
                "padding": 20,
                "shape": "callout",
                "shadow": {"color": "rgba(0,0,0,0.15)", "offsetX": 2, "offsetY": 2, "width": 6},
            },
            "draggable": "",
        }
    )
]

# Download Highcharts JS and annotations module (required for headless Chrome)
highcharts_url = "https://code.highcharts.com/highcharts.js"
highcharts_ann_url = "https://code.highcharts.com/modules/annotations.js"
with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")
with urllib.request.urlopen(highcharts_ann_url, timeout=30) as response:
    highcharts_ann_js = response.read().decode("utf-8")

# Generate HTML with inline scripts
html_str = chart.to_js_literal()
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <script>{highcharts_ann_js}</script>
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
chrome_options.add_argument("--window-size=4800,3000")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)
container = driver.find_element("id", "container")
container.screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()
