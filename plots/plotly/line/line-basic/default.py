"""
line-basic: Basic Line Plot
Library: plotly
"""

import pandas as pd
import plotly.graph_objects as go


# Data
data = pd.DataFrame({"time": [1, 2, 3, 4, 5, 6, 7], "value": [10, 15, 13, 18, 22, 19, 25]})

# Create plot
fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=data["time"],
        y=data["value"],
        mode="lines+markers",
        line={"color": "#306998", "width": 2},
        marker={"size": 8, "color": "#306998"},
        name="Value",
    )
)

# Layout
fig.update_layout(
    title={"text": "Basic Line Plot", "font": {"size": 20}, "x": 0.5, "xanchor": "center"},
    xaxis={
        "title": {"text": "Time", "font": {"size": 20}},
        "tickfont": {"size": 16},
        "gridcolor": "rgba(0,0,0,0.1)",
        "showgrid": True,
    },
    yaxis={
        "title": {"text": "Value", "font": {"size": 20}},
        "tickfont": {"size": 16},
        "gridcolor": "rgba(0,0,0,0.1)",
        "showgrid": True,
    },
    template="plotly_white",
    showlegend=False,
)

# Save
fig.write_image("plot.png", width=1600, height=900, scale=3)
