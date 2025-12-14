"""
streamgraph-basic: Basic Stream Graph
Library: pygal
"""

import numpy as np
import pygal
from pygal.style import Style


# Data: monthly streaming hours by music genre over two years
np.random.seed(42)

months = 24
genres = ["Pop", "Rock", "Hip-Hop", "Electronic", "Jazz"]

# Generate smooth, realistic streaming data with trends
base_values = {"Pop": 45, "Rock": 35, "Hip-Hop": 40, "Electronic": 30, "Jazz": 15}

data = {}
for genre in genres:
    base = base_values[genre]
    trend = np.linspace(0, np.random.uniform(-10, 15), months)
    seasonal = 8 * np.sin(np.linspace(0, 4 * np.pi, months) + np.random.uniform(0, 2 * np.pi))
    noise = np.random.randn(months) * 3
    values = base + trend + seasonal + noise
    values = np.maximum(values, 5)  # Ensure positive values
    data[genre] = values

# Calculate centered baseline for streamgraph effect
# Sum all values at each time point for centering calculation
totals = np.zeros(months)
for genre in genres:
    totals += data[genre]

# Compute streamgraph layers with centered baseline (symmetric around y=0)
# Each layer spans from bottom_y to top_y, creating river-like flow
layers = {}
cumulative_bottom = -totals / 2  # Start at negative half of total (centered)

for genre in genres:
    genre_values = data[genre]
    top = cumulative_bottom + genre_values
    # Store bottom and top boundaries for each layer
    layers[genre] = {"bottom": cumulative_bottom.copy(), "top": top.copy()}
    cumulative_bottom = top.copy()

# Upsample data for smoother appearance using linear interpolation
# This creates more points between original data for smoother polygons
x_original = np.arange(months)
num_points = 100  # Total points for smooth curves
x_smooth = np.linspace(0, months - 1, num_points)

smooth_layers = {}
for genre in genres:
    # Linear interpolation - simple but ensures no overshooting
    smooth_layers[genre] = {
        "bottom": np.interp(x_smooth, x_original, layers[genre]["bottom"]),
        "top": np.interp(x_smooth, x_original, layers[genre]["top"]),
    }

# Custom style for 4800x2700 canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#FFD43B", "#E74C3C", "#2ECC71", "#9B59B6"),
    title_font_size=72,
    label_font_size=42,
    major_label_font_size=36,
    legend_font_size=42,
    value_font_size=36,
    stroke_width=0.5,
    opacity=0.85,
    opacity_hover=0.95,
    transition="100ms ease-in",
)

# Create XY chart to support negative y-values for centered streamgraph
# Using XY allows precise control over x,y coordinates for each point
chart = pygal.XY(
    width=4800,
    height=2700,
    title="streamgraph-basic · pygal · pyplots.ai",
    x_title="Month",
    y_title="Streaming Hours (millions)",
    style=custom_style,
    fill=True,
    stroke=True,
    show_dots=False,
    show_y_guides=True,
    show_x_guides=False,
    legend_at_bottom=True,  # Move legend to bottom to avoid overlap
    legend_box_size=30,
    margin=50,
    spacing=20,
    xrange=(0, months - 1),
)

# Add each genre as an XY series with polygon fill for streamgraph effect
# Each layer is defined by its bottom and top boundaries
for genre in genres:
    bottom = smooth_layers[genre]["bottom"]
    top = smooth_layers[genre]["top"]

    # Create polygon points: go forward along top, backward along bottom
    # This creates a closed shape for the filled area
    points = []

    # Top edge (left to right)
    for i in range(num_points):
        points.append((x_smooth[i], top[i]))

    # Bottom edge (right to left) to close the polygon
    for i in range(num_points - 1, -1, -1):
        points.append((x_smooth[i], bottom[i]))

    chart.add(genre, points)

# Save as PNG and HTML
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
