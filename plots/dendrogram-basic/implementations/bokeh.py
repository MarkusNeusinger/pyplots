"""
dendrogram-basic: Basic Dendrogram
Library: bokeh
"""

import numpy as np
from bokeh.io import export_png, output_file, save
from bokeh.models import FixedTicker, Label
from bokeh.plotting import figure
from scipy.cluster.hierarchy import dendrogram as scipy_dendrogram
from scipy.cluster.hierarchy import linkage
from scipy.spatial.distance import pdist


# Data - Iris-like flower measurements for hierarchical clustering
np.random.seed(42)

labels = [
    "Setosa A",
    "Setosa B",
    "Setosa C",
    "Versicolor A",
    "Versicolor B",
    "Versicolor C",
    "Virginica A",
    "Virginica B",
    "Virginica C",
    "Virginica D",
]

# Simulated measurements (sepal length, sepal width, petal length, petal width)
# Grouped by species with small within-group variation
data = np.array(
    [
        [5.0, 3.4, 1.4, 0.2],  # Setosa A
        [4.9, 3.1, 1.5, 0.2],  # Setosa B
        [5.1, 3.5, 1.3, 0.3],  # Setosa C
        [6.2, 2.9, 4.3, 1.3],  # Versicolor A
        [5.9, 2.8, 4.1, 1.2],  # Versicolor B
        [6.0, 2.7, 4.5, 1.4],  # Versicolor C
        [6.8, 3.2, 5.9, 2.3],  # Virginica A
        [6.5, 3.0, 5.5, 2.0],  # Virginica B
        [7.0, 3.1, 5.8, 2.2],  # Virginica C
        [6.7, 3.3, 5.7, 2.1],  # Virginica D
    ]
)

# Compute linkage matrix using Ward's method
distances = pdist(data, metric="euclidean")
Z = linkage(distances, method="ward")

# Use scipy's dendrogram to get coordinates
dend = scipy_dendrogram(Z, labels=labels, no_plot=True, color_threshold=0)

# Extract dendrogram coordinates
icoord = np.array(dend["icoord"])
dcoord = np.array(dend["dcoord"])

# Create figure (4800 × 2700 px)
p = figure(
    width=4800,
    height=2700,
    title="dendrogram-basic · bokeh · pyplots.ai",
    x_axis_label="",
    y_axis_label="Distance (Ward)",
    x_range=(-5, len(labels) * 10 + 5),
    tools="",
    toolbar_location=None,
    min_border_bottom=250,  # Room for rotated labels
)

# Style the plot - scaled for 4800x2700 canvas
p.title.text_font_size = "48pt"
p.title.text_color = "#306998"
p.yaxis.axis_label_text_font_size = "36pt"
p.yaxis.major_label_text_font_size = "28pt"
p.yaxis.axis_line_width = 3
p.yaxis.major_tick_line_width = 3
p.yaxis.minor_tick_line_width = 2

# Only show positive y-axis ticks (distances are non-negative)
p.yaxis.ticker = FixedTicker(ticks=[0, 2, 4, 6, 8, 10])

# Draw dendrogram branches using multi_line
xs = []
ys = []

for i in range(len(icoord)):
    xs.append(list(icoord[i]))
    ys.append(list(dcoord[i]))

# Draw all branches with Python Blue color
p.multi_line(xs, ys, line_color="#306998", line_width=6, line_alpha=0.9)

# Add leaf labels at the bottom
ivl = dend["ivl"]  # Labels in dendrogram order

# Calculate y-range with space for labels at bottom
max_dist = max(dcoord.flatten())
label_space = max_dist * 0.25  # Reserve 25% of height for labels

# Set y-range with negative space for labels
p.y_range.start = -label_space
p.y_range.end = max_dist * 1.1

# Position labels at proper x positions (each leaf at x = 5, 15, 25, ... in scipy coords)
for i, label in enumerate(ivl):
    x_pos = 5 + i * 10  # scipy uses 5, 15, 25, ... for leaf positions
    label_obj = Label(
        x=x_pos,
        y=-label_space * 0.1,
        text=label,
        text_font_size="28pt",
        text_align="right",
        text_baseline="top",
        angle=45,
        angle_units="deg",
    )
    p.add_layout(label_obj)

# Hide x-axis (we're using custom labels)
p.xaxis.visible = False

# Style grid - only show for positive y values
p.ygrid.grid_line_alpha = 0.3
p.ygrid.grid_line_dash = "dashed"
p.ygrid.grid_line_width = 2
p.xgrid.grid_line_alpha = 0

# Add a horizontal line at y=0 to separate dendrogram from labels
p.line([-5, len(labels) * 10 + 5], [0, 0], line_color="#306998", line_width=2, line_alpha=0.5)

# Background styling
p.background_fill_color = "white"
p.border_fill_color = "white"
p.outline_line_color = None

# Save outputs
export_png(p, filename="plot.png")

# Also save HTML for interactive version
output_file("plot.html")
save(p)
