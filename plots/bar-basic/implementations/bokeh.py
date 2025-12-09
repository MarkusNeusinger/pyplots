"""
bar-basic: Basic Bar Chart
Library: bokeh
"""

import pandas as pd
from bokeh.io import export_png
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure


# Data
data = pd.DataFrame(
    {"category": ["Product A", "Product B", "Product C", "Product D", "Product E"], "value": [45, 78, 52, 91, 63]}
)

# Create ColumnDataSource
source = ColumnDataSource(data)

# Create figure with categorical x-axis
p = figure(
    width=4800,
    height=2700,
    x_range=data["category"].tolist(),
    title="Basic Bar Chart",
    x_axis_label="Category",
    y_axis_label="Value",
)

# Plot vertical bars
p.vbar(x="category", top="value", source=source, width=0.7, color="#306998", alpha=0.8)

# Styling
p.title.text_font_size = "20pt"
p.xaxis.axis_label_text_font_size = "20pt"
p.yaxis.axis_label_text_font_size = "20pt"
p.xaxis.major_label_text_font_size = "16pt"
p.yaxis.major_label_text_font_size = "16pt"
p.xgrid.grid_line_color = None
p.ygrid.grid_line_alpha = 0.3
p.y_range.start = 0

# Save
export_png(p, filename="plot.png")
