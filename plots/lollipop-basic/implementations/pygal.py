"""
lollipop-basic: Basic Lollipop Chart
Library: pygal
"""

import pygal
from pygal.style import Style


# Data - Product sales by category (sorted by value)
categories = ["Smartphones", "Laptops", "Tablets", "Headphones", "Smartwatches", "Cameras", "Speakers", "Gaming"]
values = [892, 654, 478, 312, 287, 198, 156, 134]

# Sort by value descending for better readability
sorted_data = sorted(zip(categories, values, strict=True), key=lambda x: x[1], reverse=True)
categories = [item[0] for item in sorted_data]
values = [item[1] for item in sorted_data]

# Custom style for 4800x2700 canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998",),  # Python Blue
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=42,
    value_font_size=36,
    value_label_font_size=36,
)

# Create XY chart for lollipop visualization
# Each lollipop is a line from (0, y) to (value, y) with a dot at the end
n = len(categories)
chart = pygal.XY(
    width=4800,
    height=2700,
    title="lollipop-basic · pygal · pyplots.ai",
    x_title="Sales (units)",
    style=custom_style,
    show_legend=False,  # Category names shown on y-axis
    dots_size=25,  # Large dots for lollipop heads
    stroke_style={"width": 4},  # Thin stem lines
    show_y_guides=True,
    show_x_guides=True,
    margin=100,
    xrange=(0, max(values) * 1.1),  # X-axis range
    range=(0, n + 1),  # Y-axis range to fit all categories
    y_labels=[{"label": cat, "value": n - i} for i, cat in enumerate(categories)],
)

# Create lollipop data - each category is a line from 0 to value
# Using None for first point to hide dot at baseline, only show dot at value
for i, (cat, val) in enumerate(zip(categories, values, strict=True)):
    y_pos = n - i  # Position from top to bottom (highest value at top)
    # Line from baseline to value - use dict with node config to hide baseline dot
    chart.add(cat, [{"value": (0, y_pos), "node": {"r": 0}}, {"value": (val, y_pos)}], dots_size=25)

# Save outputs
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
