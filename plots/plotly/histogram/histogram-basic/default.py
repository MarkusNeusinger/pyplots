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
fig.add_trace(go.Histogram(x=values, marker_color="#306998", opacity=0.8, nbinsx=30))

# Layout
fig.update_layout(
    title={"text": "Basic Histogram", "font": {"size": 20}, "x": 0.5, "xanchor": "center"},
    xaxis_title="Value",
    yaxis_title="Frequency",
    template="plotly_white",
    xaxis={"title_font": {"size": 20}, "tickfont": {"size": 16}},
    yaxis={"title_font": {"size": 20}, "tickfont": {"size": 16}},
    bargap=0.05,
)

# Save
fig.write_image("plot.png", width=1600, height=900, scale=3)
