""" pyplots.ai
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
half_stack = total_at_each_time / 2

# Custom style with colorblind-safe palette
# Using colors with good contrast between adjacent layers
# Avoiding problematic yellow-coral adjacency
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#2c3e50",
    foreground_strong="#2c3e50",
    foreground_subtle="#7f8c8d",
    # First color is transparent (for baseline offset layer)
    # Remaining colors are colorblind-friendly with good neighbor contrast
    colors=("rgba(255,255,255,0)", "#306998", "#2ecc71", "#9b59b6", "#e67e22", "#3498db"),
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

# Create StackedLine chart with centered baseline effect
# Adding an invisible baseline offset layer creates the symmetric appearance
chart = pygal.StackedLine(
    width=4800,
    height=2700,
    title="streamgraph-basic · pygal · pyplots.ai",
    x_title="Month",
    y_title="Streaming Hours",
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
    include_x_axis=True,
)

# Set x-axis labels showing months
chart.x_labels = month_labels
chart.x_labels_major = ["Jan'23", "Jul", "Jan'24", "Jul"]

# Add invisible baseline offset layer (creates centered/symmetric appearance)
# This negative offset pushes the zero baseline down, centering the visible streams
baseline_layer = (-half_stack).tolist()
chart.add("", baseline_layer, show_dots=False)

# Add each genre series stacked on top of the centered baseline
for genre in genres:
    chart.add(genre, data[genre])

# Save as PNG and HTML
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
