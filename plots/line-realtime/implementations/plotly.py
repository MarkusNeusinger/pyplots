"""pyplots.ai
line-realtime: Real-Time Updating Line Chart
Library: plotly | Python 3.13
Quality: pending | Created: 2025-12-31
"""

import numpy as np
import plotly.graph_objects as go


# Data - Simulated CPU usage with sliding window effect
np.random.seed(42)
n_points = 120
time_seconds = np.arange(n_points)

# Generate realistic CPU usage pattern with some spikes
base_cpu = 35 + 10 * np.sin(time_seconds * 0.1)  # Slow oscillation
noise = np.random.normal(0, 5, n_points)
spikes = np.zeros(n_points)
spike_positions = [25, 45, 70, 95]
for pos in spike_positions:
    spikes[pos : pos + 5] = np.array([15, 25, 20, 10, 5])
cpu_usage = np.clip(base_cpu + noise + spikes, 0, 100)

# Create figure with gradient fill to show live data effect
fig = go.Figure()

# Main line trace
fig.add_trace(
    go.Scatter(
        x=time_seconds,
        y=cpu_usage,
        mode="lines",
        name="CPU Usage",
        line={"color": "#306998", "width": 3},
        fill="tozeroy",
        fillcolor="rgba(48, 105, 152, 0.2)",
    )
)

# Add marker for the latest value (to emphasize real-time aspect)
latest_idx = n_points - 1
fig.add_trace(
    go.Scatter(
        x=[time_seconds[latest_idx]],
        y=[cpu_usage[latest_idx]],
        mode="markers+text",
        name=f"Current: {cpu_usage[latest_idx]:.1f}%",
        marker={"color": "#FFD43B", "size": 18, "line": {"color": "#306998", "width": 2}},
        text=[f"{cpu_usage[latest_idx]:.1f}%"],
        textposition="top center",
        textfont={"size": 20, "color": "#306998"},
    )
)

# Add fade effect on the left side using shapes to indicate scrolling direction
# Create gradient overlay shapes for the trailing edge
for i in range(10):
    alpha = 0.08 * (10 - i)
    fig.add_vrect(x0=i * 2, x1=(i + 1) * 2, fillcolor=f"rgba(255, 255, 255, {alpha})", layer="above", line_width=0)

# Add arrow annotation to show scrolling direction
fig.add_annotation(
    x=5,
    y=90,
    ax=25,
    ay=90,
    xref="x",
    yref="y",
    axref="x",
    ayref="y",
    showarrow=True,
    arrowhead=2,
    arrowsize=1.5,
    arrowwidth=3,
    arrowcolor="#306998",
)
fig.add_annotation(
    x=15, y=92, text="← Data scrolls", showarrow=False, font={"size": 18, "color": "#306998"}, xref="x", yref="y"
)

# Layout for 4800x2700
fig.update_layout(
    title={
        "text": "CPU Usage Monitor · line-realtime · plotly · pyplots.ai",
        "font": {"size": 32, "color": "#333333"},
        "x": 0.5,
        "xanchor": "center",
    },
    xaxis={
        "title": {"text": "Time (seconds)", "font": {"size": 24}},
        "tickfont": {"size": 18},
        "showgrid": True,
        "gridwidth": 1,
        "gridcolor": "rgba(0, 0, 0, 0.1)",
        "range": [0, n_points + 5],
    },
    yaxis={
        "title": {"text": "CPU Usage (%)", "font": {"size": 24}},
        "tickfont": {"size": 18},
        "showgrid": True,
        "gridwidth": 1,
        "gridcolor": "rgba(0, 0, 0, 0.1)",
        "range": [0, 105],
    },
    template="plotly_white",
    showlegend=True,
    legend={
        "font": {"size": 18},
        "x": 0.98,
        "y": 0.98,
        "xanchor": "right",
        "yanchor": "top",
        "bgcolor": "rgba(255, 255, 255, 0.8)",
        "bordercolor": "#306998",
        "borderwidth": 1,
    },
    margin={"l": 100, "r": 80, "t": 120, "b": 100},
)

# Add live indicator annotation
fig.add_annotation(
    x=0.95,
    y=0.05,
    xref="paper",
    yref="paper",
    text="● LIVE",
    showarrow=False,
    font={"size": 22, "color": "#e74c3c", "family": "Arial Black"},
    bgcolor="rgba(255, 255, 255, 0.9)",
    borderpad=8,
)

# Save as PNG (4800x2700)
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Save as interactive HTML
fig.write_html("plot.html", include_plotlyjs=True, full_html=True)
