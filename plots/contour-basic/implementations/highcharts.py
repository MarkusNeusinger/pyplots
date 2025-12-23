""" pyplots.ai
contour-basic: Basic Contour Plot
Library: highcharts unknown | Python 3.13.11
Quality: 88/100 | Created: 2025-12-23
"""

import base64
import sys
import tempfile
import time
import urllib.request
from pathlib import Path


# Avoid shadowing by matplotlib.py in the same directory
_original_path = sys.path.copy()
sys.path = [p for p in sys.path if "implementations" not in p]
import matplotlib.pyplot as mpl_plt  # noqa: E402


sys.path = _original_path

import numpy as np  # noqa: E402
from highcharts_core.chart import Chart  # noqa: E402
from highcharts_core.options import HighchartsOptions  # noqa: E402
from selenium import webdriver  # noqa: E402
from selenium.webdriver.chrome.options import Options  # noqa: E402


# Data - create a 2D scalar field using a mathematical function
np.random.seed(42)
grid_size = 100  # 100x100 grid for smooth appearance

x = np.linspace(-3, 3, grid_size)
y = np.linspace(-3, 3, grid_size)
X, Y = np.meshgrid(x, y)

# Create an interesting surface: combination of Gaussian peaks
# Simulates temperature distribution across a 2D surface
Z = (
    np.exp(-((X - 1) ** 2 + (Y - 1) ** 2))
    + 0.8 * np.exp(-((X + 1) ** 2 + (Y + 1) ** 2))
    - 0.5 * np.exp(-((X) ** 2 + (Y - 1.5) ** 2) / 0.5)
)

# Normalize Z to 0-100 range for better color mapping
Z_min, Z_max = Z.min(), Z.max()
Z_normalized = (Z - Z_min) / (Z_max - Z_min) * 100

# Create heatmap data in Highcharts format: [x_index, y_index, value]
heatmap_data = []
for y_idx in range(grid_size):
    for x_idx in range(grid_size):
        heatmap_data.append([x_idx, y_idx, round(Z_normalized[y_idx, x_idx], 1)])

# Extract contour lines using matplotlib's contour function
contour_levels = [10, 20, 30, 40, 50, 60, 70, 80, 90]

# Create a hidden figure to extract contour paths
fig_temp, ax_temp = mpl_plt.subplots()
cs = ax_temp.contour(X, Y, Z_normalized, levels=contour_levels)
mpl_plt.close(fig_temp)

# High-contrast colors for contour lines - black on light areas, white on dark areas
# Using dashed style for better visibility over filled heatmap
level_colors = {
    10: "#000000",  # Black on dark viridis background
    20: "#000000",
    30: "#ffffff",  # White for mid-tones
    40: "#ffffff",
    50: "#ffffff",
    60: "#000000",  # Black on lighter greens
    70: "#000000",
    80: "#000000",
    90: "#000000",
}

# Extract contour paths from matplotlib and convert to index coordinates
contour_series = []
label_positions = []

for i, _level in enumerate(contour_levels):
    level_val = int(cs.levels[i])
    paths = cs.allsegs[i]

    for path in paths:
        if len(path) > 5:
            # Convert real coordinates back to index coordinates for Highcharts
            # x ranges from -3 to 3, mapped to 0 to grid_size-1
            line_data = []
            step = max(1, len(path) // 100)
            decimated = path[::step]
            if len(path) > step:
                decimated = np.vstack([decimated, path[-1]])

            for p in decimated:
                # Map coordinates to indices
                x_idx = (p[0] - x[0]) / (x[-1] - x[0]) * (grid_size - 1)
                y_idx = (p[1] - y[0]) / (y[-1] - y[0]) * (grid_size - 1)
                line_data.append([round(x_idx, 2), round(y_idx, 2)])

            contour_series.append(
                {
                    "type": "line",
                    "name": f"Level {level_val}%",
                    "data": line_data,
                    "color": level_colors[level_val],
                    "lineWidth": 4,
                    "dashStyle": "Solid",
                    "marker": {"enabled": False},
                    "enableMouseTracking": False,
                    "showInLegend": False,
                    "zIndex": 10,
                }
            )

            # Store position for label on each contour level (first valid path per level)
            if len(path) > 20:
                mid_idx = len(path) // 2
                if not any(lp["level"] == level_val for lp in label_positions):
                    x_idx = (path[mid_idx][0] - x[0]) / (x[-1] - x[0]) * (grid_size - 1)
                    y_idx = (path[mid_idx][1] - y[0]) / (y[-1] - y[0]) * (grid_size - 1)
                    label_positions.append({"x": x_idx, "y": y_idx, "level": level_val})

# Create chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration
chart.options.chart = {
    "type": "heatmap",
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#ffffff",
    "marginBottom": 180,
    "marginRight": 320,
    "marginLeft": 220,
    "marginTop": 100,
}

# Title
chart.options.title = {
    "text": "contour-basic · highcharts · pyplots.ai",
    "style": {"fontSize": "64px", "fontWeight": "bold"},
}

# Create sparse category labels (show at key positions)
x_labels_sparse = ["" for _ in range(grid_size)]
y_labels_sparse = ["" for _ in range(grid_size)]
label_interval = grid_size // 6
for i in range(0, grid_size, label_interval):
    x_labels_sparse[i] = f"{x[i]:.1f}"
    y_labels_sparse[i] = f"{y[i]:.1f}"
x_labels_sparse[-1] = f"{x[-1]:.1f}"
y_labels_sparse[-1] = f"{y[-1]:.1f}"

# X-axis with visible grid lines
chart.options.x_axis = {
    "categories": x_labels_sparse,
    "title": {"text": "X Position (units)", "style": {"fontSize": "48px"}, "y": 30},
    "labels": {"style": {"fontSize": "36px"}, "rotation": 0, "y": 45},
    "lineWidth": 2,
    "tickLength": 10,
    "gridLineWidth": 2,
    "gridLineColor": "rgba(128, 128, 128, 0.5)",
    "gridLineDashStyle": "Dot",
}

# Y-axis with visible grid lines
chart.options.y_axis = {
    "categories": y_labels_sparse,
    "title": {"text": "Y Position (units)", "style": {"fontSize": "48px"}},
    "labels": {"style": {"fontSize": "36px"}},
    "reversed": False,
    "lineWidth": 2,
    "tickLength": 10,
    "gridLineWidth": 2,
    "gridLineColor": "rgba(128, 128, 128, 0.5)",
    "gridLineDashStyle": "Dot",
}

# Color axis with viridis-like gradient (colorblind-safe)
chart.options.color_axis = {
    "min": 0,
    "max": 100,
    "stops": [[0, "#440154"], [0.25, "#3b528b"], [0.5, "#21918c"], [0.75, "#5ec962"], [1, "#fde725"]],
    "labels": {"style": {"fontSize": "32px"}, "format": "{value}%"},
}

# Legend configuration (colorbar)
chart.options.legend = {
    "align": "right",
    "layout": "vertical",
    "margin": 50,
    "verticalAlign": "middle",
    "symbolHeight": 700,
    "itemStyle": {"fontSize": "32px"},
    "title": {"text": "Intensity (%)", "style": {"fontSize": "40px"}},
}

# Tooltip
chart.options.tooltip = {
    "style": {"fontSize": "32px"},
    "headerFormat": "",
    "pointFormat": "X: <b>{series.xAxis.categories.(point.x)}</b><br>"
    "Y: <b>{series.yAxis.categories.(point.y)}</b><br>"
    "Intensity: <b>{point.value}%</b>",
}

# Add heatmap series first (background - filled contour effect)
heatmap_series = {
    "name": "Surface Intensity",
    "type": "heatmap",
    "data": heatmap_data,
    "borderWidth": 0,
    "dataLabels": {"enabled": False},
    "zIndex": 1,
}

# Combine all series: heatmap first, then contour lines on top
all_series = [heatmap_series] + contour_series
chart.options.series = all_series

# Add annotations for contour level labels with high visibility
chart.options.annotations = [
    {
        "labels": [
            {
                "point": {"x": pos["x"], "y": pos["y"], "xAxis": 0, "yAxis": 0},
                "text": f"{pos['level']}%",
                "backgroundColor": "rgba(255, 255, 255, 0.95)",
                "borderColor": "#333333",
                "borderWidth": 3,
                "style": {"fontSize": "36px", "fontWeight": "bold", "color": "#000000"},
                "padding": 12,
                "borderRadius": 8,
            }
            for pos in label_positions
        ],
        "labelOptions": {"shape": "rect"},
    }
]

# Download Highcharts JS modules
highcharts_url = "https://code.highcharts.com/highcharts.js"
heatmap_url = "https://code.highcharts.com/modules/heatmap.js"
annotations_url = "https://code.highcharts.com/modules/annotations.js"

with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

with urllib.request.urlopen(heatmap_url, timeout=30) as response:
    heatmap_js = response.read().decode("utf-8")

with urllib.request.urlopen(annotations_url, timeout=30) as response:
    annotations_js = response.read().decode("utf-8")

# Generate HTML with inline scripts
html_str = chart.to_js_literal()
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <script>{heatmap_js}</script>
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
    <script src="https://code.highcharts.com/modules/heatmap.js"></script>
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
