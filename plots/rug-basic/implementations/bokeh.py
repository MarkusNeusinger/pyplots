"""
rug-basic: Basic Rug Plot
Library: bokeh
"""

import numpy as np
from bokeh.io import export_png, output_file, save
from bokeh.models import ColumnDataSource, Range1d
from bokeh.plotting import figure


# Data - bimodal distribution to show clustering
np.random.seed(42)
cluster1 = np.random.normal(25, 4, 60)
cluster2 = np.random.normal(55, 6, 40)
values = np.concatenate([cluster1, cluster2])

# Rug tick height (small relative to plot)
tick_height = 0.3

# Create ColumnDataSource
source = ColumnDataSource(data={"x": values, "y0": np.zeros(len(values)), "y1": np.full(len(values), tick_height)})

# Create figure (4800 x 2700 px)
p = figure(width=4800, height=2700, title="rug-basic · bokeh · pyplots.ai", x_axis_label="Value", y_axis_label="")

# Draw rug ticks as vertical segments
p.segment(x0="x", y0="y0", x1="x", y1="y1", source=source, line_color="#306998", line_width=3, line_alpha=0.6)

# Configure axis ranges
p.x_range = Range1d(values.min() - 5, values.max() + 5)
p.y_range = Range1d(-0.05, tick_height + 0.15)

# Hide y-axis (not meaningful for rug plot)
p.yaxis.visible = False

# Styling for 4800x2700 px
p.title.text_font_size = "28pt"
p.xaxis.axis_label_text_font_size = "22pt"
p.xaxis.major_label_text_font_size = "18pt"

# Grid styling
p.xgrid.grid_line_alpha = 0.3
p.xgrid.grid_line_dash = "dashed"
p.ygrid.visible = False

# Background
p.background_fill_color = "#fafafa"

# Save outputs
export_png(p, filename="plot.png")
output_file("plot.html")
save(p)
