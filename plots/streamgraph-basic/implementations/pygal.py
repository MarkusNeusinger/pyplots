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
time_labels = [
    f"{['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][i % 12]} {2023 + i // 12}"
    for i in range(months)
]

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
    data[genre] = values.tolist()

# Calculate centered baseline for streamgraph effect
# Sum all values at each time point
totals = np.zeros(months)
for genre in genres:
    totals += np.array(data[genre])

# Create offset data for symmetric appearance around x-axis
# We'll shift the baseline so the visualization is centered
half_totals = totals / 2

# Create stacked data with offset for centered appearance
offset_data = {}
cumulative = -half_totals.copy()  # Start from negative half
for genre in genres:
    genre_values = np.array(data[genre])
    # Store the bottom position for this layer
    offset_data[genre] = (cumulative + genre_values / 2).tolist()
    cumulative += genre_values

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
    stroke_width=2,
    opacity=0.85,
    opacity_hover=0.95,
    transition="100ms ease-in",
)

# Create stacked line chart with fill (area chart - closest to streamgraph in pygal)
chart = pygal.StackedLine(
    width=4800,
    height=2700,
    title="streamgraph-basic · pygal · pyplots.ai",
    x_title="Month",
    y_title="Streaming Hours (millions)",
    style=custom_style,
    fill=True,
    show_dots=False,
    show_y_guides=True,
    show_x_guides=False,
    x_label_rotation=45,
    truncate_label=10,
    show_minor_x_labels=False,
    legend_at_bottom=False,
    legend_box_size=30,
    margin=50,
    spacing=20,
    interpolate="cubic",  # Smooth curves
)

# Set x-axis labels (show every 3rd month to avoid crowding)
chart.x_labels = time_labels
chart.x_labels_major = [time_labels[i] for i in range(0, months, 3)]

# Add data series
for genre in genres:
    chart.add(genre, data[genre])

# Save as PNG and HTML
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
