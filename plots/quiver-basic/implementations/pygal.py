"""
quiver-basic: Basic Quiver Plot
Library: pygal
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - 2D rotation flow field: u = -y, v = x (creates circular pattern)
np.random.seed(42)
grid_size = 10
x_range = np.linspace(-3, 3, grid_size)
y_range = np.linspace(-3, 3, grid_size)
X, Y = np.meshgrid(x_range, y_range)

# Vector field: rotation around origin
U = -Y  # Horizontal component
V = X  # Vertical component

# Flatten arrays
x_flat = X.flatten()
y_flat = Y.flatten()
u_flat = U.flatten()
v_flat = V.flatten()

# Compute magnitudes for color grouping
magnitudes = np.sqrt(u_flat**2 + v_flat**2)

# Scale vectors for visualization (prevent overlap)
scale = 0.4
u_scaled = np.where(magnitudes > 0.01, u_flat / magnitudes * np.minimum(magnitudes, 2) * scale, 0)
v_scaled = np.where(magnitudes > 0.01, v_flat / magnitudes * np.minimum(magnitudes, 2) * scale, 0)

# Custom style for 4800x2700 px canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#FFD43B", "#4a90c2", "#7ab8e0", "#aad4f0"),  # Python Blue first
    opacity=0.95,
    opacity_hover=1.0,
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=42,
    value_font_size=32,
    tooltip_font_size=36,
)

# Create XY chart for quiver visualization
# Pygal doesn't have native quiver support, so we use XY chart with lines
# Each vector shown as a line with dot at tip indicating direction
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="Rotation Flow Field · quiver-basic · pygal · pyplots.ai",
    x_title="X Coordinate",
    y_title="Y Coordinate",
    show_legend=False,  # Hide legend to avoid clutter
    stroke=True,
    stroke_style={"width": 6, "linecap": "round"},
    dots_size=14,
    show_x_guides=True,
    show_y_guides=True,
    range=(-4, 4),
    xrange=(-4, 4),
    margin=50,
)

# Add each vector as a separate series (line from base to tip)
# Use node config to control dot visibility at each point
for i in range(len(x_flat)):
    if magnitudes[i] > 0.01:  # Skip near-zero vectors
        base_x = float(x_flat[i])
        base_y = float(y_flat[i])
        tip_x = float(x_flat[i] + u_scaled[i])
        tip_y = float(y_flat[i] + v_scaled[i])

        # Each vector is a line with small dot at base, larger dot at tip
        chart.add(
            None,  # No label (legend disabled)
            [
                {"value": (base_x, base_y), "node": {"r": 4}},  # Small dot at base
                {"value": (tip_x, tip_y), "node": {"r": 14}},  # Larger dot at tip
            ],
            stroke_style={"width": 6},
        )

# Save outputs
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
