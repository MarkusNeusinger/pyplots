"""pyplots.ai
line-realtime: Real-Time Updating Line Chart
Library: pygal | Python 3.13
Quality: pending | Created: 2025-12-31
"""

from datetime import datetime, timedelta

import numpy as np
import pygal
from pygal.style import Style


# Data - Simulated CPU usage with real-time characteristics
np.random.seed(42)
n_points = 60  # 60 seconds of data at 1-second intervals

# Generate realistic CPU usage pattern with some spikes
base_cpu = 35  # Base CPU usage
trend = np.linspace(0, 10, n_points)  # Slight upward trend
noise = np.random.normal(0, 8, n_points)  # Random fluctuations
spikes = np.zeros(n_points)
spike_positions = [15, 28, 42, 55]  # Add some load spikes
for pos in spike_positions:
    if pos < n_points:
        spikes[pos : min(pos + 3, n_points)] = np.array([25, 15, 8])[: min(3, n_points - pos)]

cpu_usage = base_cpu + trend + noise + spikes
cpu_usage = np.clip(cpu_usage, 0, 100)  # Keep in valid range

# Create timestamps for x-axis labels (showing sliding window)
end_time = datetime(2025, 12, 31, 14, 30, 0)
timestamps = [end_time - timedelta(seconds=n_points - 1 - i) for i in range(n_points)]

# Format labels - show every 10 seconds
x_labels = []
for i, ts in enumerate(timestamps):
    if i % 10 == 0 or i == n_points - 1:
        x_labels.append(ts.strftime("%H:%M:%S"))
    else:
        x_labels.append("")

# Custom style for 4800x2700 canvas
custom_style = Style(
    background="white",
    plot_background="#fafafa",
    foreground="#333333",
    foreground_strong="#1a1a1a",
    foreground_subtle="#666666",
    colors=("#306998", "#FFD43B", "#e74c3c"),  # Primary colors + accent for current value
    title_font_size=72,
    label_font_size=42,
    major_label_font_size=38,
    legend_font_size=48,
    value_font_size=36,
    value_label_font_size=32,
    tooltip_font_size=32,
    stroke_width=6,
    font_family="sans-serif",
    opacity=0.9,
    opacity_hover=1.0,
)

# Create line chart
chart = pygal.Line(
    width=4800,
    height=2700,
    style=custom_style,
    title="CPU Usage Monitor (Live) · line-realtime · pygal · pyplots.ai",
    x_title="Time (HH:MM:SS)",
    y_title="CPU Usage (%)",
    show_dots=True,
    dots_size=8,
    stroke_style={"width": 6, "linecap": "round", "linejoin": "round"},
    show_legend=True,
    legend_at_bottom=False,
    legend_box_size=30,
    show_x_guides=False,
    show_y_guides=True,
    y_labels_major_every=2,
    truncate_label=-1,
    x_label_rotation=45,
    range=(0, 100),
    fill=True,
    margin=60,
    margin_bottom=180,
    margin_left=180,
    print_values=False,
    show_minor_x_labels=True,
    interpolate="cubic",
)

# Set x-axis labels
chart.x_labels = x_labels

# Add main CPU usage line
chart.add("CPU Usage", list(cpu_usage), stroke_style={"width": 6})

# Get current value for display in legend
current_value = cpu_usage[-1]

# Add a horizontal reference line at warning threshold (80%)
warning_threshold = [80] * n_points
chart.add(
    "Warning Threshold (80%)",
    warning_threshold,
    stroke_style={"width": 4, "dasharray": "20, 10"},
    show_dots=False,
    fill=False,
)

# Add current value indicator (last 3 points highlighted)
highlight_values = [None] * (n_points - 3) + list(cpu_usage[-3:])
chart.add(f"Current: {current_value:.1f}%", highlight_values, stroke_style={"width": 8}, dots_size=16, fill=False)

# Save as PNG
chart.render_to_png("plot.png")

# Also save as HTML for interactivity
chart.render_to_file("plot.html")
