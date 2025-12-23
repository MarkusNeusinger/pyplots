"""pyplots.ai
histogram-basic: Basic Histogram
Library: bokeh | Python 3.13
Quality: pending | Created: 2025-12-23
"""

import numpy as np
from bokeh.io import export_png, save
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure


# Data - Heights in cm (realistic distribution)
np.random.seed(42)
values = np.random.normal(loc=170, scale=10, size=500)

# Calculate histogram bins
counts, edges = np.histogram(values, bins=25)
left_edges = edges[:-1]
right_edges = edges[1:]

source = ColumnDataSource(data={"left": left_edges, "right": right_edges, "top": counts, "bottom": [0] * len(counts)})

# Create figure (4800 x 2700 px)
p = figure(
    width=4800,
    height=2700,
    title="histogram-basic · bokeh · pyplots.ai",
    x_axis_label="Height (cm)",
    y_axis_label="Frequency",
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
    fill_alpha=0.8,
)

# Styling for 4800x2700 px
p.title.text_font_size = "28pt"
p.xaxis.axis_label_text_font_size = "22pt"
p.yaxis.axis_label_text_font_size = "22pt"
p.xaxis.major_label_text_font_size = "18pt"
p.yaxis.major_label_text_font_size = "18pt"

# Grid styling
p.xgrid.grid_line_alpha = 0.3
p.ygrid.grid_line_alpha = 0.3
p.xgrid.grid_line_dash = "dashed"
p.ygrid.grid_line_dash = "dashed"

# Y-axis starts at zero
p.y_range.start = 0

# Save outputs
export_png(p, filename="plot.png")
save(p, filename="plot.html")
