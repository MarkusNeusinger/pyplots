"""pyplots.ai
raincloud-basic: Basic Raincloud Plot
Library: highcharts unknown | Python 3.13.11
Quality: 88/100 | Created: 2025-12-25
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

# Create chart using highcharts_core
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration
chart.options.chart = {
    "type": "boxplot",
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#ffffff",
    "marginBottom": 280,
    "marginLeft": 220,
    "marginRight": 200,
    "spacingBottom": 80,
}

# Title
chart.options.title = {
    "text": "raincloud-basic · highcharts · pyplots.ai",
    "style": {"fontSize": "56px", "fontWeight": "bold"},
}

# X-axis (categories)
chart.options.x_axis = {
    "title": {"text": "Experimental Condition", "style": {"fontSize": "44px"}},
    "labels": {"style": {"fontSize": "36px"}},
    "categories": categories,
    "lineWidth": 2,
    "tickWidth": 2,
    "min": -0.5,
    "max": 3.5,
    "tickPositions": [0, 1, 2, 3],
}

# Y-axis (values)
chart.options.y_axis = {
    "title": {"text": "Reaction Time (ms)", "style": {"fontSize": "44px"}},
    "labels": {"style": {"fontSize": "36px"}},
    "gridLineWidth": 1,
    "gridLineColor": "rgba(0, 0, 0, 0.15)",
    "gridLineDashStyle": "Dash",
    "tickInterval": 50,
    "min": 250,
    "max": 650,
}

# Legend
chart.options.legend = {
    "enabled": True,
    "itemStyle": {"fontSize": "36px"},
    "align": "right",
    "verticalAlign": "top",
    "layout": "vertical",
    "x": -50,
    "y": 100,
    "backgroundColor": "rgba(255, 255, 255, 0.9)",
    "borderWidth": 1,
    "borderColor": "#cccccc",
    "padding": 20,
    "symbolWidth": 40,
    "symbolHeight": 24,
}

# Plot options
chart.options.plot_options = {
    "boxplot": {
        "medianColor": "#000000",
        "medianWidth": 8,
        "medianDashStyle": "Solid",
        "stemColor": "#1a1a1a",
        "stemWidth": 4,
        "whiskerColor": "#1a1a1a",
        "whiskerWidth": 5,
        "whiskerLength": "50%",
        "lineWidth": 4,
        "pointWidth": 70,
    },
    "scatter": {"marker": {"radius": 16, "symbol": "circle"}},
    "polygon": {"fillOpacity": 0.6, "lineWidth": 2},
}

# Create polygon data for half-violin (the "cloud") - inline KDE
# Cloud on RIGHT side for vertical orientation (rain falls from cloud)
for i, data in enumerate(all_data):
    # Inline KDE computation (Gaussian kernel)
    data_arr = np.array(data)
    n = len(data_arr)
    std = np.std(data_arr)
    iqr_val = np.percentile(data_arr, 75) - np.percentile(data_arr, 25)
    bandwidth = 0.9 * min(std, iqr_val / 1.34) * (n ** (-0.2))
    y_range = np.linspace(min(data_arr) - 20, max(data_arr) + 20, 50)
    density = np.zeros(50)
    for point in data_arr:
        density += np.exp(-0.5 * ((y_range - point) / bandwidth) ** 2)
    density = density / (n * bandwidth * np.sqrt(2 * np.pi))
    density = density / density.max() * 0.35

    # Create polygon points for filled half-violin on RIGHT side
    polygon_points = []
    # Right side: baseline at category, extend RIGHT (positive direction)
    for y, d in zip(y_range, density, strict=True):
        polygon_points.append([float(i + d + 0.05), float(y)])
    # Close polygon by going back along the baseline
    for y in reversed(y_range):
        polygon_points.append([float(i + 0.05), float(y)])

    series = PolygonSeries()
    series.data = polygon_points
    series.name = f"{categories[i]} (Cloud)"
    series.color = colors[i]
    series.fill_color = colors[i]
    series.fill_opacity = 0.6
    series.line_width = 2
    series.line_color = colors[i]
    series.enable_mouse_tracking = False
    chart.add_series(series)

# Box plot series - one point per category
box_series = BoxPlotSeries()
box_series_data = []
for i, box in enumerate(box_data):
    box_series_data.append(
        {
            "low": box["low"],
            "q1": box["q1"],
            "median": box["median"],
            "q3": box["q3"],
            "high": box["high"],
            "color": "#1a1a1a",
            "fillColor": f"rgba({int(colors[i][1:3], 16)},{int(colors[i][3:5], 16)},{int(colors[i][5:7], 16)},0.85)",
        }
    )
box_series.data = box_series_data
box_series.name = "Box Plot"
box_series.color = "#1a1a1a"
box_series.color_by_point = True
chart.add_series(box_series)

# Create jittered scatter data (the "rain") - one series per category for legend
for i, data in enumerate(all_data):
    scatter_points = []
    for val in data:
        jitter = np.random.uniform(-0.08, 0.08)
        # Rain on LEFT side (negative offset from category center)
        scatter_points.append([float(i - 0.25 + jitter), float(val)])

    scatter_series = ScatterSeries()
    scatter_series.data = scatter_points
    scatter_series.name = f"{categories[i]} (Points)"
    scatter_series.color = colors[i]
    scatter_series.opacity = 0.65
    scatter_series.marker = {"radius": 16, "lineWidth": 2, "lineColor": "rgba(0,0,0,0.4)", "fillColor": colors[i]}
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

# Save HTML for interactive viewing
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
chrome_options.add_argument("--window-size=4800,2700")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)  # Wait for chart to render
driver.save_screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()  # Clean up temp file
