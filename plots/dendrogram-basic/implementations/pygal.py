""" pyplots.ai
dendrogram-basic: Basic Dendrogram
Library: pygal 3.1.0 | Python 3.13.11
Quality: 85/100 | Created: 2025-12-23
"""

import numpy as np
import pygal
from pygal.style import Style
from scipy.cluster.hierarchy import linkage


# Data - Iris flower measurements (4 features for 15 samples)
np.random.seed(42)

# Simulate iris-like measurements: sepal length, sepal width, petal length, petal width
# Three species with distinct characteristics
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

# Compute hierarchical clustering using Ward's method
linkage_matrix = linkage(data, method="ward")

# Build dendrogram coordinates from linkage matrix
n = len(labels)

# Track x-position and height for each node (original samples + merged clusters)
node_x = {}
node_height = {}

# Compute leaf order from linkage for proper x-axis positioning (iterative approach)
root_node = 2 * n - 2
stack = [root_node]
leaf_order = []
while stack:
    node_id = stack.pop()
    if node_id < n:
        leaf_order.append(node_id)
    else:
        idx = node_id - n
        left = int(linkage_matrix[idx, 0])
        right = int(linkage_matrix[idx, 1])
        # Push right first so left is processed first (maintains order)
        stack.append(right)
        stack.append(left)

# Initialize leaf positions based on their order in the dendrogram
for pos, leaf_id in enumerate(leaf_order):
    node_x[leaf_id] = pos
    node_height[leaf_id] = 0

# Build merged clusters and collect line segments
segments = []
for idx, (left, right, dist, _) in enumerate(linkage_matrix):
    left, right = int(left), int(right)
    new_node = n + idx

    # X position is midpoint of children
    x_left = node_x[left]
    x_right = node_x[right]
    node_x[new_node] = (x_left + x_right) / 2
    node_height[new_node] = dist

    # Draw U-shape: left vertical, horizontal connector, right vertical
    h_left = node_height[left]
    h_right = node_height[right]

    # Left vertical line (from left child up to merge height)
    segments.append([(x_left, h_left), (x_left, dist)])
    # Horizontal connector at merge height
    segments.append([(x_left, dist), (x_right, dist)])
    # Right vertical line (from right child up to merge height)
    segments.append([(x_right, h_right), (x_right, dist)])

# Labels in dendrogram order
ordered_labels = [labels[i] for i in leaf_order]

# Custom style for pyplots - larger fonts for 4800x2700 canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333",
    foreground_strong="#333",
    foreground_subtle="#666",
    colors=("#306998",),  # Python Blue for dendrogram lines
    title_font_size=56,
    label_font_size=36,
    major_label_font_size=32,
    legend_font_size=32,
    value_font_size=28,
    stroke_width=5,
    opacity=1.0,
)

# Create XY chart for dendrogram
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="dendrogram-basic · pygal · pyplots.ai",
    x_title="Sample",
    y_title="Distance (Ward's Method)",
    show_legend=False,
    show_dots=False,
    stroke_style={"width": 5},
    fill=False,
    show_x_guides=False,
    show_y_guides=True,
    x_label_rotation=45,
    truncate_label=20,
)

# Set x-axis labels to show sample names in dendrogram order
chart.x_labels = ordered_labels

# Add each segment as a separate series to draw the dendrogram
for seg in segments:
    chart.add(None, seg, show_dots=False, stroke_style={"width": 5})

# Save outputs
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
