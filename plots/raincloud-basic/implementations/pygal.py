""" pyplots.ai
raincloud-basic: Basic Raincloud Plot
Library: pygal 3.1.0 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-25
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

# Custom style for 4800x2700 px canvas - scaled up for visibility
# Using very subtle grid lines (low alpha via lighter color)
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#999999",
    guide_stroke_color="#e8e8e8",  # Very light guide lines for subtle grid
    colors=tuple(group_colors * 3) + ("#222222",) * 30,
    title_font_size=96,
    label_font_size=60,
    major_label_font_size=54,
    legend_font_size=54,
    value_font_size=42,
    opacity=0.6,
    opacity_hover=0.8,
)

# Create VERTICAL XY chart for raincloud plot
# X-axis = Treatment Group (category), Y-axis = Reaction Time (value)
# For vertical orientation: cloud on RIGHT side, boxplot centered, rain on LEFT
# This follows the spec's guidance for vertical raincloud layout
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="raincloud-basic · pygal · pyplots.ai",
    x_title="Treatment Group",
    y_title="Reaction Time (ms)",
    show_legend=False,
    legend_at_bottom=False,
    legend_box_size=0,
    stroke=True,
    fill=True,
    dots_size=0,
    show_x_guides=True,
    show_y_guides=True,
    range=(100, 750),
    xrange=(0, 4),
    margin=80,
    explicit_size=True,
)

# Raincloud layout parameters (vertical orientation)
# CRITICAL: Cloud on RIGHT side, boxplot centered, rain on LEFT
# This creates the visual metaphor of rain falling from cloud
cloud_offset = 0.28  # Cloud extends to the RIGHT (positive X offset)
rain_offset = -0.32  # Rain falls to the LEFT (negative X offset)
n_kde_points = 80

# Pre-compute all raincloud components
cloud_data = []
rain_data = []
box_data = []

for i, (category, values) in enumerate(data.items()):
    center_x = i + 1  # X position for this group (1, 2, 3)
    values = np.array(values)

    # --- Half-Violin (cloud) - on RIGHT side of boxplot ---
    # Compute KDE using Silverman's rule
    n = len(values)
    std = np.std(values)
    iqr_val = np.percentile(values, 75) - np.percentile(values, 25)
    bandwidth = 0.9 * min(std, iqr_val / 1.34) * n ** (-0.2)

    # Create range of y values (reaction times) for density
    y_min, y_max = values.min(), values.max()
    padding = (y_max - y_min) * 0.1
    y_range = np.linspace(y_min - padding, y_max + padding, n_kde_points)

    # Gaussian kernel density estimation
    density = np.zeros_like(y_range)
    for v in values:
        density += np.exp(-0.5 * ((y_range - v) / bandwidth) ** 2)
    density /= n * bandwidth * np.sqrt(2 * np.pi)

    # Normalize density and place on RIGHT side (cloud)
    density = density / density.max() * cloud_offset

    # Create half-violin shape - cloud extends to right (higher X)
    cloud_points = [(center_x + d, y) for y, d in zip(y_range, density, strict=True)]
    # Close the shape along the center line
    cloud_points = [(center_x, y_range[0])] + cloud_points + [(center_x, y_range[-1]), (center_x, y_range[0])]
    cloud_data.append((category, cloud_points, group_colors[i]))

    # --- Jittered Points (rain) - on LEFT side (rain falls from cloud) ---
    np.random.seed(42 + i)
    jitter = np.random.uniform(-0.08, 0.08, len(values))
    rain_points = [(center_x + rain_offset + j, float(v)) for j, v in zip(jitter, values, strict=True)]
    rain_data.append((category, rain_points, group_colors[i]))

    # --- Box Plot (centered at group position) ---
    median = float(np.median(values))
    q1 = float(np.percentile(values, 25))
    q3 = float(np.percentile(values, 75))
    iqr = q3 - q1
    whisker_low = float(max(values.min(), q1 - 1.5 * iqr))
    whisker_high = float(min(values.max(), q3 + 1.5 * iqr))
    box_data.append((center_x, median, q1, q3, whisker_low, whisker_high, group_colors[i]))

# Add clouds (half-violins) - using empty string for label to suppress legend
for _category, cloud_points, _color in cloud_data:
    chart.add("", cloud_points, stroke=True, fill=True)

# Add rain points - increased dots_size for better visibility on 4800x2700 canvas
for _category, rain_points, _color in rain_data:
    chart.add("", rain_points, stroke=False, fill=False, dots_size=32)

# Add box plots - vertical boxes centered at each group
# Significantly increased line weights for 4800x2700 canvas
box_width = 0.10
cap_width = 0.06

for center_x, median, q1, q3, whisker_low, whisker_high, _color in box_data:
    # IQR box (vertical rectangle) - thick border for visibility
    quartile_box = [
        (center_x - box_width, q1),
        (center_x - box_width, q3),
        (center_x + box_width, q3),
        (center_x + box_width, q1),
        (center_x - box_width, q1),
    ]
    chart.add("", quartile_box, stroke=True, fill=False, show_dots=False, stroke_style={"width": 20})

    # Median line (horizontal line within box) - thickest for emphasis
    median_line = [(center_x - box_width * 1.3, median), (center_x + box_width * 1.3, median)]
    chart.add("", median_line, stroke=True, fill=False, show_dots=False, stroke_style={"width": 28})

    # Whiskers (vertical lines from box to caps)
    whisker_bottom = [(center_x, whisker_low), (center_x, q1)]
    whisker_top = [(center_x, q3), (center_x, whisker_high)]
    chart.add("", whisker_bottom, stroke=True, fill=False, show_dots=False, stroke_style={"width": 14})
    chart.add("", whisker_top, stroke=True, fill=False, show_dots=False, stroke_style={"width": 14})

    # Whisker caps (horizontal lines at ends)
    cap_bottom = [(center_x - cap_width, whisker_low), (center_x + cap_width, whisker_low)]
    cap_top = [(center_x - cap_width, whisker_high), (center_x + cap_width, whisker_high)]
    chart.add("", cap_bottom, stroke=True, fill=False, show_dots=False, stroke_style={"width": 14})
    chart.add("", cap_top, stroke=True, fill=False, show_dots=False, stroke_style={"width": 14})

# X-axis labels for treatment groups
chart.x_labels = [
    {"value": 0, "label": ""},
    {"value": 1, "label": "Control"},
    {"value": 2, "label": "Treatment A"},
    {"value": 3, "label": "Treatment B"},
    {"value": 4, "label": ""},
]

# Save outputs
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
