"""
area-basic: Basic Area Chart
Library: bokeh
"""

import pandas as pd
from bokeh.io import export_png
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure


# Data
data = pd.DataFrame(
    {
        "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        "sales": [120, 135, 148, 162, 175, 195, 210, 198, 185, 170, 158, 190],
    }
)

# Create x positions for categorical months
x = list(range(len(data["month"])))
y = data["sales"].tolist()

source = ColumnDataSource(data={"x": x, "y": y, "month": data["month"]})

# Create figure
p = figure(
    width=4800,
    height=2700,
    title="Monthly Sales Volume",
    x_axis_label="Month",
    y_axis_label="Sales ($)",
    x_range=(-0.5, len(x) - 0.5),
)

# Plot area (varea fills from y1 to y2)
p.varea(x="x", y1=0, y2="y", source=source, fill_alpha=0.7, fill_color="#306998")

# Add line on top for clearer boundary
p.line(x="x", y="y", source=source, line_width=2, line_color="#306998")

# Configure x-axis ticks to show month labels
p.xaxis.ticker = x
p.xaxis.major_label_overrides = dict(enumerate(data["month"]))

# Styling
p.title.text_font_size = "20pt"
p.xaxis.axis_label_text_font_size = "20pt"
p.yaxis.axis_label_text_font_size = "20pt"
p.xaxis.major_label_text_font_size = "16pt"
p.yaxis.major_label_text_font_size = "16pt"
p.grid.grid_line_alpha = 0.3

# Save
export_png(p, filename="plot.png")
