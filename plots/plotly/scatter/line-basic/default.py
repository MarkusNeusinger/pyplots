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
    go.Scatter(x=data["time"], y=data["value"], mode="lines", line={"color": "#306998", "width": 2}, name="Value")
)

# Layout
fig.update_layout(
    title={"text": "Basic Line Plot", "font": {"size": 20}},
    xaxis_title="Time",
    yaxis_title="Value",
    template="plotly_white",
    xaxis={"title_font": {"size": 20}, "tickfont": {"size": 16}, "showgrid": True, "gridcolor": "rgba(0,0,0,0.1)"},
    yaxis={"title_font": {"size": 20}, "tickfont": {"size": 16}, "showgrid": True, "gridcolor": "rgba(0,0,0,0.1)"},
    legend={"font": {"size": 16}},
    margin={"l": 80, "r": 40, "t": 80, "b": 60},
)

# Save
fig.write_image("plot.png", width=1600, height=900, scale=3)
