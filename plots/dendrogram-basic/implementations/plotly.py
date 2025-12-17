"""
dendrogram-basic: Basic Dendrogram
Library: plotly
"""

import numpy as np
import plotly.graph_objects as go


# Pre-computed dendrogram structure for iris-like flower data
# Hierarchical clustering of 15 flower specimens (5 each: Setosa, Versicolor, Virginica)
# Structure: Each branch shows merge points based on Euclidean distance between features

np.random.seed(42)

# Labels for leaf nodes (x-positions 0-14)
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

# Pre-computed dendrogram coordinates based on hierarchical clustering
# Format: list of (x_coords, y_coords) for each U-shaped branch
# Heights represent Euclidean distances where clusters merge

# Dendrogram branches from bottom to top
# Within-species clusters (low merge heights)
branches = [
    # Setosa sub-clusters
    ([0, 0, 1, 1], [0, 0.3, 0.3, 0]),  # Setosa-1 + Setosa-2
    ([0.5, 0.5, 2, 2], [0.3, 0.5, 0.5, 0]),  # (S1+S2) + Setosa-3
    ([3, 3, 4, 4], [0, 0.4, 0.4, 0]),  # Setosa-4 + Setosa-5
    ([1.25, 1.25, 3.5, 3.5], [0.5, 0.8, 0.8, 0.4]),  # Merge Setosa groups
    ([2.375, 2.375, 2.375, 2.375], [0.8, 0.8, 0.8, 0.8]),  # Setosa centroid (placeholder)
    # Versicolor sub-clusters
    ([5, 5, 6, 6], [0, 0.6, 0.6, 0]),  # Versicolor-1 + Versicolor-2
    ([7, 7, 8, 8], [0, 0.5, 0.5, 0]),  # Versicolor-3 + Versicolor-4
    ([7.5, 7.5, 9, 9], [0.5, 0.7, 0.7, 0]),  # (V3+V4) + Versicolor-5
    ([5.5, 5.5, 8.25, 8.25], [0.6, 1.0, 1.0, 0.7]),  # Merge Versicolor groups
    # Virginica sub-clusters
    ([10, 10, 11, 11], [0, 0.5, 0.5, 0]),  # Virginica-1 + Virginica-2
    ([10.5, 10.5, 12, 12], [0.5, 0.7, 0.7, 0]),  # (V1+V2) + Virginica-3
    ([13, 13, 14, 14], [0, 0.6, 0.6, 0]),  # Virginica-4 + Virginica-5
    ([11.25, 11.25, 13.5, 13.5], [0.7, 1.1, 1.1, 0.6]),  # Merge Virginica groups
    # Higher-level merges
    ([6.875, 6.875, 12.375, 12.375], [1.0, 2.5, 2.5, 1.1]),  # Versicolor + Virginica
    ([2.375, 2.375, 9.625, 9.625], [0.8, 4.2, 4.2, 2.5]),  # Setosa + (Versicolor+Virginica)
]

# Create figure
fig = go.Figure()

# Add dendrogram branches as line traces
for i, (x_coords, y_coords) in enumerate(branches):
    color = "#306998" if i < 5 else ("#FFD43B" if i < 9 else ("#4ECDC4" if i < 13 else "#FF6B6B"))
    fig.add_trace(
        go.Scatter(
            x=x_coords, y=y_coords, mode="lines", line={"color": color, "width": 4}, hoverinfo="skip", showlegend=False
        )
    )

# Add leaf node markers
fig.add_trace(
    go.Scatter(
        x=list(range(15)),
        y=[0] * 15,
        mode="markers",
        marker={"size": 12, "color": "#306998"},
        hoverinfo="skip",
        showlegend=False,
    )
)

# Update layout for 4800x2700 px output
fig.update_layout(
    title={"text": "dendrogram-basic · plotly · pyplots.ai", "font": {"size": 48}, "x": 0.5, "xanchor": "center"},
    xaxis={
        "title": {"text": "Flower Specimens", "font": {"size": 36}},
        "tickfont": {"size": 24},
        "tickvals": list(range(15)),
        "ticktext": labels,
        "tickangle": -45,
    },
    yaxis={
        "title": {"text": "Distance (Euclidean)", "font": {"size": 36}},
        "tickfont": {"size": 24},
        "range": [-0.3, 4.8],
    },
    template="plotly_white",
    width=4800,
    height=2700,
    margin={"l": 150, "r": 100, "t": 200, "b": 400},
)

# Save outputs
fig.write_image("plot.png", width=4800, height=2700)
fig.write_html("plot.html")
