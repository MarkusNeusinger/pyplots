"""
dendrogram-basic: Basic Dendrogram
Library: plotnine
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    element_blank,
    element_text,
    geom_segment,
    geom_text,
    ggplot,
    labs,
    scale_x_continuous,
    scale_y_continuous,
    theme,
    theme_minimal,
)
from scipy.cluster.hierarchy import linkage


np.random.seed(42)

# Data - Iris flower species measurements for hierarchical clustering
# Using 15 samples for readable dendrogram
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

# Sample measurements (sepal length, sepal width, petal length, petal width)
# Setosa: small petals, distinct
data = np.array(
    [
        [5.1, 3.5, 1.4, 0.2],  # Setosa samples
        [4.9, 3.0, 1.4, 0.2],
        [4.7, 3.2, 1.3, 0.2],
        [5.0, 3.6, 1.4, 0.2],
        [5.4, 3.9, 1.7, 0.4],
        [7.0, 3.2, 4.7, 1.4],  # Versicolor samples
        [6.4, 3.2, 4.5, 1.5],
        [6.9, 3.1, 4.9, 1.5],
        [5.5, 2.3, 4.0, 1.3],
        [6.5, 2.8, 4.6, 1.5],
        [6.3, 3.3, 6.0, 2.5],  # Virginica samples
        [5.8, 2.7, 5.1, 1.9],
        [7.1, 3.0, 5.9, 2.1],
        [6.5, 3.0, 5.8, 2.2],
        [7.6, 3.0, 6.6, 2.1],
    ]
)

# Compute hierarchical clustering using Ward's method
Z = linkage(data, method="ward")


def get_dendrogram_segments(Z, labels):
    """
    Extract segment coordinates from linkage matrix for plotting.
    Returns DataFrames for horizontal and vertical segments.
    """
    n = len(labels)

    # Track the position and height of each node
    # Initial leaves are at positions 0, 1, 2, ..., n-1 with height 0
    node_pos = {i: i for i in range(n)}
    node_height = dict.fromkeys(range(n), 0)

    h_segments = []  # horizontal segments
    v_segments = []  # vertical segments

    for i, (left, right, height, _) in enumerate(Z):
        left, right = int(left), int(right)
        new_node = n + i

        # Get positions and heights of children
        left_pos = node_pos[left]
        right_pos = node_pos[right]
        left_height = node_height[left]
        right_height = node_height[right]

        # New node position is midpoint of children
        new_pos = (left_pos + right_pos) / 2

        # Vertical segment from left child to merge height
        v_segments.append({"x": left_pos, "xend": left_pos, "y": left_height, "yend": height})

        # Vertical segment from right child to merge height
        v_segments.append({"x": right_pos, "xend": right_pos, "y": right_height, "yend": height})

        # Horizontal segment connecting the two at merge height
        h_segments.append({"x": left_pos, "xend": right_pos, "y": height, "yend": height})

        # Update node tracking
        node_pos[new_node] = new_pos
        node_height[new_node] = height

    return pd.DataFrame(h_segments), pd.DataFrame(v_segments)


# Get dendrogram segments
df_h, df_v = get_dendrogram_segments(Z, labels)

# Combine all segments
df_segments = pd.concat([df_h, df_v], ignore_index=True)

# Create label DataFrame (at bottom of dendrogram)
df_labels = pd.DataFrame(
    {
        "x": range(len(labels)),
        "y": [-0.5] * len(labels),  # Position below dendrogram
        "label": labels,
    }
)

# Calculate y-axis limits
max_height = df_segments["yend"].max()

# Plot
plot = (
    ggplot()
    + geom_segment(aes(x="x", xend="xend", y="y", yend="yend"), data=df_segments, color="#306998", size=1.5)
    + geom_text(aes(x="x", y="y", label="label"), data=df_labels, angle=45, ha="right", va="top", size=11)
    + scale_x_continuous(limits=(-1.5, len(labels) + 0.5))
    + scale_y_continuous(limits=(-4, max_height * 1.05))
    + labs(
        title="Iris Species Hierarchical Clustering · dendrogram-basic · plotnine · pyplots.ai",
        x="",
        y="Distance (Ward)",
    )
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        plot_title=element_text(size=24),
        axis_title_y=element_text(size=20),
        axis_text_y=element_text(size=16),
        axis_text_x=element_blank(),
        panel_grid_major_x=element_blank(),
        panel_grid_minor_x=element_blank(),
    )
)

plot.save("plot.png", dpi=300, verbose=False)
