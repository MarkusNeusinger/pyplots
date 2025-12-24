"""pyplots.ai
raincloud-basic: Basic Raincloud Plot
Library: pygal | Python 3.13
Quality: pending | Created: 2025-12-24
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - Reaction times (ms) for different treatment groups
np.random.seed(42)
data = {
    "Control": np.random.normal(450, 80, 60),
    "Treatment A": np.random.normal(380, 60, 55),
    "Treatment B": np.random.normal(320, 50, 50),
}

# Add some realistic variation and outliers
data["Control"] = np.append(data["Control"], [650, 680, 250])
data["Treatment A"] = np.append(data["Treatment A"], [550, 200])
data["Treatment B"] = np.append(data["Treatment B"], [480, 180])

# Custom style for 4800x2700 px canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#FFD43B", "#4CAF50", "#333333", "#666666", "#999999"),
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=42,
    value_font_size=36,
    opacity=0.7,
    opacity_hover=0.9,
)

# Create XY chart for raincloud plot
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="raincloud-basic · pygal · pyplots.ai",
    x_title="Treatment Group",
    y_title="Reaction Time (ms)",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=3,
    stroke=True,
    fill=True,
    dots_size=0,
    show_x_guides=False,
    show_y_guides=True,
    range=(100, 750),
    xrange=(0, 5),
    margin=50,
)

# Raincloud parameters
violin_width = 0.35
jitter_offset = 0.45
box_offset = 0.05
n_points = 80

# Process each category to create raincloud components
for i, (category, values) in enumerate(data.items()):
    center_x = i + 1.5
    values = np.array(values)

    # --- Half-Violin (cloud) - on the left side ---
    # Compute KDE using Silverman's rule
    n = len(values)
    std = np.std(values)
    iqr = np.percentile(values, 75) - np.percentile(values, 25)
    bandwidth = 0.9 * min(std, iqr / 1.34) * n ** (-0.2)

    # Create range of y values for density
    y_min, y_max = values.min(), values.max()
    padding = (y_max - y_min) * 0.1
    y_range = np.linspace(y_min - padding, y_max + padding, n_points)

    # Gaussian kernel density estimation
    density = np.zeros_like(y_range)
    for v in values:
        density += np.exp(-0.5 * ((y_range - v) / bandwidth) ** 2)
    density /= n * bandwidth * np.sqrt(2 * np.pi)

    # Normalize density to desired width
    density = density / density.max() * violin_width

    # Create half-violin shape (only left side - the "cloud")
    cloud_points = [(center_x - d, y) for y, d in zip(y_range, density, strict=True)]
    # Close the shape along the center line
    cloud_points = cloud_points + [(center_x, y_range[-1]), (center_x, y_range[0]), cloud_points[0]]

    chart.add(category, cloud_points)

# Add box plots and jittered points separately (without legend entries)
for i, (_category, values) in enumerate(data.items()):
    center_x = i + 1.5
    values = np.array(values)

    # --- Box Plot (center) ---
    median = float(np.median(values))
    q1 = float(np.percentile(values, 25))
    q3 = float(np.percentile(values, 75))
    iqr = q3 - q1
    whisker_low = float(max(values.min(), q1 - 1.5 * iqr))
    whisker_high = float(min(values.max(), q3 + 1.5 * iqr))

    box_width = 0.08

    # IQR box
    quartile_box = [
        (center_x + box_offset - box_width, q1),
        (center_x + box_offset - box_width, q3),
        (center_x + box_offset + box_width, q3),
        (center_x + box_offset + box_width, q1),
        (center_x + box_offset - box_width, q1),
    ]
    chart.add(None, quartile_box, stroke=True, fill=False, show_dots=False)

    # Median line
    median_line = [(center_x + box_offset - box_width * 1.2, median), (center_x + box_offset + box_width * 1.2, median)]
    chart.add(None, median_line, stroke=True, fill=False, show_dots=False, stroke_style={"width": 6})

    # Whiskers
    whisker_top = [(center_x + box_offset, q3), (center_x + box_offset, whisker_high)]
    whisker_bottom = [(center_x + box_offset, q1), (center_x + box_offset, whisker_low)]
    chart.add(None, whisker_top, stroke=True, fill=False, show_dots=False, stroke_style={"width": 3})
    chart.add(None, whisker_bottom, stroke=True, fill=False, show_dots=False, stroke_style={"width": 3})

    # Whisker caps
    cap_width = 0.04
    cap_top = [(center_x + box_offset - cap_width, whisker_high), (center_x + box_offset + cap_width, whisker_high)]
    cap_bottom = [(center_x + box_offset - cap_width, whisker_low), (center_x + box_offset + cap_width, whisker_low)]
    chart.add(None, cap_top, stroke=True, fill=False, show_dots=False, stroke_style={"width": 3})
    chart.add(None, cap_bottom, stroke=True, fill=False, show_dots=False, stroke_style={"width": 3})

    # --- Jittered Points (rain) - on the right side ---
    np.random.seed(42 + i)  # Consistent jitter per group
    jitter = np.random.uniform(-0.08, 0.08, len(values))
    rain_points = [(center_x + jitter_offset + j, float(v)) for j, v in zip(jitter, values, strict=True)]

    # Add points with smaller dots and transparency
    chart.add(None, rain_points, stroke=False, fill=False, dots_size=8)

# X-axis labels at category positions
chart.x_labels = ["", "Control", "Treatment A", "Treatment B", ""]
chart.x_labels_major_count = 3

# Save outputs
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
