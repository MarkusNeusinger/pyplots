"""pyplots.ai
heatmap-basic: Basic Heatmap
Library: bokeh | Python 3.13
Quality: pending | Created: 2025-12-23
"""

import numpy as np
from bokeh.io import export_png, save
from bokeh.models import BasicTicker, ColorBar, ColumnDataSource, LabelSet, LinearColorMapper
from bokeh.palettes import Viridis256
from bokeh.plotting import figure
from bokeh.resources import CDN


# Data - Monthly sales performance by product category
np.random.seed(42)
x_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug"]
y_labels = ["Product A", "Product B", "Product C", "Product D", "Product E", "Product F"]

# Generate heatmap values (sales performance 0-100)
values = np.random.rand(len(y_labels), len(x_labels)) * 100

# Flatten data for ColumnDataSource
x_data = []
y_data = []
value_data = []
text_data = []
text_color_data = []

for i, y in enumerate(y_labels):
    for j, x in enumerate(x_labels):
        x_data.append(x)
        y_data.append(y)
        val = values[i, j]
        value_data.append(val)
        text_data.append(f"{val:.0f}")
        # Use white text on dark cells, black on light cells
        text_color_data.append("white" if val > 50 else "black")

source = ColumnDataSource(
    data={"x": x_data, "y": y_data, "value": value_data, "text": text_data, "text_color": text_color_data}
)

# Color mapper
color_mapper = LinearColorMapper(palette=Viridis256, low=0, high=100)

# Create figure with categorical axes
p = figure(
    width=4800,
    height=2700,
    x_range=x_labels,
    y_range=y_labels,
    title="heatmap-basic · bokeh · pyplots.ai",
    x_axis_label="Month",
    y_axis_label="Product",
    toolbar_location=None,
    tools="",
)

# Plot heatmap rectangles
p.rect(
    x="x",
    y="y",
    width=1,
    height=1,
    source=source,
    fill_color={"field": "value", "transform": color_mapper},
    line_color=None,
)

# Add value annotations in cells
labels = LabelSet(
    x="x",
    y="y",
    text="text",
    text_color="text_color",
    source=source,
    text_align="center",
    text_baseline="middle",
    text_font_size="24pt",
)
p.add_layout(labels)

# Add color bar
color_bar = ColorBar(
    color_mapper=color_mapper,
    ticker=BasicTicker(desired_num_ticks=10),
    label_standoff=16,
    major_label_text_font_size="18pt",
    border_line_color=None,
    location=(0, 0),
    width=40,
    title="Sales Score",
    title_text_font_size="20pt",
)
p.add_layout(color_bar, "right")

# Styling for 4800x2700 px
p.title.text_font_size = "28pt"
p.xaxis.axis_label_text_font_size = "22pt"
p.yaxis.axis_label_text_font_size = "22pt"
p.xaxis.major_label_text_font_size = "18pt"
p.yaxis.major_label_text_font_size = "18pt"

# Grid styling - disabled for heatmap
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None

# Axis styling
p.axis.axis_line_color = "#cccccc"
p.axis.major_tick_line_color = "#cccccc"

# Background
p.background_fill_color = "#f8f8f8"
p.border_fill_color = "white"
p.outline_line_color = None

# Save PNG
export_png(p, filename="plot.png")

# Save HTML for interactive version
save(p, filename="plot.html", resources=CDN, title="heatmap-basic · bokeh · pyplots.ai")
