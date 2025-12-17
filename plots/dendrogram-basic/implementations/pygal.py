"""
dendrogram-basic: Basic Dendrogram
Library: pygal
"""

import numpy as np
import pygal
from pygal.style import Style
from scipy.cluster.hierarchy import dendrogram, linkage


# Data - Sample measurements for hierarchical clustering (like iris features)
np.random.seed(42)

# Create 10 samples representing different categories with distinguishable clusters
# Group 1: High values (samples 0-3)
group1 = np.random.randn(4, 4) + np.array([5, 5, 5, 5])
# Group 2: Medium values (samples 4-6)
group2 = np.random.randn(3, 4) + np.array([0, 0, 0, 0])
# Group 3: Low values (samples 7-9)
group3 = np.random.randn(3, 4) + np.array([-5, -5, -5, -5])

data = np.vstack([group1, group2, group3])
labels = ["A1", "A2", "A3", "A4", "B1", "B2", "B3", "C1", "C2", "C3"]

# Compute hierarchical clustering linkage matrix
Z = linkage(data, method="ward")

# Get dendrogram coordinates
dn = dendrogram(Z, labels=labels, no_plot=True)

# Map x positions to sample labels
# Dendrogram positions leaves at 5, 15, 25, etc.
n_leaves = len(dn["ivl"])
x_positions = [5 + i * 10 for i in range(n_leaves)]
pos_to_label = dict(zip(x_positions, dn["ivl"], strict=True))


def x_label_formatter(x):
    """Map x position to sample label."""
    return pos_to_label.get(int(x), "")


# Custom style for 4800x2700 px
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333",
    foreground_strong="#333",
    foreground_subtle="#666",
    colors=("#306998",),
    title_font_size=72,
    label_font_size=36,
    major_label_font_size=36,
    legend_font_size=42,
    value_font_size=36,
    tooltip_font_size=36,
    stroke_width=5,
)

# Create XY chart to draw dendrogram branches
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="dendrogram-basic \u00b7 pygal \u00b7 pyplots.ai",
    x_title="Samples",
    y_title="Distance (Ward)",
    stroke=True,
    stroke_style={"width": 5},
    show_dots=False,
    show_legend=False,
    show_x_guides=False,
    show_y_guides=True,
    truncate_label=-1,
    x_value_formatter=x_label_formatter,
)

# Build dendrogram branch points with None separators
all_points = []
for icoord, dcoord in zip(dn["icoord"], dn["dcoord"], strict=True):
    # Each branch is a U-shape with 4 points
    for i in range(4):
        all_points.append((icoord[i], dcoord[i]))
    all_points.append(None)  # Separator to break line between branches

chart.add("Dendrogram", all_points)

# Set x-axis labels at leaf positions only
chart.x_labels = x_positions

# Save as PNG and HTML
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
