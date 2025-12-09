"""
bar-basic: Basic Bar Chart
Library: pygal
"""

import pygal
from pygal.style import Style


# Data
categories = ["Product A", "Product B", "Product C", "Product D", "Product E"]
values = [45, 78, 52, 91, 63]

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
    legend_font_size=40,
    value_font_size=32,
)

# Create chart
chart = pygal.Bar(
    width=4800,
    height=2700,
    title="Basic Bar Chart",
    x_title="Category",
    y_title="Value",
    style=custom_style,
    show_legend=False,
    show_y_guides=True,
)

# Add data
chart.x_labels = categories
chart.add("Value", values)

# Save as PNG
chart.render_to_png("plot.png")
