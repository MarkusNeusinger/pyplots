"""pyplots.ai
quiver-basic: Basic Quiver Plot
Library: pygal | Python 3.13
Quality: pending | Created: 2025-12-23
"""

import math

import numpy as np
import pygal
from pygal.style import Style


# Data - Create a 10x10 grid with circular rotation pattern (u = -y, v = x)
np.random.seed(42)
grid_size = 10
x_range = np.linspace(-2, 2, grid_size)
y_range = np.linspace(-2, 2, grid_size)
X, Y = np.meshgrid(x_range, y_range)
x_flat = X.flatten()
y_flat = Y.flatten()

# Circular rotation field: u = -y, v = x
U = -y_flat
V = x_flat

# Calculate magnitude for scaling - magnitude increases with distance from origin
magnitude = np.sqrt(U**2 + V**2)

# Scale vectors proportionally to magnitude for visual clarity
# Scale factor determines overall arrow size
arrow_scale = 0.08
U_scaled = U * arrow_scale
V_scaled = V * arrow_scale

# Arrowhead parameters - proportional to arrow length
head_ratio = 0.35
head_angle = 0.5

# Build arrow data: shaft + left head + right head for each arrow
arrow_data = []
for i in range(len(x_flat)):
    # Skip zero-magnitude vectors (center point)
    if magnitude[i] < 0.01:
        continue

    x1, y1 = x_flat[i], y_flat[i]
    x2, y2 = x1 + U_scaled[i], y1 + V_scaled[i]

    # Calculate arrowhead size based on arrow length
    arrow_len = math.sqrt(U_scaled[i] ** 2 + V_scaled[i] ** 2)
    head_size = arrow_len * head_ratio

    # Calculate arrowhead points
    angle = math.atan2(V_scaled[i], U_scaled[i])
    x_left = x2 - head_size * math.cos(angle - head_angle)
    y_left = y2 - head_size * math.sin(angle - head_angle)
    x_right = x2 - head_size * math.cos(angle + head_angle)
    y_right = y2 - head_size * math.sin(angle + head_angle)

    # Shaft (base to tip)
    arrow_data.extend([(x1, y1), (x2, y2), None])
    # Left arrowhead line
    arrow_data.extend([(x2, y2), (x_left, y_left), None])
    # Right arrowhead line
    arrow_data.extend([(x2, y2), (x_right, y_right), None])

# Custom style for pyplots
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998",),
    title_font_size=56,
    label_font_size=36,
    major_label_font_size=32,
    legend_font_size=32,
    value_font_size=28,
    guide_stroke_color="#cccccc",
)

# Create chart
chart = pygal.XY(
    style=custom_style,
    width=4800,
    height=2700,
    stroke=True,
    stroke_style={"width": 5},
    show_dots=False,
    show_legend=False,
    title="quiver-basic · pygal · pyplots.ai",
    x_title="X Position",
    y_title="Y Position",
    show_x_guides=True,
    show_y_guides=True,
    range=(-2.5, 2.5),
    xrange=(-2.5, 2.5),
)

# Add vector field data
chart.add("Vectors", arrow_data)

# Save outputs
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
