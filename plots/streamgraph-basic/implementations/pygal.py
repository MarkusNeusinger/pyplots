"""pyplots.ai
streamgraph-basic: Basic Stream Graph
Library: pygal 3.1.0 | Python 3.13.11
Quality: 68/100 | Created: 2025-12-23
"""

import numpy as np
import pygal
from pygal.style import Style


# Data: monthly streaming hours by music genre over two years
np.random.seed(42)

months = 24
month_labels = [
    "Jan'23",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
    "Jan'24",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]
genres = ["Pop", "Rock", "Hip-Hop", "Electronic", "Jazz"]

# Generate smooth, realistic streaming data with trends
base_values = {"Pop": 45, "Rock": 35, "Hip-Hop": 40, "Electronic": 30, "Jazz": 15}

data = {}
for genre in genres:
    base = base_values[genre]
    # Add trend over time
    trend = np.linspace(0, np.random.uniform(-10, 15), months)
    # Seasonal variation
    seasonal = 8 * np.sin(np.linspace(0, 4 * np.pi, months) + np.random.uniform(0, 2 * np.pi))
    # Random noise
    noise = np.random.randn(months) * 3
    values = base + trend + seasonal + noise
    values = np.maximum(values, 5)  # Ensure positive values
    data[genre] = values.tolist()

# Convert data to array for streamgraph calculation
data_array = np.array([data[genre] for genre in genres])

# Calculate centered baseline for true streamgraph effect
# Symmetric baseline: streams expand outward from center (x-axis at y=0)
total_at_each_time = data_array.sum(axis=0)
baseline_offset = total_at_each_time / 2

# Custom style with colorblind-safe palette
# Using colors with good contrast between adjacent layers
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#2c3e50",
    foreground_strong="#2c3e50",
    foreground_subtle="#7f8c8d",
    # Colorblind-friendly palette with good neighbor contrast
    colors=("#306998", "#2ecc71", "#9b59b6", "#e67e22", "#3498db"),
    title_font_size=80,
    label_font_size=48,
    major_label_font_size=40,
    legend_font_size=48,
    value_font_size=36,
    opacity=0.90,
    opacity_hover=0.95,
    guide_stroke_color="#e0e0e0",
    major_guide_stroke_color="#cccccc",
)

# Create StackedLine chart - pygal's native stacked area chart
# We'll shift all data to center around zero by subtracting half the total from each layer
chart = pygal.StackedLine(
    width=4800,
    height=2700,
    title="streamgraph-basic · pygal · pyplots.ai",
    x_title="Month",
    y_title="Streaming Hours (centered)",
    style=custom_style,
    fill=True,
    show_dots=False,
    show_y_guides=True,
    show_x_guides=False,
    legend_at_bottom=True,
    legend_box_size=36,
    margin=100,
    spacing=40,
    truncate_legend=-1,
    interpolate="cubic",  # Smooth flowing curves
    show_minor_x_labels=False,
    range=(-100, 100),  # Set y-axis range to show centering around 0
)

# Set x-axis labels showing months
chart.x_labels = month_labels
chart.x_labels_major = ["Jan'23", "Jul", "Jan'24", "Jul"]

# To create a centered streamgraph with StackedLine:
# We need to shift each layer's values so the visual center is at y=0
# First layer starts at -baseline_offset, subsequent layers stack on top

# Calculate shifted values for each layer
# The first (bottom) layer is shifted down by baseline_offset
# This makes the visual center of the total stack sit at y=0
shifted_data = []
for i, genre in enumerate(genres):
    if i == 0:
        # First layer: shift down by baseline to center the stream
        shifted_values = (np.array(data[genre]) - baseline_offset).tolist()
    else:
        # Subsequent layers: use original values (they stack on top)
        shifted_values = data[genre]
    shifted_data.append((genre, shifted_values))

# Add all layers
for genre, values in shifted_data:
    chart.add(genre, values)

# Save as PNG and HTML
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
