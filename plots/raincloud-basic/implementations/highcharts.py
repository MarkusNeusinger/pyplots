""" pyplots.ai
raincloud-basic: Basic Raincloud Plot
Library: highcharts 1.10.3 | Python 3.14
Quality: 76/100 | Created: 2025-12-25
"""

import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.boxplot import BoxPlotSeries
from highcharts_core.options.series.polygon import PolygonSeries
from highcharts_core.options.series.scatter import ScatterSeries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - Reaction times (ms) for different experimental conditions
np.random.seed(42)
categories = ["Control", "Treatment A", "Treatment B", "Treatment C"]
colors = ["#306998", "#FFD43B", "#9467BD", "#17BECF"]
colors_fill = [
    "rgba(48, 105, 152, 0.55)",
    "rgba(255, 212, 59, 0.55)",
    "rgba(148, 103, 189, 0.55)",
    "rgba(23, 190, 207, 0.55)",
]

# Generate realistic reaction time data with different distributions
control = np.random.normal(450, 60, 80)  # Normal distribution
treatment_a = np.random.normal(380, 50, 80)  # Faster responses
treatment_b = np.concatenate(
    [  # Bimodal distribution
        np.random.normal(350, 30, 40),
        np.random.normal(480, 35, 40),
    ]
)
treatment_c = np.random.normal(420, 80, 80)  # More variable

all_data = [control, treatment_a, treatment_b, treatment_c]

# Calculate statistics for box plots
box_data = []
for data in all_data:
    q1 = np.percentile(data, 25)
    median = np.percentile(data, 50)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1
    lower_whisker = max(np.min(data), q1 - 1.5 * iqr)
    upper_whisker = min(np.max(data), q3 + 1.5 * iqr)
    box_data.append(
        {
            "low": float(lower_whisker),
            "q1": float(q1),
            "median": float(median),
            "q3": float(q3),
            "high": float(upper_whisker),
        }
    )

# Create chart - HORIZONTAL orientation using inverted chart
# In inverted mode: x-axis (vertical, categories on left), y-axis (horizontal, values on bottom)
# x increases DOWNWARD, so negative offset = UPWARD (clouds), positive offset = DOWNWARD (rain)
chart = Chart(container="container")
chart.options = HighchartsOptions()

chart.options.chart = {
    "type": "scatter",
    "inverted": True,
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#fafafa",
    "marginBottom": 200,
    "marginLeft": 320,
    "marginRight": 200,
    "marginTop": 180,
}

# Title
chart.options.title = {
    "text": "raincloud-basic \u00b7 highcharts \u00b7 pyplots.ai",
    "style": {"fontSize": "60px", "fontWeight": "bold", "color": "#2c3e50"},
}

# Subtitle for context
chart.options.subtitle = {
    "text": "Reaction Time Distributions Across Experimental Conditions",
    "style": {"fontSize": "38px", "color": "#7f8c8d"},
}

# X-axis: categories with explicit min/max to accommodate cloud/rain offsets
# Setting min/max on a category axis allows fractional x-coordinates for polygon/scatter
chart.options.x_axis = {
    "title": {"text": "Experimental Condition", "style": {"fontSize": "44px", "color": "#34495e"}},
    "labels": {"style": {"fontSize": "36px", "color": "#34495e"}},
    "categories": categories,
    "tickPositions": [0, 1, 2, 3],
    "min": -0.6,
    "max": 3.6,
    "lineWidth": 2,
    "lineColor": "#bdc3c7",
    "tickWidth": 0,
    "gridLineWidth": 0,
}

# Y-axis: values (Reaction Time ms) - shown horizontally at bottom
chart.options.y_axis = {
    "title": {"text": "Reaction Time (ms)", "style": {"fontSize": "44px", "color": "#34495e"}},
    "labels": {"style": {"fontSize": "36px", "color": "#34495e"}},
    "gridLineWidth": 1,
    "gridLineColor": "rgba(0, 0, 0, 0.06)",
    "gridLineDashStyle": "Dash",
    "tickInterval": 50,
    "min": 220,
    "max": 660,
    "lineWidth": 2,
    "lineColor": "#bdc3c7",
}

# Legend
chart.options.legend = {
    "enabled": True,
    "itemStyle": {"fontSize": "36px", "fontWeight": "normal", "color": "#34495e"},
    "align": "right",
    "verticalAlign": "top",
    "layout": "vertical",
    "x": -60,
    "y": 100,
    "backgroundColor": "rgba(255, 255, 255, 0.92)",
    "borderWidth": 1,
    "borderColor": "#dcdde1",
    "borderRadius": 8,
    "padding": 20,
    "symbolWidth": 40,
    "symbolHeight": 24,
}

# Plot options
chart.options.plot_options = {
    "boxplot": {
        "medianColor": "#1a1a1a",
        "medianWidth": 8,
        "stemColor": "#333333",
        "stemWidth": 3,
        "whiskerColor": "#333333",
        "whiskerWidth": 4,
        "whiskerLength": "50%",
        "lineWidth": 3,
        "pointWidth": 55,
        "fillOpacity": 0.9,
    },
    "scatter": {"marker": {"radius": 12, "symbol": "circle"}, "zIndex": 5},
    "polygon": {"fillOpacity": 0.55, "lineWidth": 2, "zIndex": 2},
}

# Add half-violin "cloud" shapes ABOVE each category baseline (negative x offset = upward on screen)
for i, data in enumerate(all_data):
    # Inline KDE using Gaussian kernel (Silverman's rule of thumb for bandwidth)
    data_arr = np.array(data)
    n = len(data_arr)
    std = np.std(data_arr)
    iqr_val = np.percentile(data_arr, 75) - np.percentile(data_arr, 25)
    bandwidth = 0.9 * min(std, iqr_val / 1.34) * (n ** (-0.2))
    y_range = np.linspace(data_arr.min() - 15, data_arr.max() + 15, 80)
    density = np.zeros(80)
    for point in data_arr:
        density += np.exp(-0.5 * ((y_range - point) / bandwidth) ** 2)
    density = density / (n * bandwidth * np.sqrt(2 * np.pi))
    density_norm = density / density.max() * 0.35  # Scale to fit

    # Cloud polygon: extends upward (negative x offset in inverted mode)
    # Start from baseline, trace the KDE shape upward, return along baseline
    polygon_points = []
    for y_val, d in zip(y_range, density_norm, strict=True):
        polygon_points.append([float(i - d - 0.05), float(y_val)])
    # Close polygon back along baseline
    for y_val in reversed(y_range):
        polygon_points.append([float(i - 0.05), float(y_val)])

    series = PolygonSeries()
    series.data = polygon_points
    series.name = categories[i]
    series.color = colors[i]
    series.fill_color = colors_fill[i]
    series.fill_opacity = 0.55
    series.line_width = 2
    series.line_color = colors[i]
    series.z_index = 2
    chart.add_series(series)

# Box plot series - single series, white fill with dark outlines for clarity
box_series = BoxPlotSeries()
box_series_data = []
for i, box in enumerate(box_data):
    box_series_data.append(
        {"x": i, "low": box["low"], "q1": box["q1"], "median": box["median"], "q3": box["q3"], "high": box["high"]}
    )
box_series.data = box_series_data
box_series.name = "Box Plot"
box_series.color = "#2c3e50"
box_series.fill_color = "rgba(255, 255, 255, 0.92)"
box_series.show_in_legend = False
box_series.z_index = 8
chart.add_series(box_series)

# Jittered scatter "rain" points BELOW each category baseline (positive x offset = downward)
for i, data in enumerate(all_data):
    scatter_points = []
    for val in data:
        jitter = np.random.uniform(-0.06, 0.06)
        scatter_points.append([float(i + 0.2 + jitter), float(val)])

    scatter_series = ScatterSeries()
    scatter_series.data = scatter_points
    scatter_series.name = categories[i]
    scatter_series.color = colors[i]
    scatter_series.marker = {
        "radius": 10,
        "lineWidth": 1,
        "lineColor": "rgba(0,0,0,0.25)",
        "fillColor": colors[i],
        "states": {"hover": {"enabled": False}},
    }
    scatter_series.opacity = 0.6
    scatter_series.show_in_legend = False
    scatter_series.z_index = 5
    chart.add_series(scatter_series)

# Download Highcharts JS and required modules
highcharts_url = "https://code.highcharts.com/highcharts.js"
with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

highcharts_more_url = "https://code.highcharts.com/highcharts-more.js"
with urllib.request.urlopen(highcharts_more_url, timeout=30) as response:
    highcharts_more_js = response.read().decode("utf-8")

# Generate HTML with inline scripts
html_str = chart.to_js_literal()

html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <script>{highcharts_more_js}</script>
</head>
<body style="margin:0;">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>{html_str}</script>
</body>
</html>"""

# Write temp HTML file
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

# Save standalone HTML for interactive viewing
with open("plot.html", "w", encoding="utf-8") as f:
    standalone_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://code.highcharts.com/highcharts.js"></script>
    <script src="https://code.highcharts.com/highcharts-more.js"></script>
</head>
<body style="margin:0;">
    <div id="container" style="width: 100%; height: 100vh;"></div>
    <script>{html_str}</script>
</body>
</html>"""
    f.write(standalone_html)

# Setup Chrome for screenshot
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=5000,3000")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)  # Wait for chart to render

# Screenshot the container element for tighter framing
container = driver.find_element("id", "container")
container.screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()  # Clean up temp file
