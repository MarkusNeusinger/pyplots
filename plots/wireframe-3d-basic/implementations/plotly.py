""" pyplots.ai
wireframe-3d-basic: Basic 3D Wireframe Plot
Library: plotly 6.5.0 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-16
"""

import numpy as np
import plotly.graph_objects as go


# Data - Create a 30x30 grid with ripple function
np.random.seed(42)
x = np.linspace(-5, 5, 30)
y = np.linspace(-5, 5, 30)
X, Y = np.meshgrid(x, y)

# z = sin(sqrt(x^2 + y^2)) ripple function
R = np.sqrt(X**2 + Y**2)
Z = np.sin(R)

# Create 3D wireframe plot using Surface with wireframe style
fig = go.Figure()

fig.add_trace(
    go.Surface(
        x=X,
        y=Y,
        z=Z,
        colorscale=[[0, "#306998"], [0.5, "#4A8CBB"], [1, "#FFD43B"]],
        showscale=True,
        colorbar={
            "title": {"text": "Z Value", "font": {"size": 20}},
            "tickfont": {"size": 16},
            "thickness": 25,
            "len": 0.7,
        },
        # Wireframe style - show dense grid lines, no surface fill
        hidesurface=True,
        contours={
            "x": {"show": True, "color": "#306998", "width": 3, "highlightwidth": 4, "usecolormap": True},
            "y": {"show": True, "color": "#306998", "width": 3, "highlightwidth": 4, "usecolormap": True},
        },
    )
)

# Layout for 4800x2700 px with 3D camera settings
fig.update_layout(
    title={"text": "wireframe-3d-basic · plotly · pyplots.ai", "font": {"size": 32}, "x": 0.5, "xanchor": "center"},
    scene={
        "xaxis": {
            "title": {"text": "X", "font": {"size": 20}},
            "tickfont": {"size": 14},
            "gridcolor": "rgba(0,0,0,0.1)",
            "backgroundcolor": "rgba(255,255,255,0.9)",
        },
        "yaxis": {
            "title": {"text": "Y", "font": {"size": 20}},
            "tickfont": {"size": 14},
            "gridcolor": "rgba(0,0,0,0.1)",
            "backgroundcolor": "rgba(255,255,255,0.9)",
        },
        "zaxis": {
            "title": {"text": "Z", "font": {"size": 20}},
            "tickfont": {"size": 14},
            "gridcolor": "rgba(0,0,0,0.1)",
            "backgroundcolor": "rgba(255,255,255,0.9)",
        },
        "camera": {
            "eye": {"x": 1.5, "y": 1.5, "z": 1.0}  # elevation ~30, azimuth ~45
        },
        "aspectmode": "cube",
    },
    template="plotly_white",
    margin={"l": 20, "r": 80, "t": 100, "b": 20},
)

# Save as PNG (4800x2700 px)
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Save interactive HTML
fig.write_html("plot.html")
