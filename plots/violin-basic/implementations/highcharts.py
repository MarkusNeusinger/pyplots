"""
violin-basic: Basic Violin Plot
Library: highcharts
"""

import json
import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def gaussian_kde(data, x_grid, bandwidth=None):
    """Simple Gaussian KDE implementation using numpy only."""
    n = len(data)
    if bandwidth is None:
        # Scott's rule for bandwidth selection
        std = np.std(data)
        bandwidth = std * (n ** (-1 / 5)) * 1.06

    # Compute KDE at each grid point
    density = np.zeros_like(x_grid, dtype=float)
    for i, x in enumerate(x_grid):
        # Gaussian kernel
        kernel = np.exp(-0.5 * ((data - x) / bandwidth) ** 2)
        density[i] = np.sum(kernel) / (n * bandwidth * np.sqrt(2 * np.pi))
    return density


# Data - Employee performance scores by department
np.random.seed(42)

departments = ["Engineering", "Marketing", "Sales", "HR", "Finance"]
data = {
    "Engineering": np.random.normal(75, 12, 150),
    "Marketing": np.concatenate([np.random.normal(65, 8, 75), np.random.normal(80, 6, 75)]),  # Bimodal
    "Sales": np.random.normal(70, 15, 150),
    "HR": np.random.normal(78, 10, 150),
    "Finance": np.random.normal(72, 9, 150),
}

# Style guide colors
colors = ["#306998", "#FFD43B", "#DC2626", "#059669", "#8B5CF6"]

# Compute KDE and build violin polygons
y_grid = np.linspace(20, 120, 200)
max_width = 0.35  # Maximum half-width of violin

violin_series = []
box_series = []
median_series = []

for idx, (dept, values) in enumerate(data.items()):
    # Compute KDE using our simple implementation
    density = gaussian_kde(values, y_grid)

    # Normalize density to max width
    density_normalized = density / density.max() * max_width

    # Build polygon coordinates for Highcharts (x, y pairs)
    # Go up left side, then down right side to form closed polygon
    polygon_points = []

    # Left side (negative x offset from center)
    for i in range(len(y_grid)):
        polygon_points.append([float(idx - density_normalized[i]), float(y_grid[i])])

    # Right side (positive x offset from center) - reversed
    for i in range(len(y_grid) - 1, -1, -1):
        polygon_points.append([float(idx + density_normalized[i]), float(y_grid[i])])

    # Close the polygon
    polygon_points.append(polygon_points[0])

    violin_series.append(
        {
            "type": "polygon",
            "name": dept,
            "data": polygon_points,
            "color": colors[idx],
            "fillOpacity": 0.7,
            "lineWidth": 2,
            "lineColor": "white",
            "enableMouseTracking": False,
        }
    )

    # Calculate statistics for inner box plot markers
    q1 = float(np.percentile(values, 25))
    median = float(np.percentile(values, 50))
    q3 = float(np.percentile(values, 75))

    # Inner quartile box (thin vertical line)
    box_width = 0.06
    box_series.append(
        {
            "type": "polygon",
            "name": f"{dept} IQR",
            "data": [
                [idx - box_width, q1],
                [idx + box_width, q1],
                [idx + box_width, q3],
                [idx - box_width, q3],
                [idx - box_width, q1],
            ],
            "color": "#333333",
            "fillOpacity": 0.9,
            "lineWidth": 0,
            "enableMouseTracking": False,
            "showInLegend": False,
        }
    )

    # Median marker (white line)
    median_series.append(
        {
            "type": "line",
            "name": f"{dept} Median",
            "data": [[idx - box_width, median], [idx + box_width, median]],
            "color": "white",
            "lineWidth": 4,
            "marker": {"enabled": False},
            "enableMouseTracking": False,
            "showInLegend": False,
        }
    )

# All series combined
all_series = violin_series + box_series + median_series

# Build chart options as JSON (without functions)
chart_options = {
    "chart": {"type": "polygon", "width": 4800, "height": 2700, "backgroundColor": "#FAFAFA"},
    "title": {"text": "Employee Performance Scores by Department", "style": {"fontSize": "48px"}},
    "xAxis": {
        "title": {"text": "Department", "style": {"fontSize": "36px"}},
        "categories": departments,
        "tickPositions": [0, 1, 2, 3, 4],
        "labels": {"style": {"fontSize": "28px"}},
        "gridLineWidth": 0,
        "min": -0.5,
        "max": 4.5,
    },
    "yAxis": {
        "title": {"text": "Performance Score", "style": {"fontSize": "36px"}},
        "min": 20,
        "max": 120,
        "labels": {"style": {"fontSize": "28px"}},
        "gridLineColor": "#E5E5E5",
        "gridLineWidth": 1,
    },
    "legend": {"enabled": True, "itemStyle": {"fontSize": "24px"}, "itemMarginBottom": 10},
    "series": all_series,
}

# Convert to JSON
options_json = json.dumps(chart_options)

# No formatter needed when using categories

# Download Highcharts JS for headless Chrome
highcharts_url = "https://code.highcharts.com/highcharts.js"
with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

highcharts_more_url = "https://code.highcharts.com/highcharts-more.js"
with urllib.request.urlopen(highcharts_more_url, timeout=30) as response:
    highcharts_more_js = response.read().decode("utf-8")

# Generate HTML with inline scripts
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <script>{highcharts_more_js}</script>
</head>
<body style="margin:0;">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>
        var options = {options_json};
        Highcharts.chart('container', options);
    </script>
</body>
</html>"""

# Write temp HTML
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

# Take screenshot with headless Chrome
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

# Save HTML for interactive version
Path("plot.html").write_text(html_content, encoding="utf-8")

# Clean up temp file
Path(temp_path).unlink()
