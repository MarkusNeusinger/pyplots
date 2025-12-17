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
from PIL import Image
from scipy.cluster.hierarchy import linkage
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - Iris flower measurements for hierarchical clustering
# Using a subset of iris data with 15 samples for readability
np.random.seed(42)

# Sample names representing different iris specimens
labels = [
    "Setosa-1",
    "Setosa-2",
    "Setosa-3",
    "Setosa-4",
    "Setosa-5",
    "Versicolor-1",
    "Versicolor-2",
    "Versicolor-3",
    "Versicolor-4",
    "Versicolor-5",
    "Virginica-1",
    "Virginica-2",
    "Virginica-3",
    "Virginica-4",
    "Virginica-5",
]

# Simulated measurements (sepal length, sepal width, petal length, petal width)
# Values are realistic for each iris species
data_matrix = np.array(
    [
        # Setosa (smaller petals, wider sepals)
        [5.0, 3.5, 1.4, 0.2],
        [4.9, 3.0, 1.4, 0.2],
        [4.7, 3.2, 1.3, 0.2],
        [5.1, 3.8, 1.5, 0.3],
        [5.4, 3.4, 1.7, 0.2],
        # Versicolor (medium measurements)
        [5.9, 2.8, 4.5, 1.3],
        [6.0, 2.7, 4.2, 1.2],
        [5.7, 2.6, 4.0, 1.3],
        [6.3, 2.9, 4.6, 1.5],
        [5.5, 2.4, 3.8, 1.1],
        # Virginica (larger petals)
        [6.5, 3.0, 5.5, 2.0],
        [6.7, 3.1, 5.6, 2.1],
        [7.0, 3.2, 5.8, 2.2],
        [6.9, 3.1, 5.4, 2.1],
        [6.3, 2.9, 5.2, 1.8],
    ]
)

# Perform hierarchical clustering
linkage_matrix = linkage(data_matrix, method="ward")

# Build dendrogram structure for Highcharts organization chart
# Convert scipy linkage matrix to parent-child relationships
n_samples = len(labels)
n_merges = len(linkage_matrix)


# Helper function to build tree structure from linkage
def build_tree_data(linkage_matrix, labels):
    """Convert scipy linkage matrix to Highcharts organization data format."""
    n = len(labels)
    nodes = {}
    data = []

    # Create leaf nodes
    for i, label in enumerate(labels):
        nodes[i] = {"id": f"leaf_{i}", "name": label, "level": 0}

    # Process merges
    for idx, (left, right, dist, _count) in enumerate(linkage_matrix):
        left_idx = int(left)
        right_idx = int(right)
        new_node_id = n + idx
        cluster_name = f"Cluster {idx + 1}"

        # Create internal node
        nodes[new_node_id] = {"id": f"cluster_{idx}", "name": cluster_name, "distance": round(dist, 2)}

        # Add edges (from parent to children)
        left_node = nodes[left_idx]
        right_node = nodes[right_idx]

        data.append({"from": f"cluster_{idx}", "to": left_node["id"]})
        data.append({"from": f"cluster_{idx}", "to": right_node["id"]})

    # Build node list with proper formatting
    node_list = []

    # Add leaf nodes (colored by species)
    colors = {"Setosa": "#306998", "Versicolor": "#FFD43B", "Virginica": "#9467BD"}
    for i, label in enumerate(labels):
        species = label.split("-")[0]
        node_list.append({"id": f"leaf_{i}", "name": label, "color": colors.get(species, "#666666")})

    # Add cluster nodes
    for idx in range(n_merges):
        dist = round(linkage_matrix[idx, 2], 2)
        node_list.append({"id": f"cluster_{idx}", "name": f"d={dist}", "color": "#888888"})

    return node_list, data


node_list, edge_data = build_tree_data(linkage_matrix, labels)

# Create chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration
chart.options.chart = {
    "type": "organization",
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#ffffff",
    "inverted": True,  # Draw from left to right (horizontal dendrogram)
}

# Title
chart.options.title = {
    "text": "Iris Species Clustering · dendrogram-basic · highcharts · pyplots.ai",
    "style": {"fontSize": "56px", "fontWeight": "bold"},
}

# Subtitle
chart.options.subtitle = {
    "text": "Hierarchical clustering using Ward linkage",
    "style": {"fontSize": "36px", "color": "#666666"},
}

# Tooltip
chart.options.tooltip = {"outside": True, "style": {"fontSize": "28px"}}

# Disable legend
chart.options.legend = {"enabled": False}

# Credits
chart.options.credits = {"enabled": False}

# Series data
chart.options.series = [
    {
        "type": "organization",
        "name": "Dendrogram",
        "keys": ["from", "to"],
        "data": edge_data,
        "nodes": node_list,
        "colorByPoint": False,
        "nodeWidth": 180,
        "nodePadding": 15,
        "borderRadius": 8,
        "borderWidth": 3,
        "dataLabels": {
            "enabled": True,
            "style": {"fontSize": "24px", "fontWeight": "normal", "textOutline": "none"},
            "nodeFormat": "{point.name}",
        },
        "link": {"type": "curved", "lineWidth": 4, "color": "#aaaaaa"},
        "levels": [
            {"level": 0, "color": "#888888", "dataLabels": {"style": {"fontSize": "22px"}}},
            {"level": 1, "color": "#888888"},
            {"level": 2, "color": "#888888"},
            {"level": 3, "color": "#888888"},
            {"level": 4, "color": "#888888"},
        ],
    }
]

# Download Highcharts JS and required modules
highcharts_url = "https://code.highcharts.com/highcharts.js"
sankey_url = "https://code.highcharts.com/modules/sankey.js"
organization_url = "https://code.highcharts.com/modules/organization.js"

with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

with urllib.request.urlopen(sankey_url, timeout=30) as response:
    sankey_js = response.read().decode("utf-8")

with urllib.request.urlopen(organization_url, timeout=30) as response:
    organization_js = response.read().decode("utf-8")

# Generate HTML with inline scripts
html_str = chart.to_js_literal()
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <script>{sankey_js}</script>
    <script>{organization_js}</script>
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
    <script src="https://code.highcharts.com/modules/sankey.js"></script>
    <script src="https://code.highcharts.com/modules/organization.js"></script>
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
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=4800,2900")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)  # Wait for chart to render
driver.save_screenshot("plot_raw.png")
driver.quit()

# Crop to exact 4800x2700 dimensions
img = Image.open("plot_raw.png")
img_cropped = img.crop((0, 0, 4800, 2700))
img_cropped.save("plot.png")
Path("plot_raw.png").unlink()

Path(temp_path).unlink()  # Clean up temp file
