"""pyplots.ai
violin-box: Violin Plot with Embedded Box Plot
Library: pygal | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - Generate distributions for different categories
np.random.seed(42)
data = {
    "Engineering": np.random.normal(85, 12, 200),
    "Marketing": np.random.normal(72, 18, 200),
    "Sales": np.random.normal(78, 22, 200),
    "Operations": np.random.normal(65, 10, 200),
}

# Custom style for 4800x2700 px canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#FFD43B", "#4CAF50", "#FF5722", "#666666", "#999999", "#333333"),
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=36,
    value_font_size=36,
    opacity=0.6,
    opacity_hover=0.8,
)

# Create XY chart for violin plot with embedded box
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="violin-box · pygal · pyplots.ai",
    x_title="Department",
    y_title="Performance Score",
    show_legend=True,
    legend_at_bottom=True,
    stroke=True,
    fill=True,
    dots_size=0,
    show_x_guides=False,
    show_y_guides=True,
    range=(0, 140),
    xrange=(0, 6),
    margin=50,
)

# Parameters for violin shapes
violin_width = 0.35
n_points = 100

# Add violins with embedded box plots for each category
for i, (category, values) in enumerate(data.items()):
    center_x = i + 1.5

    # Compute KDE using Silverman's rule
    n = len(values)
    std = np.std(values)
    iqr = np.percentile(values, 75) - np.percentile(values, 25)
    bandwidth = 0.9 * min(std, iqr / 1.34) * n ** (-0.2)

    # Create range of y values for density
    y_min, y_max = values.min(), values.max()
    y_range = np.linspace(y_min - 10, y_max + 10, n_points)

    # Gaussian kernel density estimation
    density = np.zeros_like(y_range)
    for v in values:
        density += np.exp(-0.5 * ((y_range - v) / bandwidth) ** 2)
    density /= n * bandwidth * np.sqrt(2 * np.pi)

    # Normalize density to desired width
    density = density / density.max() * violin_width

    # Create violin shape (mirrored density)
    left_points = [(center_x - d, y) for y, d in zip(y_range, density, strict=True)]
    right_points = [(center_x + d, y) for y, d in zip(y_range[::-1], density[::-1], strict=True)]
    violin_points = left_points + right_points + [left_points[0]]

    chart.add(category, violin_points)

    # Calculate box plot statistics
    median = float(np.median(values))
    q1 = float(np.percentile(values, 25))
    q3 = float(np.percentile(values, 75))
    iqr_val = q3 - q1

    # Whiskers: 1.5 * IQR or data min/max
    lower_whisker = max(values.min(), q1 - 1.5 * iqr_val)
    upper_whisker = min(values.max(), q3 + 1.5 * iqr_val)

    # Identify outliers
    outliers = values[(values < lower_whisker) | (values > upper_whisker)]

    box_width = 0.08

    # Quartile box (IQR) - white filled for contrast
    quartile_box = [
        (center_x - box_width, q1),
        (center_x - box_width, q3),
        (center_x + box_width, q3),
        (center_x + box_width, q1),
        (center_x - box_width, q1),
    ]
    chart.add(None, quartile_box, stroke=True, fill=True, show_dots=False, stroke_style={"width": 3})

    # Whisker lines (vertical lines from box to whisker ends)
    lower_whisker_line = [(center_x, q1), (center_x, lower_whisker)]
    upper_whisker_line = [(center_x, q3), (center_x, upper_whisker)]
    chart.add(None, lower_whisker_line, stroke=True, fill=False, show_dots=False, stroke_style={"width": 3})
    chart.add(None, upper_whisker_line, stroke=True, fill=False, show_dots=False, stroke_style={"width": 3})

    # Whisker caps (horizontal lines at ends)
    cap_width = box_width * 0.8
    lower_cap = [(center_x - cap_width, lower_whisker), (center_x + cap_width, lower_whisker)]
    upper_cap = [(center_x - cap_width, upper_whisker), (center_x + cap_width, upper_whisker)]
    chart.add(None, lower_cap, stroke=True, fill=False, show_dots=False, stroke_style={"width": 3})
    chart.add(None, upper_cap, stroke=True, fill=False, show_dots=False, stroke_style={"width": 3})

    # Median line (thicker, contrasting)
    median_line = [(center_x - box_width * 1.2, median), (center_x + box_width * 1.2, median)]
    chart.add(None, median_line, stroke=True, fill=False, show_dots=False, stroke_style={"width": 5})

    # Outliers as points
    if len(outliers) > 0:
        outlier_points = [(center_x, float(o)) for o in outliers]
        chart.add(None, outlier_points, stroke=False, fill=False, show_dots=True, dots_size=8)

# X-axis labels at violin positions
chart.x_labels = ["", "Engineering", "Marketing", "Sales", "Operations", ""]
chart.x_labels_major_count = 4

# Save outputs
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
