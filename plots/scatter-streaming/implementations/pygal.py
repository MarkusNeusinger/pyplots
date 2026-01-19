""" pyplots.ai
scatter-streaming: Streaming Scatter Plot
Library: pygal 3.1.0 | Python 3.13.11
Quality: 90/100 | Created: 2026-01-19
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - Simulated streaming sensor readings (150 points over 5 minutes)
np.random.seed(42)
n_points = 150

# Generate sensor readings that span the full axis range
# Temperature oscillates across 15-35°C range simulating daily variation
t = np.linspace(0, 4 * np.pi, n_points)
temperature = 25 + 8 * np.sin(t) + np.random.randn(n_points) * 2
temperature = np.clip(temperature, 15, 35)

# Humidity inversely correlated with temperature (hot = dry, cold = humid)
humidity = 75 - 1.5 * (temperature - 15) + np.random.randn(n_points) * 5
humidity = np.clip(humidity, 30, 80)

# Generate timestamps (seconds ago) for each point
timestamps = np.linspace(300, 0, n_points)  # 300s ago to now

# Define age bins with time-based labels (streaming over 5 minutes)
n_bins = 5
bin_edges = np.linspace(0, n_points, n_bins + 1, dtype=int)
# Contextual labels showing time windows
time_labels = ["0-60s ago", "60-120s ago", "120-180s ago", "180-240s ago", "240-300s ago"]
time_labels = time_labels[::-1]  # Reverse so newest is first in data order

# Color gradient from light (old) to dark (new) blue
age_colors = ("#a8c8e8", "#7baed4", "#4a90c2", "#306998", "#1a4d6e")

# Custom style for large canvas with enhanced legibility
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#222222",
    foreground_subtle="#555555",
    colors=age_colors,
    title_font_size=64,
    label_font_size=36,
    major_label_font_size=32,
    legend_font_size=40,
    value_font_size=28,
    tooltip_font_size=24,
)

# Create XY scatter chart with enhanced configuration
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
    legend_at_bottom_columns=5,
    legend_box_size=24,
    show_x_guides=True,
    show_y_guides=True,
    dots_size=14,
    range=(30, 80),
    xrange=(15, 35),
    tooltip_border_radius=8,
)

# Add each age group as a series with custom tooltips for interactivity
for i in range(n_bins):
    start_idx = bin_edges[i]
    end_idx = bin_edges[i + 1]

    # Create points with detailed tooltips showing exact sensor values
    points = []
    for j in range(start_idx, end_idx):
        temp = float(temperature[j])
        hum = float(humidity[j])
        age = float(timestamps[j])
        # Custom tooltip format using pygal's value dictionary
        points.append(
            {"value": (temp, hum), "label": f"Temp: {temp:.1f}°C | Humidity: {hum:.1f}% | Age: {age:.0f}s ago"}
        )

    # Newer data (higher i) has larger dots to show streaming progression
    chart.add(time_labels[i], points, dots_size=8 + i * 3)

# Render to PNG
chart.render_to_png("plot.png")

# Also save HTML for full interactivity with tooltips
chart.render_to_file("plot.html")
