"""
line-basic: Basic Line Plot
Library: pygal
"""

import pygal
from pygal.style import Style


# Data
time = [1, 2, 3, 4, 5, 6, 7]
value = [10, 15, 13, 18, 22, 19, 25]

# Custom style following pyplots color palette
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998",),  # Python Blue
    title_font_size=48,
    label_font_size=38,
    legend_font_size=38,
    value_font_size=32,
    value_label_font_size=32,
    tooltip_font_size=32,
)

# Create chart
chart = pygal.Line(
    width=4800,
    height=2700,
    title="Basic Line Plot",
    x_title="Time",
    y_title="Value",
    style=custom_style,
    show_legend=False,
    show_y_guides=True,
    show_x_guides=False,
    dots_size=8,
    stroke_style={"width": 4},
)

# Add data
chart.x_labels = [str(t) for t in time]
chart.add("Value", value)

# Save as PNG
chart.render_to_png("plot.png")
