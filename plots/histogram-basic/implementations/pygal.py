""" pyplots.ai
histogram-basic: Basic Histogram
Library: pygal 3.1.0 | Python 3.14.0
Quality: 81/100 | Created: 2025-12-23
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - Exam scores with visible right skew (realistic distribution)
np.random.seed(42)
base = np.random.normal(loc=64, scale=10, size=500)
skew = np.random.exponential(scale=7, size=500)
values = np.clip(base + skew, 0, 100)

# Compute histogram bins
n_bins = 25
counts, bin_edges = np.histogram(values, bins=n_bins)
hist_data = [(int(count), float(bin_edges[i]), float(bin_edges[i + 1])) for i, count in enumerate(counts)]

# Key statistics for storytelling
mean_val = float(np.mean(values))
q1, q3 = float(np.percentile(values, 25)), float(np.percentile(values, 75))

# Custom style — refined typography, subtle grid, polished chrome
custom_style = Style(
    background="white",
    plot_background="#fafafa",
    foreground="#2d2d2d",
    foreground_strong="#2d2d2d",
    foreground_subtle="#e8e8e8",
    colors=("#306998", "#d35400", "#27ae60"),
    font_family="DejaVu Sans, Helvetica, Arial, sans-serif",
    title_font_family="DejaVu Sans, Helvetica, Arial, sans-serif",
    title_font_size=56,
    label_font_size=40,
    major_label_font_size=36,
    legend_font_size=32,
    legend_font_family="DejaVu Sans, Helvetica, Arial, sans-serif",
    label_font_family="DejaVu Sans, Helvetica, Arial, sans-serif",
    major_label_font_family="DejaVu Sans, Helvetica, Arial, sans-serif",
    value_font_size=30,
    value_font_family="DejaVu Sans, Helvetica, Arial, sans-serif",
    opacity=0.82,
    opacity_hover=0.95,
    guide_stroke_color="#e0e0e0",
    guide_stroke_dasharray="4,4",
    major_guide_stroke_color="#d0d0d0",
    major_guide_stroke_dasharray="6,3",
    stroke_opacity=1.0,
    tooltip_font_size=28,
    tooltip_font_family="DejaVu Sans, Helvetica, Arial, sans-serif",
    tooltip_border_radius=10,
)

# Create histogram chart with refined layout and margins
chart = pygal.Histogram(
    width=4800,
    height=2700,
    style=custom_style,
    title="histogram-basic · pygal · pyplots.ai",
    x_title="Exam Score (points)",
    y_title="Number of Students",
    show_legend=True,
    legend_at_bottom=True,
    legend_box_size=24,
    show_y_guides=True,
    show_x_guides=False,
    value_formatter=lambda x: f"{x:,.0f}",
    tooltip_border_radius=10,
    tooltip_fancy_mode=True,
    min_scale=4,
    max_scale=8,
    margin_bottom=120,
    margin_left=80,
    margin_right=60,
    margin_top=60,
    spacing=12,
    print_values=False,
)

# Main histogram series
chart.add("Score Distribution (n=500)", hist_data)

# Mean marker — tall narrow bar as vertical reference line (pygal Histogram pattern)
marker_h = int(max(counts))
chart.add(f"Mean: {mean_val:.1f} pts", [(marker_h, mean_val - 0.4, mean_val + 0.4)], stroke_style={"width": 3})

# Interquartile range (IQR) — low shaded band shows central 50% of scores
iqr_height = int(max(counts) * 0.12)
chart.add(f"IQR: {q1:.0f}\u2013{q3:.0f} pts (middle 50%)", [(iqr_height, q1, q3)], stroke_style={"width": 2})

# Save outputs
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
