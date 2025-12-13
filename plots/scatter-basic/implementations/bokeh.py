"""
scatter-basic: Basic Scatter Plot
Library: bokeh
"""

import numpy as np
from bokeh.io import export_png
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, output_file, save


# Data
np.random.seed(42)
x = np.random.randn(100) * 2 + 10
y = x * 0.8 + np.random.randn(100) * 2

# Create ColumnDataSource
source = ColumnDataSource(data={"x": x, "y": y})

# Create figure (4800 x 2700 px for 16:9 aspect ratio)
p = figure(
    width=4800, height=2700, title="scatter-basic · bokeh · pyplots.ai", x_axis_label="X Value", y_axis_label="Y Value"
)

# Plot scatter points
p.scatter(x="x", y="y", source=source, size=15, color="#306998", alpha=0.7)

# Styling (scaled for 4800x2700 px canvas)
p.title.text_font_size = "28pt"
p.xaxis.axis_label_text_font_size = "22pt"
p.yaxis.axis_label_text_font_size = "22pt"
p.xaxis.major_label_text_font_size = "18pt"
p.yaxis.major_label_text_font_size = "18pt"
p.grid.grid_line_alpha = 0.3
p.grid.grid_line_dash = "dashed"

# Save as PNG
export_png(p, filename="plot.png")

# Save as HTML (interactive)
output_file("plot.html")
save(p)
