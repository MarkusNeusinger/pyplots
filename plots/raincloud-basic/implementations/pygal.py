""" pyplots.ai
raincloud-basic: Basic Raincloud Plot
Library: pygal 3.1.0 | Python 3.14
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
box_color = "#000000"

# Build color sequence matching series order:
# Per group: cloud, rain, box, median, whisker_l, whisker_r, cap_l, cap_r
series_colors = []
for gc in group_colors:
    series_colors.extend([gc, gc, box_color, box_color, box_color, box_color, box_color, box_color])

# Custom style for 4800x2700 px canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#999999",
    guide_stroke_color="#e8e8e8",
    colors=tuple(series_colors),
    title_font_size=96,
    label_font_size=60,
    major_label_font_size=54,
    legend_font_size=54,
    value_font_size=42,
    tooltip_font_size=42,
    opacity=0.75,
    opacity_hover=0.9,
)

# Create HORIZONTAL XY chart for raincloud plot
# X-axis = Reaction Time (value), Y-axis = Treatment Group (category)
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="raincloud-basic · pygal · pyplots.ai",
    x_title="Reaction Time (ms)",
    y_title="Treatment Group",
    show_legend=False,
    stroke=True,
    fill=True,
    dots_size=0,
    show_x_guides=True,
    show_y_guides=True,
    xrange=(100, 750),
    range=(0, 4),
    margin=80,
    explicit_size=True,
)

# Raincloud layout parameters (HORIZONTAL orientation)
# Cloud extends UPWARD (positive Y offset from category line)
# Rain falls DOWNWARD (negative Y offset from category line)
cloud_height = 0.28
rain_offset = -0.32
n_kde_points = 80
box_width = 0.10
cap_width = 0.06

for i, (category, values) in enumerate(data.items()):
    center_y = i + 1  # Y position for this group (1, 2, 3)
    values = np.array(values)

    # --- Half-Violin (cloud) - extends UPWARD from category line ---
    n = len(values)
    std = np.std(values)
    iqr_val = np.percentile(values, 75) - np.percentile(values, 25)
    bandwidth = 0.9 * min(std, iqr_val / 1.34) * n ** (-0.2)

    x_min, x_max = values.min(), values.max()
    padding = (x_max - x_min) * 0.1
    x_range = np.linspace(x_min - padding, x_max + padding, n_kde_points)

    # Gaussian KDE
    density = np.zeros_like(x_range)
    for v in values:
        density += np.exp(-0.5 * ((x_range - v) / bandwidth) ** 2)
    density /= n * bandwidth * np.sqrt(2 * np.pi)

    # Normalize and place cloud ABOVE category line (positive Y)
    density_scaled = density / density.max() * cloud_height

    # Half-violin shape: baseline at center_y, cloud rises upward
    cloud_points = [(float(x_range[0]), center_y)]
    cloud_points += [
        {"value": (float(x), center_y + float(d)), "label": f"{category} density"}
        for x, d in zip(x_range, density_scaled, strict=True)
    ]
    cloud_points += [(float(x_range[-1]), center_y), (float(x_range[0]), center_y)]
    chart.add(f"{category} cloud", cloud_points, stroke=True, fill=True)

    # --- Jittered Points (rain) - falls DOWNWARD from category line ---
    np.random.seed(42 + i)
    jitter = np.random.uniform(-0.08, 0.08, len(values))
    rain_points = [
        {"value": (float(v), center_y + rain_offset + float(j)), "label": f"{category}: {v:.0f} ms"}
        for j, v in zip(jitter, values, strict=True)
    ]
    chart.add(f"{category} rain", rain_points, stroke=False, fill=False, dots_size=32)

    # --- Box Plot (centered at category line) ---
    median = float(np.median(values))
    q1 = float(np.percentile(values, 25))
    q3 = float(np.percentile(values, 75))
    iqr = q3 - q1
    whisker_low = float(max(values.min(), q1 - 1.5 * iqr))
    whisker_high = float(min(values.max(), q3 + 1.5 * iqr))

    # IQR box (horizontal rectangle)
    quartile_box = [
        (q1, center_y - box_width),
        (q1, center_y + box_width),
        (q3, center_y + box_width),
        (q3, center_y - box_width),
        (q1, center_y - box_width),
    ]
    chart.add("", quartile_box, stroke=True, fill=False, show_dots=False, stroke_style={"width": 36})

    # Median line (vertical line within box)
    median_line = [
        {"value": (median, center_y - box_width * 1.3), "label": f"{category} median: {median:.0f} ms"},
        (median, center_y + box_width * 1.3),
    ]
    chart.add("", median_line, stroke=True, fill=False, show_dots=False, stroke_style={"width": 44})

    # Whiskers
    whisker_left = [(whisker_low, center_y), (q1, center_y)]
    whisker_right = [(q3, center_y), (whisker_high, center_y)]
    chart.add("", whisker_left, stroke=True, fill=False, show_dots=False, stroke_style={"width": 22})
    chart.add("", whisker_right, stroke=True, fill=False, show_dots=False, stroke_style={"width": 22})

    # Whisker caps
    cap_left = [(whisker_low, center_y - cap_width), (whisker_low, center_y + cap_width)]
    cap_right = [(whisker_high, center_y - cap_width), (whisker_high, center_y + cap_width)]
    chart.add("", cap_left, stroke=True, fill=False, show_dots=False, stroke_style={"width": 22})
    chart.add("", cap_right, stroke=True, fill=False, show_dots=False, stroke_style={"width": 22})

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
