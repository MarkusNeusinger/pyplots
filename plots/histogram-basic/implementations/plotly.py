"""
histogram-basic: Basic Histogram
Library: plotly
"""

import numpy as np
import plotly.graph_objects as go


# Data - simulating test scores distribution
np.random.seed(42)
values = np.random.normal(loc=72, scale=12, size=200)

# Create histogram
fig = go.Figure()
fig.add_trace(
    go.Histogram(x=values, nbinsx=25, marker={"color": "#306998", "line": {"color": "white", "width": 1}}, opacity=0.85)
)

# Layout for 4800x2700 px
fig.update_layout(
    title={"text": "histogram-basic · plotly · pyplots.ai", "font": {"size": 28}, "x": 0.5, "xanchor": "center"},
    xaxis={
        "title": {"text": "Value", "font": {"size": 22}},
        "tickfont": {"size": 18},
        "showgrid": True,
        "gridcolor": "rgba(0,0,0,0.1)",
        "gridwidth": 1,
    },
    yaxis={
        "title": {"text": "Frequency", "font": {"size": 22}},
        "tickfont": {"size": 18},
        "showgrid": True,
        "gridcolor": "rgba(0,0,0,0.1)",
        "gridwidth": 1,
        "rangemode": "tozero",
    },
    template="plotly_white",
    bargap=0,
    margin={"l": 80, "r": 50, "t": 80, "b": 80},
)

# Save as PNG and HTML
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html", include_plotlyjs=True, full_html=True)
