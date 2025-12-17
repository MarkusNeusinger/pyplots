"""
dendrogram-basic: Basic Dendrogram
Library: lets-plot
"""

import numpy as np
import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    element_blank,
    element_text,
    geom_segment,
    geom_text,
    ggplot,
    ggsize,
    labs,
    scale_color_manual,
    scale_x_continuous,
    scale_y_continuous,
    theme,
    theme_minimal,
)
from lets_plot.export import ggsave
from scipy.cluster.hierarchy import linkage


LetsPlot.setup_html()

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
linkage_matrix = linkage(data, method="ward")


# Build dendrogram coordinates from linkage matrix
def build_dendrogram_coords(linkage_matrix, labels):
    """
    Convert linkage matrix to coordinates for plotting dendrogram segments.
    Returns list of segments (x0, y0, x1, y1, color) for drawing.
    """
    n = len(labels)
    # Position of each leaf (original samples)
    leaf_positions = {i: i for i in range(n)}

    # Track y-position (height) of each node
    node_heights = dict.fromkeys(range(n), 0)

    # Store segments for plotting
    segments = []

    # Color threshold for clustering (similar to matplotlib's default)
    max_dist = linkage_matrix[:, 2].max()
    color_threshold = 0.7 * max_dist

    # Process each merge in the linkage matrix
    for i, (left, right, dist, _) in enumerate(linkage_matrix):
        left, right = int(left), int(right)
        new_node = n + i

        # Get positions of children
        left_pos = leaf_positions[left]
        right_pos = leaf_positions[right]

        # New node position is midpoint of children
        new_pos = (left_pos + right_pos) / 2
        leaf_positions[new_node] = new_pos
        node_heights[new_node] = dist

        # Determine color based on height threshold
        color = "#306998" if dist >= color_threshold else "#FFD43B"

        left_height = node_heights[left]
        right_height = node_heights[right]

        # Vertical segment from left child to merge height
        segments.append((left_pos, left_height, left_pos, dist, color))
        # Vertical segment from right child to merge height
        segments.append((right_pos, right_height, right_pos, dist, color))
        # Horizontal segment connecting the two
        segments.append((left_pos, dist, right_pos, dist, color))

    return segments, leaf_positions


# Build dendrogram
segments, leaf_positions = build_dendrogram_coords(linkage_matrix, labels)

# Create segment dataframe
segment_df = pd.DataFrame(segments, columns=["x", "y", "xend", "yend", "color"])

# Create label dataframe for x-axis labels
label_data = []
for i, label in enumerate(labels):
    label_data.append({"x": leaf_positions[i], "y": -0.8, "label": label})
label_df = pd.DataFrame(label_data)

# Plot
plot = (
    ggplot()
    + geom_segment(aes(x="x", y="y", xend="xend", yend="yend", color="color"), data=segment_df, size=1.5)
    + geom_text(aes(x="x", y="y", label="label"), data=label_df, angle=35, hjust=1, vjust=1, size=10, color="#333333")
    + scale_color_manual(values={"#306998": "#306998", "#FFD43B": "#FFD43B"}, guide="none")
    + scale_x_continuous(expand=[0.06, 0.02])  # Add space on left side for labels
    + scale_y_continuous(expand=[0.18, 0.02])  # Add space at bottom for labels, top margin
    + labs(x="Sample", y="Distance (Ward)", title="dendrogram-basic \u00b7 letsplot \u00b7 pyplots.ai")
    + theme_minimal()
    + theme(
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        axis_text_x=element_blank(),  # Hide default x-axis text (we use custom labels)
        axis_ticks_x=element_blank(),
        plot_title=element_text(size=24),
        panel_grid_major_x=element_blank(),
        panel_grid_minor_x=element_blank(),
    )
    + ggsize(1600, 900)
)

# Save PNG (scale=3 gives 4800x2700)
ggsave(plot, "plot.png", path=".", scale=3)

# Save HTML for interactivity
ggsave(plot, "plot.html", path=".")
