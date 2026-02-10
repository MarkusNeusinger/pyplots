""" pyplots.ai
scatter-basic: Basic Scatter Plot
Library: pygal 3.1.0 | Python 3.14.2
Quality: /100 | Updated: 2026-02-10
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - Coffee shop daily temperature vs iced drinks sold
np.random.seed(42)
temperature = np.random.normal(25, 8, 120).clip(5, 42)
base_sales = temperature * 3.2 + 15
noise = np.random.normal(0, 12, 120)
iced_drinks = (base_sales + noise).clip(10, 180)

# Custom style for 4800x2700 px canvas
custom_style = Style(
    background="#FAFBFC",
    plot_background="#FAFBFC",
    foreground="#2D3748",
    foreground_strong="#1A202C",
    foreground_subtle="#718096",
    colors=("#306998",),
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=44,
    legend_font_size=42,
    tooltip_font_size=36,
    opacity=0.65,
    opacity_hover=0.95,
)

# Create XY chart for scatter plot
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="scatter-basic \u00b7 pygal \u00b7 pyplots.ai",
    x_title="Daily Temperature (\u00b0C)",
    y_title="Iced Drinks Sold",
    show_legend=False,
    stroke=False,
    dots_size=14,
    show_x_guides=True,
    show_y_guides=True,
    x_label_rotation=0,
    truncate_label=-1,
)

# Add data as list of (x, y) tuples
points = [(float(t), float(d)) for t, d in zip(temperature, iced_drinks, strict=True)]
chart.add("Iced Drinks", points)

# Save outputs
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
