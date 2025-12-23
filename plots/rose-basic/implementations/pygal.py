"""pyplots.ai
rose-basic: Basic Rose Chart
Library: pygal 3.1.0 | Python 3.13.11
Quality: 58/100 | Created: 2025-12-23
"""

import pygal
from pygal.style import Style


# Data: Monthly rainfall (mm) - shows natural 12-month cycle with seasonal variation
# Pacific Northwest pattern: wet winters, dry summers
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
rainfall = [145, 115, 95, 65, 45, 35, 20, 25, 50, 90, 135, 155]

# Custom style optimized for 3600x3600 canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998",),  # Python Blue
    title_font_size=80,
    label_font_size=52,
    major_label_font_size=48,
    legend_font_size=48,
    value_font_size=40,
    stroke_width=4,
    opacity=0.85,
    opacity_hover=0.95,
)

# Create radar chart with fill as best approximation for rose chart in pygal
# Note: Pygal does not have a native rose/coxcomb chart type.
# A radar chart with fill is the closest available approximation,
# though it connects points with a polygon rather than creating separate wedges.
chart = pygal.Radar(
    width=3600,
    height=3600,
    style=custom_style,
    title="rose-basic · pygal · pyplots.ai",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=1,
    fill=True,
    show_dots=True,
    dots_size=12,
    stroke_style={"width": 4},
    inner_radius=0,
    margin=150,
    margin_bottom=250,
    spacing=40,
    show_y_guides=True,
    show_x_guides=False,
)

# Set month labels around the circle
chart.x_labels = months

# Add rainfall data series
chart.add("Monthly Rainfall (mm)", rainfall)

# Save as PNG and HTML
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
