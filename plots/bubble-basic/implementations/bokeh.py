"""
bubble-basic: Basic Bubble Chart
Library: bokeh
"""

import numpy as np
from bokeh.io import export_png
from bokeh.models import ColumnDataSource, Label
from bokeh.plotting import figure, output_file, save


# Data
np.random.seed(42)
n_points = 50
x = np.random.randn(n_points) * 2 + 10
y = x * 0.6 + np.random.randn(n_points) * 1.5 + 5
size_raw = np.abs(np.random.randn(n_points) * 30 + 50)

# Scale sizes for bubble area perception
# Map to visible range for 4800x2700 canvas
size_min, size_max = 30, 120
size_scaled = size_min + (size_max - size_min) * (size_raw - size_raw.min()) / (size_raw.max() - size_raw.min())

source = ColumnDataSource(data={"x": x, "y": y, "size": size_scaled})

# Plot
p = figure(
    width=4800, height=2700, title="bubble-basic · bokeh · pyplots.ai", x_axis_label="X Value", y_axis_label="Y Value"
)

# Create bubble scatter
p.scatter(
    x="x",
    y="y",
    size="size",
    source=source,
    fill_color="#306998",
    fill_alpha=0.6,
    line_color="#306998",
    line_alpha=0.8,
    line_width=2,
)

# Styling (scaled for 4800x2700 px canvas)
p.title.text_font_size = "36pt"
p.xaxis.axis_label_text_font_size = "24pt"
p.yaxis.axis_label_text_font_size = "24pt"
p.xaxis.major_label_text_font_size = "18pt"
p.yaxis.major_label_text_font_size = "18pt"

# Grid styling
p.grid.grid_line_alpha = 0.3
p.grid.grid_line_dash = "dashed"

# Add size legend (reference bubbles) in upper right area
legend_x = [max(x) + 1.5] * 3
legend_y_positions = [max(y) - 0.5, max(y) - 2.5, max(y) - 5]
legend_sizes = [size_min, (size_min + size_max) / 2, size_max]
legend_labels = ["Small", "Medium", "Large"]

legend_source = ColumnDataSource(data={"x": legend_x, "y": legend_y_positions, "size": legend_sizes})

p.scatter(
    x="x",
    y="y",
    size="size",
    source=legend_source,
    fill_color="#306998",
    fill_alpha=0.6,
    line_color="#306998",
    line_alpha=0.8,
    line_width=2,
)

# Add text labels for size legend
for lx, ly, label in zip(legend_x, legend_y_positions, legend_labels, strict=True):
    text_label = Label(x=lx + 1.2, y=ly, text=label, text_font_size="18pt", text_baseline="middle")
    p.add_layout(text_label)

# Add "Size" title for legend
size_title = Label(x=legend_x[0] - 0.3, y=max(y) + 1, text="Size", text_font_size="20pt", text_font_style="bold")
p.add_layout(size_title)

# Adjust x_range to accommodate legend
p.x_range.end = max(x) + 4

# Save as PNG
export_png(p, filename="plot.png")

# Save as HTML (interactive)
output_file("plot.html")
save(p)
