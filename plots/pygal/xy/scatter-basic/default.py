"""
scatter-basic: Basic Scatter Plot
Library: pygal
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - generate random data with correlation
np.random.seed(42)
x = np.random.randn(100) * 2 + 10
y = x * 0.8 + np.random.randn(100) * 2

# Combine into XY coordinate pairs for pygal
points = [(float(xi), float(yi)) for xi, yi in zip(x, y, strict=True)]

# Custom style matching pyplots palette
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998",),
    title_font_size=48,
    label_font_size=40,
    major_label_font_size=40,
    value_font_size=32,
    legend_font_size=40,
    tooltip_font_size=32,
)

# Create XY chart (scatter plot in pygal)
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="Basic Scatter Plot",
    x_title="X Value",
    y_title="Y Value",
    show_legend=False,
    stroke=False,
    dots_size=8,
    show_x_guides=True,
    show_y_guides=True,
)

# Add data series
chart.add("Data", points)

# Save as PNG
chart.render_to_png("plot.png")
