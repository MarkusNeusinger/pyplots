""" pyplots.ai
bar-stacked-labeled: Stacked Bar Chart with Total Labels
Library: pygal 3.1.0 | Python 3.13.11
Quality: 85/100 | Created: 2026-01-09
"""

import pygal
from pygal.style import Style


# Data - Quarterly revenue by product category (in thousands)
categories = ["Q1", "Q2", "Q3", "Q4"]
products = {
    "Electronics": [120, 145, 132, 168],
    "Furniture": [85, 92, 78, 105],
    "Clothing": [65, 72, 88, 95],
    "Accessories": [42, 55, 48, 62],
}

# Calculate totals for labels
totals = [sum(products[product][i] for product in products) for i in range(len(categories))]

# Custom style for large canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#FFD43B", "#4ECDC4", "#E74C3C"),
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=42,
    value_font_size=44,
    value_label_font_size=44,
    tooltip_font_size=36,
    stroke_width=2,
)

# Create stacked bar chart
chart = pygal.StackedBar(
    width=4800,
    height=2700,
    style=custom_style,
    title="bar-stacked-labeled · pygal · pyplots.ai",
    x_title="Quarter",
    y_title="Revenue ($K)",
    show_y_guides=True,
    show_x_guides=False,
    legend_at_bottom=True,
    legend_box_size=24,
    print_values=True,
    print_values_position="top",
    value_formatter=lambda x: "",  # Hide default values, use per-series formatter
    margin=50,
    spacing=80,
    truncate_legend=-1,
    x_label_rotation=0,
    range=(0, max(totals) * 1.15),  # Extra headroom for total labels
)

# Set x-axis labels
chart.x_labels = categories

# Add data series - only show labels on the top (last) series
product_list = list(products.items())
for idx, (product, values) in enumerate(product_list):
    is_top = idx == len(product_list) - 1
    if is_top:
        # Top series: show total labels above each bar
        data = [{"value": v, "formatter": lambda x, i=i: f"Total: ${totals[i]}K"} for i, v in enumerate(values)]
    else:
        # Other series: no labels
        data = values
    chart.add(product, data)

# Save as PNG and HTML
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
