"""pyplots.ai
residual-basic: Residual Plot
Library: pygal | Python 3.13
Quality: pending | Created: 2025-12-25
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - Generate realistic regression residuals
np.random.seed(42)

# Simulate a regression scenario: predicted values and residuals
n_points = 100
fitted = np.linspace(10, 50, n_points) + np.random.randn(n_points) * 3

# Create residuals that show good model behavior (random scatter around zero)
# with slight heteroscedasticity to make it more realistic/interesting
residuals = np.random.randn(n_points) * (1 + 0.03 * (fitted - 30))

# Add a few outliers to demonstrate detection capability
outlier_indices = [15, 45, 78]
residuals[outlier_indices] = [8.5, -9.2, 7.8]

# Custom style for large canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#E74C3C"),  # Python Blue for points, Red for reference
    title_font_size=48,
    label_font_size=36,
    major_label_font_size=32,
    legend_font_size=32,
    value_font_size=28,
    stroke_width=3,
    opacity=0.6,
    opacity_hover=0.9,
)

# Create XY chart for scatter plot
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="residual-basic · pygal · pyplots.ai",
    x_title="Fitted Values",
    y_title="Residuals",
    show_legend=True,
    legend_at_bottom=False,
    legend_box_size=24,
    dots_size=8,
    stroke=False,  # No lines connecting points
    show_x_guides=False,
    show_y_guides=True,
    x_label_rotation=0,
    truncate_label=-1,
    explicit_size=True,
    print_values=False,
)

# Prepare data as list of tuples for XY chart
scatter_data = [(float(fitted[i]), float(residuals[i])) for i in range(n_points)]

# Add residual points
chart.add("Residuals", scatter_data)

# Add horizontal reference line at y=0
# Create a line from min to max of fitted values
x_min, x_max = float(np.min(fitted)) - 2, float(np.max(fitted)) + 2
chart.add(
    "Zero Reference",
    [(x_min, 0), (x_max, 0)],
    stroke=True,
    dots_size=0,
    stroke_style={"width": 4, "dasharray": "10, 5"},
)

# Save outputs
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
