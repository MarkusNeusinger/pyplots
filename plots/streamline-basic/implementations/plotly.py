"""pyplots.ai
streamline-basic: Basic Streamline Plot
Library: plotly | Python 3.13
Quality: pending | Created: 2025-12-31
"""

import numpy as np
import plotly.figure_factory as ff
import plotly.graph_objects as go


# Data - Create a grid for the vector field
np.random.seed(42)
x = np.linspace(-3, 3, 30)
y = np.linspace(-3, 3, 30)

# Create vortex flow field: u = -y, v = x (circular streamlines)
# Add a source at center for more interesting pattern
X, Y = np.meshgrid(x, y)
R = np.sqrt(X**2 + Y**2) + 0.1  # Avoid division by zero

# Vortex + radial component for a spiral pattern
u = -Y / R + X / (R**2)
v = X / R + Y / (R**2)

# Normalize velocity for consistent line density
magnitude = np.sqrt(u**2 + v**2)
u_norm = u / magnitude
v_norm = v / magnitude

# Create streamline plot
fig = ff.create_streamline(x, y, u_norm, v_norm, density=1.5, arrow_scale=0.08, line={"width": 2.5, "color": "#306998"})

# Add colorbar trace for velocity magnitude (hidden points with color encoding)
scatter = go.Scatter(
    x=[None],
    y=[None],
    mode="markers",
    marker={
        "size": 0,
        "color": [0, np.max(magnitude)],
        "colorscale": [[0, "#306998"], [1, "#FFD43B"]],
        "colorbar": {
            "title": {"text": "Velocity<br>Magnitude", "font": {"size": 18}},
            "tickfont": {"size": 16},
            "len": 0.6,
            "thickness": 25,
        },
        "showscale": True,
    },
    showlegend=False,
    hoverinfo="skip",
)
fig.add_trace(scatter)

# Update layout for large canvas
fig.update_layout(
    title={"text": "streamline-basic · plotly · pyplots.ai", "font": {"size": 28}, "x": 0.5, "xanchor": "center"},
    xaxis={
        "title": {"text": "X Position", "font": {"size": 22}},
        "tickfont": {"size": 18},
        "showgrid": True,
        "gridwidth": 1,
        "gridcolor": "rgba(0,0,0,0.1)",
        "zeroline": True,
        "zerolinewidth": 2,
        "zerolinecolor": "rgba(0,0,0,0.3)",
    },
    yaxis={
        "title": {"text": "Y Position", "font": {"size": 22}},
        "tickfont": {"size": 18},
        "showgrid": True,
        "gridwidth": 1,
        "gridcolor": "rgba(0,0,0,0.1)",
        "zeroline": True,
        "zerolinewidth": 2,
        "zerolinecolor": "rgba(0,0,0,0.3)",
        "scaleanchor": "x",
        "scaleratio": 1,
    },
    template="plotly_white",
    margin={"l": 100, "r": 120, "t": 100, "b": 100},
    plot_bgcolor="white",
    showlegend=False,
)

# Save as PNG (4800 x 2700 px)
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Save interactive HTML version
fig.write_html("plot.html", include_plotlyjs="cdn")
