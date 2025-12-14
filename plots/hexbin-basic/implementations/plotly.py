"""
hexbin-basic: Basic Hexbin Plot
Library: plotly
"""

import numpy as np
import plotly.graph_objects as go


# Data - generate clustered bivariate data (10,000 points)
np.random.seed(42)
n_points = 10000

# Create clustered distribution with 3 centers
centers = [(0, 0), (3, 3), (-2, 4)]
points_per_cluster = n_points // 3

x_data = []
y_data = []

for cx, cy in centers:
    x_data.extend(np.random.randn(points_per_cluster) * 1.2 + cx)
    y_data.extend(np.random.randn(points_per_cluster) * 1.2 + cy)

x = np.array(x_data)
y = np.array(y_data)

# Create density plot (Plotly doesn't have native hexbin, using Histogram2dContour)
fig = go.Figure()

# Add 2D histogram as filled contour (density representation similar to hexbin)
fig.add_trace(
    go.Histogram2dContour(
        x=x,
        y=y,
        colorscale="Viridis",
        contours={"coloring": "heatmap", "showlabels": False},
        nbinsx=30,
        nbinsy=30,
        colorbar={
            "title": {"text": "Count", "font": {"size": 20}},
            "tickfont": {"size": 16},
            "thickness": 30,
            "len": 0.8,
        },
        hovertemplate="x: %{x:.2f}<br>y: %{y:.2f}<br>Count: %{z}<extra></extra>",
    )
)

# Layout
fig.update_layout(
    title={"text": "hexbin-basic · plotly · pyplots.ai", "font": {"size": 32}, "x": 0.5, "xanchor": "center"},
    xaxis={
        "title": {"text": "X Value", "font": {"size": 24}},
        "tickfont": {"size": 18},
        "gridcolor": "rgba(128, 128, 128, 0.2)",
        "gridwidth": 1,
        "zeroline": False,
    },
    yaxis={
        "title": {"text": "Y Value", "font": {"size": 24}},
        "tickfont": {"size": 18},
        "gridcolor": "rgba(128, 128, 128, 0.2)",
        "gridwidth": 1,
        "zeroline": False,
    },
    template="plotly_white",
    margin={"l": 100, "r": 120, "t": 100, "b": 100},
)

# Save as PNG (4800x2700 px)
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Save interactive HTML
fig.write_html("plot.html", include_plotlyjs=True, full_html=True)
