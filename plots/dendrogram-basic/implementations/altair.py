""" pyplots.ai
dendrogram-basic: Basic Dendrogram
Library: altair 6.0.0 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-17
"""

import altair as alt
import numpy as np
import pandas as pd
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
            5.0 + np.random.randn() * 0.3,  # sepal length
            3.4 + np.random.randn() * 0.3,  # sepal width
            1.5 + np.random.randn() * 0.2,  # petal length
            0.3 + np.random.randn() * 0.1,  # petal width
        ]
    )

# Versicolor: medium measurements
for i in range(samples_per_species):
    labels.append(f"Versicolor-{i + 1}")
    data.append(
        [
            5.9 + np.random.randn() * 0.4,  # sepal length
            2.8 + np.random.randn() * 0.3,  # sepal width
            4.3 + np.random.randn() * 0.4,  # petal length
            1.3 + np.random.randn() * 0.2,  # petal width
        ]
    )

# Virginica: longer petals and sepals
for i in range(samples_per_species):
    labels.append(f"Virginica-{i + 1}")
    data.append(
        [
            6.6 + np.random.randn() * 0.5,  # sepal length
            3.0 + np.random.randn() * 0.3,  # sepal width
            5.5 + np.random.randn() * 0.5,  # petal length
            2.0 + np.random.randn() * 0.3,  # petal width
        ]
    )

data = np.array(data)
n_samples = len(labels)

# Compute hierarchical clustering using Ward's method
Z = linkage(data, method="ward")


# Build dendrogram structure from linkage matrix
# Track x-positions and heights for each node
node_positions = {}  # node_id -> (x_pos, height)
next_cluster_id = n_samples

# Initialize leaf positions (will be reordered based on linkage)
leaf_order = []


# Recursive function to get leaf order from linkage
def get_leaf_order(node_id, Z, n):
    """Get the order of leaves under a given node."""
    if node_id < n:
        return [node_id]
    else:
        row = Z[node_id - n]
        left = int(row[0])
        right = int(row[1])
        return get_leaf_order(left, Z, n) + get_leaf_order(right, Z, n)


# Get proper leaf ordering from hierarchical structure
leaf_order = get_leaf_order(2 * n_samples - 2, Z, n_samples)

# Assign x-positions to leaves based on their order
leaf_x_positions = {leaf_id: i for i, leaf_id in enumerate(leaf_order)}

# Initialize leaf nodes with height 0
for leaf_id, x_pos in leaf_x_positions.items():
    node_positions[leaf_id] = (x_pos, 0)

# Build line segments for dendrogram
lines_data = []

# Color threshold for distinguishing clusters (70% of max height)
color_threshold = 0.7 * Z[:, 2].max()

for i, row in enumerate(Z):
    left_id = int(row[0])
    right_id = int(row[1])
    merge_height = row[2]
    new_cluster_id = n_samples + i

    left_x, left_h = node_positions[left_id]
    right_x, right_h = node_positions[right_id]

    # New cluster x-position is the mean of children
    new_x = (left_x + right_x) / 2
    node_positions[new_cluster_id] = (new_x, merge_height)

    # Determine color based on merge height
    color = "#306998" if merge_height > color_threshold else "#FFD43B"

    # Left vertical line (from left child to merge height)
    lines_data.append(
        {"x": left_x, "y": left_h, "x2": left_x, "y2": merge_height, "color": color, "segment": f"v_left_{i}"}
    )

    # Right vertical line (from right child to merge height)
    lines_data.append(
        {"x": right_x, "y": right_h, "x2": right_x, "y2": merge_height, "color": color, "segment": f"v_right_{i}"}
    )

    # Horizontal line connecting left and right at merge height
    lines_data.append(
        {"x": left_x, "y": merge_height, "x2": right_x, "y2": merge_height, "color": color, "segment": f"h_{i}"}
    )

lines_df = pd.DataFrame(lines_data)

# Create label data for x-axis
label_data = pd.DataFrame(
    {"x": [leaf_x_positions[leaf_id] for leaf_id in leaf_order], "label": [labels[leaf_id] for leaf_id in leaf_order]}
)

# Create the dendrogram lines chart with padding on x-axis
x_padding = 0.5  # Add space on left and right edges
dendrogram_lines = (
    alt.Chart(lines_df)
    .mark_rule(strokeWidth=3)
    .encode(
        x=alt.X("x:Q", axis=None, scale=alt.Scale(domain=[-x_padding, n_samples - 1 + x_padding])),
        x2="x2:Q",
        y=alt.Y("y:Q", title="Distance (Ward)", scale=alt.Scale(domain=[0, Z[:, 2].max() * 1.05])),
        y2="y2:Q",
        color=alt.Color("color:N", scale=None),
    )
)

# Create x-axis labels at bottom (positioned inside chart area)
x_labels = (
    alt.Chart(label_data)
    .mark_text(angle=315, align="right", baseline="top", fontSize=14)
    .encode(
        x=alt.X("x:Q", axis=None, scale=alt.Scale(domain=[-x_padding, n_samples - 1 + x_padding])),
        y=alt.value(830),
        text="label:N",
    )
)

# Combine charts
chart = (
    alt.layer(dendrogram_lines, x_labels)
    .properties(width=1600, height=900, title=alt.Title("dendrogram-basic · altair · pyplots.ai", fontSize=28))
    .configure_axis(labelFontSize=18, titleFontSize=22, gridOpacity=0.3, gridDash=[4, 4])
    .configure_view(strokeWidth=0)
)

# Save
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
