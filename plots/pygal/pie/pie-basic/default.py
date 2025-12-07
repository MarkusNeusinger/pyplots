"""
pie-basic: Basic Pie Chart
Library: pygal
"""

import pygal
from pygal.style import Style


# Data
categories = ["Product A", "Product B", "Product C", "Product D", "Other"]
values = [35, 25, 20, 15, 5]

# Custom style matching default-style-guide.md colors
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#FFD43B", "#DC2626", "#059669", "#8B5CF6"),
    title_font_size=60,
    legend_font_size=48,
    value_font_size=48,
    tooltip_font_size=36,
)

# Create pie chart
chart = pygal.Pie(
    width=4800,
    height=2700,
    title="Market Share Distribution",
    style=custom_style,
    inner_radius=0,
    show_legend=True,
    legend_at_bottom=True,
)

# Add data slices
for category, value in zip(categories, values, strict=True):
    chart.add(category, value)

# Save as PNG
chart.render_to_png("plot.png")
