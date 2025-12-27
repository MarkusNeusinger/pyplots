""" pyplots.ai
dendrogram-basic: Basic Dendrogram
Library: plotly 6.5.0 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-23
"""

import numpy as np
import plotly.figure_factory as ff


# Data - Iris-like flower measurements for 15 samples
np.random.seed(42)
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

# Create clustered data representing flower measurements (sepal length, sepal width, petal length, petal width)
# Setosa: small petals, medium sepals
setosa = np.random.randn(5, 4) * 0.3 + np.array([5.0, 3.4, 1.5, 0.2])
# Versicolor: medium measurements
versicolor = np.random.randn(5, 4) * 0.4 + np.array([5.9, 2.8, 4.3, 1.3])
# Virginica: large petals and sepals
virginica = np.random.randn(5, 4) * 0.4 + np.array([6.6, 3.0, 5.5, 2.0])

data = np.vstack([setosa, versicolor, virginica])

# Create dendrogram
fig = ff.create_dendrogram(
    data,
    labels=labels,
    linkagefun=lambda x: __import__("scipy.cluster.hierarchy", fromlist=["linkage"]).linkage(x, method="ward"),
    color_threshold=3.0,
)

# Update layout for large canvas
fig.update_layout(
    title={"text": "dendrogram-basic · plotly · pyplots.ai", "font": {"size": 28}, "x": 0.5, "xanchor": "center"},
    xaxis={"title": {"text": "Iris Flower Samples", "font": {"size": 22}}, "tickfont": {"size": 16}, "tickangle": -45},
    yaxis={"title": {"text": "Distance (Ward)", "font": {"size": 22}}, "tickfont": {"size": 18}},
    template="plotly_white",
    width=1600,
    height=900,
    margin={"l": 80, "r": 40, "t": 100, "b": 150},
)

# Update line widths for visibility
fig.update_traces(line={"width": 3})

# Save outputs
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html")
