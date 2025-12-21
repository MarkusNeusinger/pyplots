""" pyplots.ai
bubble-basic: Basic Bubble Chart
Library: pygal 3.1.0 | Python 3.13.11
Quality: 88/100 | Created: 2025-12-14
"""

import numpy as np
import pygal
from pygal.style import Style


# Data
np.random.seed(42)
n_points = 30

x = np.random.randn(n_points) * 2 + 10
y = x * 0.7 + np.random.randn(n_points) * 2 + 5
size = np.abs(np.random.randn(n_points) * 50 + 100)

# Normalize sizes for bubble display (scale to reasonable range for pygal)
size_min, size_max = size.min(), size.max()
size_normalized = 20 + (size - size_min) / (size_max - size_min) * 80

# Bin bubbles by size for pygal (doesn't support per-point size)
small = [(x[i], y[i]) for i in range(n_points) if size_normalized[i] < 50]
medium = [(x[i], y[i]) for i in range(n_points) if 50 <= size_normalized[i] < 75]
large = [(x[i], y[i]) for i in range(n_points) if size_normalized[i] >= 75]

# Custom style for 4800x2700 px canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#4a8cc2", "#6ba3d6"),
    opacity=0.6,
    opacity_hover=0.8,
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=42,
    value_font_size=36,
    tooltip_font_size=36,
)

# Create XY chart for bubble visualization
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="bubble-basic · pygal · pyplots.ai",
    x_title="X Value",
    y_title="Y Value",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=3,
    stroke=False,
    dots_size=20,
    show_x_guides=True,
    show_y_guides=True,
)

# Add series with different dot sizes for bubble effect
chart.add("Small (Size < 50)", small, dots_size=20)
chart.add("Medium (50 ≤ Size < 75)", medium, dots_size=35)
chart.add("Large (Size ≥ 75)", large, dots_size=50)

# Save outputs
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
