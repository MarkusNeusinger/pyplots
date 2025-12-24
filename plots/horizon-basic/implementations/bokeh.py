""" pyplots.ai
horizon-basic: Horizon Chart
Library: bokeh 3.8.1 | Python 3.13.11
Quality: 86/100 | Created: 2025-12-24
"""

import numpy as np
from bokeh.io import export_png
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Label, Range1d, Title
from bokeh.plotting import figure, output_file, save


# Data - Server metrics over 24 hours for 6 servers
np.random.seed(42)

n_points = 200
n_series = 6
server_names = ["Web Server 1", "Web Server 2", "Database", "Cache Server", "API Gateway", "Load Balancer"]

# Create time series data with different patterns
hours = np.linspace(0, 24, n_points)

# Each server has a different pattern
series_data = []
for i, name in enumerate(server_names):
    # Base pattern with some periodicity
    base = np.sin(hours * np.pi / 6 + i * 0.5) * 20
    # Add some noise and trends
    noise = np.random.randn(n_points) * 10
    trend = np.sin(hours * np.pi / 12) * 15 * (1 + i * 0.2)
    # Add some spikes for realism
    spikes = np.zeros(n_points)
    spike_locations = np.random.choice(n_points, size=5, replace=False)
    spikes[spike_locations] = np.random.randn(5) * 30

    values = base + noise + trend + spikes
    series_data.append({"name": name, "hours": hours, "values": values})

# Horizon chart parameters
n_bands = 3  # Number of positive/negative bands
chart_width = 4800
total_height = 2700
individual_height = total_height // n_series  # ~450px per series

# Define colors - blue for positive, red for negative with increasing intensity
pos_colors = ["#a6cee3", "#306998", "#08306b"]  # Light to dark blue (using Python Blue)
neg_colors = ["#fbb4ae", "#e31a1c", "#67000d"]  # Light to dark red

# Create individual horizon plots
plots = []

for idx, data in enumerate(series_data):
    values = data["values"]
    x = data["hours"]
    name = data["name"]

    # Normalize values to fit in bands
    max_abs = np.max(np.abs(values))
    band_size = max_abs / n_bands

    # Create figure for this series
    p = figure(
        width=chart_width,
        height=individual_height,
        x_range=Range1d(0, 24),
        y_range=Range1d(0, band_size),
        tools="pan,wheel_zoom,box_zoom,reset,hover",
        toolbar_location="right" if idx == 0 else None,
    )

    # Configure axes
    if idx < len(series_data) - 1:
        p.xaxis.visible = False
    else:
        p.xaxis.axis_label = "Hour of Day"
        p.xaxis.axis_label_text_font_size = "24pt"
        p.xaxis.major_label_text_font_size = "20pt"

    p.yaxis.visible = False
    p.grid.visible = False
    p.outline_line_color = "#cccccc"
    p.outline_line_width = 1

    # Add series name as label on the left
    label = Label(
        x=0.3,
        y=band_size * 0.5,
        text=name,
        text_font_size="20pt",
        text_align="left",
        text_baseline="middle",
        text_color="#333333",
    )
    p.add_layout(label)

    # Draw horizon bands (folded areas)
    for band_idx in range(n_bands):
        band_min = band_idx * band_size

        # Positive values for this band
        pos_vals = np.clip(values - band_min, 0, band_size)
        pos_vals = np.where(values > band_min, pos_vals, 0)

        # Negative values for this band (mirrored)
        neg_vals = np.clip(-values - band_min, 0, band_size)
        neg_vals = np.where(values < -band_min, neg_vals, 0)

        # Create patches for positive band
        if np.any(pos_vals > 0):
            source_pos = ColumnDataSource(data={"x": x, "y": pos_vals})
            p.varea(x="x", y1=0, y2="y", source=source_pos, fill_color=pos_colors[band_idx], fill_alpha=0.9)

        # Create patches for negative band
        if np.any(neg_vals > 0):
            source_neg = ColumnDataSource(data={"x": x, "y": neg_vals})
            p.varea(x="x", y1=0, y2="y", source=source_neg, fill_color=neg_colors[band_idx], fill_alpha=0.9)

    plots.append(p)

# Add main title to the first plot
plots[0].add_layout(Title(text="horizon-basic · bokeh · pyplots.ai", text_font_size="32pt", align="center"), "above")

# Combine all plots vertically
layout = column(*plots)

# Save as HTML (interactive)
output_file("plot.html", title="Horizon Chart - pyplots.ai")
save(layout)

# Save as PNG
export_png(layout, filename="plot.png", width=chart_width, height=total_height)
