"""
scatter-basic: Basic Scatter Plot
Library: plotly
"""

import numpy as np
import plotly.graph_objects as go


# Data
np.random.seed(42)
x = np.random.randn(100) * 2 + 10
y = x * 0.8 + np.random.randn(100) * 2

# Create figure
fig = go.Figure()

fig.add_trace(
    go.Scatter(x=x, y=y, mode="markers", marker={"size": 10, "color": "#306998", "opacity": 0.7}, name="Data Points")
)

# Layout
fig.update_layout(
    title={"text": "Basic Scatter Plot", "font": {"size": 40}, "x": 0.5, "xanchor": "center"},
    xaxis={
        "title": {"text": "X Value", "font": {"size": 40}},
        "tickfont": {"size": 32},
        "showgrid": True,
        "gridwidth": 1,
        "gridcolor": "rgba(128, 128, 128, 0.3)",
    },
    yaxis={
        "title": {"text": "Y Value", "font": {"size": 40}},
        "tickfont": {"size": 32},
        "showgrid": True,
        "gridwidth": 1,
        "gridcolor": "rgba(128, 128, 128, 0.3)",
    },
    template="plotly_white",
    showlegend=False,
    margin={"l": 100, "r": 50, "t": 100, "b": 100},
)

# Save
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html")
