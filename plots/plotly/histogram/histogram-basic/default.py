"""
histogram-basic: Basic Histogram
Library: plotly
"""

import numpy as np
import plotly.graph_objects as go


# Data
np.random.seed(42)
values = np.random.normal(100, 15, 500)

# Create figure
fig = go.Figure()
fig.add_trace(
    go.Histogram(
        x=values, marker_color="#306998", opacity=0.85, hovertemplate="Range: %{x}<br>Count: %{y}<extra></extra>"
    )
)

# Layout
fig.update_layout(
    title={"text": "Basic Histogram", "font": {"size": 40}, "x": 0.5, "xanchor": "center"},
    xaxis_title={"text": "Value", "font": {"size": 40}},
    yaxis_title={"text": "Frequency", "font": {"size": 40}},
    template="plotly_white",
    xaxis={"tickfont": {"size": 32}, "showgrid": True, "gridcolor": "rgba(0,0,0,0.1)"},
    yaxis={"tickfont": {"size": 32}, "showgrid": True, "gridcolor": "rgba(0,0,0,0.1)"},
    bargap=0.05,
)

# Save
fig.write_image("plot.png", width=1600, height=900, scale=3)
