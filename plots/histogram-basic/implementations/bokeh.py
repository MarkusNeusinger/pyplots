"""pyplots.ai
histogram-basic: Basic Histogram
Library: bokeh 3.8.2 | Python 3.14.0
Quality: /100 | Updated: 2026-02-13
"""

import numpy as np
from bokeh.io import export_png, output_file, save
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure


# Data - Marathon finish times in minutes (right-skewed distribution)
np.random.seed(42)
values = np.concatenate([np.random.normal(loc=240, scale=30, size=400), np.random.normal(loc=300, scale=20, size=100)])
values = values[values > 120]

# Calculate histogram bins
counts, edges = np.histogram(values, bins=25)
left_edges = edges[:-1]
right_edges = edges[1:]

source = ColumnDataSource(
    data={
        "left": left_edges,
        "right": right_edges,
        "top": counts,
        "bottom": [0] * len(counts),
        "count": counts,
        "bin_start": [f"{e:.0f}" for e in left_edges],
        "bin_end": [f"{e:.0f}" for e in right_edges],
    }
)

# Create figure (4800 x 2700 px)
p = figure(
    width=4800,
    height=2700,
    title="histogram-basic \u00b7 bokeh \u00b7 pyplots.ai",
    x_axis_label="Finish Time (min)",
    y_axis_label="Frequency",
    toolbar_location=None,
)

# Plot histogram as quad glyphs (bars without gaps)
p.quad(
    left="left",
    right="right",
    top="top",
    bottom="bottom",
    source=source,
    fill_color="#306998",
    line_color="white",
    line_width=2,
    fill_alpha=0.85,
    hover_fill_color="#4A8BBE",
    hover_fill_alpha=1.0,
)

# HoverTool - Bokeh's distinctive interactive feature
hover = HoverTool(tooltips=[("Range", "@bin_start\u2013@bin_end min"), ("Count", "@count")], mode="mouse")
p.add_tools(hover)

# Text sizing for 4800x2700 canvas
p.title.text_font_size = "40pt"
p.xaxis.axis_label_text_font_size = "30pt"
p.yaxis.axis_label_text_font_size = "30pt"
p.xaxis.major_label_text_font_size = "24pt"
p.yaxis.major_label_text_font_size = "24pt"

# Grid styling - y-axis only, subtle
p.xgrid.visible = False
p.ygrid.grid_line_alpha = 0.2

# Clean frame
p.outline_line_color = None
p.background_fill_color = "white"
p.border_fill_color = "white"
p.xaxis.axis_line_width = 2
p.yaxis.axis_line_width = 2

# Y-axis starts at zero
p.y_range.start = 0

# Margin padding for balanced layout
p.min_border_left = 120
p.min_border_bottom = 100

# Save outputs
export_png(p, filename="plot.png")
output_file("plot.html")
save(p)
