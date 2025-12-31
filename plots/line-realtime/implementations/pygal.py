"""pyplots.ai
line-realtime: Real-Time Updating Line Chart
Library: pygal 3.1.0 | Python 3.13.11
Quality: 88/100 | Created: 2025-12-31
"""

from datetime import datetime, timedelta

import numpy as np
import pygal
from pygal.style import Style


# Data - Simulated CPU usage with real-time characteristics
np.random.seed(42)
n_points = 60  # 60 seconds of data at 1-second intervals

# Generate realistic CPU usage pattern with spikes crossing the warning threshold
base_cpu = 45  # Base CPU usage
trend = np.linspace(0, 15, n_points)  # Upward trend approaching warning zone
noise = np.random.normal(0, 6, n_points)  # Random fluctuations
spikes = np.zeros(n_points)
# Add load spikes - one major spike crossing the 80% warning threshold
spike_positions = [15, 28, 42]
spike_magnitudes = [20, 45, 25]  # Second spike will push above 80%
for pos, mag in zip(spike_positions, spike_magnitudes, strict=True):
    if pos < n_points:
        decay = np.array([mag, mag * 0.6, mag * 0.3])[: min(3, n_points - pos)]
        spikes[pos : min(pos + 3, n_points)] = decay

cpu_usage = base_cpu + trend + noise + spikes
cpu_usage = np.clip(cpu_usage, 5, 98)  # Keep in valid range with headroom

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
    colors=("#a0a0a0", "#306998", "#FFD43B", "#e74c3c"),  # Faded gray, primary, warning, live indicator
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

# Add faded trailing edge (older data) to indicate scrolling direction
# First 10 points shown with reduced opacity to create fade effect
fade_end = 10
fade_values = list(cpu_usage[:fade_end]) + [None] * (n_points - fade_end)
chart.add(
    "← Older Data", fade_values, stroke_style={"width": 4, "opacity": 0.35}, dots_size=4, fill=False, show_dots=True
)

# Add main CPU usage line (without faded portion for visual clarity)
main_values = [None] * (fade_end - 1) + list(cpu_usage[fade_end - 1 :])
chart.add("CPU Usage", main_values, stroke_style={"width": 6})

# Get current value for display in legend
current_value = cpu_usage[-1]

# Add a horizontal reference line at warning threshold (80%)
warning_threshold = [80] * n_points
chart.add(
    "Warning 80%", warning_threshold, stroke_style={"width": 4, "dasharray": "20, 10"}, show_dots=False, fill=False
)

# Add current value indicator (last 5 points highlighted) with "LIVE" indicator
highlight_values = [None] * (n_points - 5) + list(cpu_usage[-5:])
chart.add(f"LIVE → {current_value:.1f}%", highlight_values, stroke_style={"width": 8}, dots_size=16, fill=False)

# Save as PNG
chart.render_to_png("plot.png")

# Also save as HTML for interactivity
chart.render_to_file("plot.html")
