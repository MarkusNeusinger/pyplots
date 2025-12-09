"""
area-stacked: Stacked Area Chart
Library: plotly
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go


# Data - Monthly revenue by product line over 2 years
np.random.seed(42)
dates = pd.date_range(start="2022-01-01", periods=24, freq="MS")

# Generate realistic revenue data with slight trends
base_product_a = 120 + np.arange(24) * 2 + np.random.randn(24) * 10
base_product_b = 90 + np.arange(24) * 1.5 + np.random.randn(24) * 8
base_product_c = 60 + np.arange(24) * 1 + np.random.randn(24) * 6
base_product_d = 40 + np.arange(24) * 0.5 + np.random.randn(24) * 5

# Ensure all values are positive
product_a = np.maximum(base_product_a, 10)
product_b = np.maximum(base_product_b, 10)
product_c = np.maximum(base_product_c, 10)
product_d = np.maximum(base_product_d, 10)

# Colors from style guide
colors = ["#306998", "#FFD43B", "#DC2626", "#059669"]

# Create figure
fig = go.Figure()

# Add traces in order (largest at bottom for stability)
# Product A - largest contributor
fig.add_trace(
    go.Scatter(
        x=dates,
        y=product_a,
        name="Product A",
        mode="lines",
        line={"width": 0.5, "color": colors[0]},
        fill="tozeroy",
        fillcolor="rgba(48, 105, 152, 0.75)",
        stackgroup="one",
    )
)

# Product B
fig.add_trace(
    go.Scatter(
        x=dates,
        y=product_b,
        name="Product B",
        mode="lines",
        line={"width": 0.5, "color": colors[1]},
        fill="tonexty",
        fillcolor="rgba(255, 212, 59, 0.75)",
        stackgroup="one",
    )
)

# Product C
fig.add_trace(
    go.Scatter(
        x=dates,
        y=product_c,
        name="Product C",
        mode="lines",
        line={"width": 0.5, "color": colors[2]},
        fill="tonexty",
        fillcolor="rgba(220, 38, 38, 0.75)",
        stackgroup="one",
    )
)

# Product D - smallest contributor
fig.add_trace(
    go.Scatter(
        x=dates,
        y=product_d,
        name="Product D",
        mode="lines",
        line={"width": 0.5, "color": colors[3]},
        fill="tonexty",
        fillcolor="rgba(5, 150, 105, 0.75)",
        stackgroup="one",
    )
)

# Layout
fig.update_layout(
    title={"text": "Monthly Revenue by Product Line", "font": {"size": 36}},
    xaxis_title={"text": "Date", "font": {"size": 32}},
    yaxis_title={"text": "Revenue ($K)", "font": {"size": 32}},
    template="plotly_white",
    legend={"font": {"size": 28}, "orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "center", "x": 0.5},
    xaxis={"tickfont": {"size": 24}, "showgrid": True, "gridwidth": 1, "gridcolor": "rgba(0, 0, 0, 0.1)"},
    yaxis={"tickfont": {"size": 24}, "showgrid": True, "gridwidth": 1, "gridcolor": "rgba(0, 0, 0, 0.1)"},
    margin={"l": 80, "r": 40, "t": 120, "b": 80},
)

# Save as PNG and HTML
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html")
