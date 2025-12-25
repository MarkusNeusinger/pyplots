""" pyplots.ai
raincloud-basic: Basic Raincloud Plot
Library: pygal 3.1.0 | Python 3.13.11
Quality: 72/100 | Created: 2025-12-25
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

# Group colors - distinct for each category (colorblind-safe)
group_colors = ["#306998", "#FFD43B", "#4CAF50"]

# Custom style for 4800x2700 px canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=tuple(group_colors * 3) + ("#222222",) * 30,
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=42,
    value_font_size=36,
    opacity=0.6,
    opacity_hover=0.8,
)

# Create HORIZONTAL XY chart for raincloud plot
# X-axis = Reaction Time (value), Y-axis = Treatment Group (category)
# This allows cloud ABOVE, boxplot centered, rain BELOW for each group
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="raincloud-basic · pygal · pyplots.ai",
    x_title="Reaction Time (ms)",
    y_title="Treatment Group",
    show_legend=True,
    legend_at_bottom=True,
    legend_box_size=30,
    truncate_legend=-1,
    stroke=True,
    fill=True,
    dots_size=0,
    show_x_guides=True,
    show_y_guides=True,
    xrange=(100, 750),
    range=(0, 4),
    margin=50,
    explicit_size=True,
)

# Raincloud layout parameters (horizontal orientation)
# CRITICAL: Cloud ABOVE boxplot, rain BELOW - like rain falling from cloud
# Y-axis: higher Y = cloud (top), lower Y = rain (bottom)
cloud_offset = 0.25  # Cloud extends ABOVE center (positive Y)
rain_offset = -0.30  # Rain falls BELOW center (negative Y)
n_kde_points = 80

# Pre-compute all raincloud components
cloud_data = []
rain_data = []
box_data = []

for i, (category, values) in enumerate(data.items()):
    center_y = i + 1  # Y position for this group (1, 2, 3)
    values = np.array(values)

    # --- Half-Violin (cloud) - ABOVE the boxplot ---
    # Compute KDE using Silverman's rule
    n = len(values)
    std = np.std(values)
    iqr_val = np.percentile(values, 75) - np.percentile(values, 25)
    bandwidth = 0.9 * min(std, iqr_val / 1.34) * n ** (-0.2)

    # Create range of x values (reaction times) for density
    x_min, x_max = values.min(), values.max()
    padding = (x_max - x_min) * 0.1
    x_range = np.linspace(x_min - padding, x_max + padding, n_kde_points)

    # Gaussian kernel density estimation
    density = np.zeros_like(x_range)
    for v in values:
        density += np.exp(-0.5 * ((x_range - v) / bandwidth) ** 2)
    density /= n * bandwidth * np.sqrt(2 * np.pi)

    # Normalize density and place ABOVE center (cloud on top)
    density = density / density.max() * cloud_offset

    # Create half-violin shape - cloud extends upward (higher Y)
    cloud_points = [(x, center_y + d) for x, d in zip(x_range, density, strict=True)]
    # Close the shape along the center line
    cloud_points = [(x_range[0], center_y)] + cloud_points + [(x_range[-1], center_y), (x_range[0], center_y)]
    cloud_data.append((category, cloud_points, group_colors[i]))

    # --- Jittered Points (rain) - BELOW the boxplot (rain falls from cloud) ---
    np.random.seed(42 + i)
    jitter = np.random.uniform(-0.08, 0.08, len(values))
    rain_points = [(float(v), center_y + rain_offset + j) for j, v in zip(jitter, values, strict=True)]
    rain_data.append((category, rain_points, group_colors[i]))

    # --- Box Plot (centered at group position) ---
    median = float(np.median(values))
    q1 = float(np.percentile(values, 25))
    q3 = float(np.percentile(values, 75))
    iqr = q3 - q1
    whisker_low = float(max(values.min(), q1 - 1.5 * iqr))
    whisker_high = float(min(values.max(), q3 + 1.5 * iqr))
    box_data.append((center_y, median, q1, q3, whisker_low, whisker_high, group_colors[i]))

# Add clouds (half-violins) with category labels for legend
for category, cloud_points, _color in cloud_data:
    chart.add(category, cloud_points, stroke=True, fill=True)

# Add rain points (no legend entry to avoid duplicates)
for _category, rain_points, _color in rain_data:
    chart.add(None, rain_points, stroke=False, fill=False, dots_size=14)

# Add box plots - horizontal boxes centered at each group
box_height = 0.08
cap_height = 0.04

for center_y, median, q1, q3, whisker_low, whisker_high, _color in box_data:
    # IQR box (horizontal rectangle)
    quartile_box = [
        (q1, center_y - box_height),
        (q1, center_y + box_height),
        (q3, center_y + box_height),
        (q3, center_y - box_height),
        (q1, center_y - box_height),
    ]
    chart.add(None, quartile_box, stroke=True, fill=False, show_dots=False, stroke_style={"width": 6})

    # Median line (vertical line within box)
    median_line = [(median, center_y - box_height * 1.3), (median, center_y + box_height * 1.3)]
    chart.add(None, median_line, stroke=True, fill=False, show_dots=False, stroke_style={"width": 10})

    # Whiskers (horizontal lines from box to caps)
    whisker_left = [(whisker_low, center_y), (q1, center_y)]
    whisker_right = [(q3, center_y), (whisker_high, center_y)]
    chart.add(None, whisker_left, stroke=True, fill=False, show_dots=False, stroke_style={"width": 5})
    chart.add(None, whisker_right, stroke=True, fill=False, show_dots=False, stroke_style={"width": 5})

    # Whisker caps (vertical lines at ends)
    cap_left = [(whisker_low, center_y - cap_height), (whisker_low, center_y + cap_height)]
    cap_right = [(whisker_high, center_y - cap_height), (whisker_high, center_y + cap_height)]
    chart.add(None, cap_left, stroke=True, fill=False, show_dots=False, stroke_style={"width": 5})
    chart.add(None, cap_right, stroke=True, fill=False, show_dots=False, stroke_style={"width": 5})

# Y-axis labels for treatment groups
chart.y_labels = [
    {"value": 0, "label": ""},
    {"value": 1, "label": "Control"},
    {"value": 2, "label": "Treatment A"},
    {"value": 3, "label": "Treatment B"},
    {"value": 4, "label": ""},
]

# Save outputs
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
