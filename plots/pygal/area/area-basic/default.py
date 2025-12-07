"""
area-basic: Basic Area Chart
Library: pygal
"""

import pygal
from pygal.style import Style


# Data - monthly sales example from spec
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
sales = [100, 150, 130, 180, 200, 220]

# Custom style with project palette
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998",),
    font_family="sans-serif",
    title_font_size=60,
    label_font_size=48,
    major_label_font_size=48,
    legend_font_size=48,
    value_font_size=36,
    opacity=0.5,
    opacity_hover=0.7,
)

# Create area chart (Line chart with fill=True)
chart = pygal.Line(
    width=4800,
    height=2700,
    title="Monthly Sales",
    x_title="Month",
    y_title="Sales ($)",
    style=custom_style,
    show_legend=False,
    fill=True,
    show_x_guides=False,
    show_y_guides=True,
    dots_size=8,
    stroke_style={"width": 4},
)

# Add data
chart.x_labels = months
chart.add("Sales", sales)

# Save
chart.render_to_png("plot.png")
