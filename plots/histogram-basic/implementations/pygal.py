"""
histogram-basic: Basic Histogram
Library: pygal
"""

import numpy as np
import pygal
from pygal.style import Style


# Data
np.random.seed(42)
values = np.random.normal(100, 15, 500)  # 500 values, mean=100, std=15

# Calculate histogram bins
counts, bin_edges = np.histogram(values, bins=20)

# Convert to pygal histogram format: (height, start, end)
histogram_data = [(int(count), float(bin_edges[i]), float(bin_edges[i + 1])) for i, count in enumerate(counts)]

# Custom style matching default style guide colors
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    opacity="0.8",
    opacity_hover="0.9",
    colors=("#306998",),  # Python Blue
    guide_stroke_color="#cccccc",
    major_guide_stroke_color="#cccccc",
    title_font_size=48,
    label_font_size=36,
    major_label_font_size=36,
)

# Create histogram chart
chart = pygal.Histogram(
    width=4800,
    height=2700,
    title="Basic Histogram",
    x_title="Value",
    y_title="Frequency",
    style=custom_style,
    show_legend=False,
    show_y_guides=True,
    show_x_guides=False,
)

# Add histogram data
chart.add("Distribution", histogram_data)

# Save to PNG
chart.render_to_png("plot.png")
