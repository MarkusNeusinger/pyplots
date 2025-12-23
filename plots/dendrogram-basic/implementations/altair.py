""" pyplots.ai
dendrogram-basic: Basic Dendrogram
Library: altair 6.0.0 | Python 3.13.11
Quality: 93/100 | Created: 2025-12-23
"""

import altair as alt
import numpy as np
import pandas as pd
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
n_samples = len(labels)

# Compute hierarchical clustering using Ward's method
Z = linkage(data, method="ward")

# Use scipy's dendrogram function to get proper leaf ordering and coordinates
dendro = dendrogram(Z, labels=labels, no_plot=True)

# Extract coordinates from scipy's dendrogram output (icoord, dcoord)
# Each cluster merge has 4 x-coords and 4 y-coords forming a U-shape
lines_data = []
color_threshold = 0.7 * Z[:, 2].max()

for xpts, ypts in zip(dendro["icoord"], dendro["dcoord"], strict=True):
    # Each U-shape has 3 segments: left vertical, horizontal, right vertical
    # Points: (x0,y0) - (x1,y1) - (x2,y2) - (x3,y3)
    max_height = max(ypts)
    color = "#306998" if max_height > color_threshold else "#FFD43B"

    # Left vertical segment
    lines_data.append({"x": xpts[0], "y": ypts[0], "x2": xpts[1], "y2": ypts[1], "color": color})
    # Horizontal segment
    lines_data.append({"x": xpts[1], "y": ypts[1], "x2": xpts[2], "y2": ypts[2], "color": color})
    # Right vertical segment
    lines_data.append({"x": xpts[2], "y": ypts[2], "x2": xpts[3], "y2": ypts[3], "color": color})

lines_df = pd.DataFrame(lines_data)

# Create label data for x-axis using scipy's leaf positions
ivl = dendro["ivl"]  # Ordered labels from dendrogram
# Labels are positioned at 5, 15, 25, ... (5 + 10*i)
label_positions = [5 + 10 * i for i in range(len(ivl))]
label_data = pd.DataFrame({"x": label_positions, "label": ivl})

# Get x-axis domain from the dendrogram coordinates
x_min = min(min(xpts) for xpts in dendro["icoord"]) - 5
x_max = max(max(xpts) for xpts in dendro["icoord"]) + 5

# Create the dendrogram lines chart
dendrogram_lines = (
    alt.Chart(lines_df)
    .mark_rule(strokeWidth=3)
    .encode(
        x=alt.X("x:Q", axis=None, scale=alt.Scale(domain=[x_min, x_max])),
        x2="x2:Q",
        y=alt.Y("y:Q", title="Distance (Ward)", scale=alt.Scale(domain=[0, Z[:, 2].max() * 1.1])),
        y2="y2:Q",
        color=alt.Color("color:N", scale=None),
    )
)

# Create x-axis labels at bottom
x_labels = (
    alt.Chart(label_data)
    .mark_text(angle=315, align="right", baseline="top", fontSize=14)
    .encode(x=alt.X("x:Q", axis=None, scale=alt.Scale(domain=[x_min, x_max])), y=alt.value(850), text="label:N")
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
