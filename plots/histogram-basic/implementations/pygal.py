""" pyplots.ai
histogram-basic: Basic Histogram
Library: pygal 3.1.0 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-23
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - Exam scores with realistic distribution
np.random.seed(42)
values = np.random.normal(loc=72, scale=14, size=500)
values = np.clip(values, 0, 100)  # Exam scores between 0-100

# Compute histogram bins manually since pygal.Histogram expects bin data
n_bins = 20
counts, bin_edges = np.histogram(values, bins=n_bins)

# Prepare data for pygal.Histogram: list of (count, start, end) tuples
hist_data = [(int(count), float(bin_edges[i]), float(bin_edges[i + 1])) for i, count in enumerate(counts)]

# Custom style for 4800x2700 canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333",
    foreground_strong="#333",
    foreground_subtle="#666",
    colors=("#306998",),
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
)

# Add histogram data
chart.add("Distribution", hist_data)

# Save outputs
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
