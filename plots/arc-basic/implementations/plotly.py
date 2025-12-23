""" pyplots.ai
arc-basic: Basic Arc Diagram
Library: plotly 6.5.0 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-23
"""

import numpy as np
import plotly.graph_objects as go


# Data: Character interactions in a story narrative
nodes = ["Alice", "Bob", "Carol", "David", "Eve", "Frank", "Grace", "Henry", "Iris", "Jack"]
n_nodes = len(nodes)

# Edges: pairs of (source_idx, target_idx, weight)
# Demonstrates short-range and long-range connections with varying weights
edges = [
    (0, 1, 3),  # Alice-Bob (neighbors, strong connection)
    (0, 3, 2),  # Alice-David (medium distance)
    (1, 2, 2),  # Bob-Carol
    (2, 4, 3),  # Carol-Eve
    (3, 5, 2),  # David-Frank
    (4, 6, 2),  # Eve-Grace
    (5, 7, 3),  # Frank-Henry
    (0, 8, 1),  # Alice-Iris (long arc)
    (2, 9, 2),  # Carol-Jack (long arc)
    (1, 4, 2),  # Bob-Eve (medium arc)
    (3, 7, 1),  # David-Henry (long arc)
    (6, 9, 2),  # Grace-Jack
]

# Node positions along horizontal axis
x_positions = np.linspace(0, 10, n_nodes)

# Create figure
fig = go.Figure()

# Draw arcs as smooth parabolic curves
for src, tgt, weight in edges:
    x_src = x_positions[src]
    x_tgt = x_positions[tgt]

    # Arc height proportional to distance between nodes
    distance = abs(tgt - src)
    arc_height = distance * 0.4

    # Create smooth arc using multiple points
    t = np.linspace(0, 1, 50)
    x_arc = x_src + t * (x_tgt - x_src)
    y_arc = arc_height * 4 * t * (1 - t)  # Parabolic arc

    # Line width based on weight
    line_width = 2 + weight * 1.5

    fig.add_trace(
        go.Scatter(
            x=x_arc,
            y=y_arc,
            mode="lines",
            line={"width": line_width, "color": "#306998"},
            opacity=0.6,
            hoverinfo="skip",
            showlegend=False,
        )
    )

# Draw nodes on horizontal axis
fig.add_trace(
    go.Scatter(
        x=x_positions,
        y=[0] * n_nodes,
        mode="markers+text",
        marker={"size": 24, "color": "#FFD43B", "line": {"width": 3, "color": "#306998"}},
        text=nodes,
        textposition="bottom center",
        textfont={"size": 18, "color": "#306998"},
        hovertemplate="%{text}<extra></extra>",
        showlegend=False,
    )
)

# Draw horizontal baseline
fig.add_trace(
    go.Scatter(
        x=[x_positions[0] - 0.3, x_positions[-1] + 0.3],
        y=[0, 0],
        mode="lines",
        line={"width": 3, "color": "#888888"},
        hoverinfo="skip",
        showlegend=False,
    )
)

# Layout
fig.update_layout(
    title={"text": "arc-basic · plotly · pyplots.ai", "font": {"size": 32}, "x": 0.5, "xanchor": "center"},
    xaxis={"showgrid": False, "zeroline": False, "showticklabels": False, "title": None, "range": [-0.5, 10.5]},
    yaxis={
        "showgrid": False,
        "zeroline": False,
        "showticklabels": False,
        "title": None,
        "range": [-1.5, 4],
        "scaleanchor": "x",
        "scaleratio": 0.5,
    },
    template="plotly_white",
    plot_bgcolor="white",
    margin={"l": 50, "r": 50, "t": 100, "b": 80},
)

# Save outputs
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html", include_plotlyjs="cdn")
