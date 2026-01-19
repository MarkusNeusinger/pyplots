"""pyplots.ai
map-route-path: Route Path Map
Library: pygal | Python 3.13
Quality: pending | Created: 2025-01-19
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - Simulated hiking trail GPS track (Central Park loop)
np.random.seed(42)

# Generate a realistic hiking trail path
n_points = 100
t = np.linspace(0, 2 * np.pi, n_points)

# Base path: elongated loop shape
base_lon = -73.97 + 0.015 * np.sin(t)
base_lat = 40.77 + 0.025 * np.cos(t) * (1 + 0.3 * np.sin(2 * t))

# Add small GPS noise for realism
lon = base_lon + np.random.normal(0, 0.0005, n_points)
lat = base_lat + np.random.normal(0, 0.0003, n_points)

# Custom style for pyplots
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#22AA22", "#DD3333"),
    title_font_size=48,
    label_font_size=28,
    major_label_font_size=24,
    legend_font_size=24,
    value_font_size=20,
    stroke_width=4,
    opacity=0.9,
)

# Create XY chart for route visualization
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="map-route-path · pygal · pyplots.ai",
    x_title="Longitude",
    y_title="Latitude",
    show_dots=False,
    stroke_style={"width": 4},
    show_x_guides=True,
    show_y_guides=True,
    dots_size=8,
)

# Add the route path as connected XY points
route_data = list(zip(lon, lat, strict=False))
chart.add("Hiking Trail", route_data, show_dots=False, stroke_style={"width": 4})

# Add start point (green)
chart.add("Start", [(lon[0], lat[0])], dots_size=20, stroke=False)

# Add end point (red)
chart.add("End", [(lon[-1], lat[-1])], dots_size=20, stroke=False)

# Save outputs
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
