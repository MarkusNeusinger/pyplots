"""pyplots.ai
histogram-2d: 2D Histogram Heatmap
Library: plotly | Python 3.13
Quality: pending | Created: 2025-12-25
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# Data - bivariate normal with correlation (5000 points for good density)
np.random.seed(42)
n_points = 5000

# Create correlated data with interesting cluster structure
mean = [0, 0]
cov = [[1, 0.7], [0.7, 1]]  # Positive correlation
data = np.random.multivariate_normal(mean, cov, n_points)
x = data[:, 0]
y = data[:, 1]

# Create figure with marginal histograms
fig = make_subplots(
    rows=2,
    cols=2,
    column_widths=[0.82, 0.18],
    row_heights=[0.18, 0.82],
    horizontal_spacing=0.02,
    vertical_spacing=0.02,
    specs=[[{"type": "xy"}, None], [{"type": "xy"}, {"type": "xy"}]],
)

# Main 2D histogram heatmap
fig.add_trace(
    go.Histogram2d(
        x=x,
        y=y,
        colorscale="Viridis",
        nbinsx=40,
        nbinsy=40,
        colorbar=dict(title=dict(text="Count", font=dict(size=20)), tickfont=dict(size=16), len=0.75, x=1.02),
    ),
    row=2,
    col=1,
)

# Marginal histogram for X (top)
fig.add_trace(go.Histogram(x=x, nbinsx=40, marker=dict(color="#306998"), showlegend=False), row=1, col=1)

# Marginal histogram for Y (right)
fig.add_trace(go.Histogram(y=y, nbinsy=40, marker=dict(color="#306998"), showlegend=False), row=2, col=2)

# Update layout
fig.update_layout(
    title=dict(text="histogram-2d · plotly · pyplots.ai", font=dict(size=32), x=0.5, xanchor="center"),
    template="plotly_white",
    bargap=0.05,
)

# Update axes for main plot
fig.update_xaxes(title=dict(text="X Value", font=dict(size=22)), tickfont=dict(size=18), row=2, col=1)
fig.update_yaxes(title=dict(text="Y Value", font=dict(size=22)), tickfont=dict(size=18), row=2, col=1)

# Hide axis labels for marginal plots
fig.update_xaxes(showticklabels=False, row=1, col=1)
fig.update_yaxes(showticklabels=False, row=1, col=1)
fig.update_xaxes(showticklabels=False, row=2, col=2)
fig.update_yaxes(showticklabels=False, row=2, col=2)

# Match axis ranges between main plot and marginals
fig.update_xaxes(matches="x3", row=1, col=1)
fig.update_yaxes(matches="y3", row=2, col=2)

# Save as PNG (4800 x 2700 px)
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Save as interactive HTML
fig.write_html("plot.html", include_plotlyjs="cdn")
