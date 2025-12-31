"""pyplots.ai
streamline-basic: Basic Streamline Plot
Library: plotly 6.5.0 | Python 3.13.11
Quality: 78/100 | Created: 2025-12-31
"""

import numpy as np
import plotly.figure_factory as ff


# Data - Create a grid for the vector field
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
speed = np.sqrt(u**2 + v**2)
u_norm = u / speed
v_norm = v / speed

# Create streamline plot
fig = ff.create_streamline(x, y, u_norm, v_norm, density=1.5, arrow_scale=0.08, line={"width": 2.5, "color": "#306998"})

# Update layout for large canvas with symmetric axis ranges
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
        "range": [-3.5, 3.5],
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
        "range": [-3.5, 3.5],
        "scaleanchor": "x",
        "scaleratio": 1,
    },
    template="plotly_white",
    margin={"l": 100, "r": 100, "t": 100, "b": 100},
    plot_bgcolor="white",
    showlegend=False,
)

# Save as PNG (4800 x 2700 px)
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Save interactive HTML version
fig.write_html("plot.html", include_plotlyjs="cdn")
