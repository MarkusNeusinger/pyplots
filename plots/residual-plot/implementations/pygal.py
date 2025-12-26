"""pyplots.ai
residual-plot: Residual Plot
Library: pygal | Python 3.13
Quality: pending | Created: 2025-12-26
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - Linear regression example with some non-linearity
np.random.seed(42)
n_points = 100

# Generate fitted values (x-axis)
fitted_values = np.linspace(10, 100, n_points)

# Generate residuals with slight heteroscedasticity and a few outliers
base_residuals = np.random.normal(0, 5, n_points)
# Add slight heteroscedasticity (variance increases with fitted values)
heteroscedasticity = (fitted_values / 100) * np.random.normal(0, 3, n_points)
residuals = base_residuals + heteroscedasticity

# Add a few outliers
outlier_indices = [15, 45, 78]
residuals[outlier_indices] = [25, -22, 28]

# Calculate standard deviation for reference bands
std_residuals = np.std(residuals)

# Identify outliers (beyond 2 standard deviations)
outlier_mask = np.abs(residuals) > 2 * std_residuals

# Custom style for 4800x2700 canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#E74C3C", "#888888"),  # Python Blue, red for outliers, gray for zero line
    title_font_size=60,
    label_font_size=44,
    major_label_font_size=40,
    legend_font_size=40,
    value_font_size=32,
    tooltip_font_size=32,
    stroke_width=3,
)

# Create XY scatter chart for residual plot
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="residual-plot · pygal · pyplots.ai",
    x_title="Fitted Values",
    y_title="Residuals",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=3,
    show_x_guides=True,
    show_y_guides=True,
    stroke=False,
    dots_size=18,
    truncate_legend=-1,
    x_label_rotation=0,
)

# Prepare data points - separate normal and outlier points
normal_points = [(float(fitted_values[i]), float(residuals[i])) for i in range(n_points) if not outlier_mask[i]]
outlier_points = [(float(fitted_values[i]), float(residuals[i])) for i in range(n_points) if outlier_mask[i]]

# Add data series
chart.add("Residuals", normal_points)
chart.add("Outliers (>2σ)", outlier_points)

# Add zero reference line (using Line chart overlay via XY with same points)
zero_line_points = [(float(fitted_values[0]), 0), (float(fitted_values[-1]), 0)]
chart.add(
    "Zero Reference", zero_line_points, stroke=True, show_dots=False, stroke_style={"width": 4, "dasharray": "15, 10"}
)

# Save as PNG and HTML
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
