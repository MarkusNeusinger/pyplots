"""pyplots.ai
curve-bias-variance-tradeoff: Bias-Variance Tradeoff Curve
Library: pygal | Python 3.13
Quality: pending | Created: 2025-01-26
"""

import numpy as np
import pygal
from pygal.style import Style


# Data: Generate theoretical bias-variance tradeoff curves
np.random.seed(42)
complexity = np.linspace(0.5, 10, 100)

# Bias squared: decreases with complexity (high bias at low complexity)
bias_squared = 4.0 / (1 + 0.8 * complexity)

# Variance: increases with complexity (high variance at high complexity)
variance = 0.1 * complexity**1.5

# Irreducible error: constant noise floor
irreducible_error = np.full_like(complexity, 0.5)

# Total error: sum of all components
total_error = bias_squared + variance + irreducible_error

# Find optimal complexity point (minimum total error)
optimal_idx = np.argmin(total_error)
optimal_complexity = complexity[optimal_idx]
optimal_error = total_error[optimal_idx]

# Custom style for pyplots
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333",
    foreground_strong="#333",
    foreground_subtle="#666",
    colors=("#306998", "#FFD43B", "#E74C3C", "#27AE60", "#8E44AD"),
    title_font_size=48,
    label_font_size=32,
    major_label_font_size=28,
    legend_font_size=28,
    value_font_size=24,
    stroke_width=4,
)

# Create XY chart for smooth curves
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="curve-bias-variance-tradeoff \u00b7 pygal \u00b7 pyplots.ai",
    x_title="Model Complexity",
    y_title="Prediction Error",
    show_dots=False,
    stroke_style={"width": 5},
    show_x_guides=True,
    show_y_guides=True,
    legend_at_bottom=True,
    legend_box_size=24,
    truncate_legend=-1,
)

# Prepare data for XY chart (list of tuples)
bias_data = [(float(x), float(y)) for x, y in zip(complexity, bias_squared, strict=True)]
variance_data = [(float(x), float(y)) for x, y in zip(complexity, variance, strict=True)]
irreducible_data = [(float(x), float(y)) for x, y in zip(complexity, irreducible_error, strict=True)]
total_data = [(float(x), float(y)) for x, y in zip(complexity, total_error, strict=True)]

# Add curves
chart.add("Bias\u00b2", bias_data, stroke_style={"width": 5, "dasharray": "10, 5"})
chart.add("Variance", variance_data, stroke_style={"width": 5, "dasharray": "5, 3"})
chart.add("Total Error", total_data, stroke_style={"width": 6})
chart.add("Irreducible Error", irreducible_data, stroke_style={"width": 4, "dasharray": "2, 2"})

# Add optimal point marker (larger dot for visibility)
chart.add(
    f"Optimal (complexity={optimal_complexity:.1f})",
    [(float(optimal_complexity), float(optimal_error))],
    dots_size=20,
    stroke=False,
)

# Save outputs
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
