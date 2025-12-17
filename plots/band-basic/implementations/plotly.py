"""
band-basic: Basic Band Plot
Library: plotly
"""

import numpy as np
import plotly.graph_objects as go


# Data
np.random.seed(42)
x = np.linspace(0, 10, 100)
# Central trend line with some curvature
y_center = 2 + 0.5 * x + 0.3 * np.sin(x * 1.5)
# Uncertainty grows with x (heteroscedasticity)
uncertainty = 0.3 + 0.1 * x
y_lower = y_center - 1.96 * uncertainty
y_upper = y_center + 1.96 * uncertainty

# Plot
fig = go.Figure()

# Band (fill between lower and upper bounds)
fig.add_trace(
    go.Scatter(
        x=np.concatenate([x, x[::-1]]),
        y=np.concatenate([y_upper, y_lower[::-1]]),
        fill="toself",
        fillcolor="rgba(48, 105, 152, 0.3)",
        line={"color": "rgba(255, 255, 255, 0)"},
        hoverinfo="skip",
        showlegend=True,
        name="95% Confidence Interval",
    )
)

# Central trend line
fig.add_trace(go.Scatter(x=x, y=y_center, mode="lines", line={"color": "#306998", "width": 4}, name="Trend Line"))

# Layout
fig.update_layout(
    title={"text": "band-basic · plotly · pyplots.ai", "font": {"size": 48}, "x": 0.5, "xanchor": "center"},
    xaxis={
        "title": {"text": "Time", "font": {"size": 36}},
        "tickfont": {"size": 28},
        "gridcolor": "rgba(128, 128, 128, 0.3)",
        "gridwidth": 1,
    },
    yaxis={
        "title": {"text": "Value", "font": {"size": 36}},
        "tickfont": {"size": 28},
        "gridcolor": "rgba(128, 128, 128, 0.3)",
        "gridwidth": 1,
    },
    legend={
        "font": {"size": 28},
        "yanchor": "top",
        "y": 0.99,
        "xanchor": "left",
        "x": 0.01,
        "bgcolor": "rgba(255, 255, 255, 0.8)",
    },
    template="plotly_white",
    margin={"l": 100, "r": 50, "t": 120, "b": 100},
)

# Save
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html", include_plotlyjs=True, full_html=True)
