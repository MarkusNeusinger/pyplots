"""pyplots.ai
scatter-3d: 3D Scatter Plot
Library: plotly | Python 3.13
Quality: pending | Created: 2025-12-25
"""

import numpy as np
import plotly.graph_objects as go


# Data - 3D clustered data demonstrating spatial relationships
np.random.seed(42)

# Create three distinct clusters in 3D space
cluster1_x = np.random.randn(50) * 2 + 5
cluster1_y = np.random.randn(50) * 2 + 5
cluster1_z = np.random.randn(50) * 2 + 5

cluster2_x = np.random.randn(50) * 2 - 5
cluster2_y = np.random.randn(50) * 2 + 5
cluster2_z = np.random.randn(50) * 2 - 5

cluster3_x = np.random.randn(50) * 2
cluster3_y = np.random.randn(50) * 2 - 5
cluster3_z = np.random.randn(50) * 2

x = np.concatenate([cluster1_x, cluster2_x, cluster3_x])
y = np.concatenate([cluster1_y, cluster2_y, cluster3_y])
z = np.concatenate([cluster1_z, cluster2_z, cluster3_z])

# Color by z-value to demonstrate 4th dimension encoding
color = z

# Create 3D scatter plot
fig = go.Figure(
    data=[
        go.Scatter3d(
            x=x,
            y=y,
            z=z,
            mode="markers",
            marker={
                "size": 10,
                "color": color,
                "colorscale": "Viridis",
                "opacity": 0.8,
                "colorbar": {
                    "title": {"text": "Z Value", "font": {"size": 20}},
                    "tickfont": {"size": 16},
                    "thickness": 30,
                    "len": 0.7,
                },
            },
        )
    ]
)

# Update layout for large canvas
fig.update_layout(
    title={"text": "scatter-3d · plotly · pyplots.ai", "font": {"size": 32}, "x": 0.5, "xanchor": "center"},
    scene={
        "xaxis": {
            "title": {"text": "X Coordinate", "font": {"size": 20}},
            "tickfont": {"size": 14},
            "gridcolor": "rgba(128, 128, 128, 0.3)",
        },
        "yaxis": {
            "title": {"text": "Y Coordinate", "font": {"size": 20}},
            "tickfont": {"size": 14},
            "gridcolor": "rgba(128, 128, 128, 0.3)",
        },
        "zaxis": {
            "title": {"text": "Z Coordinate", "font": {"size": 20}},
            "tickfont": {"size": 14},
            "gridcolor": "rgba(128, 128, 128, 0.3)",
        },
        "camera": {"eye": {"x": 1.5, "y": 1.5, "z": 1.2}},
        "bgcolor": "white",
    },
    template="plotly_white",
    margin={"l": 50, "r": 50, "t": 100, "b": 50},
)

# Save as PNG (4800 x 2700 px)
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Save interactive HTML
fig.write_html("plot.html", include_plotlyjs="cdn")
