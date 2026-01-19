""" pyplots.ai
scatter-streaming: Streaming Scatter Plot
Library: plotly 6.5.2 | Python 3.13.11
Quality: 91/100 | Created: 2026-01-19
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go


# Data - Simulated streaming sensor data (temperature vs humidity readings)
np.random.seed(42)
n_points = 200

# Generate timestamps representing streaming arrival times
timestamps = pd.date_range(start="2026-01-19 10:00:00", periods=n_points, freq="5s")

# Simulate sensor readings with slight drift over time
time_idx = np.arange(n_points)
base_temp = 22 + np.sin(time_idx / 30) * 3  # Temperature oscillating around 22C
base_humidity = 55 + np.cos(time_idx / 25) * 10  # Humidity oscillating around 55%

# Add noise to simulate real sensor data
x = base_temp + np.random.randn(n_points) * 0.8  # Temperature (C)
y = base_humidity + np.random.randn(n_points) * 2  # Humidity (%)

# Calculate opacity based on recency (older points more transparent)
# Oldest point = 0.15 opacity, newest point = 1.0 opacity
opacity_values = np.linspace(0.15, 1.0, n_points)

# Color gradient from old (lighter blue) to new (deep blue)
colors = [f"rgba(48, 105, 152, {op})" for op in opacity_values]

# Create figure
fig = go.Figure()

# Add scatter trace with varying opacity for streaming effect
fig.add_trace(
    go.Scatter(
        x=x,
        y=y,
        mode="markers",
        marker={"size": 14, "color": colors, "line": {"width": 1, "color": "rgba(48, 105, 152, 0.5)"}},
        text=[
            f"Time: {t.strftime('%H:%M:%S')}<br>Temp: {temp:.1f}C<br>Humidity: {hum:.1f}%"
            for t, temp, hum in zip(timestamps, x, y, strict=True)
        ],
        hoverinfo="text",
        showlegend=False,
    )
)

# Add annotation indicating data flow direction (newest points)
newest_idx = -1
fig.add_annotation(
    x=x[newest_idx],
    y=y[newest_idx],
    text="Latest",
    showarrow=True,
    arrowhead=2,
    arrowsize=1.5,
    arrowwidth=2,
    arrowcolor="#306998",
    ax=40,
    ay=-40,
    font={"size": 18, "color": "#306998"},
)

# Add annotation for oldest visible points
oldest_idx = 0
fig.add_annotation(
    x=x[oldest_idx],
    y=y[oldest_idx],
    text="Oldest",
    showarrow=True,
    arrowhead=2,
    arrowsize=1.5,
    arrowwidth=2,
    arrowcolor="rgba(48, 105, 152, 0.4)",
    ax=-40,
    ay=40,
    font={"size": 18, "color": "rgba(48, 105, 152, 0.6)"},
)

# Layout
fig.update_layout(
    title={"text": "scatter-streaming · plotly · pyplots.ai", "font": {"size": 28}, "x": 0.5, "xanchor": "center"},
    xaxis={
        "title": {"text": "Temperature (°C)", "font": {"size": 22}},
        "tickfont": {"size": 18},
        "gridcolor": "rgba(0,0,0,0.1)",
        "zeroline": False,
    },
    yaxis={
        "title": {"text": "Humidity (%)", "font": {"size": 22}},
        "tickfont": {"size": 18},
        "gridcolor": "rgba(0,0,0,0.1)",
        "zeroline": False,
    },
    template="plotly_white",
    showlegend=False,
    margin={"l": 80, "r": 80, "t": 100, "b": 80},
)

# Add a subtle note about the streaming nature
fig.add_annotation(
    x=0.5,
    y=-0.12,
    xref="paper",
    yref="paper",
    text="200 sensor readings | Point opacity indicates recency (older → faded, newer → solid)",
    font={"size": 16, "color": "gray"},
    showarrow=False,
)

# Save outputs
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html", include_plotlyjs="cdn")
