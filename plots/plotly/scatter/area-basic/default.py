"""
area-basic: Basic Area Chart
Library: plotly
"""

import pandas as pd
import plotly.graph_objects as go


# Data
data = pd.DataFrame(
    {
        "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        "sales": [120, 135, 148, 162, 175, 195, 210, 198, 185, 170, 158, 190],
    }
)

# Create figure
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=data["month"],
        y=data["sales"],
        mode="lines",
        fill="tozeroy",
        fillcolor="rgba(48, 105, 152, 0.5)",
        line={"color": "#306998", "width": 2},
        name="Sales",
    )
)

# Layout
fig.update_layout(
    title={"text": "Monthly Sales Trend", "font": {"size": 20}, "x": 0.5, "xanchor": "center"},
    xaxis_title={"text": "Month", "font": {"size": 20}},
    yaxis_title={"text": "Sales ($)", "font": {"size": 20}},
    template="plotly_white",
    xaxis={"tickfont": {"size": 16}, "showgrid": True, "gridcolor": "rgba(0, 0, 0, 0.1)"},
    yaxis={"tickfont": {"size": 16}, "showgrid": True, "gridcolor": "rgba(0, 0, 0, 0.1)"},
    showlegend=False,
    margin={"l": 80, "r": 40, "t": 80, "b": 80},
)

# Save
fig.write_image("plot.png", width=1600, height=900, scale=3)
