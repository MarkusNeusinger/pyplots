"""
dendrogram-basic: Basic Dendrogram
Library: bokeh
"""

import numpy as np
from bokeh.io import export_png
from bokeh.models import Label
from bokeh.plotting import figure, output_file, save
from scipy.cluster.hierarchy import leaves_list, linkage


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

# Get leaf order for x-axis positioning
leaf_order = leaves_list(linkage_matrix)
ordered_labels = [labels[i] for i in leaf_order]

# Build dendrogram structure manually
# Position of each node (leaf nodes get integer positions)
node_positions = {}
for idx, leaf_idx in enumerate(leaf_order):
    node_positions[leaf_idx] = idx

# Color threshold for distinguishing clusters
max_dist = linkage_matrix[:, 2].max()
color_threshold = 0.7 * max_dist

# Collect line segments for drawing
line_xs = []
line_ys = []
line_colors = []

# Process each merge in the linkage matrix
for i, (left, right, dist, _) in enumerate(linkage_matrix):
    left, right = int(left), int(right)
    new_node = n_samples + i

    # Get x positions of children
    left_x = node_positions[left]
    right_x = node_positions[right]

    # Get y positions (heights) of children
    if left < n_samples:
        left_y = 0
    else:
        left_y = linkage_matrix[left - n_samples, 2]

    if right < n_samples:
        right_y = 0
    else:
        right_y = linkage_matrix[right - n_samples, 2]

    # New node position is midpoint of children
    new_x = (left_x + right_x) / 2
    node_positions[new_node] = new_x

    # Determine color based on threshold
    color = "#306998" if dist > color_threshold else "#FFD43B"

    # Draw left vertical line
    line_xs.append([left_x, left_x])
    line_ys.append([left_y, dist])
    line_colors.append(color)

    # Draw right vertical line
    line_xs.append([right_x, right_x])
    line_ys.append([right_y, dist])
    line_colors.append(color)

    # Draw horizontal line connecting the two
    line_xs.append([left_x, right_x])
    line_ys.append([dist, dist])
    line_colors.append(color)

# Create figure with extra space at bottom for labels
p = figure(
    width=4800,
    height=2700,
    title="dendrogram-basic · bokeh · pyplots.ai",
    x_axis_label="Sample",
    y_axis_label="Distance (Ward)",
    x_range=(-0.5, n_samples - 0.5),
    y_range=(-max_dist * 0.15, max_dist * 1.1),
)

# Draw dendrogram lines
for xs, ys, color in zip(line_xs, line_ys, line_colors, strict=True):
    p.line(xs, ys, line_width=3, line_color=color)

# Add leaf labels
for idx, label in enumerate(ordered_labels):
    label_obj = Label(
        x=idx,
        y=-max_dist * 0.01,
        text=label,
        text_font_size="16pt",
        text_align="right",
        angle=0.785,  # 45 degrees in radians
        angle_units="rad",
        y_offset=-10,
    )
    p.add_layout(label_obj)

# Style
p.title.text_font_size = "28pt"
p.xaxis.axis_label_text_font_size = "22pt"
p.yaxis.axis_label_text_font_size = "22pt"
p.xaxis.major_label_text_font_size = "0pt"  # Hide default x-axis labels
p.yaxis.major_label_text_font_size = "18pt"

# Grid styling
p.xgrid.visible = False
p.ygrid.grid_line_alpha = 0.3
p.ygrid.grid_line_dash = "dashed"

# Remove tick marks on x-axis
p.xaxis.major_tick_line_color = None
p.xaxis.minor_tick_line_color = None

# Clean outline
p.outline_line_color = None

# Save outputs
export_png(p, filename="plot.png")
output_file("plot.html")
save(p)
