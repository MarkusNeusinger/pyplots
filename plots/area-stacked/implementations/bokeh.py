"""
area-stacked: Stacked Area Chart
Library: bokeh
"""

import numpy as np
import pandas as pd
from bokeh.io import export_png, output_file, save
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure


# Data - monthly revenue by product line over 2 years
np.random.seed(42)
months = pd.date_range(start="2022-01-01", periods=24, freq="MS")

# Generate realistic revenue data with trends
base = np.linspace(10, 15, 24) + np.random.randn(24) * 0.5
product_a = base * 3 + np.random.randn(24) * 2  # Largest, at bottom
product_b = base * 2 + np.random.randn(24) * 1.5
product_c = base * 1.5 + np.random.randn(24) * 1
product_d = base * 1 + np.random.randn(24) * 0.8  # Smallest, at top

# Ensure no negative values
product_a = np.maximum(product_a, 5)
product_b = np.maximum(product_b, 3)
product_c = np.maximum(product_c, 2)
product_d = np.maximum(product_d, 1)

# Create stacked values (cumulative)
stack_a = product_a
stack_b = stack_a + product_b
stack_c = stack_b + product_c
stack_d = stack_c + product_d

# Color palette from style guide
colors = ["#306998", "#FFD43B", "#DC2626", "#059669"]

# Create figure
p = figure(
    width=4800,
    height=2700,
    title="Monthly Revenue by Product Line (2022-2023)",
    x_axis_type="datetime",
    x_axis_label="Month",
    y_axis_label="Revenue ($ thousands)",
)

# Create data source for patches
# For stacked areas, we need to create closed polygons
x_forward = list(months)
x_backward = list(reversed(months))

# Product A (bottom layer) - from 0 to stack_a
source_a = ColumnDataSource(data={"x": x_forward + x_backward, "y": list(stack_a) + [0] * len(months)})

# Product B - from stack_a to stack_b
source_b = ColumnDataSource(data={"x": x_forward + x_backward, "y": list(stack_b) + list(reversed(stack_a))})

# Product C - from stack_b to stack_c
source_c = ColumnDataSource(data={"x": x_forward + x_backward, "y": list(stack_c) + list(reversed(stack_b))})

# Product D (top layer) - from stack_c to stack_d
source_d = ColumnDataSource(data={"x": x_forward + x_backward, "y": list(stack_d) + list(reversed(stack_c))})

# Draw stacked areas using patches
p.patch(
    x="x",
    y="y",
    source=source_a,
    fill_color=colors[0],
    fill_alpha=0.75,
    line_color=colors[0],
    line_width=2,
    legend_label="Product A",
)
p.patch(
    x="x",
    y="y",
    source=source_b,
    fill_color=colors[1],
    fill_alpha=0.75,
    line_color=colors[1],
    line_width=2,
    legend_label="Product B",
)
p.patch(
    x="x",
    y="y",
    source=source_c,
    fill_color=colors[2],
    fill_alpha=0.75,
    line_color=colors[2],
    line_width=2,
    legend_label="Product C",
)
p.patch(
    x="x",
    y="y",
    source=source_d,
    fill_color=colors[3],
    fill_alpha=0.75,
    line_color=colors[3],
    line_width=2,
    legend_label="Product D",
)

# Style title and axes
p.title.text_font_size = "20pt"
p.xaxis.axis_label_text_font_size = "20pt"
p.yaxis.axis_label_text_font_size = "20pt"
p.xaxis.major_label_text_font_size = "16pt"
p.yaxis.major_label_text_font_size = "16pt"

# Legend styling
p.legend.location = "top_left"
p.legend.label_text_font_size = "16pt"
p.legend.background_fill_alpha = 0.7

# Grid styling
p.xgrid.grid_line_alpha = 0.3
p.ygrid.grid_line_alpha = 0.3

# Save as PNG
export_png(p, filename="plot.png")

# Save as HTML for interactive viewing
output_file("plot.html")
save(p)
