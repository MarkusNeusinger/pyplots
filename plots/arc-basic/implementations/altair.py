"""
arc-basic: Basic Arc Diagram
Library: altair
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - Character interactions in a story chapter
np.random.seed(42)

nodes = ["Alice", "Bob", "Carol", "David", "Eve", "Frank", "Grace", "Henry", "Ivy", "Jack"]
n_nodes = len(nodes)

# Edges representing character interactions (various distances)
edges = [
    (0, 1, 3),  # Alice-Bob (short range, strong)
    (0, 4, 2),  # Alice-Eve (medium range)
    (1, 2, 4),  # Bob-Carol (short range, strongest)
    (2, 5, 2),  # Carol-Frank (medium range)
    (3, 7, 3),  # David-Henry (long range)
    (4, 5, 1),  # Eve-Frank (short range, weak)
    (0, 9, 2),  # Alice-Jack (longest range)
    (6, 8, 3),  # Grace-Ivy (short range)
    (1, 6, 2),  # Bob-Grace (long range)
    (3, 4, 1),  # David-Eve (short range, weak)
    (5, 9, 2),  # Frank-Jack (long range)
    (2, 3, 3),  # Carol-David (short range)
]

# Create arc data - each arc is a series of points forming a semicircle
arc_data = []
for source, target, weight in edges:
    # Arc center and radius
    x_start = source
    x_end = target
    x_center = (x_start + x_end) / 2
    radius = abs(x_end - x_start) / 2

    # Generate points along the arc (semicircle above the axis)
    n_points = 50
    angles = np.linspace(np.pi, 0, n_points)
    for i, angle in enumerate(angles):
        x = x_center + radius * np.cos(angle)
        y = radius * np.sin(angle)
        arc_data.append(
            {
                "x": x,
                "y": y,
                "edge_id": f"{source}-{target}",
                "weight": weight,
                "source": nodes[source],
                "target": nodes[target],
                "order": i,
            }
        )

arc_df = pd.DataFrame(arc_data)

# Create node data
node_df = pd.DataFrame({"x": range(n_nodes), "y": [0] * n_nodes, "label": nodes})

# Arc chart with lines grouped by edge_id
arcs = (
    alt.Chart(arc_df)
    .mark_line(strokeCap="round")
    .encode(
        x=alt.X("x:Q", axis=None),
        y=alt.Y("y:Q", axis=None),
        detail="edge_id:N",
        strokeWidth=alt.StrokeWidth(
            "weight:Q",
            scale=alt.Scale(range=[3, 12]),
            legend=alt.Legend(title="Interaction Strength", titleFontSize=18, labelFontSize=16),
        ),
        color=alt.value("#306998"),
        opacity=alt.value(0.6),
        order="order:O",
    )
)

# Node points
node_points = (
    alt.Chart(node_df)
    .mark_circle(size=400, color="#FFD43B", stroke="#306998", strokeWidth=3)
    .encode(x=alt.X("x:Q"), y=alt.Y("y:Q"))
)

# Node labels below the axis
node_labels = (
    alt.Chart(node_df)
    .mark_text(fontSize=20, dy=35, fontWeight="bold", color="#333333")
    .encode(x=alt.X("x:Q"), y=alt.Y("y:Q"), text="label:N")
)

# Combine all layers
chart = (
    alt.layer(arcs, node_points, node_labels)
    .properties(
        width=1600, height=900, title=alt.Title(text="arc-basic · altair · pyplots.ai", fontSize=32, anchor="middle")
    )
    .configure_view(strokeWidth=0)
)

# Save as PNG and HTML
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
