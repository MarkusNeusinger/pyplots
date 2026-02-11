"""pyplots.ai
area-basic: Basic Area Chart
Library: plotly 6.5.2 | Python 3.14.2
Quality: /100 | Updated: 2026-02-11
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go


# Data - daily website visitors over a month
np.random.seed(42)
dates = pd.date_range("2024-01-01", periods=30, freq="D")

# Simulate realistic website traffic with weekly patterns and trend
base = 5000
trend = np.linspace(0, 1500, 30)
weekly_pattern = 1000 * np.sin(np.arange(30) * 2 * np.pi / 7)
noise = np.random.randn(30) * 500
visitors = base + trend + weekly_pattern + noise
visitors = np.maximum(visitors, 2000).astype(int)

# Create figure
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=dates,
        y=visitors,
        mode="lines",
        fill="tozeroy",
        fillcolor="rgba(48, 105, 152, 0.35)",
        line={"color": "#306998", "width": 3, "shape": "spline"},
        name="Daily Visitors",
        hovertemplate="<b>%{x|%b %d, %Y}</b><br>Visitors: %{y:,}<extra></extra>",
    )
)

# Annotate peak traffic day
peak_idx = int(np.argmax(visitors))
fig.add_annotation(
    x=dates[peak_idx],
    y=visitors[peak_idx],
    text=f"Peak: {visitors[peak_idx]:,}",
    showarrow=True,
    arrowhead=2,
    arrowsize=1.5,
    ax=0,
    ay=-40,
    font={"size": 16, "color": "#306998"},
    bordercolor="#306998",
    borderwidth=1.5,
    borderpad=4,
    bgcolor="rgba(255, 255, 255, 0.85)",
)

# Layout
fig.update_layout(
    title={
        "text": "Daily Website Visitors · area-basic · plotly · pyplots.ai",
        "font": {"size": 28},
        "x": 0.5,
        "xanchor": "center",
    },
    xaxis={
        "title": {"text": "Date (January 2024)", "font": {"size": 22}},
        "tickfont": {"size": 18},
        "showgrid": True,
        "gridwidth": 1,
        "gridcolor": "rgba(0, 0, 0, 0.15)",
        "dtick": 7 * 24 * 60 * 60 * 1000,
        "tickformat": "%b %d",
    },
    yaxis={
        "title": {"text": "Visitors (daily count)", "font": {"size": 22}},
        "tickfont": {"size": 18},
        "showgrid": True,
        "gridwidth": 1,
        "gridcolor": "rgba(0, 0, 0, 0.15)",
        "tickformat": ",",
    },
    template="plotly_white",
    showlegend=False,
    margin={"l": 80, "r": 40, "t": 80, "b": 60},
    hovermode="x unified",
)

# Save as PNG (4800x2700 px)
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Save interactive HTML with range slider for exploration
fig.update_layout(xaxis_rangeslider_visible=True)
fig.write_html("plot.html")
