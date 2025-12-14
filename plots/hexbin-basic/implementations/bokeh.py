"""
hexbin-basic: Basic Hexbin Plot
Library: bokeh
"""

from collections import Counter

import numpy as np
from bokeh.io import export_png, save
from bokeh.models import ColorBar, ColumnDataSource, LinearColorMapper
from bokeh.palettes import Viridis256
from bokeh.plotting import figure


# Data - clustered bivariate distribution
np.random.seed(42)

# Create clustered data with 3 centers
centers = [(-2, -2), (2, 2), (0, 3)]
cluster_sizes = [4000, 4000, 2000]

x_data = []
y_data = []
for (cx, cy), size in zip(centers, cluster_sizes, strict=True):
    x_data.extend(np.random.randn(size) * 1.2 + cx)
    y_data.extend(np.random.randn(size) * 1.2 + cy)

x = np.array(x_data)
y = np.array(y_data)

# Hexbin computation
gridsize = 25
x_min, x_max = x.min(), x.max()
y_min, y_max = y.min(), y.max()

# Add padding
x_padding = (x_max - x_min) * 0.05
y_padding = (y_max - y_min) * 0.05
x_min -= x_padding
x_max += x_padding
y_min -= y_padding
y_max += y_padding

# Hexagon dimensions
hex_width = (x_max - x_min) / gridsize
hex_height = hex_width * 2 / np.sqrt(3)

# Calculate bin indices for each point (offset rows for hexagonal packing)
y_idx = np.floor((y - y_min) / (hex_height * 0.75)).astype(int)
x_offset = np.where(y_idx % 2 == 1, 0.5, 0)
x_idx_adj = np.floor((x - x_min) / hex_width - x_offset).astype(int)

# Count points in each hexagon
counts = Counter(zip(x_idx_adj, y_idx, strict=True))

# Calculate hexagon centers and counts
hex_x = []
hex_y = []
hex_counts = []

for (xi, yi), count in counts.items():
    offset = 0.5 if yi % 2 == 1 else 0
    center_x = x_min + (xi + 0.5 + offset) * hex_width
    center_y = y_min + yi * hex_height * 0.75 + hex_height / 2
    hex_x.append(center_x)
    hex_y.append(center_y)
    hex_counts.append(count)

hex_x = np.array(hex_x)
hex_y = np.array(hex_y)
hex_counts = np.array(hex_counts)

# Generate hexagon vertices for patches
hex_size = hex_width * 0.58  # Slightly smaller than full to show gaps
angles = np.linspace(0, 2 * np.pi, 7)[:-1] + np.pi / 6  # Flat-topped hexagon angles

xs = []
ys = []
for cx, cy in zip(hex_x, hex_y, strict=True):
    vx = (cx + hex_size * np.cos(angles)).tolist()
    vy = (cy + hex_size * np.sin(angles)).tolist()
    xs.append(vx)
    ys.append(vy)

# Create color mapper
mapper = LinearColorMapper(palette=Viridis256, low=hex_counts.min(), high=hex_counts.max())

source = ColumnDataSource(data={"xs": xs, "ys": ys, "counts": hex_counts})

# Plot
p = figure(
    width=4800,
    height=2700,
    title="hexbin-basic · bokeh · pyplots.ai",
    x_axis_label="X Value",
    y_axis_label="Y Value",
    tools="",
    toolbar_location=None,
)

p.patches(
    xs="xs",
    ys="ys",
    source=source,
    fill_color={"field": "counts", "transform": mapper},
    line_color="white",
    line_width=0.5,
    alpha=0.9,
)

# Color bar
color_bar = ColorBar(
    color_mapper=mapper,
    width=30,
    location=(0, 0),
    title="Count",
    title_text_font_size="20pt",
    major_label_text_font_size="16pt",
)
p.add_layout(color_bar, "right")

# Styling for 4800x2700
p.title.text_font_size = "28pt"
p.xaxis.axis_label_text_font_size = "22pt"
p.yaxis.axis_label_text_font_size = "22pt"
p.xaxis.major_label_text_font_size = "18pt"
p.yaxis.major_label_text_font_size = "18pt"

p.xaxis.axis_line_width = 2
p.yaxis.axis_line_width = 2
p.xaxis.major_tick_line_width = 2
p.yaxis.major_tick_line_width = 2

p.xgrid.grid_line_alpha = 0.3
p.ygrid.grid_line_alpha = 0.3
p.xgrid.grid_line_dash = "dashed"
p.ygrid.grid_line_dash = "dashed"

# Save
export_png(p, filename="plot.png")
save(p, filename="plot.html")
