"""pyplots.ai
line-realtime: Real-Time Updating Line Chart
Library: bokeh | Python 3.13
Quality: pending | Created: 2025-12-31
"""

import numpy as np
import pandas as pd
from bokeh.io import export_png, output_file, save
from bokeh.models import Arrow, ColumnDataSource, Label, Range1d, VeeHead
from bokeh.plotting import figure


# Data - Simulated CPU usage over time with sliding window effect
np.random.seed(42)

# Generate 100 points of CPU usage data (we'll show last 60 as "visible window")
n_total = 100
n_visible = 60

# Create timestamps (every 100ms for last 10 seconds)
timestamps = pd.date_range(end=pd.Timestamp.now(), periods=n_total, freq="100ms")

# Generate realistic CPU usage with some patterns
base_usage = 45  # Base CPU usage %
trend = np.linspace(0, 10, n_total)  # Slight upward trend
noise = np.cumsum(np.random.randn(n_total) * 2)  # Random walk component
spikes = np.zeros(n_total)
spike_indices = [15, 35, 55, 78]  # Add some usage spikes
for idx in spike_indices:
    if idx < n_total:
        spikes[idx : idx + 5] = np.array([15, 25, 20, 10, 5])[: n_total - idx]

cpu_usage = base_usage + trend + noise + spikes
cpu_usage = np.clip(cpu_usage, 5, 95)  # Keep between 5-95%

# For static image: show the "visible window" portion
visible_timestamps = timestamps[-n_visible:]
visible_values = cpu_usage[-n_visible:]

# Create color gradient to show recency (older points fade)
alpha_values = np.linspace(0.3, 1.0, n_visible)
point_sizes = np.linspace(15, 30, n_visible)

# Create source for the main line with all data columns
source = ColumnDataSource(
    data={"x": visible_timestamps, "y": visible_values, "alpha": alpha_values, "size": point_sizes}
)

# Create figure - 4800x2700 for 16:9
p = figure(
    width=4800,
    height=2700,
    title="CPU Usage Monitor · line-realtime · bokeh · pyplots.ai",
    x_axis_label="Time",
    y_axis_label="CPU Usage (%)",
    x_axis_type="datetime",
    tools="",
    toolbar_location=None,
)

# Set axis range for Y with some padding
p.y_range = Range1d(0, 100)

# Draw gradient segments to show fading effect on older data
# Use multiple line segments with decreasing alpha
segment_size = 5
for i in range(0, n_visible - segment_size, segment_size):
    segment_x = visible_timestamps[i : i + segment_size + 1]
    segment_y = visible_values[i : i + segment_size + 1]
    segment_alpha = 0.3 + 0.7 * (i / n_visible)
    p.line(x=segment_x, y=segment_y, line_width=6, line_color="#306998", line_alpha=segment_alpha)

# Draw the most recent portion with full opacity
p.line(x=visible_timestamps[-15:], y=visible_values[-15:], line_width=8, line_color="#306998", line_alpha=1.0)

# Add scatter points (larger on recent, smaller on older)
p.scatter(
    x="x", y="y", source=source, size="size", fill_color="#306998", fill_alpha="alpha", line_color="white", line_width=2
)

# Highlight the current/latest value with a larger marker
latest_x = visible_timestamps[-1]
latest_y = visible_values[-1]
p.scatter(x=[latest_x], y=[latest_y], size=40, fill_color="#FFD43B", line_color="#306998", line_width=4)

# Add label showing current value
current_value_label = Label(
    x=latest_x,
    y=latest_y + 8,
    text=f"Current: {latest_y:.1f}%",
    text_font_size="36pt",
    text_color="#306998",
    text_font_style="bold",
    text_align="center",
)
p.add_layout(current_value_label)

# Add arrow indicating scroll direction (data flowing left)
arrow = Arrow(
    end=VeeHead(size=35, fill_color="#666666", line_color="#666666"),
    x_start=visible_timestamps[10],
    y_start=12,
    x_end=visible_timestamps[2],
    y_end=12,
    line_color="#666666",
    line_width=4,
)
p.add_layout(arrow)

# Add text label for scroll indicator
scroll_label = Label(
    x=visible_timestamps[6],
    y=16,
    text="Older data scrolls off",
    text_font_size="24pt",
    text_color="#666666",
    text_font_style="italic",
    text_align="center",
)
p.add_layout(scroll_label)

# Styling
p.title.text_font_size = "40pt"
p.title.text_color = "#306998"
p.xaxis.axis_label_text_font_size = "28pt"
p.yaxis.axis_label_text_font_size = "28pt"
p.xaxis.major_label_text_font_size = "22pt"
p.yaxis.major_label_text_font_size = "22pt"

# Grid styling
p.xgrid.grid_line_alpha = 0.3
p.ygrid.grid_line_alpha = 0.3
p.xgrid.grid_line_dash = [6, 4]
p.ygrid.grid_line_dash = [6, 4]

# Background
p.background_fill_color = "#fafafa"
p.border_fill_color = "white"

# Axis styling
p.xaxis.axis_line_width = 2
p.yaxis.axis_line_width = 2
p.xaxis.major_tick_line_width = 2
p.yaxis.major_tick_line_width = 2

# Save as PNG and HTML
export_png(p, filename="plot.png")
output_file("plot.html", title="Real-Time Line Chart - Bokeh")
save(p)
