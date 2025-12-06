"""
box-basic: Basic Box Plot
Library: pygal
"""

import numpy as np
import pygal
from pygal.style import Style


# Data
np.random.seed(42)
group_a = np.random.normal(50, 10, 50).tolist()
group_b = np.random.normal(60, 15, 50).tolist()
group_c = np.random.normal(45, 8, 50).tolist()
group_d = np.random.normal(70, 20, 50).tolist()

# Custom style using project palette
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#FFD43B", "#DC2626", "#059669", "#8B5CF6", "#F97316"),
    title_font_size=48,
    label_font_size=40,
    legend_font_size=36,
    value_font_size=32,
)

# Create box plot
chart = pygal.Box(
    width=4800,
    height=2700,
    title="Basic Box Plot",
    x_title="Group",
    y_title="Value",
    style=custom_style,
    show_legend=True,
    legend_at_bottom=True,
)

# Add data series
chart.add("A", group_a)
chart.add("B", group_b)
chart.add("C", group_c)
chart.add("D", group_d)

# Save
chart.render_to_png("plot.png")
