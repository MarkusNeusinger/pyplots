"""pyplots.ai
area-basic: Basic Area Chart
Library: bokeh | Python 3.13
Quality: pending | Created: 2025-12-23
"""

import numpy as np
import pandas as pd
from bokeh.io import export_png, output_file, save
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure


# Data - daily website visitors over a month
np.random.seed(42)
dates = pd.date_range(start="2024-01-01", periods=31, freq="D")
base_visitors = 5000
trend = np.linspace(0, 1500, 31)
weekly_pattern = 800 * np.sin(np.arange(31) * 2 * np.pi / 7)
noise = np.random.randn(31) * 400
visitors = base_visitors + trend + weekly_pattern + noise
visitors = np.maximum(visitors, 1000)  # Ensure positive values

source = ColumnDataSource(data={"date": dates, "visitors": visitors})

# Create figure (4800 x 2700 px)
p = figure(
    width=4800,
    height=2700,
    title="area-basic · bokeh · pyplots.ai",
    x_axis_label="Date",
    y_axis_label="Daily Visitors",
    x_axis_type="datetime",
)

# Area chart - fill from bottom to line
p.varea(x="date", y1=0, y2="visitors", source=source, fill_color="#306998", fill_alpha=0.4)

# Line on top for clear edge
p.line(x="date", y="visitors", source=source, line_color="#306998", line_width=5)

# Styling for 4800x2700 px - scaled up for large canvas
p.title.text_font_size = "48pt"
p.xaxis.axis_label_text_font_size = "36pt"
p.yaxis.axis_label_text_font_size = "36pt"
p.xaxis.major_label_text_font_size = "28pt"
p.yaxis.major_label_text_font_size = "28pt"

# Grid styling
p.xgrid.grid_line_alpha = 0.3
p.ygrid.grid_line_alpha = 0.3
p.xgrid.grid_line_dash = [6, 4]
p.ygrid.grid_line_dash = [6, 4]

# Axis line styling
p.xaxis.axis_line_width = 2
p.yaxis.axis_line_width = 2
p.xaxis.major_tick_line_width = 2
p.yaxis.major_tick_line_width = 2

# Remove toolbar for clean export
p.toolbar_location = None

# Ensure y-axis starts at 0
p.y_range.start = 0

# Add padding to margins
p.min_border_left = 120
p.min_border_bottom = 100

# Save as PNG
export_png(p, filename="plot.png")

# Save as HTML for interactive viewing
output_file("plot.html")
save(p)
