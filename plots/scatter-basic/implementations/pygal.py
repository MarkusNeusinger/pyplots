""" pyplots.ai
scatter-basic: Basic Scatter Plot
Library: pygal 3.1.0 | Python 3.14
Quality: 78/100 | Created: 2025-12-22
"""

import numpy as np
import pygal
from pygal.style import Style


# Data — study hours vs exam scores with realistic positive correlation (r~0.7)
np.random.seed(42)
n = 120
study_hours = np.random.uniform(2, 14, n)
exam_scores = study_hours * 4.5 + np.random.normal(0, 5.5, n) + 25
exam_scores = np.clip(exam_scores, 15, 100)

# Shared font family
font = "DejaVu Sans, Helvetica, Arial, sans-serif"

# Custom style for 4800x2700 px canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#e0e0e0",
    colors=("#306998",),
    font_family=font,
    title_font_family=font,
    title_font_size=56,
    label_font_size=42,
    major_label_font_size=38,
    legend_font_size=36,
    legend_font_family=font,
    value_font_size=30,
    tooltip_font_size=30,
    tooltip_font_family=font,
    opacity=0.7,
    opacity_hover=0.9,
)

# Create XY chart (stroke=False for scatter behavior)
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="scatter-basic · pygal · pyplots.ai",
    x_title="Study Hours per Week (hrs)",
    y_title="Exam Score (%)",
    show_legend=False,
    stroke=False,
    dots_size=14,
    show_x_guides=True,
    show_y_guides=True,
    x_value_formatter=lambda x: f"{x:.0f}",
    value_formatter=lambda y: f"{y:.0f}%",
    margin_bottom=80,
    margin_left=80,
    margin_right=60,
    margin_top=60,
)

# Add data as list of (x, y) tuples
points = [(float(h), float(s)) for h, s in zip(study_hours, exam_scores, strict=True)]
chart.add("Students", points)

# Save outputs
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
