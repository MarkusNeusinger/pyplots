"""
dendrogram-basic: Basic Dendrogram
Library: altair
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - Iris flower measurements for hierarchical clustering
np.random.seed(42)

# Sample of iris-like data with 15 items for readable dendrogram
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

# Measurements: sepal_length, sepal_width, petal_length, petal_width
data = np.array(
    [
        # Setosa (small petals, wider sepals)
        [5.1, 3.5, 1.4, 0.2],
        [4.9, 3.0, 1.4, 0.2],
        [5.0, 3.4, 1.5, 0.2],
        [4.8, 3.1, 1.4, 0.1],
        [5.2, 3.5, 1.5, 0.2],
        # Versicolor (medium petals)
        [6.4, 3.2, 4.5, 1.5],
        [6.1, 2.8, 4.0, 1.3],
        [5.9, 3.0, 4.2, 1.5],
        [6.3, 2.9, 4.3, 1.3],
        [6.0, 2.7, 4.1, 1.3],
        # Virginica (large petals)
        [7.2, 3.6, 6.1, 2.5],
        [7.4, 2.8, 6.1, 1.9],
        [6.9, 3.1, 5.4, 2.1],
        [7.1, 3.0, 5.9, 2.1],
        [6.8, 3.0, 5.5, 2.1],
    ]
)

n = len(data)

# Compute pairwise Euclidean distances
dist_matrix = np.zeros((n, n))
for i in range(n):
    for j in range(i + 1, n):
        dist_matrix[i, j] = np.sqrt(np.sum((data[i] - data[j]) ** 2))
        dist_matrix[j, i] = dist_matrix[i, j]

# Agglomerative hierarchical clustering (Ward's method approximation using average linkage)
# Track cluster membership and sizes
cluster_id = list(range(n))  # Each point starts as its own cluster
cluster_size = [1] * n
linkage_matrix = []  # Store merge history: [idx1, idx2, distance, size]

# Track which points belong to each cluster
clusters = {i: [i] for i in range(n)}
next_cluster_id = n

for _merge_step in range(n - 1):
    # Find closest pair of clusters
    min_dist = np.inf
    merge_i, merge_j = -1, -1

    active_clusters = list(clusters.keys())
    for i_idx, ci in enumerate(active_clusters):
        for cj in active_clusters[i_idx + 1 :]:
            # Average linkage distance between clusters
            total_dist = 0
            for pi in clusters[ci]:
                for pj in clusters[cj]:
                    total_dist += dist_matrix[pi, pj]
            avg_dist = total_dist / (len(clusters[ci]) * len(clusters[cj]))

            if avg_dist < min_dist:
                min_dist = avg_dist
                merge_i, merge_j = ci, cj

    # Merge clusters
    new_size = len(clusters[merge_i]) + len(clusters[merge_j])
    linkage_matrix.append([merge_i, merge_j, min_dist, new_size])

    # Create new cluster
    clusters[next_cluster_id] = clusters[merge_i] + clusters[merge_j]
    del clusters[merge_i]
    del clusters[merge_j]
    next_cluster_id += 1

linkage_matrix = np.array(linkage_matrix)

# Build dendrogram coordinates from linkage matrix
# Track x-position (center) and height for each cluster
cluster_x = {}  # x-position of cluster center
cluster_height = {}  # height (distance) where cluster was formed

# Initial leaves get evenly spaced x-positions
leaf_order = []  # Will store ordered leaf indices


# Recursively compute leaf order (in-order traversal of dendrogram tree)
def get_leaf_order(cluster_idx, linkage_mat, n_leaves):
    if cluster_idx < n_leaves:
        return [cluster_idx]
    else:
        row = linkage_mat[int(cluster_idx - n_leaves)]
        left = get_leaf_order(int(row[0]), linkage_mat, n_leaves)
        right = get_leaf_order(int(row[1]), linkage_mat, n_leaves)
        return left + right


leaf_order = get_leaf_order(2 * n - 2, linkage_matrix, n)

# Assign x-positions to leaves (spacing of 10, starting at 5 like scipy)
for i, leaf_idx in enumerate(leaf_order):
    cluster_x[leaf_idx] = 5 + i * 10
    cluster_height[leaf_idx] = 0

# Build dendrogram lines
icoord = []  # x coordinates for each link (4 points per U-shape)
dcoord = []  # y coordinates for each link (4 points per U-shape)

for i, (idx1, idx2, dist, _) in enumerate(linkage_matrix):
    idx1, idx2 = int(idx1), int(idx2)
    new_cluster_id = n + i

    x1 = cluster_x[idx1]
    x2 = cluster_x[idx2]
    h1 = cluster_height[idx1]
    h2 = cluster_height[idx2]

    # U-shape: left-bottom, left-top, right-top, right-bottom
    icoord.append([x1, x1, x2, x2])
    dcoord.append([h1, dist, dist, h2])

    # Store new cluster position at center
    cluster_x[new_cluster_id] = (x1 + x2) / 2
    cluster_height[new_cluster_id] = dist

icoord = np.array(icoord)
dcoord = np.array(dcoord)

# Build line segments for the dendrogram
# Each link in the dendrogram is drawn as a U-shape connecting two children to parent
segments = []
for i in range(len(icoord)):
    # Each U-shape has 4 points: left-bottom, left-top, right-top, right-bottom
    xs = icoord[i]
    ys = dcoord[i]

    # Create 3 line segments for the U-shape
    # Vertical left leg
    segments.append({"x1": xs[0], "y1": ys[0], "x2": xs[1], "y2": ys[1], "segment": i * 3})
    # Horizontal bar
    segments.append({"x1": xs[1], "y1": ys[1], "x2": xs[2], "y2": ys[2], "segment": i * 3 + 1})
    # Vertical right leg
    segments.append({"x1": xs[2], "y1": ys[2], "x2": xs[3], "y2": ys[3], "segment": i * 3 + 2})

segments_df = pd.DataFrame(segments)

# Get leaf positions and labels for x-axis
ordered_labels = [labels[i] for i in leaf_order]
leaf_positions = [5 + i * 10 for i in range(len(leaf_order))]

# Create label dataframe
label_df = pd.DataFrame(
    {
        "x": leaf_positions,
        "y": [-0.3] * len(ordered_labels),  # position below axis
        "label": ordered_labels,
    }
)

# Colors - use Python Blue for the dendrogram lines
python_blue = "#306998"

# Create dendrogram chart using rule marks for line segments
dendrogram_chart = (
    alt.Chart(segments_df)
    .mark_rule(color=python_blue, strokeWidth=3)
    .encode(
        x=alt.X("x1:Q", axis=alt.Axis(labels=False, ticks=False, title=None, domain=False)),
        x2="x2:Q",
        y=alt.Y("y1:Q", title="Distance (Ward)", axis=alt.Axis(labelFontSize=18, titleFontSize=22)),
        y2="y2:Q",
    )
)

# Add leaf labels at the bottom
leaf_labels = (
    alt.Chart(label_df)
    .mark_text(
        angle=315,  # Rotate labels (315 = -45 degrees)
        align="right",
        baseline="middle",
        fontSize=16,
        color="#333333",
    )
    .encode(x="x:Q", y="y:Q", text="label:N")
)

# Combine charts
chart = (
    alt.layer(dendrogram_chart, leaf_labels)
    .properties(
        width=1400,
        height=800,
        title=alt.Title(
            "Iris Species Clustering · dendrogram-basic · altair · pyplots.ai", fontSize=28, anchor="middle"
        ),
    )
    .configure_axis(gridColor="#E0E0E0", gridOpacity=0.3, domainColor="#666666")
    .configure_view(strokeWidth=0)
)

# Save
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
