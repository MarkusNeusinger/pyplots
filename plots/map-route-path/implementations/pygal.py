"""pyplots.ai
map-route-path: Route Path Map
Library: pygal 3.1.0 | Python 3.13.11
Quality: 72/100 | Created: 2026-01-19
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - Simulated hiking trail GPS track (Central Park loop)
np.random.seed(42)

# Generate a realistic hiking trail path with time progression
n_points = 100
t = np.linspace(0, 2 * np.pi, n_points)

# Base path: elongated loop shape
base_lon = -73.97 + 0.015 * np.sin(t)
base_lat = 40.77 + 0.025 * np.cos(t) * (1 + 0.3 * np.sin(2 * t))

# Add small GPS noise for realism
lon = base_lon + np.random.normal(0, 0.0005, n_points)
lat = base_lat + np.random.normal(0, 0.0003, n_points)

# Color gradient from blue to purple to show time progression
# Split route into segments with different colors
n_segments = 5
segment_size = n_points // n_segments

# Define gradient colors (blue -> cyan -> green -> yellow -> orange)
gradient_colors = ["#0066CC", "#0099AA", "#22AA66", "#AAAA22", "#DD6622"]

# Custom style for pyplots
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=tuple(gradient_colors + ["#22AA22", "#DD3333"]),
    title_font_size=48,
    label_font_size=28,
    major_label_font_size=24,
    legend_font_size=24,
    value_font_size=20,
    stroke_width=5,
    opacity=0.95,
)

# Create XY chart for route visualization
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="map-route-path · pygal · pyplots.ai",
    x_title="Longitude (degrees)",
    y_title="Latitude (degrees)",
    show_dots=True,
    dots_size=3,
    stroke_style={"width": 5},
    show_x_guides=True,
    show_y_guides=True,
)

# Add route segments with color gradient to show time progression
for i in range(n_segments):
    start_idx = i * segment_size
    end_idx = min((i + 1) * segment_size + 1, n_points)
    segment_data = list(zip(lon[start_idx:end_idx], lat[start_idx:end_idx], strict=False))
    label = f"Segment {i + 1}" if i > 0 else "Route Start →"
    chart.add(label, segment_data, dots_size=3, stroke_style={"width": 5})

# Add start point marker (large green dot)
chart.add("▶ Start", [{"value": (lon[0], lat[0]), "node": {"r": 25}}], dots_size=25, stroke=False, show_dots=True)

# Add end point marker (large red dot)
chart.add("◼ End", [{"value": (lon[-1], lat[-1]), "node": {"r": 25}}], dots_size=25, stroke=False, show_dots=True)

# Save outputs
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
