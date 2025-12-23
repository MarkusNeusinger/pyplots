"""pyplots.ai
rose-basic: Basic Rose Chart
Library: pygal 3.1.0 | Python 3.13.11
Quality: 73/100 | Created: 2025-12-23
"""

import pygal
from pygal.style import Style


# Data: Monthly rainfall (mm) - shows natural 12-month cycle with seasonal variation
# Pacific Northwest pattern: wet winters, dry summers
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
rainfall = [145, 115, 95, 65, 45, 35, 20, 25, 50, 90, 135, 155]

# Color gradient: darker blue = higher rainfall, lighter blue = lower rainfall
# Manually calculated based on value range (20-155mm)
colors = (
    "#306998",  # Jan: 145mm - dark
    "#456f9a",  # Feb: 115mm
    "#5a769d",  # Mar: 95mm
    "#6f7d9f",  # Apr: 65mm
    "#8484a2",  # May: 45mm
    "#998ba4",  # Jun: 35mm
    "#a992a7",  # Jul: 20mm - lightest
    "#a48fa6",  # Aug: 25mm
    "#7f81a1",  # Sep: 50mm
    "#5f789e",  # Oct: 90mm
    "#3a6c99",  # Nov: 135mm
    "#2b6697",  # Dec: 155mm - darkest
)

# Custom style optimized for 3600x3600 canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=colors,
    title_font_size=80,
    label_font_size=48,
    major_label_font_size=48,
    legend_font_size=44,
    value_font_size=40,
    stroke_width=2,
    opacity=0.9,
    opacity_hover=1.0,
    value_colors=("#333333",),
)

# Rose chart approximation using Pie chart with equal-angle wedges
# Pygal lacks native rose charts. A Pie chart provides wedge-shaped segments
# (closer to rose/coxcomb than Radar's connected polygon).
# Color intensity encodes value magnitude since pygal doesn't support variable radii.
chart = pygal.Pie(
    width=3600,
    height=3600,
    style=custom_style,
    title="rose-basic · pygal · pyplots.ai",
    show_legend=False,
    inner_radius=0.12,
    half_pie=False,
    margin=80,
    print_values=True,
    print_labels=True,
)

# Each month gets equal slice (equal angles), color intensity shows rainfall magnitude
for month, value in zip(months, rainfall, strict=True):
    chart.add(month, [{"value": 1, "label": f"{month}\n{value} mm"}])

# Hide default value display (we show values in labels)
chart.value_formatter = lambda x: ""

# Save as PNG and HTML
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
