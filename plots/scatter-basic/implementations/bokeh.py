"""
scatter-basic: Basic Scatter Plot
Library: bokeh
"""

import numpy as np
from bokeh.io import export_png
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure


# Data
np.random.seed(42)
x = np.random.randn(100) * 2 + 10
y = x * 0.8 + np.random.randn(100) * 2

source = ColumnDataSource(data={"x": x, "y": y})

# Create figure (4800 × 2700 px for 16:9 aspect ratio)
p = figure(width=4800, height=2700, title="Basic Scatter Plot", x_axis_label="X Value", y_axis_label="Y Value")

# Plot scatter
p.scatter(x="x", y="y", source=source, size=12, color="#306998", alpha=0.7)

# Styling
p.title.text_font_size = "20pt"
p.xaxis.axis_label_text_font_size = "20pt"
p.yaxis.axis_label_text_font_size = "20pt"
p.xaxis.major_label_text_font_size = "16pt"
p.yaxis.major_label_text_font_size = "16pt"
p.grid.grid_line_alpha = 0.3

# Save
export_png(p, filename="plot.png")
