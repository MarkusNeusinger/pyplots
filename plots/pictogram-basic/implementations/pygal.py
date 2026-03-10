""" pyplots.ai
pictogram-basic: Pictogram Chart (Isotype Visualization)
Library: pygal 3.1.0 | Python 3.14.3
Quality: 75/100 | Created: 2026-03-10
"""

import pygal
from pygal.style import Style


# Data - Fruit production (thousands of tonnes)
categories = ["Apples", "Oranges", "Bananas", "Grapes", "Mangoes"]
values = [35, 22, 18, 12, 8]
icon_unit = 5  # Each dot represents 5 thousand tonnes

# Build dot matrix data: each full unit = 1.0, partial = fraction
max_icons = max(v // icon_unit + (1 if v % icon_unit else 0) for v in values)
dot_data = {}
for cat, val in zip(categories, values, strict=True):
    full = val // icon_unit
    remainder = val % icon_unit
    row = [1.0] * full
    if remainder:
        row.append(remainder / icon_unit)
    # Pad with None so all rows same length
    row += [None] * (max_icons - len(row))
    dot_data[cat] = row

# Style
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#cccccc",
    colors=("#306998", "#E6A817", "#2E8B57", "#8B5CF6", "#E05D44"),
    title_font_size=48,
    label_font_size=32,
    major_label_font_size=28,
    legend_font_size=28,
    value_font_size=20,
    tooltip_font_size=24,
)

# Plot
chart = pygal.Dot(
    width=4800,
    height=2700,
    style=custom_style,
    title="Fruit Production (each dot = 5k tonnes) · pictogram-basic · pygal · pyplots.ai",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=5,
    show_x_guides=False,
    show_y_guides=False,
    spacing=40,
    margin=50,
    margin_left=60,
    margin_right=60,
    margin_top=80,
    margin_bottom=150,
    x_label_rotation=0,
    truncate_label=-1,
    truncate_legend=-1,
    dot_size=40,
)

# X-axis labels showing cumulative value
chart.x_labels = [str((i + 1) * icon_unit) for i in range(max_icons)]

# Add each category as a series
for cat in categories:
    chart.add(cat, dot_data[cat])

# Save
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
