"""pyplots.ai
contour-decision-boundary: Decision Boundary Classifier Visualization
Library: highcharts | Python 3.13
Quality: pending | Created: 2025-12-31
"""

import json
import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from sklearn.datasets import make_moons
from sklearn.neighbors import KNeighborsClassifier


# Data: Generate moon-shaped classification dataset
np.random.seed(42)
X, y = make_moons(n_samples=150, noise=0.25, random_state=42)

# Train a KNN classifier
classifier = KNeighborsClassifier(n_neighbors=15)
classifier.fit(X, y)

# Create mesh grid for decision boundary
x_min, x_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
y_min, y_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5
resolution = 100
xx, yy = np.meshgrid(np.linspace(x_min, x_max, resolution), np.linspace(y_min, y_max, resolution))

# Predict class probabilities on mesh grid
mesh_points = np.c_[xx.ravel(), yy.ravel()]
Z_proba = classifier.predict_proba(mesh_points)[:, 1]  # Probability of class 1
Z = Z_proba.reshape(xx.shape)

# Prepare heatmap data for decision regions
# Format: [[x_index, y_index, value], ...]
heatmap_data = []
for i in range(resolution):
    for j in range(resolution):
        heatmap_data.append([j, i, round(Z[i, j], 3)])

# Prepare scatter data for training points
class_0_points = [[float(X[i, 0]), float(X[i, 1])] for i in range(len(y)) if y[i] == 0]
class_1_points = [[float(X[i, 0]), float(X[i, 1])] for i in range(len(y)) if y[i] == 1]

# Download Highcharts JS and heatmap module
highcharts_url = "https://code.highcharts.com/highcharts.js"
heatmap_url = "https://code.highcharts.com/modules/heatmap.js"

with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

with urllib.request.urlopen(heatmap_url, timeout=30) as response:
    heatmap_js = response.read().decode("utf-8")

# Create chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart options
chart.options.chart = {
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#ffffff",
    "marginBottom": 150,
    "marginLeft": 150,
    "marginRight": 200,
}

# Title
chart.options.title = {
    "text": "contour-decision-boundary · highcharts · pyplots.ai",
    "style": {"fontSize": "48px", "fontWeight": "bold"},
}

# Subtitle
chart.options.subtitle = {"text": "KNN Classifier on Moon-shaped Data", "style": {"fontSize": "32px"}}

# X-axis for heatmap (categories for grid indices, but we'll overlay scatter with actual values)
x_categories = [str(round(v, 2)) for v in np.linspace(x_min, x_max, resolution)]
y_categories = [str(round(v, 2)) for v in np.linspace(y_min, y_max, resolution)]

# Color axis for heatmap (decision probability)
chart.options.color_axis = {
    "min": 0,
    "max": 1,
    "stops": [
        [0, "#306998"],  # Python Blue for class 0
        [0.5, "#f5f5f5"],  # Light gray at boundary
        [1, "#FFD43B"],  # Python Yellow for class 1
    ],
    "labels": {"style": {"fontSize": "24px"}},
}

# Build complete options as dict for complex multi-series chart
options_dict = {
    "chart": {
        "width": 4800,
        "height": 2700,
        "backgroundColor": "#ffffff",
        "marginBottom": 280,
        "marginLeft": 280,
        "marginRight": 400,
        "marginTop": 180,
    },
    "title": {
        "text": "contour-decision-boundary · highcharts · pyplots.ai",
        "style": {"fontSize": "56px", "fontWeight": "bold"},
    },
    "subtitle": {"text": "KNN Classifier Decision Boundary on Moon-shaped Data", "style": {"fontSize": "38px"}},
    "xAxis": [
        {
            "categories": x_categories,
            "title": {"text": "Feature X1", "style": {"fontSize": "38px", "fontWeight": "bold"}},
            "labels": {"style": {"fontSize": "24px"}, "step": 20},
            "tickInterval": 20,
        },
        {"min": x_min, "max": x_max, "title": {"text": None}, "labels": {"enabled": False}, "visible": False},
    ],
    "yAxis": [
        {
            "categories": y_categories,
            "title": {"text": "Feature X2", "style": {"fontSize": "38px", "fontWeight": "bold"}},
            "labels": {"style": {"fontSize": "24px"}, "step": 20},
            "tickInterval": 20,
            "reversed": False,
        },
        {"min": y_min, "max": y_max, "title": {"text": None}, "labels": {"enabled": False}, "visible": False},
    ],
    "colorAxis": {
        "min": 0,
        "max": 1,
        "stops": [[0, "#306998"], [0.5, "#E8E8E8"], [1, "#FFD43B"]],
        "labels": {"style": {"fontSize": "28px"}},
    },
    "legend": {
        "enabled": True,
        "align": "right",
        "verticalAlign": "middle",
        "layout": "vertical",
        "itemStyle": {"fontSize": "32px", "fontWeight": "normal"},
        "symbolRadius": 6,
        "symbolHeight": 20,
        "symbolWidth": 20,
    },
    "plotOptions": {
        "heatmap": {"borderWidth": 0, "colsize": 1, "rowsize": 1},
        "scatter": {"marker": {"radius": 18, "lineWidth": 4, "lineColor": "#333333"}},
    },
    "series": [
        {
            "type": "heatmap",
            "name": "Decision Region",
            "data": heatmap_data,
            "xAxis": 0,
            "yAxis": 0,
            "showInLegend": False,
        },
        {
            "type": "scatter",
            "name": "Class 0 (Moon A)",
            "data": class_0_points,
            "xAxis": 1,
            "yAxis": 1,
            "color": "#1a4971",
            "marker": {"symbol": "circle", "fillColor": "#306998"},
        },
        {
            "type": "scatter",
            "name": "Class 1 (Moon B)",
            "data": class_1_points,
            "xAxis": 1,
            "yAxis": 1,
            "color": "#cc9a00",
            "marker": {"symbol": "diamond", "fillColor": "#FFD43B"},
        },
    ],
}

# Generate JavaScript from options dict
options_js = json.dumps(options_dict)
chart_js = f"Highcharts.chart('container', {options_js});"

# HTML content with inline scripts
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <script>{heatmap_js}</script>
</head>
<body style="margin:0; padding:0;">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>{chart_js}</script>
</body>
</html>"""

# Save HTML for debugging
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Write temp HTML and take screenshot
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
