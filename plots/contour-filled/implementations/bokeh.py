""" pyplots.ai
contour-filled: Filled Contour Plot
Library: bokeh 3.8.1 | Python 3.13.11
Quality: 78/100 | Created: 2025-12-30
"""

import numpy as np
from bokeh.io import export_png, output_file, save
from bokeh.models import BasicTicker, ColorBar, LinearColorMapper
from bokeh.palettes import Viridis256
from bokeh.plotting import figure


# Data - Gaussian peaks forming an interesting surface
np.random.seed(42)
x = np.linspace(-3, 3, 80)
y = np.linspace(-3, 3, 80)
X, Y = np.meshgrid(x, y)

# Create surface with multiple Gaussian peaks (like terrain elevation)
Z = (
    1.5 * np.exp(-((X - 1) ** 2 + (Y - 1) ** 2))
    + 2.0 * np.exp(-((X + 1.5) ** 2 + (Y + 0.5) ** 2) / 1.5)
    + 1.0 * np.exp(-((X - 0.5) ** 2 + (Y + 1.5) ** 2) / 0.8)
    - 0.5 * np.exp(-((X + 0.5) ** 2 + (Y - 1.5) ** 2) / 0.5)
)

# Create figure at 4800x2700 px
p = figure(
    width=4800,
    height=2700,
    title="contour-filled · bokeh · pyplots.ai",
    x_axis_label="X Coordinate",
    y_axis_label="Y Coordinate",
    x_range=(x.min(), x.max()),
    y_range=(y.min(), y.max()),
    tools="",
)

# Color mapper for the surface
color_mapper = LinearColorMapper(palette=Viridis256, low=Z.min(), high=Z.max())

# Plot the filled surface using image
p.image(image=[Z], x=x.min(), y=y.min(), dw=x.max() - x.min(), dh=y.max() - y.min(), color_mapper=color_mapper)

# Add colorbar
color_bar = ColorBar(
    color_mapper=color_mapper,
    ticker=BasicTicker(desired_num_ticks=10),
    label_standoff=20,
    title="Surface Value",
    title_text_font_size="20pt",
    major_label_text_font_size="16pt",
    width=40,
    padding=30,
)
p.add_layout(color_bar, "right")

# Style text for large canvas
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

# Background
p.background_fill_color = None
p.border_fill_color = None

# Save as PNG and HTML
export_png(p, filename="plot.png")

# Also save as HTML for interactive viewing
output_file("plot.html")
save(p)
