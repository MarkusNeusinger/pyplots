"""
dendrogram-basic: Basic Dendrogram
Library: plotly
"""

import numpy as np
import plotly.figure_factory as ff
from scipy.cluster.hierarchy import linkage


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

# Create dendrogram using plotly figure factory
fig = ff.create_dendrogram(
    data,
    labels=labels,
    linkagefun=lambda x: linkage(x, method="ward"),
    colorscale=["#306998", "#FFD43B", "#306998", "#FFD43B", "#306998"],  # Python colors
)

# Update layout for 4800x2700 px output
fig.update_layout(
    title={"text": "dendrogram-basic · plotly · pyplots.ai", "font": {"size": 28}, "x": 0.5, "xanchor": "center"},
    xaxis={"title": {"text": "Sample", "font": {"size": 22}}, "tickfont": {"size": 14}, "tickangle": 45},
    yaxis={
        "title": {"text": "Distance (Ward)", "font": {"size": 22}},
        "tickfont": {"size": 18},
        "gridcolor": "rgba(0,0,0,0.1)",
        "gridwidth": 1,
    },
    template="plotly_white",
    showlegend=False,
    margin={"l": 80, "r": 40, "t": 100, "b": 150},
)

# Update line widths for visibility at high resolution
fig.update_traces(line={"width": 3})

# Save as PNG and HTML
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html", include_plotlyjs="cdn")
