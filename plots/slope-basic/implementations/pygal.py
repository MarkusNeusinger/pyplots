"""pyplots.ai
slope-basic: Basic Slope Chart (Slopegraph)
Library: pygal 3.1.0 | Python 3.13.11
Quality: 87/100 | Created: 2025-12-23
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

# Determine color for each product based on direction of change
colors = []
for i in range(len(products)):
    if q4_sales[i] >= q1_sales[i]:
        colors.append(COLOR_INCREASE)
    else:
        colors.append(COLOR_DECREASE)

# Custom style for 4800x2700 px with direction-based colors
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=tuple(colors),
    title_font_size=72,
    label_font_size=40,
    major_label_font_size=48,
    legend_font_size=36,
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
    legend_at_bottom=True,
    legend_box_size=24,
    truncate_legend=-1,
    interpolate=None,
    margin=60,
)

# X-axis labels (two time points)
chart.x_labels = ["Q1", "Q4"]

# Add each product as a series with two values (Q1 and Q4)
# Include direction indicator in legend for clarity
for i, product in enumerate(products):
    direction = "↑" if q4_sales[i] >= q1_sales[i] else "↓"
    chart.add(f"{product} {direction}", [q1_sales[i], q4_sales[i]])

# Save as PNG and HTML
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
