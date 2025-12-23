""" pyplots.ai
arc-basic: Basic Arc Diagram
Library: altair 6.0.0 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-23
"""

import altair as alt
import numpy as np
import pandas as pd


# Data: Character interactions in a story chapter
np.random.seed(42)

nodes = ["Alice", "Bob", "Carol", "David", "Eve", "Frank", "Grace", "Henry", "Iris", "Jack"]
n_nodes = len(nodes)

# Edges: pairs of connected nodes with weights
edges = [
    (0, 1, 3),  # Alice-Bob (strong connection)
    (0, 3, 2),  # Alice-David
    (1, 2, 2),  # Bob-Carol
    (2, 4, 1),  # Carol-Eve
    (3, 5, 2),  # David-Frank
    (4, 6, 1),  # Eve-Grace
    (0, 7, 1),  # Alice-Henry (long-range)
    (1, 5, 2),  # Bob-Frank
    (2, 3, 3),  # Carol-David (strong)
    (5, 8, 1),  # Frank-Iris
    (6, 9, 2),  # Grace-Jack
    (0, 9, 1),  # Alice-Jack (longest range)
    (3, 7, 2),  # David-Henry
    (7, 8, 1),  # Henry-Iris
    (8, 9, 2),  # Iris-Jack
]

# Node positions along x-axis
x_positions = np.linspace(0, 100, n_nodes)
y_baseline = 10

# Create node dataframe
nodes_df = pd.DataFrame({"x": x_positions, "y": [y_baseline] * n_nodes, "name": nodes})

# Create arc paths - each arc as a series of points following a semicircle
arc_data = []
points_per_arc = 50

for edge_id, (start, end, weight) in enumerate(edges):
    x_start = x_positions[start]
    x_end = x_positions[end]

    # Arc height proportional to distance between nodes
    distance = abs(end - start)
    height = 8 * distance

    # Generate points along a semicircle arc
    angles = np.linspace(0, np.pi, points_per_arc)

    x_center = (x_start + x_end) / 2
    radius_x = abs(x_end - x_start) / 2
    radius_y = height / 2

    for i, angle in enumerate(angles):
        arc_data.append(
            {
                "edge_id": edge_id,
                "x": x_center - radius_x * np.cos(angle),
                "y": y_baseline + radius_y * np.sin(angle),
                "weight": weight,
                "order": i,
            }
        )

arcs_df = pd.DataFrame(arc_data)

# Create arc chart with lines
arcs = (
    alt.Chart(arcs_df)
    .mark_line(strokeWidth=2, opacity=0.6)
    .encode(
        x=alt.X("x:Q", axis=None),
        y=alt.Y("y:Q", axis=None),
        detail="edge_id:N",
        strokeWidth=alt.StrokeWidth("weight:Q", scale=alt.Scale(domain=[1, 3], range=[2, 6]), legend=None),
        color=alt.value("#306998"),
    )
    .properties(width=1600, height=900)
)

# Create node points
node_points = (
    alt.Chart(nodes_df)
    .mark_circle(size=600, color="#FFD43B", stroke="#306998", strokeWidth=3)
    .encode(x=alt.X("x:Q", axis=None), y=alt.Y("y:Q", axis=None))
)

# Create node labels
node_labels = (
    alt.Chart(nodes_df)
    .mark_text(dy=30, fontSize=18, fontWeight="bold", color="#306998")
    .encode(x=alt.X("x:Q"), y=alt.Y("y:Q"), text="name:N")
)

# Combine layers
chart = (
    alt.layer(arcs, node_points, node_labels)
    .properties(
        width=1600,
        height=900,
        title=alt.Title("Character Interactions · arc-basic · altair · pyplots.ai", fontSize=28, anchor="middle"),
    )
    .configure_view(strokeWidth=0)
)

# Save outputs
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
