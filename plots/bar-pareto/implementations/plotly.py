""" pyplots.ai
bar-pareto: Pareto Chart with Cumulative Line
Library: plotly 6.6.0 | Python 3.14.3
Quality: 84/100 | Created: 2026-03-20
"""

import numpy as np
import plotly.graph_objects as go


# Data
categories = [
    "Scratches",
    "Dents",
    "Misalignment",
    "Cracks",
    "Discoloration",
    "Burrs",
    "Warping",
    "Contamination",
    "Chipping",
    "Porosity",
]
counts = np.array([142, 118, 87, 64, 53, 38, 29, 21, 15, 9])

sort_idx = np.argsort(-counts)
categories = [categories[i] for i in sort_idx]
counts = counts[sort_idx]

cumulative_pct = np.cumsum(counts) / counts.sum() * 100

# Plot
fig = go.Figure()

fig.add_trace(
    go.Bar(x=categories, y=counts, marker={"color": "#306998", "line": {"width": 0}}, name="Defect Count", yaxis="y")
)

fig.add_trace(
    go.Scatter(
        x=categories,
        y=cumulative_pct,
        mode="lines+markers",
        marker={"size": 12, "color": "#E85D3A", "line": {"width": 2, "color": "white"}},
        line={"width": 3, "color": "#E85D3A"},
        name="Cumulative %",
        yaxis="y2",
    )
)

# 80% reference line
fig.add_hline(y=80, line={"color": "#999999", "width": 2, "dash": "dash"}, yref="y2")
fig.add_annotation(
    x=categories[-1],
    y=80,
    yref="y2",
    text="80%",
    showarrow=False,
    font={"size": 16, "color": "#999999"},
    xanchor="left",
    xshift=10,
)

# Style
fig.update_layout(
    title={"text": "bar-pareto · plotly · pyplots.ai", "font": {"size": 28}},
    xaxis={"title": {"text": "Defect Type", "font": {"size": 22}}, "tickfont": {"size": 16}},
    yaxis={
        "title": {"text": "Frequency", "font": {"size": 22}},
        "tickfont": {"size": 18},
        "showgrid": True,
        "gridcolor": "rgba(0,0,0,0.08)",
    },
    yaxis2={
        "title": {"text": "Cumulative Percentage (%)", "font": {"size": 22}},
        "tickfont": {"size": 18},
        "overlaying": "y",
        "side": "right",
        "range": [0, 105],
        "showgrid": False,
        "ticksuffix": "%",
    },
    template="plotly_white",
    legend={"font": {"size": 16}, "x": 0.75, "y": 0.25, "bgcolor": "rgba(255,255,255,0.8)"},
    bargap=0.15,
    plot_bgcolor="white",
    margin={"t": 80, "b": 60, "l": 60, "r": 80},
)

# Save
fig.write_html("plot.html")
fig.write_image("plot.png", width=1600, height=900, scale=3)
