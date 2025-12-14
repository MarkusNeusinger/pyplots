"""
violin-basic: Basic Violin Plot
Library: pygal
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - Generate distributions for different categories
np.random.seed(42)
categories = ["Engineering", "Marketing", "Sales", "Operations"]
data = {
    "Engineering": np.random.normal(85, 12, 200),
    "Marketing": np.random.normal(72, 15, 200),
    "Sales": np.random.normal(78, 20, 200),
    "Operations": np.random.normal(65, 10, 200),
}

# Custom style for 4800x2700 px canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#FFD43B", "#4CAF50", "#FF5722", "#666666", "#999999", "#333333", "#AAAAAA"),
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=36,
    value_font_size=36,
    opacity=0.7,
    opacity_hover=0.9,
)

# Create XY chart for violin plot
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="violin-basic · pygal · pyplots.ai",
    x_title="Category",
    y_title="Performance Score",
    show_legend=True,
    legend_at_bottom=True,
    stroke=True,
    fill=True,
    dots_size=0,
    show_x_guides=False,
    show_y_guides=True,
    range=(20, 130),
    xrange=(0, 6),
    margin=50,
)

# Parameters for violin shapes
violin_width = 0.4
n_points = 100

# Add violins for each category
for i, (category, values) in enumerate(data.items()):
    center_x = i + 1.5  # Space categories more

    # Compute KDE using Silverman's rule
    n = len(values)
    std = np.std(values)
    iqr = np.percentile(values, 75) - np.percentile(values, 25)
    bandwidth = 0.9 * min(std, iqr / 1.34) * n ** (-0.2)

    # Create range of y values for density
    y_min, y_max = values.min(), values.max()
    y_range = np.linspace(y_min - 5, y_max + 5, n_points)

    # Gaussian kernel density estimation
    density = np.zeros_like(y_range)
    for v in values:
        density += np.exp(-0.5 * ((y_range - v) / bandwidth) ** 2)
    density /= n * bandwidth * np.sqrt(2 * np.pi)

    # Normalize density to desired width
    density = density / density.max() * violin_width

    # Create violin shape points (mirrored density)
    # Left side (going up)
    left_points = [(center_x - d, y) for y, d in zip(y_range, density, strict=True)]
    # Right side (going down)
    right_points = [(center_x + d, y) for y, d in zip(y_range[::-1], density[::-1], strict=True)]
    # Close the shape
    violin_points = left_points + right_points + [left_points[0]]

    chart.add(category, violin_points)

    # Add median marker as separate small line
    median = float(np.median(values))
    q1 = float(np.percentile(values, 25))
    q3 = float(np.percentile(values, 75))
    box_width = 0.06

    # Quartile box (IQR)
    quartile_box = [
        (center_x - box_width, q1),
        (center_x - box_width, q3),
        (center_x + box_width, q3),
        (center_x + box_width, q1),
        (center_x - box_width, q1),
    ]
    chart.add(None, quartile_box, stroke=True, fill=False, show_dots=False)

    # Median line
    median_line = [(center_x - box_width * 1.5, median), (center_x + box_width * 1.5, median)]
    chart.add(None, median_line, stroke=True, fill=False, show_dots=False, stroke_style={"width": 4})

# Configure x-axis to show category names at violin positions
chart.x_labels = ["", "Engineering", "Marketing", "Sales", "Operations", ""]
chart.x_labels_major_count = 4

# Save outputs
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
