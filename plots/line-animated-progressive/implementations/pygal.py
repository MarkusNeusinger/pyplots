""" pyplots.ai
line-animated-progressive: Animated Line Plot Over Time
Library: pygal 3.1.0 | Python 3.13.11
Quality: 62/100 | Created: 2026-01-07
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - Monthly website traffic over 12 months
np.random.seed(42)
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
base_traffic = 50000
trend = np.linspace(0, 30000, 12)
seasonal = 5000 * np.sin(np.linspace(0, 2 * np.pi, 12))
noise = np.random.normal(0, 2000, 12)
visitors = base_traffic + trend + seasonal + noise
visitors = np.maximum(visitors, 10000).astype(int)

# Custom style for pyplots canvas (4800x2700)
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#FFD43B", "#5A9BD5", "#70AD47"),
    font_family="sans-serif",
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=48,
    legend_font_size=48,
    value_font_size=40,
    stroke_width=8,
    opacity=0.85,
    opacity_hover=1.0,
    transition="100ms ease-in",
)

# Create a line chart showing progressive reveal via small multiples approach
# Pygal doesn't support animation, so we show the complete line with
# progressive stages overlaid to indicate the direction of data flow

chart = pygal.Line(
    width=4800,
    height=2700,
    style=custom_style,
    title="line-animated-progressive · pygal · pyplots.ai",
    x_title="Month",
    y_title="Website Visitors",
    show_x_guides=False,
    show_y_guides=True,
    show_dots=True,
    dots_size=16,
    stroke_style={"width": 8, "linecap": "round", "linejoin": "round"},
    fill=False,
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=4,
    truncate_legend=-1,
    margin=80,
    spacing=50,
    show_minor_x_labels=True,
    x_label_rotation=0,
    print_values=False,
    print_zeroes=False,
    interpolate="cubic",
)

# Set x-axis labels
chart.x_labels = months

# Add data series showing progressive stages of reveal
# Stage 1: First quarter (Q1) - blue
q1_data = list(visitors[:3]) + [None] * 9
chart.add("Q1 Progress", q1_data)

# Stage 2: First half (H1) - yellow
h1_data = list(visitors[:6]) + [None] * 6
chart.add("H1 Progress", h1_data)

# Stage 3: Three quarters (Q3) - light blue
q3_data = list(visitors[:9]) + [None] * 3
chart.add("Q3 Progress", q3_data)

# Stage 4: Complete year (Full) - green
full_data = list(visitors)
chart.add("Full Year", full_data)

# Save outputs
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
