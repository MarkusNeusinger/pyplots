""" pyplots.ai
bar-sorted: Sorted Bar Chart
Library: bokeh 3.8.1 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-30
"""

import numpy as np
from bokeh.io import export_png
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure


# Data - Sales performance by product (descending order)
np.random.seed(42)
products = [
    "Product A",
    "Product B",
    "Product C",
    "Product D",
    "Product E",
    "Product F",
    "Product G",
    "Product H",
    "Product I",
    "Product J",
]
values = [450, 385, 340, 310, 275, 230, 195, 160, 120, 85]

# Sort by value (descending) - already sorted, but explicit for clarity
sorted_indices = np.argsort(values)[::-1]
sorted_products = [products[i] for i in sorted_indices]
sorted_values = [values[i] for i in sorted_indices]

# Create data source
source = ColumnDataSource(data={"products": sorted_products, "values": sorted_values})

# Create figure with categorical x-axis (in sorted order)
p = figure(
    x_range=sorted_products,
    width=4800,
    height=2700,
    title="bar-sorted · bokeh · pyplots.ai",
    x_axis_label="Product",
    y_axis_label="Sales (Units)",
    toolbar_location=None,
)

# Plot bars - using Python Blue as primary color
p.vbar(
    x="products",
    top="values",
    source=source,
    width=0.7,
    fill_color="#306998",
    line_color="#1e4a6e",
    line_width=2,
    fill_alpha=0.9,
)

# Text styling for large canvas
p.title.text_font_size = "28pt"
p.xaxis.axis_label_text_font_size = "22pt"
p.yaxis.axis_label_text_font_size = "22pt"
p.xaxis.major_label_text_font_size = "18pt"
p.yaxis.major_label_text_font_size = "18pt"
p.xaxis.major_label_orientation = 0.7  # Slight rotation for readability

# Grid styling
p.xgrid.grid_line_color = None
p.ygrid.grid_line_alpha = 0.3
p.ygrid.grid_line_dash = "dashed"

# Axis styling
p.y_range.start = 0
p.outline_line_color = None

# Save
export_png(p, filename="plot.png")
