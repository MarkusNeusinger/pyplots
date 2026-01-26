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
    colors=("#3498DB", "#F39C12", "#E74C3C", "#27AE60", "#9B59B6", "#1ABC9C", "#E91E63"),
    title_font_size=48,
    label_font_size=32,
    major_label_font_size=28,
    legend_font_size=28,
    value_font_size=24,
    stroke_width=4,
    opacity=0.15,
    opacity_hover=0.25,
)

# Create XY chart for smooth curves
# Title includes the formula as annotation since pygal has limited text annotation support
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="curve-bias-variance-tradeoff · pygal · pyplots.ai\nTotal Error = Bias² + Variance + Irreducible Error",
    x_title="Model Complexity (Low → High)",
    y_title="Prediction Error",
    show_dots=False,
    stroke_style={"width": 5},
    show_x_guides=True,
    show_y_guides=True,
    legend_at_bottom=True,
    legend_box_size=24,
    truncate_legend=-1,
    x_label_rotation=0,
    range=(0, 4.5),
)

# Prepare data for XY chart (list of tuples)
bias_data = [(float(x), float(y)) for x, y in zip(complexity, bias_squared, strict=True)]
variance_data = [(float(x), float(y)) for x, y in zip(complexity, variance, strict=True)]
irreducible_data = [(float(x), float(y)) for x, y in zip(complexity, irreducible_error, strict=True)]
total_data = [(float(x), float(y)) for x, y in zip(complexity, total_error, strict=True)]

# Create shaded regions to indicate underfitting (left) and overfitting (right) zones
# Underfitting zone: from start to optimal point
underfitting_zone = [(0.5, 0), (0.5, 4.5), (optimal_complexity, 4.5), (optimal_complexity, 0)]
# Overfitting zone: from optimal point to end
overfitting_zone = [(optimal_complexity, 0), (optimal_complexity, 4.5), (10, 4.5), (10, 0)]

# Add shaded regions first (so curves are drawn on top)
chart.add(
    "← Underfitting (High Bias)", underfitting_zone, fill=True, stroke=False, show_dots=False, formatter=lambda x: ""
)
chart.add(
    "Overfitting (High Variance) →", overfitting_zone, fill=True, stroke=False, show_dots=False, formatter=lambda x: ""
)

# Add curves with distinct styles - labels describe behavior for direct identification
chart.add(
    "Bias² (decreases with complexity)", bias_data, stroke_style={"width": 6, "dasharray": "15, 8"}, show_dots=False
)
chart.add(
    "Variance (increases with complexity)",
    variance_data,
    stroke_style={"width": 6, "dasharray": "8, 4"},
    show_dots=False,
)
chart.add("Total Error (U-shaped minimum)", total_data, stroke_style={"width": 7}, show_dots=False)
chart.add(
    "Irreducible Error (constant noise floor)",
    irreducible_data,
    stroke_style={"width": 5, "dasharray": "3, 3"},
    show_dots=False,
)

# Add optimal point as a vertical line with prominent markers
# Create a vertical line at optimal complexity from bottom to the total error point
vertical_line = [(float(optimal_complexity), 0), (float(optimal_complexity), float(optimal_error))]
chart.add(
    f"★ Optimal Point (complexity = {optimal_complexity:.1f})",
    vertical_line,
    stroke_style={"width": 4, "dasharray": "5, 5"},
    show_dots=True,
    dots_size=12,
)

# Save outputs
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
