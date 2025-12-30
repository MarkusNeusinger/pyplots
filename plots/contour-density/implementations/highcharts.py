"""pyplots.ai
contour-density: Density Contour Plot
Library: highcharts | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import base64
import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - generate bivariate data with clusters to demonstrate density contours
np.random.seed(42)

# Create 3 clusters of points with different densities
n1, n2, n3 = 150, 100, 80

# Cluster 1: High density cluster (main cluster)
cluster1_x = np.random.normal(2.5, 0.8, n1)
cluster1_y = np.random.normal(3.0, 0.7, n1)

# Cluster 2: Medium density cluster
cluster2_x = np.random.normal(-1.5, 1.0, n2)
cluster2_y = np.random.normal(1.0, 0.9, n2)

# Cluster 3: Lower density cluster
cluster3_x = np.random.normal(0.5, 1.2, n3)
cluster3_y = np.random.normal(-1.5, 1.1, n3)

# Combine all points
x_points = np.concatenate([cluster1_x, cluster2_x, cluster3_x])
y_points = np.concatenate([cluster1_y, cluster2_y, cluster3_y])

# Create grid for density evaluation
grid_size = 80
x_min, x_max = x_points.min() - 1.5, x_points.max() + 1.5
y_min, y_max = y_points.min() - 1.5, y_points.max() + 1.5

x_grid = np.linspace(x_min, x_max, grid_size)
y_grid = np.linspace(y_min, y_max, grid_size)
X, Y = np.meshgrid(x_grid, y_grid)

# Compute 2D Kernel Density Estimation using Gaussian kernel (manual implementation)
# Scott's rule for 2D bandwidth
n = len(x_points)
std_x = np.std(x_points)
std_y = np.std(y_points)
bandwidth = n ** (-1 / 6)  # Scott's rule for 2D
h_x = bandwidth * std_x
h_y = bandwidth * std_y

# Evaluate Gaussian KDE on grid
Z = np.zeros_like(X)
for xi, yi in zip(x_points, y_points, strict=True):
    Z += np.exp(-0.5 * (((X - xi) / h_x) ** 2 + ((Y - yi) / h_y) ** 2))
Z /= n * 2 * np.pi * h_x * h_y

# Normalize to 0-100 for percentage-based contour levels
Z_min, Z_max = Z.min(), Z.max()
Z_normalized = (Z - Z_min) / (Z_max - Z_min) * 100


def marching_squares_contour(Z, level):
    """Extract contour paths using marching squares algorithm with linear interpolation."""
    rows, cols = Z.shape
    segments = []

    ms_table = {
        0: [],
        1: [[3, 2]],
        2: [[1, 2]],
        3: [[3, 1]],
        4: [[0, 1]],
        5: [[0, 3], [1, 2]],
        6: [[0, 2]],
        7: [[0, 3]],
        8: [[0, 3]],
        9: [[0, 2]],
        10: [[0, 1], [2, 3]],
        11: [[0, 1]],
        12: [[1, 3]],
        13: [[1, 2]],
        14: [[2, 3]],
        15: [],
    }

    for i in range(rows - 1):
        for j in range(cols - 1):
            tl, tr = Z[i, j], Z[i, j + 1]
            br, bl = Z[i + 1, j + 1], Z[i + 1, j]

            config = 0
            if tl >= level:
                config |= 8
            if tr >= level:
                config |= 4
            if br >= level:
                config |= 2
            if bl >= level:
                config |= 1

            edges = ms_table[config]
            if not edges:
                continue

            edge_points = {}

            if tl != tr:
                t = (level - tl) / (tr - tl)
                if 0 <= t <= 1:
                    edge_points[0] = (j + t, i)

            if tr != br:
                t = (level - tr) / (br - tr)
                if 0 <= t <= 1:
                    edge_points[1] = (j + 1, i + t)

            if bl != br:
                t = (level - bl) / (br - bl)
                if 0 <= t <= 1:
                    edge_points[2] = (j + t, i + 1)

            if tl != bl:
                t = (level - tl) / (bl - tl)
                if 0 <= t <= 1:
                    edge_points[3] = (j, i + t)

            for e1, e2 in edges:
                if e1 in edge_points and e2 in edge_points:
                    segments.append((edge_points[e1], edge_points[e2]))

    return segments


def connect_segments(segments):
    """Connect line segments into continuous paths."""
    if not segments:
        return []

    paths = []
    remaining = list(segments)

    while remaining:
        seg = remaining.pop(0)
        path = [seg[0], seg[1]]

        changed = True
        while changed:
            changed = False
            for i, seg in enumerate(remaining):
                if np.allclose(seg[0], path[-1], atol=0.01):
                    path.append(seg[1])
                    remaining.pop(i)
                    changed = True
                    break
                elif np.allclose(seg[1], path[-1], atol=0.01):
                    path.append(seg[0])
                    remaining.pop(i)
                    changed = True
                    break
                elif np.allclose(seg[1], path[0], atol=0.01):
                    path.insert(0, seg[0])
                    remaining.pop(i)
                    changed = True
                    break
                elif np.allclose(seg[0], path[0], atol=0.01):
                    path.insert(0, seg[1])
                    remaining.pop(i)
                    changed = True
                    break

        if len(path) >= 4:
            paths.append(path)

    return paths


# Extract contour lines at various density levels
contour_levels = [10, 20, 30, 40, 50, 60, 70, 80, 90]

# Colorblind-safe colors for contour lines (viridis-inspired)
level_colors = {
    10: "#440154",
    20: "#482878",
    30: "#3e4989",
    40: "#31688e",
    50: "#26828e",
    60: "#1f9e89",
    70: "#35b779",
    80: "#6ece58",
    90: "#fde725",
}

contour_series = []
label_positions = []

for level in contour_levels:
    segments = marching_squares_contour(Z_normalized, level)
    paths = connect_segments(segments)

    for path in paths:
        if len(path) < 4:
            continue

        # Convert grid indices to real coordinates
        real_path = []
        for pt in path:
            real_x = x_min + (pt[0] / (grid_size - 1)) * (x_max - x_min)
            real_y = y_min + (pt[1] / (grid_size - 1)) * (y_max - y_min)
            real_path.append([round(real_x, 3), round(real_y, 3)])

        # Subsample for performance
        step = max(1, len(real_path) // 100)
        subsampled = real_path[::step]
        if len(real_path) > step and real_path[-1] != subsampled[-1]:
            subsampled.append(real_path[-1])

        # Add contour line with appropriate color
        contour_series.append(
            {
                "type": "line",
                "name": f"Density {level}%",
                "data": subsampled,
                "color": level_colors[level],
                "lineWidth": 4,
                "dashStyle": "Solid",
                "marker": {"enabled": False},
                "enableMouseTracking": False,
                "showInLegend": False,
                "zIndex": 5 + level // 10,
            }
        )

        # Store label position for key levels
        key_levels = [20, 50, 80]
        if level in key_levels and len(path) > 8 and not any(lp["level"] == level for lp in label_positions):
            mid_idx = len(path) // 2
            mid_x = x_min + (path[mid_idx][0] / (grid_size - 1)) * (x_max - x_min)
            mid_y = y_min + (path[mid_idx][1] / (grid_size - 1)) * (y_max - y_min)
            label_positions.append({"x": mid_x, "y": mid_y, "level": level})

# Prepare scatter data (subsample for clarity)
sample_idx = np.random.choice(len(x_points), size=min(150, len(x_points)), replace=False)
scatter_data = [[round(float(x_points[i]), 3), round(float(y_points[i]), 3)] for i in sample_idx]

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
    "marginRight": 150,
    "marginLeft": 220,
    "marginTop": 140,
}

# Title
chart.options.title = {
    "text": "contour-density · highcharts · pyplots.ai",
    "style": {"fontSize": "64px", "fontWeight": "bold"},
}

# X-axis
chart.options.x_axis = {
    "title": {"text": "X Variable", "style": {"fontSize": "48px"}, "margin": 25},
    "labels": {"style": {"fontSize": "36px"}},
    "lineWidth": 3,
    "tickWidth": 3,
    "gridLineWidth": 1,
    "gridLineColor": "rgba(0, 0, 0, 0.15)",
    "gridLineDashStyle": "Dot",
    "min": x_min,
    "max": x_max,
}

# Y-axis
chart.options.y_axis = {
    "title": {"text": "Y Variable", "style": {"fontSize": "48px"}},
    "labels": {"style": {"fontSize": "36px"}},
    "lineWidth": 3,
    "tickWidth": 3,
    "gridLineWidth": 1,
    "gridLineColor": "rgba(0, 0, 0, 0.15)",
    "gridLineDashStyle": "Dot",
    "min": y_min,
    "max": y_max,
}

# Add scatter series first (background)
scatter_series = {
    "type": "scatter",
    "name": "Data Points",
    "data": scatter_data,
    "color": "rgba(48, 105, 152, 0.35)",
    "marker": {
        "radius": 10,
        "fillColor": "rgba(48, 105, 152, 0.35)",
        "lineWidth": 2,
        "lineColor": "rgba(48, 105, 152, 0.6)",
    },
    "zIndex": 2,
    "showInLegend": True,
}

# Combine all series
all_series = [scatter_series] + contour_series
chart.options.series = all_series

# Legend configuration
chart.options.legend = {
    "enabled": True,
    "align": "right",
    "verticalAlign": "top",
    "layout": "vertical",
    "x": -30,
    "y": 100,
    "floating": True,
    "itemStyle": {"fontSize": "32px"},
    "symbolRadius": 6,
    "symbolHeight": 20,
    "symbolWidth": 30,
}

# Add density gradient legend (custom annotation)
gradient_labels = [
    {
        "point": {"x": x_max - 0.3, "y": y_max - 0.5, "xAxis": 0, "yAxis": 0},
        "text": "Density",
        "style": {"fontSize": "36px", "fontWeight": "bold"},
    },
    {
        "point": {"x": x_max - 0.3, "y": y_max - 1.0, "xAxis": 0, "yAxis": 0},
        "text": "High",
        "style": {"fontSize": "28px"},
        "backgroundColor": "#fde725",
    },
    {
        "point": {"x": x_max - 0.3, "y": y_max - 1.4, "xAxis": 0, "yAxis": 0},
        "text": "Medium",
        "style": {"fontSize": "28px"},
        "backgroundColor": "#26828e",
    },
    {
        "point": {"x": x_max - 0.3, "y": y_max - 1.8, "xAxis": 0, "yAxis": 0},
        "text": "Low",
        "style": {"fontSize": "28px"},
        "backgroundColor": "#440154",
    },
]

# Add annotations for contour level labels
annotations_list = []
for pos in label_positions:
    annotations_list.append(
        {
            "point": {"x": pos["x"], "y": pos["y"], "xAxis": 0, "yAxis": 0},
            "text": f"{pos['level']}%",
            "backgroundColor": "rgba(255, 255, 255, 0.9)",
            "borderColor": level_colors[pos["level"]],
            "borderWidth": 3,
            "style": {"fontSize": "28px", "fontWeight": "bold", "color": "#000000"},
            "padding": 8,
            "borderRadius": 6,
        }
    )

chart.options.annotations = [{"labels": annotations_list, "labelOptions": {"shape": "rect"}}]

# Tooltip
chart.options.tooltip = {
    "style": {"fontSize": "28px"},
    "headerFormat": "<b>Data Point</b><br>",
    "pointFormat": "X: {point.x:.2f}<br>Y: {point.y:.2f}",
}

# Download Highcharts JS modules
highcharts_url = "https://code.highcharts.com/highcharts.js"
annotations_url = "https://code.highcharts.com/modules/annotations.js"

with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

with urllib.request.urlopen(annotations_url, timeout=30) as response:
    annotations_js = response.read().decode("utf-8")

# Generate HTML with inline scripts
html_str = chart.to_js_literal()
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <script>{annotations_js}</script>
</head>
<body style="margin:0;">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>{html_str}</script>
</body>
</html>"""

# Save HTML for interactive version
with open("plot.html", "w", encoding="utf-8") as f:
    standalone_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://code.highcharts.com/highcharts.js"></script>
    <script src="https://code.highcharts.com/modules/annotations.js"></script>
</head>
<body style="margin:0;">
    <div id="container" style="width: 100%; height: 100vh;"></div>
    <script>{html_str}</script>
</body>
</html>"""
    f.write(standalone_html)

# Write temp HTML and take screenshot
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--hide-scrollbars")
chrome_options.add_argument("--force-device-scale-factor=1")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)

# Use CDP for full page screenshot
screenshot_config = {"captureBeyondViewport": True, "clip": {"x": 0, "y": 0, "width": 4800, "height": 2700, "scale": 1}}
result = driver.execute_cdp_cmd("Page.captureScreenshot", screenshot_config)
with open("plot.png", "wb") as f:
    f.write(base64.b64decode(result["data"]))
driver.quit()

Path(temp_path).unlink()
