"""pyplots.ai
scatter-regression-lowess: Scatter Plot with LOWESS Regression
Library: pygal | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import numpy as np
import pygal
from pygal.style import Style
from statsmodels.nonparametric.smoothers_lowess import lowess


# Data - Generate non-linear pattern with varying trend
np.random.seed(42)
n_points = 150
x = np.linspace(0, 10, n_points)
# Create a complex non-linear pattern: sine wave + quadratic trend + noise
y = 3 * np.sin(x * 0.8) + 0.3 * x**1.5 + np.random.normal(0, 1.2, n_points)

# Calculate LOWESS smoothed curve
lowess_result = lowess(y, x, frac=0.35, return_sorted=True)
x_smooth = lowess_result[:, 0]
y_smooth = lowess_result[:, 1]

# Custom style for large canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#FFD43B", "#E74C3C"),
    title_font_size=48,
    label_font_size=36,
    major_label_font_size=28,
    legend_font_size=28,
    value_font_size=24,
    stroke_width=5,
    opacity=0.6,
    opacity_hover=0.9,
)

# Create XY chart for scatter plot
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="scatter-regression-lowess · pygal · pyplots.ai",
    x_title="X Value",
    y_title="Y Value",
    show_dots=True,
    dots_size=8,
    stroke=False,
    show_x_guides=True,
    show_y_guides=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=2,
)

# Add scatter points (as XY data with no stroke)
scatter_data = list(zip(x, y, strict=True))
chart.add("Data Points", scatter_data, stroke=False, dots_size=10)

# Add LOWESS curve (as line with no dots)
lowess_data = list(zip(x_smooth, y_smooth, strict=True))
chart.add("LOWESS Curve (frac=0.35)", lowess_data, stroke=True, show_dots=False, stroke_style={"width": 6})

# Save as PNG and SVG/HTML
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
