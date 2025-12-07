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

fig.add_trace(go.Scatter(x=x, y=y, mode="markers", marker={"size": 10, "color": "#306998", "opacity": 0.7}))

# Layout
fig.update_layout(
    title={"text": "Basic Scatter Plot", "font": {"size": 20}, "x": 0.5, "xanchor": "center"},
    xaxis={
        "title": {"text": "X Value", "font": {"size": 20}},
        "tickfont": {"size": 16},
        "showgrid": True,
        "gridcolor": "rgba(0, 0, 0, 0.1)",
    },
    yaxis={
        "title": {"text": "Y Value", "font": {"size": 20}},
        "tickfont": {"size": 16},
        "showgrid": True,
        "gridcolor": "rgba(0, 0, 0, 0.1)",
    },
    template="plotly_white",
    plot_bgcolor="white",
)

# Save
fig.write_image("plot.png", width=1600, height=900, scale=3)
