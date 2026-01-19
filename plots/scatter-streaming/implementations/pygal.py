"""pyplots.ai
scatter-streaming: Streaming Scatter Plot
Library: pygal | Python 3.13
Quality: pending | Created: 2025-01-19
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - Simulated streaming sensor readings
np.random.seed(42)
n_points = 150

# Generate sensor readings: temperature vs humidity with some correlation
temperature = 20 + np.cumsum(np.random.randn(n_points) * 0.3)  # Wandering temperature
humidity = 50 + 0.5 * (temperature - 25) + np.random.randn(n_points) * 5  # Correlated humidity

# Normalize for axis ranges
temperature = np.clip(temperature, 15, 35)
humidity = np.clip(humidity, 30, 80)

# Custom style for large canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998",),  # Python blue
    title_font_size=48,
    label_font_size=32,
    major_label_font_size=28,
    legend_font_size=28,
    value_font_size=24,
    tooltip_font_size=20,
)

# Create XY scatter chart
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="scatter-streaming · pygal · pyplots.ai",
    x_title="Temperature (°C)",
    y_title="Humidity (%)",
    show_dots=True,
    stroke=False,
    show_legend=True,
    legend_at_bottom=True,
    show_x_guides=True,
    show_y_guides=True,
    dots_size=12,
    range=(30, 80),
    xrange=(15, 35),
)

# Group points by age into bins for visual age encoding
# Pygal doesn't support per-point opacity, so we use varying dot sizes
n_bins = 5
bin_edges = np.linspace(0, n_points, n_bins + 1, dtype=int)
labels = ["Oldest", "Older", "Recent", "Newer", "Newest"]

# Add each age group as a series with increasing dot sizes
for i in range(n_bins):
    start_idx = bin_edges[i]
    end_idx = bin_edges[i + 1]

    # Extract points for this age bin
    points = [(float(temperature[j]), float(humidity[j])) for j in range(start_idx, end_idx)]

    # Newer data has larger dots to show streaming progression
    chart.add(f"{labels[i]} data", points, dots_size=8 + i * 2)

# Render to PNG
chart.render_to_png("plot.png")

# Also save HTML for interactivity
chart.render_to_file("plot.html")
