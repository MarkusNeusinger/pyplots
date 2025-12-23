"""pyplots.ai
pie-basic: Basic Pie Chart
Library: pygal | Python 3.13
Quality: pending | Created: 2025-12-23
"""

import pygal
from pygal.style import Style


# Data - Market share distribution
categories = ["Product A", "Product B", "Product C", "Product D", "Product E"]
values = [35, 25, 20, 12, 8]

# Custom style for 3600x3600 px (square format for pie chart)
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333",
    foreground_strong="#333",
    foreground_subtle="#666",
    colors=("#306998", "#FFD43B", "#4ECDC4", "#FF6B6B", "#95E1D3"),
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=48,
    legend_font_size=42,
    value_font_size=42,
    tooltip_font_size=36,
)

# Create pie chart
chart = pygal.Pie(
    width=3600,
    height=3600,
    style=custom_style,
    title="pie-basic · pygal · pyplots.ai",
    inner_radius=0,
    legend_at_bottom=True,
    legend_at_bottom_columns=5,
    print_values=True,
    print_values_position="center",
    value_formatter=lambda x: f"{x}%",
)

# Add data slices
for category, value in zip(categories, values, strict=True):
    chart.add(category, value)

# Save as PNG and HTML
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
