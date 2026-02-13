""" pyplots.ai
histogram-basic: Basic Histogram
Library: pygal 3.1.0 | Python 3.14.0
Quality: 72/100 | Created: 2025-12-23
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - Exam scores with slight right skew (realistic distribution)
np.random.seed(42)
raw = np.random.normal(loc=68, scale=12, size=500)
skew_shift = np.random.exponential(scale=4, size=500)
values = np.clip(raw + skew_shift, 0, 100)

# Compute histogram bins manually since pygal.Histogram expects (count, start, end) tuples
n_bins = 20
counts, bin_edges = np.histogram(values, bins=n_bins)
hist_data = [(int(count), float(bin_edges[i]), float(bin_edges[i + 1])) for i, count in enumerate(counts)]

# Custom style for 4800x2700 canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333",
    foreground_strong="#333",
    foreground_subtle="#ddd",
    colors=("#306998",),
    opacity=0.9,
    title_font_size=60,
    label_font_size=42,
    major_label_font_size=38,
    legend_font_size=36,
    value_font_size=32,
)

# Create histogram chart
chart = pygal.Histogram(
    width=4800,
    height=2700,
    style=custom_style,
    title="histogram-basic · pygal · pyplots.ai",
    x_title="Exam Score (points)",
    y_title="Number of Students",
    show_legend=False,
    show_y_guides=True,
    show_x_guides=False,
    tooltip_border_radius=6,
    value_formatter=lambda x: f"{x:.0f} students",
)

# Add histogram data
chart.add("Distribution", hist_data)

# Save outputs
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
