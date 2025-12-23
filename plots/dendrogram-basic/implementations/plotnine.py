"""pyplots.ai
dendrogram-basic: Basic Dendrogram
Library: plotnine | Python 3.13
Quality: pending | Created: 2025-12-23
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    element_blank,
    element_line,
    element_text,
    geom_segment,
    geom_text,
    ggplot,
    labs,
    scale_color_manual,
    scale_x_continuous,
    scale_y_continuous,
    theme,
    theme_minimal,
)
from scipy.cluster.hierarchy import dendrogram, linkage


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

# Compute hierarchical clustering using Ward's method
linkage_matrix = linkage(data, method="ward")

# Extract dendrogram coordinates using scipy (no_plot=True returns coordinates only)
dend = dendrogram(linkage_matrix, labels=labels, no_plot=True)

# Convert dendrogram coordinates to segment data for plotnine
# icoord contains x coords (pairs of 4 for each merge)
# dcoord contains y coords (pairs of 4 for each merge)
segments = []
color_threshold = 0.7 * max(linkage_matrix[:, 2])

for xs, ys in zip(dend["icoord"], dend["dcoord"], strict=True):
    # Each merge has 4 points forming a U-shape: [x1, x2, x3, x4], [y1, y2, y3, y4]
    # We need 3 segments: left vertical, horizontal, right vertical

    # Determine color based on height (merge distance)
    merge_height = max(ys)
    if merge_height > color_threshold:
        color = "#306998"  # Python Blue for high-level merges
    else:
        color = "#FFD43B"  # Python Yellow for low-level merges

    segments.append({"x": xs[0], "xend": xs[1], "y": ys[0], "yend": ys[1], "color": color})
    segments.append({"x": xs[1], "xend": xs[2], "y": ys[1], "yend": ys[2], "color": color})
    segments.append({"x": xs[2], "xend": xs[3], "y": ys[2], "yend": ys[3], "color": color})

segments_df = pd.DataFrame(segments)

# Create label data using the actual leaf positions from dendrogram
# dend['leaves'] gives the order, and x positions are at 5, 15, 25, ... (spacing of 10)
leaf_positions = [(i + 1) * 10 - 5 for i in range(len(dend["ivl"]))]
ivl = dend["ivl"]  # Reordered labels from dendrogram
label_df = pd.DataFrame({"x": leaf_positions, "label": ivl, "y": [-0.8] * len(ivl)})

# Plot using plotnine's native geom_segment
plot = (
    ggplot()
    + geom_segment(aes(x="x", xend="xend", y="y", yend="yend", color="color"), data=segments_df, size=1.8)
    + geom_text(aes(x="x", y="y", label="label"), data=label_df, angle=45, ha="right", va="top", size=9)
    + scale_color_manual(values={"#306998": "#306998", "#FFD43B": "#FFD43B"}, guide=None)
    + scale_x_continuous(breaks=[], expand=(0.12, 0.05))
    + scale_y_continuous(expand=(0.25, 0.02))
    + labs(x="Sample", y="Distance (Ward)", title="dendrogram-basic · plotnine · pyplots.ai")
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        text=element_text(size=14),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        axis_text_x=element_blank(),
        plot_title=element_text(size=24),
        panel_grid_major_x=element_blank(),
        panel_grid_minor_x=element_blank(),
        panel_grid_major_y=element_line(alpha=0.3, linetype="dashed"),
    )
)

plot.save("plot.png", dpi=300)
