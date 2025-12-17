"""
dendrogram-basic: Basic Dendrogram
Library: highcharts
"""

import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.area import LineSeries
from scipy.cluster.hierarchy import dendrogram, linkage
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - Iris flower measurements (4 features for 15 samples)
np.random.seed(42)

samples_per_species = 5
labels = []
data = []

# Setosa: shorter petals, wider sepals
for i in range(samples_per_species):
    labels.append(f"Setosa-{i + 1}")
    data.append(
        [
            5.0 + np.random.randn() * 0.3,
            3.4 + np.random.randn() * 0.3,
            1.5 + np.random.randn() * 0.2,
            0.3 + np.random.randn() * 0.1,
        ]
    )

# Versicolor: medium measurements
for i in range(samples_per_species):
    labels.append(f"Versicolor-{i + 1}")
    data.append(
        [
            5.9 + np.random.randn() * 0.4,
            2.8 + np.random.randn() * 0.3,
            4.3 + np.random.randn() * 0.4,
            1.3 + np.random.randn() * 0.2,
        ]
    )

# Virginica: longer petals and sepals
for i in range(samples_per_species):
    labels.append(f"Virginica-{i + 1}")
    data.append(
        [
            6.6 + np.random.randn() * 0.5,
            3.0 + np.random.randn() * 0.3,
            5.5 + np.random.randn() * 0.5,
            2.0 + np.random.randn() * 0.3,
        ]
    )

data = np.array(data)

# Compute linkage matrix using Ward's method
linkage_matrix = linkage(data, method="ward")

# Get dendrogram structure
dend = dendrogram(linkage_matrix, labels=labels, no_plot=True)

# Extract coordinates for drawing
icoord = dend["icoord"]  # x coordinates
dcoord = dend["dcoord"]  # y coordinates (distances)
ivl = dend["ivl"]  # leaf labels in order

# Create line series data for each U-shape in the dendrogram
line_series_data = []
for xs, ys in zip(icoord, dcoord, strict=True):
    # Each U-shape has 4 points
    points = [[xs[j], ys[j]] for j in range(4)]
    line_series_data.append(
        {"data": points, "color": "#306998", "lineWidth": 3, "marker": {"enabled": False}, "enableMouseTracking": False}
    )

# Create chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Configure chart
chart.options.chart = {
    "type": "line",
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#ffffff",
    "marginBottom": 300,
    "spacingBottom": 50,
}

# Title
chart.options.title = {
    "text": "dendrogram-basic · highcharts · pyplots.ai",
    "style": {"fontSize": "56px", "fontWeight": "bold"},
}

# X-axis with sample labels
# Dendrogram x-coords are at 5, 15, 25, ... for leaves
x_positions = [(i * 10) + 5 for i in range(len(ivl))]
chart.options.x_axis = {
    "title": {"text": "Sample", "style": {"fontSize": "44px"}},
    "tickPositions": x_positions,
    "labels": {"style": {"fontSize": "24px"}, "rotation": 45},
    "min": 0,
    "max": len(ivl) * 10,
    "gridLineWidth": 0,
    "lineWidth": 2,
}

# Y-axis for distance
chart.options.y_axis = {
    "title": {"text": "Distance (Ward)", "style": {"fontSize": "44px"}},
    "labels": {"style": {"fontSize": "32px"}},
    "gridLineColor": "rgba(0,0,0,0.1)",
    "gridLineWidth": 1,
    "min": 0,
}

# Hide legend
chart.options.legend = {"enabled": False}

# Plot options for lines
chart.options.plot_options = {
    "line": {"lineWidth": 4, "marker": {"enabled": False}, "states": {"hover": {"enabled": False}}}
}

# Add each line segment as a series
for series_data in line_series_data:
    series = LineSeries()
    series.data = series_data["data"]
    series.color = series_data["color"]
    series.line_width = 4
    series.marker = {"enabled": False}
    series.enable_mouse_tracking = False
    chart.add_series(series)

# Download Highcharts JS for inline embedding
highcharts_url = "https://code.highcharts.com/highcharts.js"
with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

# Generate HTML with inline scripts
html_str = chart.to_js_literal()

# Create JavaScript formatter function for x-axis labels
labels_js = str(ivl).replace("'", '"')
formatter_js = f"""function() {{
    var labels = {labels_js};
    var idx = Math.round((this.value - 5) / 10);
    return (idx >= 0 && idx < labels.length) ? labels[idx] : '';
}}"""

# Inject formatter into the xAxis labels configuration
# Find the rotation property in labels and add formatter after it
html_str = html_str.replace(
    "rotation: 45,",
    "rotation: 45,\nformatter: " + formatter_js + ",",
    1,  # Replace only first occurrence
)

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

# Save HTML file
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
chrome_options.add_argument("--window-size=4800,2800")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)

# Get container element and screenshot it for exact dimensions
container = driver.find_element("id", "container")
container.screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()
