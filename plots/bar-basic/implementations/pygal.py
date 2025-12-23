"""pyplots.ai
bar-basic: Basic Bar Chart
Library: pygal | Python 3.13
Quality: pending | Created: 2025-12-23
"""

import pygal
from pygal.style import Style


# Data - Quarterly sales by product category
categories = ["Electronics", "Clothing", "Home & Garden", "Sports", "Books", "Toys"]
values = [45200, 32800, 28500, 19700, 15300, 12400]

# Custom style using PyPlots color palette
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998",),  # Python Blue for all bars
    title_font_size=48,
    label_font_size=38,
    major_label_font_size=38,
    value_font_size=32,
    value_label_font_size=32,
    legend_font_size=38,
)

# Create chart
chart = pygal.Bar(
    width=4800,
    height=2700,
    title="bar-basic · pygal · pyplots.ai",
    x_title="Category",
    y_title="Sales ($)",
    style=custom_style,
    show_legend=False,
    print_values=True,
    print_values_position="top",
    value_formatter=lambda x: f"${x:,.0f}",
    show_y_guides=True,
    show_x_guides=False,
    margin=50,
    spacing=30,
)

# Add data
chart.x_labels = categories
chart.add("Sales", values)

# Save outputs
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
