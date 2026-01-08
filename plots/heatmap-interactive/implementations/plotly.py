""" pyplots.ai
heatmap-interactive: Interactive Heatmap with Hover and Zoom
Library: plotly 6.5.1 | Python 3.13.11
Quality: 92/100 | Created: 2026-01-08
"""

import numpy as np
import plotly.graph_objects as go


# Data - Generate a correlation-like matrix for exploration
np.random.seed(42)
n_rows, n_cols = 25, 30

# Create row and column labels
row_labels = [f"Variable {i + 1}" for i in range(n_rows)]
col_labels = [f"Feature {j + 1}" for j in range(n_cols)]

# Generate correlation-like data with patterns
base_matrix = np.random.randn(n_rows, n_cols)
# Add some structure - blocks of correlation
for i in range(0, n_rows, 5):
    for j in range(0, n_cols, 6):
        block_size_r = min(5, n_rows - i)
        block_size_c = min(6, n_cols - j)
        base_matrix[i : i + block_size_r, j : j + block_size_c] += np.random.uniform(-1, 1)

# Normalize to range [-1, 1] for correlation-like values
z_values = np.tanh(base_matrix * 0.5)

# Create custom hover text
hover_text = [
    [f"Row: {row_labels[i]}<br>Column: {col_labels[j]}<br>Value: {z_values[i, j]:.3f}" for j in range(n_cols)]
    for i in range(n_rows)
]

# Create heatmap figure
fig = go.Figure(
    data=go.Heatmap(
        z=z_values,
        x=col_labels,
        y=row_labels,
        colorscale="RdBu_r",
        zmid=0,
        zmin=-1,
        zmax=1,
        hovertemplate="%{text}<extra></extra>",
        text=hover_text,
        colorbar=dict(
            title=dict(text="Correlation", font=dict(size=20)), tickfont=dict(size=16), thickness=25, len=0.9
        ),
    )
)

# Update layout for interactivity and visibility
fig.update_layout(
    title=dict(text="heatmap-interactive · plotly · pyplots.ai", font=dict(size=32), x=0.5, xanchor="center"),
    xaxis=dict(
        title=dict(text="Features", font=dict(size=24)),
        tickfont=dict(size=14),
        tickangle=-45,
        showgrid=False,
        constrain="domain",
    ),
    yaxis=dict(
        title=dict(text="Variables", font=dict(size=24)),
        tickfont=dict(size=14),
        showgrid=False,
        autorange="reversed",
        constrain="domain",
        scaleanchor="x",
    ),
    template="plotly_white",
    width=1600,
    height=900,
    margin=dict(l=120, r=80, t=100, b=120),
    # Enable zoom and pan
    dragmode="zoom",
)

# Add modebar buttons for interactivity
fig.update_layout(
    modebar=dict(
        orientation="h",
        bgcolor="rgba(255,255,255,0.8)",
        add=["zoom", "pan", "zoomIn", "zoomOut", "autoScale", "resetScale"],
    )
)

# Enable spike lines for crosshair effect on hover
fig.update_xaxes(
    showspikes=True, spikemode="across", spikesnap="cursor", spikethickness=2, spikecolor="#306998", spikedash="solid"
)
fig.update_yaxes(
    showspikes=True, spikemode="across", spikesnap="cursor", spikethickness=2, spikecolor="#306998", spikedash="solid"
)

# Save as PNG
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Save interactive HTML
fig.write_html("plot.html", include_plotlyjs=True, full_html=True)
