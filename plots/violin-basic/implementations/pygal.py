""" pyplots.ai
violin-basic: Basic Violin Plot
Library: pygal 3.1.0 | Python 3.14.3
Quality: 80/100 | Updated: 2026-02-21
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - Test scores across 4 class groups with distinct distribution shapes
np.random.seed(42)
data = {
    "Honors": np.clip(np.random.normal(88, 6, 200), 50, 100),
    "Standard": np.clip(np.random.normal(74, 10, 200), 40, 100),
    "Remedial": np.clip(np.random.normal(62, 8, 200), 30, 100),
    "Advanced": np.clip(np.random.normal(82, 14, 200), 45, 100),
}

# Colors: each violin gets 3 series (fill, IQR box, median line)
# Palette cycles per series, so position matters
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#cccccc",
    colors=(
        "#306998",
        "#1a1a1a",
        "#1a1a1a",
        "#E8875B",
        "#1a1a1a",
        "#1a1a1a",
        "#5BA37E",
        "#1a1a1a",
        "#1a1a1a",
        "#C4A23D",
        "#1a1a1a",
        "#1a1a1a",
    ),
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=36,
    value_font_size=36,
    opacity=0.75,
    opacity_hover=0.9,
)

# Create XY chart for violin plot (pygal has no native violin)
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="violin-basic · pygal · pyplots.ai",
    x_title="Class Group",
    y_title="Test Score",
    show_legend=False,
    stroke=True,
    fill=True,
    dots_size=0,
    show_x_guides=False,
    show_y_guides=True,
    range=(30, 105),
    xrange=(0, 5.5),
    margin=50,
)

# Violin shape parameters
violin_width = 0.4
n_points = 100

# Build violins with quartile markers and median lines
for i, (category, values) in enumerate(data.items()):
    center_x = i + 1.25

    # KDE using Silverman's rule
    n = len(values)
    std = np.std(values)
    iqr = np.percentile(values, 75) - np.percentile(values, 25)
    bandwidth = 0.9 * min(std, iqr / 1.34) * n ** (-0.2)

    # Y values for density estimation
    y_min, y_max = values.min(), values.max()
    y_range = np.linspace(y_min - 3, y_max + 3, n_points)

    # Gaussian kernel density estimation
    density = np.zeros_like(y_range)
    for v in values:
        density += np.exp(-0.5 * ((y_range - v) / bandwidth) ** 2)
    density /= n * bandwidth * np.sqrt(2 * np.pi)

    # Normalize density to desired width
    density = density / density.max() * violin_width

    # Mirrored violin shape
    left_points = [(center_x - d, y) for y, d in zip(y_range, density, strict=True)]
    right_points = [(center_x + d, y) for y, d in zip(y_range[::-1], density[::-1], strict=True)]
    violin_points = left_points + right_points + [left_points[0]]
    chart.add(category, violin_points)

    # Quartile markers and median
    median = float(np.median(values))
    q1 = float(np.percentile(values, 25))
    q3 = float(np.percentile(values, 75))
    box_w = 0.15

    # IQR box — filled dark for strong contrast
    quartile_box = [
        (center_x - box_w, q1),
        (center_x - box_w, q3),
        (center_x + box_w, q3),
        (center_x + box_w, q1),
        (center_x - box_w, q1),
    ]
    chart.add(None, quartile_box, stroke=True, fill=True, show_dots=False, stroke_style={"width": 3})

    # Median line — thick dark stroke
    median_line = [(center_x - box_w * 1.3, median), (center_x + box_w * 1.3, median)]
    chart.add(None, median_line, stroke=True, fill=False, show_dots=False, stroke_style={"width": 8})

# X-axis labels at violin positions
chart.x_labels = ["", "Honors", "Standard", "Remedial", "Advanced", ""]
chart.x_labels_major_count = 4

# Save
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
