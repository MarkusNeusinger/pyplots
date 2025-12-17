"""
slope-basic: Basic Slope Chart (Slopegraph)
Library: pygal
"""

import pygal
from pygal.style import Style


# Data - Sales figures comparing Q1 vs Q4 for 10 products
products = [
    "Product A",
    "Product B",
    "Product C",
    "Product D",
    "Product E",
    "Product F",
    "Product G",
    "Product H",
    "Product I",
    "Product J",
]
q1_sales = [85, 72, 95, 45, 68, 52, 78, 62, 88, 40]
q4_sales = [92, 58, 102, 75, 65, 71, 82, 48, 95, 55]

# Custom style for 4800x2700 px
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=(
        "#306998",
        "#FFD43B",
        "#e74c3c",
        "#2ecc71",
        "#9b59b6",
        "#f39c12",
        "#1abc9c",
        "#e67e22",
        "#3498db",
        "#c0392b",
    ),
    title_font_size=72,
    label_font_size=40,
    major_label_font_size=48,
    legend_font_size=40,
    value_font_size=36,
    stroke_width=4,
)

# Create slope chart using Line chart with only 2 x-axis points
chart = pygal.Line(
    width=4800,
    height=2700,
    title="slope-basic · pygal · pyplots.ai",
    x_title="Time Period",
    y_title="Sales (units)",
    style=custom_style,
    show_dots=True,
    dots_size=12,
    stroke_style={"width": 4},
    show_y_guides=True,
    show_x_guides=False,
    show_legend=True,
    legend_at_bottom=False,
    truncate_legend=-1,
    interpolate=None,
)

# X-axis labels (two time points)
chart.x_labels = ["Q1", "Q4"]

# Add each product as a series with two values (Q1 and Q4)
for i, product in enumerate(products):
    chart.add(product, [q1_sales[i], q4_sales[i]])

# Save as PNG and HTML
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
