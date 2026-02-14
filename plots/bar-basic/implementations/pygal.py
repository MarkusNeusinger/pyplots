"""pyplots.ai
bar-basic: Basic Bar Chart
Library: pygal 3.1.0 | Python 3.14
Quality: /100 | Updated: 2026-02-14
"""

import pygal
from pygal.style import Style


# Data - Quarterly sales by product category
categories = ["Electronics", "Clothing", "Home & Garden", "Sports", "Books", "Toys"]
values = [52400, 34100, 28500, 17600, 11200, 6800]

# Custom style
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#cccccc",
    colors=("#306998",),
    title_font_size=48,
    label_font_size=40,
    major_label_font_size=40,
    value_font_size=34,
    value_label_font_size=34,
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
    rounded_bars=2,
)

# Add data
chart.x_labels = categories
chart.add("Sales", values)

# Save
chart.render_to_png("plot.png")
