""" pyplots.ai
bar-stacked: Stacked Bar Chart
Library: pygal 3.1.0 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-25
"""

import pygal
from pygal.style import Style


# Data: Quarterly revenue by product category (in millions USD)
categories = ["Q1", "Q2", "Q3", "Q4"]
products = {
    "Software": [12.5, 15.2, 18.1, 22.4],
    "Hardware": [8.3, 9.1, 7.8, 10.2],
    "Services": [5.2, 6.8, 8.5, 9.1],
    "Cloud": [3.1, 5.5, 9.2, 14.3],
}

# Custom style for 4800x2700 canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#FFD43B", "#4ECDC4", "#E76F51"),
    title_font_size=48,
    label_font_size=38,
    major_label_font_size=36,
    legend_font_size=36,
    value_font_size=28,
    value_label_font_size=28,
    stroke_width=2,
)

# Create stacked bar chart
chart = pygal.StackedBar(
    width=4800,
    height=2700,
    style=custom_style,
    title="bar-stacked · pygal · pyplots.ai",
    x_title="Quarter",
    y_title="Revenue (Million USD)",
    show_y_guides=True,
    show_x_guides=False,
    legend_at_bottom=False,
    legend_box_size=24,
    spacing=80,
    margin=60,
    margin_top=120,
    margin_bottom=120,
    print_values=False,
    show_legend=True,
)

# Set x-axis labels
chart.x_labels = categories

# Add data series (stacked components)
for product_name, values in products.items():
    chart.add(product_name, values)

# Save as PNG and HTML
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
