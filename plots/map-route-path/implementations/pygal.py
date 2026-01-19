"""pyplots.ai
map-route-path: Route Path Map
Library: pygal 3.1.0 | Python 3.13.11
Quality: 68/100 | Created: 2026-01-19
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

# Split route into segments with distinct colors for time progression
n_segments = 5
segment_size = n_points // n_segments

# Define distinct gradient colors with high contrast (blue -> cyan -> green -> yellow -> red)
gradient_colors = ["#1E3A8A", "#0891B2", "#16A34A", "#EAB308", "#DC2626"]

# Custom style with larger fonts for better legibility
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#1F2937",
    foreground_strong="#111827",
    foreground_subtle="#4B5563",
    colors=tuple(gradient_colors + ["#15803D", "#B91C1C"]),
    title_font_size=64,
    label_font_size=36,
    major_label_font_size=32,
    legend_font_size=36,
    value_font_size=28,
    stroke_width=8,
    opacity=1.0,
)

# Create XY chart for route visualization
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="map-route-path · pygal · pyplots.ai",
    x_title="Longitude (degrees)",
    y_title="Latitude (degrees)",
    show_dots=False,
    stroke_style={"width": 8, "linecap": "round", "linejoin": "round"},
    show_x_guides=True,
    show_y_guides=True,
    legend_at_bottom=True,
    legend_box_size=24,
    truncate_legend=-1,
)

# Add route segments with color gradient to show time progression
segment_labels = ["1: Start", "2: Morning", "3: Midday", "4: Afternoon", "5: End"]
for i in range(n_segments):
    start_idx = i * segment_size
    end_idx = min((i + 1) * segment_size + 1, n_points)
    segment_data = list(zip(lon[start_idx:end_idx], lat[start_idx:end_idx], strict=False))
    chart.add(segment_labels[i], segment_data, stroke_style={"width": 8})

# Add start point marker (distinct green square)
start_data = [(lon[0], lat[0])]
chart.add("▶ START", [{"value": start_data[0], "node": {"r": 20}}], dots_size=20, stroke=False, show_dots=True)

# Add end point marker (distinct red square)
end_data = [(lon[-1], lat[-1])]
chart.add("◼ FINISH", [{"value": end_data[0], "node": {"r": 20}}], dots_size=20, stroke=False, show_dots=True)

# Save outputs
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
