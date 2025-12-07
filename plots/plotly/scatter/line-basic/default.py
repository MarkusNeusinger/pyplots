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
fig.add_trace(go.Scatter(x=time, y=value, mode="lines", line={"color": "#306998", "width": 2}, name="Value"))

# Layout
fig.update_layout(
    title={"text": "Basic Line Plot", "font": {"size": 20}, "x": 0.5},
    xaxis_title="Time",
    yaxis_title="Value",
    xaxis={"tickfont": {"size": 16}, "title_font": {"size": 20}, "gridcolor": "rgba(0,0,0,0.1)"},
    yaxis={"tickfont": {"size": 16}, "title_font": {"size": 20}, "gridcolor": "rgba(0,0,0,0.1)"},
    template="plotly_white",
    showlegend=False,
)

# Save
fig.write_image("plot.png", width=1600, height=900, scale=3)
