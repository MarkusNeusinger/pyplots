""" pyplots.ai
area-basic: Basic Area Chart
Library: pygal 3.1.0 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-14
"""

import pygal
from pygal.style import Style


# Data - Daily website visitors over a month
days = list(range(1, 31))
visitors = [
    1250,
    1380,
    1420,
    1180,
    980,
    890,
    920,
    1340,
    1520,
    1680,
    1590,
    1450,
    1120,
    1080,
    1560,
    1720,
    1890,
    2010,
    1850,
    1420,
    1380,
    1680,
    1920,
    2150,
    2080,
    1950,
    1620,
    1540,
    1780,
    1920,
]

# Custom style for 4800x2700 canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333",
    foreground_strong="#333",
    foreground_subtle="#666",
    colors=("#306998",),
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=42,
    value_font_size=36,
    opacity=0.4,
    opacity_hover=0.6,
)

# Create area chart (Line with fill=True)
chart = pygal.Line(
    width=4800,
    height=2700,
    title="area-basic · pygal · pyplots.ai",
    x_title="Day of Month",
    y_title="Visitors",
    style=custom_style,
    fill=True,
    show_dots=True,
    dots_size=6,
    stroke_style={"width": 4},
    show_y_guides=True,
    show_x_guides=False,
    x_label_rotation=0,
    legend_at_bottom=True,
    truncate_legend=-1,
)

# Add data - show every 5th day label for readability
chart.x_labels = [str(d) if d % 5 == 0 or d == 1 else "" for d in days]
chart.add("Daily Visitors", visitors)

# Save outputs
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
