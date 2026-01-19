"""pyplots.ai
scatter-streaming: Streaming Scatter Plot
Library: bokeh | Python 3.13
Quality: pending | Created: 2025-01-19
"""

import numpy as np
import pandas as pd
from bokeh.io import export_png
from bokeh.models import ColumnDataSource
from bokeh.palettes import Blues9
from bokeh.plotting import figure, output_file, save


# Data: Simulated sensor readings (temperature vs humidity)
# Streaming effect shown via opacity gradient (older points = more transparent)
np.random.seed(42)

# Simulate streaming data buffer with 200 points
n_points = 200

# Generate timestamps spanning 10 minutes of "streaming" data
timestamps = pd.date_range(start="2025-01-19 10:00:00", periods=n_points, freq="3s")

# Simulate correlated sensor readings (temperature vs humidity)
# Start from a base and add cumulative drift + noise to simulate real sensor behavior
base_temp = 22.0  # Celsius
base_humidity = 55.0  # Percent

# Create correlated drift with noise
temp_drift = np.cumsum(np.random.randn(n_points) * 0.1)
humidity_drift = np.cumsum(np.random.randn(n_points) * 0.2)

x = base_temp + temp_drift + np.random.randn(n_points) * 0.3  # Temperature
y = base_humidity + humidity_drift + np.random.randn(n_points) * 0.5  # Humidity

# Calculate point age for opacity (0 = oldest, 1 = newest)
# This creates the streaming effect: older points fade out
age_fraction = np.linspace(0, 1, n_points)

# Map age to opacity (older = more transparent)
# Minimum alpha of 0.15 so oldest points are still barely visible
alpha_values = 0.15 + 0.85 * age_fraction

# Map age to color intensity (using blues - newer points are darker blue)
color_indices = (age_fraction * (len(Blues9) - 1)).astype(int)
colors = [Blues9[::-1][i] for i in color_indices]  # Reverse so newer = darker

# Point sizes: newer points slightly larger
sizes = 8 + 10 * age_fraction

# Create ColumnDataSource
source = ColumnDataSource(
    data={
        "x": x,
        "y": y,
        "timestamp": timestamps,
        "alpha": alpha_values,
        "color": colors,
        "size": sizes,
        "age": age_fraction,
    }
)

# Create figure (4800 x 2700 px)
p = figure(
    width=4800,
    height=2700,
    title="scatter-streaming · bokeh · pyplots.ai",
    x_axis_label="Temperature (°C)",
    y_axis_label="Relative Humidity (%)",
    tools="",
    toolbar_location=None,
)

# Plot scatter points with age-based opacity and color
p.scatter(
    x="x",
    y="y",
    source=source,
    size="size",
    fill_color="color",
    fill_alpha="alpha",
    line_color="color",
    line_alpha="alpha",
    line_width=1,
)

# Add markers for newest points to highlight data flow direction
# Mark the 5 most recent points with a distinct ring
newest_idx = n_points - 5
p.scatter(
    x=x[newest_idx:],
    y=y[newest_idx:],
    size=25,
    fill_color=None,
    line_color="#306998",
    line_width=3,
    legend_label="Newest Points",
)

# Styling for large canvas
p.title.text_font_size = "32pt"
p.title.text_color = "#306998"
p.xaxis.axis_label_text_font_size = "24pt"
p.yaxis.axis_label_text_font_size = "24pt"
p.xaxis.major_label_text_font_size = "18pt"
p.yaxis.major_label_text_font_size = "18pt"

# Grid styling
p.xgrid.grid_line_color = "#cccccc"
p.ygrid.grid_line_color = "#cccccc"
p.xgrid.grid_line_alpha = 0.5
p.ygrid.grid_line_alpha = 0.5
p.xgrid.grid_line_dash = "dashed"
p.ygrid.grid_line_dash = "dashed"

# Background
p.background_fill_color = "#fafafa"
p.border_fill_color = "white"

# Axis styling
p.xaxis.axis_line_color = "#666666"
p.yaxis.axis_line_color = "#666666"
p.xaxis.axis_line_width = 2
p.yaxis.axis_line_width = 2

# Legend styling
p.legend.location = "top_left"
p.legend.label_text_font_size = "18pt"
p.legend.background_fill_alpha = 0.8
p.legend.border_line_color = "#cccccc"

# Save as PNG
export_png(p, filename="plot.png")

# Also save as HTML for interactive version
output_file("plot.html")
save(p)
