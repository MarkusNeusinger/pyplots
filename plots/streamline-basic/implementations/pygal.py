""" pyplots.ai
streamline-basic: Basic Streamline Plot
Library: pygal 3.1.0 | Python 3.13.11
Quality: 72/100 | Created: 2025-12-31
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - Vortex flow field (circular streamlines)
# u = -y, v = x creates counterclockwise circular flow
np.random.seed(42)

# Grid for vector field
grid_size = 30
x_range = np.linspace(-3, 3, grid_size)
y_range = np.linspace(-3, 3, grid_size)
X, Y = np.meshgrid(x_range, y_range)


def get_velocity(x, y):
    """Get velocity components at a point (vortex field)."""
    # Add slight radial component for spiral effect
    r = np.sqrt(x**2 + y**2)
    factor = 1.0 / (1.0 + 0.1 * r)  # Decay with distance
    u = -y * factor
    v = x * factor
    return u, v


def trace_streamline(x0, y0, dt=0.05, max_steps=200, bounds=3.0):
    """Trace a streamline from a starting point."""
    points = [(x0, y0)]
    x, y = x0, y0

    for _ in range(max_steps):
        u, v = get_velocity(x, y)
        speed = np.sqrt(u**2 + v**2)
        if speed < 0.001:  # Stagnation point
            break

        # Normalize and step
        x_new = x + dt * u / speed
        y_new = y + dt * v / speed

        # Check bounds
        if abs(x_new) > bounds or abs(y_new) > bounds:
            break

        x, y = x_new, y_new
        points.append((x, y))

    return points


# Generate streamlines from seed points distributed around the field
# Use a circular arrangement of starting points at various radii
streamlines = []
num_radii = 5
points_per_radius = 8

for r_idx in range(1, num_radii + 1):
    radius = r_idx * 0.5  # Radii: 0.5, 1.0, 1.5, 2.0, 2.5
    for angle_idx in range(points_per_radius):
        angle = 2 * np.pi * angle_idx / points_per_radius
        x0 = radius * np.cos(angle)
        y0 = radius * np.sin(angle)
        streamline = trace_streamline(x0, y0)
        if len(streamline) > 5:  # Only keep meaningful streamlines
            streamlines.append(streamline)

# Calculate magnitude for each streamline to assign color bins
# Use starting point magnitude as indicator
magnitudes = []
for sl in streamlines:
    x0, y0 = sl[0]
    r = np.sqrt(x0**2 + y0**2)
    magnitudes.append(r)

# Color bins based on radial distance (correlates with flow speed)
num_bins = 5
max_mag = max(magnitudes) if magnitudes else 1.0
bin_colors = ["#306998", "#3d8cc7", "#5ab4dc", "#e6a020", "#FFD43B"]
bin_labels = ["Inner", "Near-Inner", "Middle", "Near-Outer", "Outer"]

# Group streamlines by bins
binned_streamlines = {i: [] for i in range(num_bins)}
for sl, mag in zip(streamlines, magnitudes, strict=False):
    bin_idx = min(int((mag / max_mag) * num_bins), num_bins - 1)
    binned_streamlines[bin_idx].append(sl)

# Custom style with larger fonts for readability
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#555555",
    colors=tuple(bin_colors),
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=40,
    legend_font_size=48,
    value_font_size=32,
    guide_stroke_color="#cccccc",
)

# Create chart
chart = pygal.XY(
    style=custom_style,
    width=4800,
    height=2700,
    stroke=True,
    stroke_style={"width": 8},
    show_dots=False,
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=5,
    title="streamline-basic · pygal · pyplots.ai",
    x_title="X Position",
    y_title="Y Position",
    show_x_guides=True,
    show_y_guides=True,
    range=(-3.5, 3.5),
    xrange=(-3.5, 3.5),
)

# Add each bin as a series
for bin_idx in range(num_bins):
    series_data = []
    for sl in binned_streamlines[bin_idx]:
        # Add streamline points
        for point in sl:
            series_data.append(point)
        # Add None to separate streamlines
        series_data.append(None)

    if series_data:
        chart.add(bin_labels[bin_idx], series_data)

# Save outputs
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
