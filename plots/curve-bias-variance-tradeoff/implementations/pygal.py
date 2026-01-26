"""pyplots.ai
curve-bias-variance-tradeoff: Bias-Variance Tradeoff Curve
Library: pygal 3.1.0 | Python 3.13.11
Quality: 82/100 | Created: 2026-01-26
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

# Custom style for pyplots with distinct colors for each series
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333",
    foreground_strong="#333",
    foreground_subtle="#666",
    colors=("#3498DB", "#F39C12", "#E74C3C", "#27AE60", "#9B59B6"),
    title_font_size=56,
    label_font_size=36,
    major_label_font_size=32,
    legend_font_size=32,
    value_font_size=28,
    stroke_width=5,
)

# Create XY chart for smooth curves
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="curve-bias-variance-tradeoff · pygal · pyplots.ai",
    x_title="Model Complexity (Low → High)",
    y_title="Prediction Error  |  Total = Bias² + Variance + Irreducible",
    show_dots=False,
    stroke_style={"width": 6},
    show_x_guides=True,
    show_y_guides=True,
    legend_at_bottom=True,
    legend_box_size=28,
    truncate_legend=-1,
    range=(0, 4.5),
    xrange=(0, 11),
)

# Prepare data for XY chart (list of tuples)
bias_data = [(float(x), float(y)) for x, y in zip(complexity, bias_squared, strict=True)]
variance_data = [(float(x), float(y)) for x, y in zip(complexity, variance, strict=True)]
irreducible_data = [(float(x), float(y)) for x, y in zip(complexity, irreducible_error, strict=True)]
total_data = [(float(x), float(y)) for x, y in zip(complexity, total_error, strict=True)]

# Add curves with distinct styles and concise legend labels
chart.add("Bias²", bias_data, stroke_style={"width": 7, "dasharray": "20, 10"}, show_dots=False)
chart.add("Variance", variance_data, stroke_style={"width": 7, "dasharray": "10, 5"}, show_dots=False)
chart.add("Total Error", total_data, stroke_style={"width": 8}, show_dots=False)
chart.add("Irreducible Error", irreducible_data, stroke_style={"width": 6, "dasharray": "4, 4"}, show_dots=False)

# Add optimal point marker - a single prominent point at the minimum
optimal_point = [(float(optimal_complexity), float(optimal_error))]
chart.add(f"Optimal (x={optimal_complexity:.1f})", optimal_point, show_dots=True, dots_size=20, stroke=False)

# Save as PNG only
chart.render_to_png("plot.png")
