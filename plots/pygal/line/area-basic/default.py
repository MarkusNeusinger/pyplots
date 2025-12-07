"""
area-basic: Basic Area Chart
Library: pygal
"""

import pygal
from pygal.style import Style


# Data - monthly sales data
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
sales = [120, 135, 148, 162, 175, 195, 210, 198, 185, 170, 158, 190]

# Custom style with PyPlots color palette
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    opacity=0.7,
    opacity_hover=0.9,
    colors=("#306998",),  # Python Blue from style guide
    font_family="Arial, sans-serif",
    title_font_size=48,
    label_font_size=36,
    major_label_font_size=36,
    legend_font_size=36,
)

# Create area chart (Line chart with fill=True)
chart = pygal.Line(
    width=4800,
    height=2700,
    title="Monthly Sales Performance",
    x_title="Month",
    y_title="Sales (Units)",
    style=custom_style,
    fill=True,
    show_legend=True,
    legend_at_bottom=True,
    show_x_guides=False,
    show_y_guides=True,
    dots_size=6,
    stroke_style={"width": 4},
)

# Set x-axis labels
chart.x_labels = months

# Add data series
chart.add("Sales", sales)

# Save as PNG
chart.render_to_png("plot.png")
