"""pyplots.ai
contour-basic: Basic Contour Plot
Library: plotly | Python 3.13
Quality: pending | Created: 2025-12-23
"""

import numpy as np
import plotly.graph_objects as go


# Data - Simulated terrain elevation map (50x50 grid)
# Represents a mountainous region with peaks and valleys
np.random.seed(42)

# Coordinates in kilometers
x = np.linspace(0, 10, 50)  # 10 km east-west span
y = np.linspace(0, 10, 50)  # 10 km north-south span
X, Y = np.meshgrid(x, y)

# Elevation in meters - combination of terrain features
# Main mountain peak centered at (6, 5) with secondary ridge
elevation = (
    800 * np.exp(-((X - 6) ** 2 + (Y - 5) ** 2) / 4)  # Main peak ~800m
    + 500 * np.exp(-((X - 3) ** 2 + (Y - 7) ** 2) / 3)  # Secondary peak ~500m
    + 300 * np.exp(-((X - 2) ** 2 + (Y - 2) ** 2) / 5)  # Hill ~300m
    + 50 * np.sin(X * 0.8) * np.cos(Y * 0.6)  # Rolling terrain
    + 100  # Base elevation
)

# Create contour plot with filled regions and lines
fig = go.Figure()

# Filled contour for terrain visualization
fig.add_trace(
    go.Contour(
        x=x,
        y=y,
        z=elevation,
        colorscale="Viridis",
        contours={"showlabels": True, "labelfont": {"size": 16, "color": "white"}},
        colorbar={
            "title": {"text": "Elevation (m)", "font": {"size": 20}},
            "tickfont": {"size": 16},
            "thickness": 30,
            "len": 0.9,
        },
        line={"width": 2},
    )
)

# Layout for 4800x2700 px
fig.update_layout(
    title={
        "text": "Terrain Elevation Map · contour-basic · plotly · pyplots.ai",
        "font": {"size": 32},
        "x": 0.5,
        "xanchor": "center",
    },
    xaxis={"title": {"text": "Distance East (km)", "font": {"size": 24}}, "tickfont": {"size": 18}},
    yaxis={"title": {"text": "Distance North (km)", "font": {"size": 24}}, "tickfont": {"size": 18}},
    template="plotly_white",
    margin={"l": 100, "r": 120, "t": 100, "b": 100},
)

# Save as PNG (4800x2700 px)
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Save interactive HTML
fig.write_html("plot.html")
