""" pyplots.ai
violin-basic: Basic Violin Plot
Library: highcharts unknown | Python 3.13.11
Quality: 85/100 | Created: 2025-12-23
"""

import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.polygon import PolygonSeries
from highcharts_core.options.series.scatter import ScatterSeries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - generate sample distributions for 4 categories
np.random.seed(42)
categories = ["Group A", "Group B", "Group C", "Group D"]
colors = ["#306998", "#FFD43B", "#9467BD", "#17BECF"]

# Generate data with different distributions
raw_data = {
    "Group A": np.random.normal(50, 12, 200),
    "Group B": np.concatenate([np.random.normal(40, 8, 100), np.random.normal(65, 8, 100)]),  # Bimodal
    "Group C": np.random.normal(60, 10, 200),
    "Group D": np.random.exponential(15, 200) + 30,  # Skewed
}


# Kernel Density Estimation
def kde(data, x_grid, bandwidth=None):
    """Compute Gaussian KDE at given x values."""
    n = len(data)
    if bandwidth is None:
        # Silverman's rule of thumb
        bandwidth = 1.06 * np.std(data) * n ** (-1 / 5)
    result = np.zeros_like(x_grid)
    for xi in data:
        result += np.exp(-0.5 * ((x_grid - xi) / bandwidth) ** 2)
    result /= n * bandwidth * np.sqrt(2 * np.pi)
    return result


# Calculate KDE and statistics for each category
violin_width = 0.35  # Half-width of violin in category units
violin_data = []

for i, cat in enumerate(categories):
    data = raw_data[cat]

    # Compute KDE
    y_min, y_max = data.min() - 5, data.max() + 5
    y_grid = np.linspace(y_min, y_max, 100)
    density = kde(data, y_grid)

    # Normalize density to fit within violin width
    density_norm = density / density.max() * violin_width

    # Statistics for markers
    q1 = np.percentile(data, 25)
    median = np.percentile(data, 50)
    q3 = np.percentile(data, 75)

    violin_data.append(
        {
            "category": cat,
            "index": i,
            "y_grid": y_grid,
            "density": density_norm,
            "q1": q1,
            "median": median,
            "q3": q3,
            "color": colors[i],
        }
    )

# Create chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration
chart.options.chart = {
    "type": "scatter",
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#ffffff",
    "marginBottom": 200,
    "marginLeft": 250,
    "marginRight": 100,
}

# Title
chart.options.title = {
    "text": "violin-basic · highcharts · pyplots.ai",
    "style": {"fontSize": "72px", "fontWeight": "bold"},
}

# X-axis (categories)
chart.options.x_axis = {
    "title": {"text": "Category", "style": {"fontSize": "48px"}},
    "labels": {"style": {"fontSize": "36px"}, "format": "{value}"},
    "min": -0.5,
    "max": 3.5,
    "tickPositions": [0, 1, 2, 3],
    "categories": categories,
    "lineWidth": 2,
}

# Y-axis (values)
chart.options.y_axis = {
    "title": {"text": "Value", "style": {"fontSize": "48px"}},
    "labels": {"style": {"fontSize": "36px"}},
    "gridLineWidth": 1,
    "gridLineColor": "rgba(0, 0, 0, 0.1)",
}

# Legend
chart.options.legend = {"enabled": True, "itemStyle": {"fontSize": "36px"}}

# Plot options
chart.options.plot_options = {
    "polygon": {"lineWidth": 3, "fillOpacity": 0.6, "enableMouseTracking": True},
    "scatter": {"marker": {"radius": 14, "symbol": "circle"}},
}

# Add violin shapes as polygon series
for v in violin_data:
    # Create polygon points for the violin shape
    # Go up the right side, then down the left side to form a closed shape
    polygon_points = []

    # Right side (positive x offset from center)
    for y_val, dens in zip(v["y_grid"], v["density"], strict=True):
        polygon_points.append([float(v["index"] + dens), float(y_val)])

    # Left side (negative x offset from center) - reversed to close the polygon
    for j in range(len(v["y_grid"]) - 1, -1, -1):
        y_val = v["y_grid"][j]
        dens = v["density"][j]
        polygon_points.append([float(v["index"] - dens), float(y_val)])

    series = PolygonSeries()
    series.data = polygon_points
    series.name = v["category"]
    series.color = v["color"]
    series.fill_color = v["color"]
    series.fill_opacity = 0.6
    chart.add_series(series)

# Add median markers as scatter points
med_series = ScatterSeries()
med_series.data = [[float(v["index"]), float(v["median"])] for v in violin_data]
med_series.name = "Median"
med_series.marker = {"fillColor": "#ffffff", "lineColor": "#000000", "lineWidth": 4, "radius": 14, "symbol": "circle"}
chart.add_series(med_series)

# Add quartile box indicators (thin rectangles for IQR)
for v in violin_data:
    # Create a thin box for IQR
    box_width = 0.05
    box_points = [
        [float(v["index"] - box_width), float(v["q1"])],
        [float(v["index"] + box_width), float(v["q1"])],
        [float(v["index"] + box_width), float(v["q3"])],
        [float(v["index"] - box_width), float(v["q3"])],
    ]

    box_series = PolygonSeries()
    box_series.data = box_points
    box_series.name = f"{v['category']} IQR"
    box_series.show_in_legend = False
    box_series.color = "#000000"
    box_series.fill_color = "#000000"
    box_series.fill_opacity = 0.8
    chart.add_series(box_series)

# Download Highcharts JS files
highcharts_url = "https://code.highcharts.com/highcharts.js"
with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

# Polygon requires highcharts-more.js
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

# Take screenshot with Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=5000,3000")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)  # Wait for chart to render

container = driver.find_element("id", "container")
container.screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()  # Clean up temp file
