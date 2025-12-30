"""pyplots.ai
line-interactive: Interactive Line Chart with Hover and Zoom
Library: plotly | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go


# Data - Server CPU usage over 7 days (hourly readings)
np.random.seed(42)
n_points = 168  # 7 days * 24 hours

dates = pd.date_range("2024-01-01", periods=n_points, freq="h")

# Simulate realistic CPU usage pattern with daily cycles and some anomalies
base = 35  # base CPU usage
daily_pattern = 20 * np.sin(np.linspace(0, 7 * 2 * np.pi, n_points))  # daily cycle
weekly_trend = np.linspace(0, 10, n_points)  # slight upward trend
noise = np.random.normal(0, 5, n_points)

# Add some random spikes (anomalies)
spikes = np.zeros(n_points)
spike_indices = [45, 92, 120, 155]
for idx in spike_indices:
    spikes[idx] = np.random.uniform(20, 35)

cpu_usage = base + daily_pattern + weekly_trend + noise + spikes
cpu_usage = np.clip(cpu_usage, 5, 100)  # Keep within 5-100%

# Create figure with interactive features
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=dates,
        y=cpu_usage,
        mode="lines",
        name="CPU Usage",
        line={"color": "#306998", "width": 2.5},
        hovertemplate="<b>%{x|%Y-%m-%d %H:%M}</b><br>CPU Usage: %{y:.1f}%<extra></extra>",
    )
)

# Layout with interactive features
fig.update_layout(
    title={
        "text": "Server Metrics · line-interactive · plotly · pyplots.ai",
        "font": {"size": 28},
        "x": 0.5,
        "xanchor": "center",
    },
    xaxis={
        "title": {"text": "Date & Time", "font": {"size": 22}},
        "tickfont": {"size": 16},
        "rangeslider": {"visible": True, "thickness": 0.08},
        "rangeselector": {
            "buttons": [
                {"count": 1, "label": "1d", "step": "day", "stepmode": "backward"},
                {"count": 3, "label": "3d", "step": "day", "stepmode": "backward"},
                {"step": "all", "label": "All"},
            ],
            "font": {"size": 14},
            "bgcolor": "#f0f0f0",
            "activecolor": "#FFD43B",
        },
        "showgrid": True,
        "gridwidth": 1,
        "gridcolor": "rgba(0,0,0,0.1)",
    },
    yaxis={
        "title": {"text": "CPU Usage (%)", "font": {"size": 22}},
        "tickfont": {"size": 16},
        "range": [0, 105],
        "showgrid": True,
        "gridwidth": 1,
        "gridcolor": "rgba(0,0,0,0.1)",
    },
    template="plotly_white",
    hovermode="x unified",
    dragmode="zoom",
    margin={"l": 80, "r": 40, "t": 100, "b": 80},
)

# Add modebar buttons for interactivity
fig.update_layout(
    modebar={
        "add": ["zoom", "pan", "zoomIn", "zoomOut", "resetScale"],
        "remove": ["lasso", "select"],
        "bgcolor": "rgba(255,255,255,0.8)",
    }
)

# Save as PNG (static snapshot)
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Save as HTML (interactive version)
fig.write_html("plot.html", include_plotlyjs=True, full_html=True)
