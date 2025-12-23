"""pyplots.ai
slope-basic: Basic Slope Chart (Slopegraph)
Library: pygal 3.1.0 | Python 3.13.11
Quality: 82/100 | Created: 2025-12-23
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

# Colorblind-friendly colors for increase vs decrease (spec requirement)
# Using blue for increase, orange for decrease - distinguishable for colorblind
COLOR_INCREASE = "#2166AC"  # Blue - value went up
COLOR_DECREASE = "#D6604D"  # Orange-red - value went down

# Separate products by direction for proper color grouping
increasing_products = []
decreasing_products = []
for i, product in enumerate(products):
    if q4_sales[i] >= q1_sales[i]:
        increasing_products.append((product, q1_sales[i], q4_sales[i]))
    else:
        decreasing_products.append((product, q1_sales[i], q4_sales[i]))

# Build color tuple: one color per series, matching direction
# First all increasing (blue), then all decreasing (orange)
series_colors = tuple([COLOR_INCREASE] * len(increasing_products) + [COLOR_DECREASE] * len(decreasing_products))

# Custom style for 4800x2700 px - colors per series matching direction
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=series_colors,
    title_font_size=72,
    label_font_size=40,
    major_label_font_size=48,
    legend_font_size=36,
    value_font_size=36,
    stroke_width=4,
    value_label_font_size=32,
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
    legend_at_bottom=True,
    legend_box_size=24,
    truncate_legend=-1,
    interpolate=None,
    margin=80,
    print_values=True,
    print_labels=True,
)

# X-axis labels (two time points)
chart.x_labels = ["Q1", "Q4"]

# Add increasing products first (blue color) with endpoint labels
for product, start, end in increasing_products:
    chart.add(
        f"{product} (Increase)",
        [{"value": start, "label": f"{product}: {start}"}, {"value": end, "label": f"{product}: {end}"}],
    )

# Add decreasing products (orange color) with endpoint labels
for product, start, end in decreasing_products:
    chart.add(
        f"{product} (Decrease)",
        [{"value": start, "label": f"{product}: {start}"}, {"value": end, "label": f"{product}: {end}"}],
    )

# Save as PNG and HTML
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
