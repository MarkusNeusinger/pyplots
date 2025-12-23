"""pyplots.ai
area-basic: Basic Area Chart
Library: plotly | Python 3.13
Quality: pending | Created: 2025-12-23
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
visitors = np.maximum(visitors, 2000)  # Ensure no negative values

# Create figure
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=dates,
        y=visitors,
        mode="lines",
        fill="tozeroy",
        fillcolor="rgba(48, 105, 152, 0.4)",
        line={"color": "#306998", "width": 3},
        name="Daily Visitors",
    )
)

# Layout with proper sizing for 4800x2700 px
fig.update_layout(
    title={
        "text": "Daily Website Visitors · area-basic · plotly · pyplots.ai",
        "font": {"size": 28},
        "x": 0.5,
        "xanchor": "center",
    },
    xaxis={
        "title": {"text": "Date", "font": {"size": 22}},
        "tickfont": {"size": 18},
        "showgrid": True,
        "gridwidth": 1,
        "gridcolor": "rgba(0, 0, 0, 0.1)",
    },
    yaxis={
        "title": {"text": "Visitors (daily count)", "font": {"size": 22}},
        "tickfont": {"size": 18},
        "showgrid": True,
        "gridwidth": 1,
        "gridcolor": "rgba(0, 0, 0, 0.1)",
    },
    template="plotly_white",
    showlegend=False,
    margin={"l": 80, "r": 40, "t": 80, "b": 60},
)

# Save as PNG (4800x2700 px)
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Save interactive HTML
fig.write_html("plot.html")
