"""
rose-basic: Basic Rose Chart
Library: pygal
"""

import pygal
from pygal.style import Style


# Data - Monthly rainfall (mm) showing natural cyclical pattern
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
rainfall = [78, 62, 55, 42, 38, 52, 65, 72, 85, 98, 102, 89]

# Custom style for 4800x2700 canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998",),
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=42,
    value_font_size=36,
    stroke_width=4,
    opacity=0.85,
    opacity_hover=0.95,
)

# Create radar chart (rose/nightingale style)
chart = pygal.Radar(
    width=4800,
    height=2700,
    style=custom_style,
    title="Monthly Rainfall (mm) · rose-basic · pygal · pyplots.ai",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=1,
    dots_size=12,
    show_dots=True,
    fill=True,
)

# Set month labels around the radar
chart.x_labels = months

# Add data series
chart.add("Rainfall", rainfall)

# Save outputs
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
