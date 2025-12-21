""" pyplots.ai
line-basic: Basic Line Plot
Library: bokeh 3.8.1 | Python 3.13.11
Quality: 88/100 | Created: 2025-12-13
"""

import numpy as np
from bokeh.io import export_png, output_file, save
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure


# Data - Monthly sales figures for a year
np.random.seed(42)
months = np.arange(1, 13)
base_sales = 50 + np.linspace(0, 30, 12)  # Upward trend
noise = np.random.randn(12) * 5
sales = base_sales + noise

# Create ColumnDataSource
source = ColumnDataSource(data={"x": months, "y": sales})

# Create figure (4800 × 2700 px)
p = figure(
    width=4800,
    height=2700,
    title="line-basic · bokeh · pyplots.ai",
    x_axis_label="Month",
    y_axis_label="Sales (thousands)",
)

# Plot line with markers
p.line(x="x", y="y", source=source, line_width=4, line_color="#306998", legend_label="Sales")
p.scatter(x="x", y="y", source=source, size=18, fill_color="#306998", line_color="white", line_width=2)

# Style text sizes for 4800x2700 px
p.title.text_font_size = "48pt"
p.xaxis.axis_label_text_font_size = "36pt"
p.yaxis.axis_label_text_font_size = "36pt"
p.xaxis.major_label_text_font_size = "28pt"
p.yaxis.major_label_text_font_size = "28pt"

# Grid styling
p.grid.grid_line_alpha = 0.3
p.grid.grid_line_dash = "dashed"

# Legend styling
p.legend.label_text_font_size = "28pt"
p.legend.location = "top_left"
p.legend.background_fill_alpha = 0.7

# Save as PNG and HTML
export_png(p, filename="plot.png")

output_file("plot.html")
save(p)
