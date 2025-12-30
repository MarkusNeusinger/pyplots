""" pyplots.ai
bar-categorical: Categorical Count Bar Chart
Library: pygal 3.1.0 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-30
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - Raw categorical values (counts computed automatically)
np.random.seed(42)
categories = ["Laptop", "Smartphone", "Tablet", "Desktop", "Smartwatch", "Headphones"]
weights = [0.25, 0.30, 0.15, 0.10, 0.12, 0.08]  # Probability weights for realistic distribution
raw_data = np.random.choice(categories, size=500, p=weights)

# Count frequencies
unique, counts = np.unique(raw_data, return_counts=True)
category_counts = dict(zip(unique, counts, strict=True))

# Sort by count descending for better visualization
sorted_items = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
sorted_categories = [item[0] for item in sorted_items]
sorted_counts = [item[1] for item in sorted_items]

# Custom style for 4800x2700 canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#FFD43B", "#4B8BBE", "#FFE873", "#306998", "#FFD43B"),
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=42,
    value_font_size=36,
    value_label_font_size=36,
    tooltip_font_size=36,
    stroke_width=2,
    opacity=0.9,
    opacity_hover=1.0,
)

# Create chart
chart = pygal.Bar(
    width=4800,
    height=2700,
    title="bar-categorical · pygal · pyplots.ai",
    x_title="Product Category",
    y_title="Count (Frequency)",
    style=custom_style,
    show_legend=False,
    show_y_guides=True,
    show_x_guides=False,
    print_values=True,
    print_values_position="top",
    value_formatter=lambda x: str(int(x)),
    margin=60,
    spacing=40,
    truncate_label=-1,
    x_label_rotation=0,
)

# Set x-axis labels
chart.x_labels = sorted_categories

# Add data - single series with counts
chart.add("Count", sorted_counts)

# Save as PNG and HTML
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
