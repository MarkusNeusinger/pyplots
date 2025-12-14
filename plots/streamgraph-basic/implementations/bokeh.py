"""
streamgraph-basic: Basic Stream Graph
Library: bokeh
"""

import numpy as np
import pandas as pd
from bokeh.io import export_png, output_file, save
from bokeh.models import ColumnDataSource, Legend
from bokeh.plotting import figure


# Data: monthly streaming hours by music genre over two years
np.random.seed(42)

months = pd.date_range(start="2022-01-01", periods=24, freq="ME")
categories = ["Pop", "Rock", "Hip-Hop", "Electronic", "Jazz", "Classical"]

# Generate smooth streaming data for each genre
n_points = len(months)
base = np.linspace(0, 4 * np.pi, n_points)

data = {
    "Pop": 40 + 15 * np.sin(base) + np.random.randn(n_points) * 3,
    "Rock": 35 + 10 * np.sin(base + 1) + np.random.randn(n_points) * 2,
    "Hip-Hop": 30 + 20 * np.sin(base + 2) + np.random.randn(n_points) * 4,
    "Electronic": 25 + 12 * np.sin(base + 3) + np.random.randn(n_points) * 2,
    "Jazz": 15 + 8 * np.sin(base + 4) + np.random.randn(n_points) * 1.5,
    "Classical": 12 + 5 * np.sin(base + 5) + np.random.randn(n_points) * 1,
}

# Ensure all values are positive
for cat in categories:
    data[cat] = np.abs(data[cat])

# Convert to DataFrame
df = pd.DataFrame(data)
df["month"] = months

# Calculate stacked values with symmetric baseline (centered around 0)
values = df[categories].values
cumulative = np.cumsum(values, axis=1)
total = cumulative[:, -1]

# Center the baseline: offset so the middle is at 0
baseline_offset = total / 2
y_bottom = np.zeros_like(values)
y_top = np.zeros_like(values)

for i in range(len(categories)):
    if i == 0:
        y_bottom[:, i] = -baseline_offset
        y_top[:, i] = y_bottom[:, i] + values[:, i]
    else:
        y_bottom[:, i] = y_top[:, i - 1]
        y_top[:, i] = y_bottom[:, i] + values[:, i]

# Colors - Python Blue first, then harmonious colorblind-safe palette
colors = ["#306998", "#FFD43B", "#E07A5F", "#81B29A", "#F2CC8F", "#3D405B"]

# Create figure
p = figure(
    width=4800,
    height=2700,
    title="streamgraph-basic \u00b7 bokeh \u00b7 pyplots.ai",
    x_axis_label="Time",
    y_axis_label="Streaming Hours",
    x_axis_type="datetime",
)

# Style title and axes for large canvas
p.title.text_font_size = "32pt"
p.xaxis.axis_label_text_font_size = "24pt"
p.yaxis.axis_label_text_font_size = "24pt"
p.xaxis.major_label_text_font_size = "18pt"
p.yaxis.major_label_text_font_size = "18pt"

# Create patches for each category (streamgraph layers)
legend_items = []
x_values = df["month"].values

for i, cat in enumerate(categories):
    # Create polygon coordinates for smooth stacked area
    # Go forward along top, then backward along bottom
    xs = np.concatenate([x_values, x_values[::-1]])
    ys = np.concatenate([y_top[:, i], y_bottom[:, i][::-1]])

    source = ColumnDataSource(data={"x": xs, "y": ys})

    renderer = p.patch(
        x="x", y="y", source=source, fill_color=colors[i], fill_alpha=0.85, line_color=colors[i], line_width=2
    )
    legend_items.append((cat, [renderer]))

# Add legend outside the plot
legend = Legend(items=legend_items, location="center")
legend.label_text_font_size = "18pt"
legend.glyph_height = 30
legend.glyph_width = 30
legend.spacing = 10
p.add_layout(legend, "right")

# Grid styling
p.grid.grid_line_alpha = 0.3
p.grid.grid_line_dash = [6, 4]

# Remove y-axis labels (streamgraph values are relative)
p.yaxis.visible = True
p.outline_line_color = None

# Save as PNG
export_png(p, filename="plot.png")

# Also save interactive HTML
output_file("plot.html")
save(p)
