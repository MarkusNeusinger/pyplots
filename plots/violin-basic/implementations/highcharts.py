""" pyplots.ai
violin-basic: Basic Violin Plot
Library: highcharts 1.10.3 | Python 3.14.3
Quality: 79/100 | Updated: 2026-02-21
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
from scipy.stats import gaussian_kde
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - test scores across 4 study groups with distinct distributions
np.random.seed(42)
categories = ["Group A", "Group B", "Group C", "Group D"]
colors = ["#306998", "#FFD43B", "#9467BD", "#17BECF"]

raw_data = {
    "Group A": np.random.normal(50, 12, 200),
    "Group B": np.concatenate([np.random.normal(40, 8, 100), np.random.normal(65, 8, 100)]),  # Bimodal
    "Group C": np.random.normal(60, 10, 200),
    "Group D": np.random.exponential(15, 200) + 30,  # Skewed
}

# Calculate KDE and statistics for each category
violin_width = 0.35
violin_data = []

for i, cat in enumerate(categories):
    data = raw_data[cat]
    y_min, y_max = data.min() - 5, data.max() + 5
    y_grid = np.linspace(y_min, y_max, 100)
    kde_func = gaussian_kde(data)
    density = kde_func(y_grid)
    density_norm = density / density.max() * violin_width

    violin_data.append(
        {
            "category": cat,
            "index": i,
            "y_grid": y_grid,
            "density": density_norm,
            "q1": float(np.percentile(data, 25)),
            "median": float(np.percentile(data, 50)),
            "q3": float(np.percentile(data, 75)),
            "color": colors[i],
        }
    )

# Chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

chart.options.chart = {
    "type": "scatter",
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#ffffff",
    "marginBottom": 180,
    "marginLeft": 240,
    "marginRight": 80,
    "marginTop": 160,
}

chart.options.title = {
    "text": "violin-basic \u00b7 highcharts \u00b7 pyplots.ai",
    "style": {"fontSize": "72px", "fontWeight": "bold", "color": "#333333"},
}

chart.options.x_axis = {
    "title": {"text": "Study Group", "style": {"fontSize": "52px", "color": "#555555"}},
    "labels": {"style": {"fontSize": "44px", "color": "#555555"}},
    "min": -0.5,
    "max": 3.5,
    "tickPositions": [0, 1, 2, 3],
    "categories": categories,
    "lineWidth": 2,
    "lineColor": "#cccccc",
    "tickLength": 0,
}

chart.options.y_axis = {
    "title": {"text": "Test Score (points)", "style": {"fontSize": "52px", "color": "#555555"}},
    "labels": {"style": {"fontSize": "44px", "color": "#555555"}},
    "gridLineWidth": 1,
    "gridLineColor": "rgba(0, 0, 0, 0.08)",
    "lineWidth": 2,
    "lineColor": "#cccccc",
}

chart.options.legend = {
    "enabled": True,
    "itemStyle": {"fontSize": "40px", "color": "#555555"},
    "verticalAlign": "top",
    "align": "right",
    "layout": "vertical",
    "x": -20,
    "y": 80,
    "floating": True,
}

chart.options.plot_options = {
    "polygon": {"lineWidth": 2, "fillOpacity": 0.55, "enableMouseTracking": True},
    "scatter": {"marker": {"radius": 18, "symbol": "circle"}, "zIndex": 10},
}

# Violin shapes as polygon series
for v in violin_data:
    polygon_points = []
    for y_val, dens in zip(v["y_grid"], v["density"], strict=True):
        polygon_points.append([float(v["index"] + dens), float(y_val)])
    for j in range(len(v["y_grid"]) - 1, -1, -1):
        polygon_points.append([float(v["index"] - v["density"][j]), float(v["y_grid"][j])])

    series = PolygonSeries()
    series.data = polygon_points
    series.name = v["category"]
    series.color = v["color"]
    series.fill_color = v["color"]
    series.fill_opacity = 0.55
    chart.add_series(series)

# Median markers
med_series = ScatterSeries()
med_series.data = [[float(v["index"]), float(v["median"])] for v in violin_data]
med_series.name = "Median"
med_series.color = "#333333"
med_series.marker = {"fillColor": "#ffffff", "lineColor": "#333333", "lineWidth": 6, "radius": 18, "symbol": "diamond"}
med_series.z_index = 20
chart.add_series(med_series)

# IQR boxes (thin rectangles for interquartile range)
for v in violin_data:
    box_width = 0.06
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
    box_series.color = "#333333"
    box_series.fill_color = "#333333"
    box_series.fill_opacity = 0.85
    chart.add_series(box_series)

# Export
highcharts_url = "https://cdn.jsdelivr.net/npm/highcharts@11/highcharts.js"
with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

highcharts_more_url = "https://cdn.jsdelivr.net/npm/highcharts@11/highcharts-more.js"
with urllib.request.urlopen(highcharts_more_url, timeout=30) as response:
    highcharts_more_js = response.read().decode("utf-8")

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

with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

with open("plot.html", "w", encoding="utf-8") as f:
    standalone_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://cdn.jsdelivr.net/npm/highcharts@11/highcharts.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/highcharts@11/highcharts-more.js"></script>
</head>
<body style="margin:0;">
    <div id="container" style="width: 100%; height: 100vh;"></div>
    <script>{html_str}</script>
</body>
</html>"""
    f.write(standalone_html)

# Screenshot
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=4900,2800")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)

container = driver.find_element("id", "container")
container.screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()
