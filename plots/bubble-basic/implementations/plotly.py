""" pyplots.ai
bubble-basic: Basic Bubble Chart
Library: plotly 6.5.0 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-14
"""

import numpy as np
import plotly.graph_objects as go


# Data
np.random.seed(42)
n_points = 50

x = np.random.randn(n_points) * 10 + 50
y = x * 0.8 + np.random.randn(n_points) * 8 + 10
size_values = np.abs(np.random.randn(n_points) * 20 + 30)

# Normalize size for bubble scaling (area-based)
size_min, size_max = 15, 80
size_normalized = (size_values - size_values.min()) / (size_values.max() - size_values.min())
bubble_sizes = size_min + size_normalized * (size_max - size_min)

# Plot
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=x,
        y=y,
        mode="markers",
        marker={
            "size": bubble_sizes,
            "color": "#306998",
            "opacity": 0.6,
            "line": {"width": 1, "color": "#1a3d5c"},
            "sizemode": "diameter",
        },
        text=[f"Size: {s:.1f}" for s in size_values],
        hovertemplate="<b>X:</b> %{x:.1f}<br><b>Y:</b> %{y:.1f}<br>%{text}<extra></extra>",
    )
)

# Layout
fig.update_layout(
    title={"text": "bubble-basic · plotly · pyplots.ai", "font": {"size": 32}, "x": 0.5, "xanchor": "center"},
    xaxis={
        "title": {"text": "X Variable", "font": {"size": 24}},
        "tickfont": {"size": 18},
        "gridcolor": "rgba(0,0,0,0.1)",
        "gridwidth": 1,
    },
    yaxis={
        "title": {"text": "Y Variable", "font": {"size": 24}},
        "tickfont": {"size": 18},
        "gridcolor": "rgba(0,0,0,0.1)",
        "gridwidth": 1,
    },
    template="plotly_white",
    showlegend=False,
    margin={"l": 100, "r": 100, "t": 120, "b": 100},
)

# Save
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html", include_plotlyjs="cdn")
