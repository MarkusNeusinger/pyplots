""" pyplots.ai
polar-basic: Basic Polar Chart
Library: bokeh 3.8.1 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-14
"""

import numpy as np
from bokeh.io import export_png, save
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure


# Data - Hourly temperature readings (24-hour cycle)
np.random.seed(42)
hours = np.arange(24)
theta = hours * (2 * np.pi / 24)  # Convert hours to radians (0-2π)

# Temperature pattern with random variation
base_temp = 15 + 8 * np.sin(theta - np.pi / 2)  # Peak at noon, low at night
temperature = base_temp + np.random.randn(24) * 1.5
radius = temperature - temperature.min() + 2  # Normalize to positive radius

# Convert polar to Cartesian for bokeh (bokeh doesn't have native polar support)
x = radius * np.cos(theta - np.pi / 2)  # Rotate so 0h is at top
y = radius * np.sin(theta - np.pi / 2)

source = ColumnDataSource(data={"x": x, "y": y, "radius": radius, "theta": theta, "hour": hours, "temp": temperature})

# Create figure
p = figure(
    width=4800,
    height=2700,
    title="polar-basic · bokeh · pyplots.ai",
    x_axis_label="",
    y_axis_label="",
    match_aspect=True,
)

# Draw polar grid manually
max_radius = np.ceil(radius.max()) + 1
grid_radii = np.linspace(0, max_radius, 5)[1:]  # Skip 0

# Radial gridlines (circles)
for r in grid_radii:
    circle_theta = np.linspace(0, 2 * np.pi, 100)
    cx = r * np.cos(circle_theta)
    cy = r * np.sin(circle_theta)
    p.line(cx, cy, line_color="#cccccc", line_width=1.5, line_alpha=0.5)

# Angular gridlines (spokes) at hour positions
for hour in [0, 3, 6, 9, 12, 15, 18, 21]:
    angle = hour * (2 * np.pi / 24) - np.pi / 2  # Rotate so 0h is at top
    p.line(
        [0, max_radius * np.cos(angle)],
        [0, max_radius * np.sin(angle)],
        line_color="#cccccc",
        line_width=1.5,
        line_alpha=0.5,
    )

# Add hour labels around the edge
label_radius = max_radius + 1.5
for hour in [0, 3, 6, 9, 12, 15, 18, 21]:
    angle = hour * (2 * np.pi / 24) - np.pi / 2
    lx = label_radius * np.cos(angle)
    ly = label_radius * np.sin(angle)
    label = f"{hour:02d}:00"
    p.text(
        x=[lx],
        y=[ly],
        text=[label],
        text_align="center",
        text_baseline="middle",
        text_font_size="18pt",
        text_color="#666666",
    )

# Connect points with line (in order)
p.line(x="x", y="y", source=source, line_color="#306998", line_width=3, line_alpha=0.7)

# Close the loop by connecting last point to first
p.line([x[-1], x[0]], [y[-1], y[0]], line_color="#306998", line_width=3, line_alpha=0.7)

# Plot data points
p.scatter(x="x", y="y", source=source, size=20, color="#306998", alpha=0.8)

# Styling
p.title.text_font_size = "28pt"
p.title.align = "center"

# Hide axes (we have our own polar grid)
p.xaxis.visible = False
p.yaxis.visible = False
p.xgrid.visible = False
p.ygrid.visible = False
p.outline_line_color = None

# Save outputs
export_png(p, filename="plot.png")
save(p, filename="plot.html")
