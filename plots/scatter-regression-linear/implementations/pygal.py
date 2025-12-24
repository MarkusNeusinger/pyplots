""" pyplots.ai
scatter-regression-linear: Scatter Plot with Linear Regression
Library: pygal 3.1.0 | Python 3.13.11
Quality: 78/100 | Created: 2025-12-24
"""

import numpy as np
import pygal
from pygal.style import Style
from scipy import stats


# Data - Study hours vs exam scores
np.random.seed(42)
n_points = 80
x = np.random.uniform(1, 10, n_points)
y = 45 + 5 * x + np.random.normal(0, 8, n_points)

# Calculate linear regression
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
r_squared = r_value**2

# Generate regression line points
x_line = np.linspace(min(x), max(x), 100)
y_line = slope * x_line + intercept

# Calculate confidence interval (95%)
n = len(x)
x_mean = np.mean(x)
se_y = np.sqrt(np.sum((y - (slope * x + intercept)) ** 2) / (n - 2))
t_val = stats.t.ppf(0.975, n - 2)
se_line = se_y * np.sqrt(1 / n + (x_line - x_mean) ** 2 / np.sum((x - x_mean) ** 2))
ci_upper = y_line + t_val * se_line
ci_lower = y_line - t_val * se_line

# Style for 4800x2700 px canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#FFD43B", "#306998"),
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=42,
    value_font_size=36,
    stroke_width=5,
    opacity=0.7,
    opacity_hover=0.9,
)

# Create XY scatter chart
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="scatter-regression-linear · pygal · pyplots.ai",
    x_title="Study Hours",
    y_title="Exam Score",
    show_legend=True,
    legend_at_bottom=False,
    legend_box_size=36,
    dots_size=12,
    stroke=False,
    show_x_guides=True,
    show_y_guides=True,
    truncate_legend=-1,
)

# Add scatter points
scatter_data = [{"value": (float(x[i]), float(y[i])), "label": ""} for i in range(n_points)]
chart.add("Data Points", scatter_data, dots_size=12, stroke=False)

# Add regression line
line_data = [(float(x_line[i]), float(y_line[i])) for i in range(len(x_line))]
chart.add(f"Regression (R² = {r_squared:.3f})", line_data, stroke=True, show_dots=False, stroke_style={"width": 6})

# Add confidence interval bounds (upper and lower)
ci_upper_data = [(float(x_line[i]), float(ci_upper[i])) for i in range(0, len(x_line), 5)]
ci_lower_data = [(float(x_line[i]), float(ci_lower[i])) for i in range(0, len(x_line), 5)]

chart.add("95% CI Upper", ci_upper_data, stroke=True, show_dots=False, stroke_style={"width": 3, "dasharray": "10,5"})
chart.add("95% CI Lower", ci_lower_data, stroke=True, show_dots=False, stroke_style={"width": 3, "dasharray": "10,5"})

# Render to PNG and HTML
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
