"""pyplots.ai
bar-sorted: Sorted Bar Chart
Library: pygal 3.1.0 | Python 3.13.11
Quality: 72/100 | Created: 2025-12-30
"""

import pygal
from pygal.style import Style


# Data - Monthly sales by product category (sorted descending)
categories = ["Electronics", "Clothing", "Home & Garden", "Sports", "Books", "Toys", "Beauty", "Food"]
values = [4850, 3720, 2980, 2450, 1890, 1560, 1240, 980]

# Sort data by values (descending) - already sorted, but making it explicit
sorted_pairs = sorted(zip(categories, values, strict=True), key=lambda x: x[1], reverse=True)

# Custom style for 4800x2700 canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998",),  # Python Blue for all bars
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=42,
    value_font_size=36,
    value_label_font_size=36,
    tooltip_font_size=36,
    stroke_width=2,
)

# Extract sorted categories and values (reversed for pygal which renders bottom-to-top)
sorted_categories = [pair[0] for pair in reversed(sorted_pairs)]
sorted_values = [pair[1] for pair in reversed(sorted_pairs)]

# Create horizontal bar chart (better for category labels)
chart = pygal.HorizontalBar(
    width=4800,
    height=2700,
    style=custom_style,
    title="bar-sorted · pygal · pyplots.ai",
    x_title="Sales (USD)",
    show_legend=False,
    show_x_guides=True,
    print_values=True,
    print_values_position="center",
    value_formatter=lambda x: f"${x:,.0f}",
    margin=80,
    spacing=30,
    truncate_label=-1,
)

# Set category labels on Y-axis (x_labels maps to Y-axis in HorizontalBar)
chart.x_labels = sorted_categories

# Add data as single series (no legend needed since x_labels provide categories)
chart.add("Sales", sorted_values)

# Save as PNG and HTML
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
