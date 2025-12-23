""" pyplots.ai
rose-basic: Basic Rose Chart
Library: pygal 3.1.0 | Python 3.13.11
Quality: 58/100 | Created: 2025-12-23
"""

import pygal
from pygal.style import Style


# Data: Monthly rainfall (mm) - shows natural 12-month cycle
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
rainfall = [78, 52, 65, 48, 55, 72, 85, 92, 88, 95, 82, 70]

# Custom style for pyplots (4800x2700 canvas)
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998",),  # Python Blue
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=42,
    value_font_size=36,
    stroke_width=2,
    opacity=0.85,
    opacity_hover=0.95,
)

# Create rose chart using Radar with fill
# Pygal's Radar chart with fill creates a rose/polar area effect
chart = pygal.Radar(
    width=3600,
    height=3600,
    style=custom_style,
    title="rose-basic · pygal · pyplots.ai",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=1,
    fill=True,  # Fill the radar to create rose effect
    show_dots=True,
    dots_size=8,
    stroke_style={"width": 3},
    inner_radius=0,  # Start from center
    margin=100,
    spacing=50,
)

# Set category labels (months around the circle)
chart.x_labels = months

# Add the rainfall data
chart.add("Monthly Rainfall (mm)", rainfall)

# Save as PNG and HTML
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
