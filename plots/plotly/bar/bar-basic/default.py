"""
bar-basic: Basic Bar Chart
Library: plotly
"""

import pandas as pd
import plotly.graph_objects as go


# Data
data = pd.DataFrame(
    {"category": ["Product A", "Product B", "Product C", "Product D", "Product E"], "value": [45, 78, 52, 91, 63]}
)

# Create figure
fig = go.Figure()

fig.add_trace(go.Bar(x=data["category"], y=data["value"], marker_color="#306998"))

# Layout
fig.update_layout(
    title={"text": "Basic Bar Chart", "font": {"size": 20}, "x": 0.5, "xanchor": "center"},
    xaxis_title="Category",
    yaxis_title="Value",
    template="plotly_white",
    font={"size": 16},
    xaxis={"tickfont": {"size": 16}},
    yaxis={"tickfont": {"size": 16}},
)

# Save as PNG (4800 × 2700 px)
fig.write_image("plot.png", width=1600, height=900, scale=3)
