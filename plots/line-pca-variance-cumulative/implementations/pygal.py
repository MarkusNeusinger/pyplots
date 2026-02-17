""" pyplots.ai
line-pca-variance-cumulative: Cumulative Explained Variance for PCA Component Selection
Library: pygal 3.1.0 | Python 3.14.3
Quality: 75/100 | Created: 2026-02-17
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - Realistic PCA variance ratios for a 13-feature dataset (Wine-like)
eigenvalues = np.array([4.73, 2.51, 1.45, 0.92, 0.85, 0.64, 0.55, 0.35, 0.29, 0.21, 0.17, 0.13, 0.08])
explained_variance_ratio = eigenvalues / eigenvalues.sum()
cumulative_variance = np.cumsum(explained_variance_ratio) * 100
n_components = len(cumulative_variance)
component_labels = [str(i) for i in range(1, n_components + 1)]

# Custom style
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333",
    foreground_strong="#333",
    foreground_subtle="#E0E0E0",
    colors=("#306998", "#D35400", "#27AE60"),
    opacity=1.0,
    opacity_hover=1.0,
    stroke_opacity=1.0,
    stroke_opacity_hover=1.0,
    stroke_width=6,
    stroke_width_hover=8,
    dot_opacity=1.0,
    title_font_size=64,
    label_font_size=44,
    major_label_font_size=40,
    legend_font_size=40,
    value_font_size=34,
    tooltip_font_size=32,
    title_font_family="sans-serif",
    label_font_family="sans-serif",
    value_font_family="sans-serif",
)

# Chart
chart = pygal.Line(
    width=4800,
    height=2700,
    title="line-pca-variance-cumulative · pygal · pyplots.ai",
    x_title="Number of Components",
    y_title="Cumulative Explained Variance (%)",
    style=custom_style,
    show_dots=True,
    dots_size=8,
    show_y_guides=True,
    show_x_guides=False,
    legend_at_bottom=True,
    truncate_legend=-1,
    range=(0, 105),
    margin=30,
    margin_bottom=100,
    y_labels_major_every=1,
    show_minor_y_labels=False,
    stroke_style={"width": 6},
)

# X-axis and Y-axis labels
chart.x_labels = component_labels
chart.y_labels = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 100]

# Cumulative variance line
chart.add("Cumulative Variance", [round(v, 1) for v in cumulative_variance], stroke_style={"width": 6})

# 90% threshold line (dashed)
chart.add("90% Threshold", [90] * n_components, show_dots=False, stroke_style={"width": 4, "dasharray": "20, 10"})

# 95% threshold line (dashed)
chart.add("95% Threshold", [95] * n_components, show_dots=False, stroke_style={"width": 4, "dasharray": "20, 10"})

# Save
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
