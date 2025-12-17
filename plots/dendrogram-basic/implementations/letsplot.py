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
    element_line,
    element_text,
    geom_segment,
    geom_text,
    ggplot,
    ggsize,
    labs,
    scale_x_continuous,
    scale_y_continuous,
    theme,
    theme_minimal,
)
from lets_plot.export import ggsave
from scipy.cluster.hierarchy import linkage


LetsPlot.setup_html()

# Data - Iris flower measurements for hierarchical clustering
np.random.seed(42)
labels = [
    "Setosa-1",
    "Setosa-2",
    "Setosa-3",
    "Setosa-4",
    "Versicolor-1",
    "Versicolor-2",
    "Versicolor-3",
    "Virginica-1",
    "Virginica-2",
    "Virginica-3",
    "Setosa-5",
    "Versicolor-4",
    "Virginica-4",
    "Virginica-5",
]

# Simulated iris measurements (sepal length, sepal width, petal length, petal width)
# Setosa: small petals, moderate sepals
# Versicolor: medium everything
# Virginica: large petals, larger sepals
measurements = np.array(
    [
        [5.1, 3.5, 1.4, 0.2],  # Setosa-1
        [4.9, 3.0, 1.4, 0.2],  # Setosa-2
        [5.0, 3.4, 1.5, 0.2],  # Setosa-3
        [4.8, 3.1, 1.4, 0.1],  # Setosa-4
        [6.1, 2.9, 4.7, 1.4],  # Versicolor-1
        [5.8, 2.7, 4.1, 1.0],  # Versicolor-2
        [6.0, 2.8, 4.5, 1.3],  # Versicolor-3
        [6.5, 3.0, 5.8, 2.2],  # Virginica-1
        [6.7, 3.1, 5.6, 2.1],  # Virginica-2
        [6.9, 3.2, 5.7, 2.3],  # Virginica-3
        [5.2, 3.5, 1.5, 0.2],  # Setosa-5
        [5.9, 2.8, 4.3, 1.3],  # Versicolor-4
        [6.4, 2.8, 5.6, 2.1],  # Virginica-4
        [6.8, 3.0, 5.5, 2.1],  # Virginica-5
    ]
)

# Compute hierarchical clustering using Ward's method
Z = linkage(measurements, method="ward")

n_samples = len(labels)


# Function to extract dendrogram coordinates from linkage matrix
def get_dendrogram_coords(Z, labels):
    """Extract line segments for drawing dendrogram."""
    n = len(labels)

    # Track x-position and height of each node
    node_x = {}  # x-position of each node (leaf or internal)
    node_h = {}  # height of each node

    # Initialize leaf nodes (evenly spaced)
    for i in range(n):
        node_x[i] = i
        node_h[i] = 0

    # Build internal nodes from linkage matrix
    segments = []
    for i, row in enumerate(Z):
        left, right, height, _ = row
        left, right = int(left), int(right)

        new_node = n + i

        # Get x positions of children
        left_x = node_x[left]
        right_x = node_x[right]
        left_h = node_h[left]
        right_h = node_h[right]

        # New node x is midpoint of children
        new_x = (left_x + right_x) / 2
        node_x[new_node] = new_x
        node_h[new_node] = height

        # Add segments: vertical lines up from children, horizontal connector
        # Left vertical line (from child height to merge height)
        segments.append({"x": left_x, "xend": left_x, "y": left_h, "yend": height})
        # Right vertical line
        segments.append({"x": right_x, "xend": right_x, "y": right_h, "yend": height})
        # Horizontal connector at merge height
        segments.append({"x": left_x, "xend": right_x, "y": height, "yend": height})

    return segments, node_x


# Get dendrogram segments and leaf positions
segments, leaf_positions = get_dendrogram_coords(Z, labels)
segments_df = pd.DataFrame(segments)

# Create leaf labels dataframe
leaf_df = pd.DataFrame(
    {
        "x": [leaf_positions[i] for i in range(n_samples)],
        "y": [-0.3] * n_samples,  # Slightly below the baseline
        "label": labels,
    }
)

# Get max height for axis scaling
max_height = Z[:, 2].max()

# Plot
plot = (
    ggplot()
    + geom_segment(aes(x="x", y="y", xend="xend", yend="yend"), data=segments_df, color="#306998", size=1.5)
    + geom_text(aes(x="x", y="y", label="label"), data=leaf_df, angle=45, hjust=1, size=11, color="#333333")
    + scale_x_continuous(limits=(-1, n_samples))
    + scale_y_continuous(limits=(-max_height * 0.35, max_height * 1.1))
    + labs(title="dendrogram-basic \u00b7 lets-plot \u00b7 pyplots.ai", x="", y="Distance (Ward)")
    + ggsize(1600, 900)
    + theme_minimal()
    + theme(
        plot_title=element_text(size=24, hjust=0.5),
        axis_title_y=element_text(size=20),
        axis_text_y=element_text(size=16),
        axis_text_x=element_blank(),
        axis_ticks_x=element_blank(),
        panel_grid_major_x=element_blank(),
        panel_grid_minor_x=element_blank(),
        panel_grid_major_y=element_line(color="#CCCCCC", size=0.5, linetype="dashed"),
    )
)

# Save PNG (scale 3x to get 4800 x 2700 px)
ggsave(plot, "plot.png", path=".", scale=3)

# Save HTML for interactive version
ggsave(plot, "plot.html", path=".")
