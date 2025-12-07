"""
line-basic: Basic Line Plot
Library: plotly
"""

import plotly.graph_objects as go


# Data
time = [1, 2, 3, 4, 5, 6, 7]
value = [10, 15, 13, 18, 22, 19, 25]

# Create plot
fig = go.Figure()
fig.add_trace(go.Scatter(x=time, y=value, mode="lines", line={"color": "#306998", "width": 3}))

# Layout
fig.update_layout(
    title={"text": "Basic Line Plot", "font": {"size": 36}},
    xaxis_title="Time",
    yaxis_title="Value",
    template="plotly_white",
    showlegend=False,
    xaxis={"title_font": {"size": 28}, "tickfont": {"size": 22}, "showgrid": True, "gridcolor": "rgba(0,0,0,0.1)"},
    yaxis={"title_font": {"size": 28}, "tickfont": {"size": 22}, "showgrid": True, "gridcolor": "rgba(0,0,0,0.1)"},
    margin={"l": 80, "r": 40, "t": 100, "b": 80},
)

# Save
fig.write_image("plot.png", width=1600, height=900, scale=3)
