"""
errorbar-basic: Basic Error Bar Plot
Library: plotly
"""

import numpy as np
import plotly.graph_objects as go


# Data
np.random.seed(42)
categories = ["Control", "Treatment A", "Treatment B", "Treatment C", "Treatment D"]
means = np.array([45.2, 52.8, 61.3, 48.9, 67.5])
# Varying error magnitudes to demonstrate feature
errors = np.array([4.5, 6.2, 3.8, 7.1, 5.3])

# Create figure
fig = go.Figure()

# Add bar trace with error bars
fig.add_trace(
    go.Bar(
        x=categories,
        y=means,
        error_y={"type": "data", "array": errors, "visible": True, "thickness": 3, "width": 12},
        marker={"color": "#306998", "line": {"color": "#1e4a6e", "width": 2}},
        width=0.6,
    )
)

# Layout configuration for 4800x2700
fig.update_layout(
    title={"text": "errorbar-basic · plotly · pyplots.ai", "font": {"size": 48}, "x": 0.5, "xanchor": "center"},
    xaxis={"title": {"text": "Experimental Group", "font": {"size": 36}}, "tickfont": {"size": 28}},
    yaxis={
        "title": {"text": "Response Value (units)", "font": {"size": 36}},
        "tickfont": {"size": 28},
        "gridcolor": "rgba(128,128,128,0.3)",
        "gridwidth": 1,
        "range": [0, 85],
    },
    template="plotly_white",
    bargap=0.3,
    margin={"l": 120, "r": 80, "t": 120, "b": 100},
)

# Save
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html")
