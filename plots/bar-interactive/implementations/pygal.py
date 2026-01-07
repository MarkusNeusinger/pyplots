""" pyplots.ai
bar-interactive: Interactive Bar Chart with Hover and Click
Library: pygal 3.1.0 | Python 3.13.11
Quality: 91/100 | Created: 2026-01-07
"""

import pygal
from pygal.style import Style


# Data - Product sales by category with additional details
categories = ["Electronics", "Clothing", "Home & Garden", "Sports", "Books", "Toys", "Health", "Food"]
sales = [12500, 8900, 6700, 5400, 4200, 3800, 3100, 2800]
growth = ["+15%", "+8%", "+12%", "-3%", "+5%", "+22%", "+9%", "+4%"]

# Custom style for pyplots (large canvas: 4800x2700)
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#FFD43B", "#4CAF50", "#FF5722", "#9C27B0", "#00BCD4", "#FF9800", "#795548"),
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=42,
    value_font_size=36,
    tooltip_font_size=36,
    stroke_width=2,
    opacity=0.9,
    opacity_hover=1.0,
    transition="400ms ease-in-out",
)

# Create interactive bar chart
chart = pygal.Bar(
    width=4800,
    height=2700,
    style=custom_style,
    title="bar-interactive · pygal · pyplots.ai",
    x_title="Product Category",
    y_title="Sales (USD)",
    show_legend=True,
    legend_at_bottom=False,
    legend_box_size=24,
    show_y_guides=True,
    show_x_guides=False,
    x_label_rotation=0,
    print_values=False,
    print_zeroes=False,
    human_readable=True,
    spacing=30,
    margin=60,
    margin_top=100,
    margin_bottom=120,
    truncate_legend=-1,
    truncate_label=-1,
)

# Add data with custom tooltips showing sales value and growth percentage
# Each value includes tooltip text for hover interaction
chart.add(
    "Q4 Sales",
    [{"value": sales[i], "label": f"{categories[i]}: ${sales[i]:,} ({growth[i]} YoY)"} for i in range(len(categories))],
)

# Set x-axis labels
chart.x_labels = categories

# Save as PNG and HTML for interactivity
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
