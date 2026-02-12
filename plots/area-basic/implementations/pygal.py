""" pyplots.ai
area-basic: Basic Area Chart
Library: pygal 3.1.0 | Python 3.14.2
Quality: 84/100 | Created: 2025-12-23
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

# Key data points for annotations
peak_day = visitors.index(max(visitors))
low_day = visitors.index(min(visitors))

# Custom style for 4800x2700 canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333",
    foreground_strong="#333",
    foreground_subtle="#999",
    colors=("#306998",),
    title_font_size=56,
    label_font_size=40,
    major_label_font_size=36,
    value_font_size=32,
    opacity=0.35,
    opacity_hover=0.5,
)

# Create area chart (Line with fill=True)
chart = pygal.Line(
    width=4800,
    height=2700,
    title="Daily Website Visitors \u00b7 area-basic \u00b7 pygal \u00b7 pyplots.ai",
    x_title="Day of Month",
    y_title="Visitors",
    style=custom_style,
    fill=True,
    show_dots=True,
    dots_size=12,
    stroke_style={"width": 5},
    show_y_guides=True,
    show_x_guides=False,
    x_label_rotation=0,
    show_legend=False,
    value_formatter=lambda x: f"{x:,.0f}",
    min_scale=4,
)

# Add data with annotations on key points
annotated_visitors = []
for i, v in enumerate(visitors):
    if i == peak_day:
        annotated_visitors.append({"value": v, "label": f"Peak: {v:,} visitors (Day {i + 1})"})
    elif i == low_day:
        annotated_visitors.append({"value": v, "label": f"Low: {v:,} visitors (Day {i + 1})"})
    else:
        annotated_visitors.append(v)

# X-axis labels - show every 5th day for readability
chart.x_labels = [str(d) if d % 5 == 0 or d == 1 else "" for d in days]
chart.add("Daily Visitors", annotated_visitors)

# Save outputs
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
