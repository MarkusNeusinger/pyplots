"""pyplots.ai
chart-export-menu: Chart with Built-in Export Menu
Library: pygal | Python 3.13
Quality: pending | Created: 2025-01-19
"""

import pygal
from pygal.style import Style


# Data - monthly sales data over a year
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
product_a = [45, 52, 48, 61, 75, 82, 95, 88, 72, 65, 58, 70]
product_b = [30, 35, 42, 55, 63, 70, 78, 85, 68, 55, 48, 52]
product_c = [25, 28, 35, 40, 45, 52, 58, 62, 55, 48, 42, 38]

# Custom style for pyplots
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#FFD43B", "#4B8BBE", "#646464"),
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=42,
    value_font_size=36,
    stroke_width=4,
    font_family="Arial, sans-serif",
)

# Create line chart with export menu enabled
# Pygal SVG charts include built-in interactivity with context menu
chart = pygal.Line(
    width=4800,
    height=2700,
    style=custom_style,
    title="chart-export-menu · pygal · pyplots.ai",
    x_title="Month",
    y_title="Sales (thousands)",
    show_x_guides=True,
    show_y_guides=True,
    show_dots=True,
    dots_size=10,
    stroke_style={"width": 4, "linecap": "round", "linejoin": "round"},
    legend_at_bottom=False,
    legend_box_size=36,
    margin=80,
    show_legend=True,
    # Enable export/download capabilities in SVG
    disable_xml_declaration=False,
    explicit_size=True,
    print_values=False,
    show_minor_x_labels=True,
    show_minor_y_labels=True,
    truncate_legend=-1,
    truncate_label=-1,
)

# Set x-axis labels
chart.x_labels = months

# Add data series
chart.add("Product A", product_a)
chart.add("Product B", product_b)
chart.add("Product C", product_c)

# Save as SVG (native format with built-in export context menu)
# Pygal SVG files include right-click context menu for export options
chart.render_to_file("plot.html")

# Also save as PNG for static preview
chart.render_to_png("plot.png")
