"""pyplots.ai
raincloud-basic: Basic Raincloud Plot
Library: pygal | Python 3.13
Quality: pending | Created: 2025-12-25
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

# Group colors - distinct for each category
group_colors = ["#306998", "#FFD43B", "#4CAF50"]

# Custom style for 4800x2700 px canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=tuple(group_colors * 3) + ("#222222",) * 20,  # Repeat colors, box elements dark
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=42,
    value_font_size=36,
    opacity=0.6,
    opacity_hover=0.8,
)

# Create XY chart for raincloud plot
# Use explicit_size=True and truncate_legend=-1 to force legend rendering
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="raincloud-basic · pygal · pyplots.ai",
    x_title="Treatment Group",
    y_title="Reaction Time (ms)",
    show_legend=True,
    legend_at_bottom=True,
    legend_box_size=30,
    truncate_legend=-1,  # Don't truncate legend entries
    stroke=True,
    fill=True,
    dots_size=0,
    show_x_guides=False,
    show_y_guides=True,
    range=(100, 750),
    xrange=(0, 5),
    margin=50,
    explicit_size=True,
)

# Raincloud layout parameters
# CRITICAL: Rain must fall BELOW cloud per specification
# Layout (top to bottom for each group): cloud (half-violin) -> boxplot -> rain points
cloud_height = 0.30  # Height for half-violin (above center)
box_offset = 0.0  # Boxplot at center line
rain_offset = -0.40  # Rain falls below center (negative = below)
n_points = 80

# Pre-compute all raincloud components
cloud_data = []
rain_data = []
box_data = []

for i, (category, values) in enumerate(data.items()):
    center_x = i + 1.5
    values = np.array(values)

    # --- Half-Violin (cloud) - ABOVE the center ---
    # Compute KDE using Silverman's rule
    n = len(values)
    std = np.std(values)
    iqr_val = np.percentile(values, 75) - np.percentile(values, 25)
    bandwidth = 0.9 * min(std, iqr_val / 1.34) * n ** (-0.2)

    # Create range of y values for density
    y_min, y_max = values.min(), values.max()
    padding = (y_max - y_min) * 0.1
    y_range = np.linspace(y_min - padding, y_max + padding, n_points)

    # Gaussian kernel density estimation
    density = np.zeros_like(y_range)
    for v in values:
        density += np.exp(-0.5 * ((y_range - v) / bandwidth) ** 2)
    density /= n * bandwidth * np.sqrt(2 * np.pi)

    # Normalize density to desired height and place ABOVE center (positive offset)
    density = density / density.max() * cloud_height

    # Create half-violin shape on TOP (cloud above boxplot)
    cloud_points = [(center_x + d, y) for y, d in zip(y_range, density, strict=True)]
    # Close the shape along the center line
    cloud_points = [(center_x, y_range[0])] + cloud_points + [(center_x, y_range[-1]), (center_x, y_range[0])]
    cloud_data.append((category, cloud_points, group_colors[i]))

    # --- Jittered Points (rain) - BELOW the center (rain falls from cloud) ---
    np.random.seed(42 + i)  # Consistent jitter per group
    jitter = np.random.uniform(-0.06, 0.06, len(values))
    rain_points = [(center_x + rain_offset + j, float(v)) for j, v in zip(jitter, values, strict=True)]
    rain_data.append((category, rain_points, group_colors[i]))

    # --- Box Plot (center) ---
    median = float(np.median(values))
    q1 = float(np.percentile(values, 25))
    q3 = float(np.percentile(values, 75))
    iqr = q3 - q1
    whisker_low = float(max(values.min(), q1 - 1.5 * iqr))
    whisker_high = float(min(values.max(), q3 + 1.5 * iqr))
    box_data.append((center_x, median, q1, q3, whisker_low, whisker_high, group_colors[i]))

# Add clouds (half-violins) with category labels for legend
for category, cloud_points, _color in cloud_data:
    chart.add(category, cloud_points, stroke=True, fill=True)

# Add rain points (no legend entry to avoid duplicates)
for _category, rain_points, _color in rain_data:
    chart.add(None, rain_points, stroke=False, fill=False, dots_size=16)

# Add box plots - use contrasting dark color for visibility
box_width = 0.12
cap_width = 0.06

for center_x, median, q1, q3, whisker_low, whisker_high, _color in box_data:
    box_x = center_x + box_offset

    # IQR box outline
    quartile_box = [
        (box_x - box_width, q1),
        (box_x - box_width, q3),
        (box_x + box_width, q3),
        (box_x + box_width, q1),
        (box_x - box_width, q1),
    ]
    chart.add(None, quartile_box, stroke=True, fill=False, show_dots=False, stroke_style={"width": 6})

    # Median line - MUCH thicker and red for clear distinction from box edges
    median_line = [(box_x - box_width * 1.2, median), (box_x + box_width * 1.2, median)]
    chart.add(None, median_line, stroke=True, fill=False, show_dots=False, stroke_style={"width": 12})

    # Whiskers - vertical lines from box to caps
    whisker_top = [(box_x, q3), (box_x, whisker_high)]
    whisker_bottom = [(box_x, q1), (box_x, whisker_low)]
    chart.add(None, whisker_top, stroke=True, fill=False, show_dots=False, stroke_style={"width": 6})
    chart.add(None, whisker_bottom, stroke=True, fill=False, show_dots=False, stroke_style={"width": 6})

    # Whisker caps
    cap_top = [(box_x - cap_width, whisker_high), (box_x + cap_width, whisker_high)]
    cap_bottom = [(box_x - cap_width, whisker_low), (box_x + cap_width, whisker_low)]
    chart.add(None, cap_top, stroke=True, fill=False, show_dots=False, stroke_style={"width": 6})
    chart.add(None, cap_bottom, stroke=True, fill=False, show_dots=False, stroke_style={"width": 6})

# X-axis labels at category positions
chart.x_labels = ["", "Control", "Treatment A", "Treatment B", ""]
chart.x_labels_major_count = 3

# Save outputs
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
