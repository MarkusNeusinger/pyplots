"""pyplots.ai
heatmap-interactive: Interactive Heatmap with Hover and Zoom
Library: bokeh | Python 3.13
Quality: pending | Created: 2026-01-08
"""

import numpy as np
from bokeh.io import export_png
from bokeh.models import ColorBar, ColumnDataSource, HoverTool, LinearColorMapper, WheelZoomTool
from bokeh.palettes import Viridis256
from bokeh.plotting import figure, output_file, save
from bokeh.transform import transform


# Data - Generate a realistic matrix (e.g., product performance by region)
np.random.seed(42)

# Create row and column labels
n_rows, n_cols = 20, 15
regions = [f"Region {i + 1}" for i in range(n_rows)]
products = [f"Product {chr(65 + i)}" for i in range(n_cols)]

# Generate performance values (0-100 scale)
base = np.random.rand(n_rows, n_cols) * 60 + 20  # Base values 20-80
# Add some patterns - some regions perform better
for i in range(5):
    base[i, :] += 15
# Some products perform better across all regions
for j in [2, 5, 10]:
    base[:, j] += 10
# Clip to valid range
values = np.clip(base, 0, 100)

# Create flattened data for ColumnDataSource
x_flat = []
y_flat = []
value_flat = []
for i, region in enumerate(regions):
    for j, product in enumerate(products):
        x_flat.append(product)
        y_flat.append(region)
        value_flat.append(values[i, j])

source = ColumnDataSource(data={"x": x_flat, "y": y_flat, "value": value_flat})

# Color mapper
color_mapper = LinearColorMapper(palette=Viridis256, low=0, high=100)

# Create figure with categorical axes
p = figure(
    width=4800,
    height=2700,
    title="heatmap-interactive · bokeh · pyplots.ai",
    x_range=products,
    y_range=list(reversed(regions)),  # Reverse for top-to-bottom display
    x_axis_label="Product",
    y_axis_label="Region",
    tools="pan,wheel_zoom,box_zoom,reset",
    toolbar_location="right",
)

# Draw heatmap cells using rect
p.rect(
    x="x", y="y", width=0.95, height=0.95, source=source, fill_color=transform("value", color_mapper), line_color=None
)

# Add hover tool with crosshair effect
hover = HoverTool(tooltips=[("Region", "@y"), ("Product", "@x"), ("Performance", "@value{0.1}")], mode="mouse")
p.add_tools(hover)

# Color bar - scaled for large canvas
color_bar = ColorBar(
    color_mapper=color_mapper,
    location=(0, 0),
    title="Performance Score",
    title_text_font_size="28pt",
    major_label_text_font_size="22pt",
    bar_line_color=None,
    width=50,
    padding=20,
)
p.add_layout(color_bar, "right")

# Styling for large canvas - scale up for 4800x2700
p.title.text_font_size = "48pt"
p.xaxis.axis_label_text_font_size = "36pt"
p.yaxis.axis_label_text_font_size = "36pt"
p.xaxis.major_label_text_font_size = "24pt"
p.yaxis.major_label_text_font_size = "24pt"
p.xaxis.major_label_orientation = 0.7  # Slight angle for readability

# Grid and axis styling
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None
p.axis.axis_line_color = "#666666"
p.axis.major_tick_line_color = "#666666"

# Background
p.background_fill_color = "#f8f8f8"
p.border_fill_color = "white"

# Configure zoom tool to be active by default
p.toolbar.active_scroll = p.select_one(WheelZoomTool)

# Save as PNG
export_png(p, filename="plot.png")

# Save as HTML for interactive version
output_file("plot.html", title="Interactive Heatmap")
save(p)
