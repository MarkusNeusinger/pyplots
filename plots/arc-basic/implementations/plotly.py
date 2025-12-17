"""
arc-basic: Basic Arc Diagram
Library: plotly
"""

import numpy as np
import plotly.graph_objects as go


# Data: Character interactions in a story
np.random.seed(42)

nodes = ["Alice", "Bob", "Carol", "David", "Eve", "Frank", "Grace", "Henry", "Iris", "Jack"]

# Edges: (source_idx, target_idx, weight)
# Representing character interactions - mix of short and long range connections
edges = [
    (0, 1, 3),  # Alice-Bob: close, strong
    (0, 4, 2),  # Alice-Eve: medium range
    (0, 8, 1),  # Alice-Iris: long range
    (1, 2, 2),  # Bob-Carol: close
    (2, 3, 3),  # Carol-David: close, strong
    (2, 7, 1),  # Carol-Henry: long range
    (3, 5, 2),  # David-Frank: medium
    (4, 6, 2),  # Eve-Grace: close
    (5, 6, 1),  # Frank-Grace: close
    (5, 9, 2),  # Frank-Jack: medium
    (6, 8, 1),  # Grace-Iris: close
    (7, 9, 3),  # Henry-Jack: close, strong
    (1, 6, 1),  # Bob-Grace: long range
    (3, 8, 2),  # David-Iris: long range
]

n_nodes = len(nodes)
node_x = np.arange(n_nodes)
node_y = np.zeros(n_nodes)

# Create figure
fig = go.Figure()

# Draw arcs
colors = ["#306998", "#FFD43B", "#4B8BBE", "#FFE873", "#2E5A8B"]

for src, tgt, weight in edges:
    # Arc parameters
    x_start, x_end = node_x[src], node_x[tgt]
    x_mid = (x_start + x_end) / 2
    arc_span = abs(x_end - x_start)

    # Height proportional to distance between nodes
    arc_height = arc_span * 0.4

    # Create arc using quadratic bezier approximation with many points
    t = np.linspace(0, 1, 50)
    # Quadratic bezier: P = (1-t)²P0 + 2(1-t)tP1 + t²P2
    arc_x = (1 - t) ** 2 * x_start + 2 * (1 - t) * t * x_mid + t**2 * x_end
    arc_y = (1 - t) ** 2 * 0 + 2 * (1 - t) * t * arc_height + t**2 * 0

    # Color based on edge weight
    color = colors[weight - 1] if weight <= len(colors) else colors[-1]

    # Line width based on weight
    line_width = weight * 2 + 2

    fig.add_trace(
        go.Scatter(
            x=arc_x,
            y=arc_y,
            mode="lines",
            line={"width": line_width, "color": color},
            opacity=0.6,
            hoverinfo="text",
            text=f"{nodes[src]} — {nodes[tgt]} (weight: {weight})",
            showlegend=False,
        )
    )

# Draw nodes
fig.add_trace(
    go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        marker={"size": 20, "color": "#306998", "line": {"width": 2, "color": "white"}},
        text=nodes,
        textposition="bottom center",
        textfont={"size": 16, "color": "#333333"},
        hoverinfo="text",
        hovertext=nodes,
        showlegend=False,
    )
)

# Layout
fig.update_layout(
    title={
        "text": "arc-basic · plotly · pyplots.ai",
        "font": {"size": 28, "color": "#333333"},
        "x": 0.5,
        "xanchor": "center",
    },
    xaxis={
        "title": {"text": "Characters (Sequential Order)", "font": {"size": 22}},
        "tickfont": {"size": 18},
        "showgrid": False,
        "zeroline": False,
        "showticklabels": False,
    },
    yaxis={
        "title": {"text": "Connection Strength", "font": {"size": 22}},
        "tickfont": {"size": 18},
        "showgrid": True,
        "gridcolor": "rgba(0,0,0,0.1)",
        "zeroline": True,
        "zerolinecolor": "rgba(0,0,0,0.3)",
        "zerolinewidth": 2,
        "range": [-0.8, 4.5],
    },
    template="plotly_white",
    margin={"l": 80, "r": 80, "t": 100, "b": 120},
    plot_bgcolor="white",
)

# Save as PNG (4800 x 2700 px)
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Save as HTML for interactivity
fig.write_html("plot.html", include_plotlyjs="cdn")
