"""
histogram-basic: Basic Histogram
Library: plotly
"""

import numpy as np
import plotly.graph_objects as go


# Data
np.random.seed(42)
values = np.random.normal(100, 15, 500)  # 500 values, mean=100, std=15

# Create figure
fig = go.Figure()
fig.add_trace(go.Histogram(x=values, marker={"color": "#306998", "line": {"color": "white", "width": 1}}, opacity=0.85))

# Layout
fig.update_layout(
    title={"text": "Basic Histogram", "font": {"size": 40}, "x": 0.5, "xanchor": "center"},
    xaxis_title="Value",
    yaxis_title="Frequency",
    template="plotly_white",
    font={"size": 32},
    xaxis={"title_font": {"size": 40}, "tickfont": {"size": 32}, "showgrid": True, "gridcolor": "rgba(0,0,0,0.1)"},
    yaxis={"title_font": {"size": 40}, "tickfont": {"size": 32}, "showgrid": True, "gridcolor": "rgba(0,0,0,0.1)"},
    bargap=0.05,
)

# Save
fig.write_image("plot.png", width=1600, height=900, scale=3)
