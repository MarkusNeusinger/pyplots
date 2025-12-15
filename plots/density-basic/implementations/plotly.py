"""
density-basic: Basic Density Plot
Library: plotly
"""

import numpy as np
import plotly.graph_objects as go


# Data - Test scores with realistic bimodal distribution
np.random.seed(42)
scores = np.concatenate(
    [
        np.random.normal(72, 10, 300),  # Main group around 72
        np.random.normal(88, 5, 100),  # High achievers around 88
    ]
)

# Compute KDE using Silverman's rule of thumb for bandwidth
n = len(scores)
std = np.std(scores, ddof=1)
iqr = np.percentile(scores, 75) - np.percentile(scores, 25)
bandwidth = 0.9 * min(std, iqr / 1.34) * n ** (-0.2)

# Evaluate density at each point on a grid
x_range = np.linspace(scores.min() - 10, scores.max() + 10, 500)
density = np.zeros_like(x_range)
for xi in scores:
    density += np.exp(-0.5 * ((x_range - xi) / bandwidth) ** 2)
density /= n * bandwidth * np.sqrt(2 * np.pi)

# Create figure
fig = go.Figure()

# Density curve with fill
fig.add_trace(
    go.Scatter(
        x=x_range,
        y=density,
        mode="lines",
        fill="tozeroy",
        fillcolor="rgba(48, 105, 152, 0.3)",
        line={"color": "#306998", "width": 4},
        name="Density",
        hovertemplate="Score: %{x:.1f}<br>Density: %{y:.4f}<extra></extra>",
    )
)

# Rug plot showing individual observations
fig.add_trace(
    go.Scatter(
        x=scores,
        y=[-0.001] * len(scores),
        mode="markers",
        marker={"symbol": "line-ns", "size": 12, "color": "#306998", "line": {"width": 1.5}},
        name="Observations",
        hovertemplate="Score: %{x:.1f}<extra></extra>",
    )
)

# Layout
fig.update_layout(
    title={"text": "density-basic · plotly · pyplots.ai", "font": {"size": 36}, "x": 0.5, "xanchor": "center"},
    xaxis={
        "title": {"text": "Test Score", "font": {"size": 28}},
        "tickfont": {"size": 22},
        "showgrid": True,
        "gridwidth": 1,
        "gridcolor": "rgba(128, 128, 128, 0.2)",
        "zeroline": False,
    },
    yaxis={
        "title": {"text": "Density", "font": {"size": 28}},
        "tickfont": {"size": 22},
        "showgrid": True,
        "gridwidth": 1,
        "gridcolor": "rgba(128, 128, 128, 0.2)",
        "zeroline": False,
        "rangemode": "tozero",
    },
    template="plotly_white",
    showlegend=True,
    legend={
        "font": {"size": 20},
        "x": 0.98,
        "y": 0.98,
        "xanchor": "right",
        "yanchor": "top",
        "bgcolor": "rgba(255, 255, 255, 0.8)",
    },
    margin={"l": 100, "r": 60, "t": 100, "b": 100},
)

# Save as PNG and HTML
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html", include_plotlyjs="cdn")
