"""pyplots.ai
arc-basic: Basic Arc Diagram
Library: plotly 6.5.2 | Python 3.14.3
Quality: /100 | Updated: 2026-02-23
"""

import numpy as np
import plotly.graph_objects as go


# Data: Character interactions in a story narrative
nodes = ["Alice", "Bob", "Carol", "David", "Eve", "Frank", "Grace", "Henry", "Iris", "Jack"]
n_nodes = len(nodes)

# Edges: pairs of (source_idx, target_idx, weight)
edges = [
    (0, 1, 3),  # Alice-Bob (neighbors, strong)
    (0, 3, 2),  # Alice-David
    (1, 2, 2),  # Bob-Carol
    (2, 4, 3),  # Carol-Eve (strong)
    (3, 5, 2),  # David-Frank
    (4, 6, 2),  # Eve-Grace
    (5, 7, 3),  # Frank-Henry (strong)
    (0, 8, 1),  # Alice-Iris (long, weak)
    (2, 9, 2),  # Carol-Jack (long)
    (1, 4, 2),  # Bob-Eve
    (3, 7, 1),  # David-Henry (long, weak)
    (6, 9, 2),  # Grace-Jack
]

# Node positions along horizontal axis
x_positions = np.linspace(0, 10, n_nodes)

# Weight-based styling: opacity and width encode connection strength
arc_styles = {
    1: {"color": "rgba(48, 105, 152, 0.30)", "width": 2.0},
    2: {"color": "rgba(48, 105, 152, 0.55)", "width": 3.0},
    3: {"color": "rgba(48, 105, 152, 0.85)", "width": 4.5},
}

# Create figure
fig = go.Figure()

# Draw arcs as smooth parabolic curves
for src, tgt, weight in edges:
    x_src, x_tgt = x_positions[src], x_positions[tgt]
    arc_height = abs(tgt - src) * 0.45

    t = np.linspace(0, 1, 50)
    x_arc = x_src + t * (x_tgt - x_src)
    y_arc = arc_height * 4 * t * (1 - t)

    style = arc_styles[weight]
    fig.add_trace(
        go.Scatter(
            x=x_arc,
            y=y_arc,
            mode="lines",
            line={"width": style["width"], "color": style["color"]},
            hoverinfo="text",
            hovertext=f"{nodes[src]} — {nodes[tgt]}  (weight {weight})",
            showlegend=False,
        )
    )

# Draw nodes on horizontal axis
fig.add_trace(
    go.Scatter(
        x=x_positions,
        y=np.zeros(n_nodes),
        mode="markers+text",
        marker={"size": 24, "color": "#FFD43B", "line": {"width": 2.5, "color": "#306998"}},
        text=nodes,
        textposition="bottom center",
        textfont={"size": 18, "color": "#2a2a2a"},
        hovertemplate="<b>%{text}</b><extra></extra>",
        showlegend=False,
    )
)

# Subtle horizontal baseline
fig.add_shape(
    type="line", x0=x_positions[0] - 0.3, x1=x_positions[-1] + 0.3, y0=0, y1=0, line={"width": 1.5, "color": "#CCCCCC"}
)

# Layout
fig.update_layout(
    title={
        "text": "arc-basic · plotly · pyplots.ai",
        "font": {"size": 30, "color": "#2a2a2a"},
        "x": 0.5,
        "xanchor": "center",
        "y": 0.96,
    },
    xaxis={"showgrid": False, "zeroline": False, "showticklabels": False, "showline": False, "range": [-0.5, 10.5]},
    yaxis={"showgrid": False, "zeroline": False, "showticklabels": False, "showline": False, "range": [-0.6, 4.5]},
    hovermode="closest",
    hoverlabel={"bgcolor": "white", "font_size": 14, "font_color": "#306998"},
    template="plotly_white",
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin={"l": 30, "r": 30, "t": 70, "b": 30},
)

# Save outputs
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html", include_plotlyjs="cdn")
