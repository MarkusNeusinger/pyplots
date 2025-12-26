""" pyplots.ai
silhouette-basic: Silhouette Plot
Library: pygal 3.1.0 | Python 3.13.11
Quality: 85/100 | Created: 2025-12-26
"""

import numpy as np
import pygal
from pygal.style import Style
from sklearn.cluster import KMeans
from sklearn.datasets import load_iris
from sklearn.metrics import silhouette_samples, silhouette_score


# Data - Cluster iris dataset into 3 groups
np.random.seed(42)
iris = load_iris()
X = iris.data
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
cluster_labels = kmeans.fit_predict(X)

# Compute silhouette scores
silhouette_vals = silhouette_samples(X, cluster_labels)
avg_silhouette = silhouette_score(X, cluster_labels)
n_clusters = 3

# Colors for each cluster (Python Blue, Python Yellow, Red)
cluster_colors = ["#306998", "#FFD43B", "#E74C3C"]

# Custom style for pyplots
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=tuple(cluster_colors),
    title_font_size=48,
    label_font_size=32,
    major_label_font_size=28,
    legend_font_size=28,
    value_font_size=24,
    stroke_width=0,
)

# Process and sort silhouette values within each cluster (descending for visual appeal)
all_bars = []
cluster_avgs = {}

for i in range(n_clusters):
    cluster_silhouette_vals = silhouette_vals[cluster_labels == i]
    cluster_silhouette_vals = np.sort(cluster_silhouette_vals)[::-1]  # Descending
    cluster_avgs[i] = np.mean(cluster_silhouette_vals)

    for val in cluster_silhouette_vals:
        all_bars.append((i, val))

# Create horizontal bar chart for silhouette plot
chart = pygal.HorizontalStackedBar(
    width=4800,
    height=2700,
    style=custom_style,
    title=f"silhouette-basic \u00b7 pygal \u00b7 pyplots.ai\nOverall Average Silhouette Score: {avg_silhouette:.3f}",
    x_title="Silhouette Coefficient",
    y_title="Samples (grouped by cluster)",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=3,
    show_y_guides=False,
    show_x_guides=True,
    print_values=False,
    range=(-0.2, 1.0),
    spacing=0,
    margin=50,
    margin_bottom=150,
    stack_from_top=True,
    show_y_labels=False,  # Hide crowded sample labels
)

# Build data series for each cluster
cluster_names = [
    f"Cluster 0 (avg: {cluster_avgs[0]:.3f})",
    f"Cluster 1 (avg: {cluster_avgs[1]:.3f})",
    f"Cluster 2 (avg: {cluster_avgs[2]:.3f})",
]

for cluster_idx in range(n_clusters):
    series_data = []
    for c, val in all_bars:
        if c == cluster_idx:
            series_data.append(val)
        else:
            series_data.append(None)
    chart.add(cluster_names[cluster_idx], series_data)

# Save outputs
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
