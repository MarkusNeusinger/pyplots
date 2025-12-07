"""
histogram-basic: Basic Histogram
Library: bokeh
"""

import numpy as np
from bokeh.io import export_png
from bokeh.plotting import figure


# Data - 500 normally distributed values (mean=100, std=15)
np.random.seed(42)
values = np.random.normal(100, 15, 500)

# Compute histogram bins
hist, edges = np.histogram(values, bins=30)

# Create figure (4800 x 2700 px for high resolution)
p = figure(width=4800, height=2700, title="Basic Histogram", x_axis_label="Value", y_axis_label="Frequency")

# Draw histogram using quad glyph
p.quad(
    top=hist,
    bottom=0,
    left=edges[:-1],
    right=edges[1:],
    fill_color="#306998",
    fill_alpha=0.7,
    line_color="white",
    line_width=1,
)

# Style title
p.title.text_font_size = "20pt"
p.title.align = "center"

# Style axis labels
p.xaxis.axis_label_text_font_size = "20pt"
p.yaxis.axis_label_text_font_size = "20pt"
p.xaxis.major_label_text_font_size = "16pt"
p.yaxis.major_label_text_font_size = "16pt"

# Style grid - subtle
p.xgrid.grid_line_alpha = 0.3
p.ygrid.grid_line_alpha = 0.3

# Ensure y-axis starts at zero
p.y_range.start = 0

# Save as PNG
export_png(p, filename="plot.png")
