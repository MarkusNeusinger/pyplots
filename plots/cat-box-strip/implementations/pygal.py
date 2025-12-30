"""pyplots.ai
cat-box-strip: Box Plot with Strip Overlay
Library: pygal | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - Generate distributions for different measurement conditions
np.random.seed(42)
raw_data = {
    "Control": np.random.normal(52, 12, 40),
    "Treatment A": np.random.normal(68, 10, 45),
    "Treatment B": np.random.normal(74, 15, 35),
    "Treatment C": np.random.normal(61, 8, 50),
}

# Clip all values to realistic 0-100 range (test scores)
data = {k: np.clip(v, 0, 100) for k, v in raw_data.items()}

# Add some outliers to show box plot features
data["Treatment A"] = np.append(data["Treatment A"], [42, 95])
data["Treatment B"] = np.append(data["Treatment B"], [30, 98])

# Colors - primary blue for boxes, yellow for strip points
box_color = "#306998"  # Python Blue
point_color = "#FFD43B"  # Python Yellow
line_color = "#333333"  # Dark gray for whiskers and median

# Build color sequence for all series
# Pattern: box, whisker lines (4), caps (2), median, strip points = 9 series per category
colors_list = []
for _ in range(4):
    colors_list.extend(
        [
            box_color,  # Box outline
            line_color,
            line_color,  # Lower/upper whisker
            line_color,
            line_color,  # Lower/upper cap
            line_color,  # Median
            point_color,  # Strip points
        ]
    )

# Custom style for 4800x2700 px canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=tuple(colors_list),
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=42,
    value_font_size=36,
    opacity=0.8,
    opacity_hover=0.95,
)

# Create XY chart for combined box plot with strip overlay
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="cat-box-strip · pygal · pyplots.ai",
    x_title="Condition",
    y_title="Score (0-100 scale)",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=3,
    stroke=True,
    fill=False,
    dots_size=0,
    show_x_guides=False,
    show_y_guides=True,
    range=(0, 110),
    xrange=(0, 6),
    margin=50,
)

# Box and strip styling parameters
box_width = 0.25
strip_jitter = 0.12

# Stroke styles for box plot elements
box_stroke_style = {"width": 5, "dasharray": ""}
median_stroke_style = {"width": 6, "dasharray": ""}
whisker_stroke_style = {"width": 3, "dasharray": ""}

# Track if legend entries have been added (only add once)
added_box_legend = False
added_median_legend = False
added_strip_legend = False

# Add box plots with strip overlay for each category
for i, (_category, values) in enumerate(data.items()):
    center_x = i + 1.5

    # Calculate box plot statistics
    median = float(np.median(values))
    q1 = float(np.percentile(values, 25))
    q3 = float(np.percentile(values, 75))
    iqr_val = q3 - q1

    # Whiskers: 1.5 * IQR or data min/max
    lower_whisker = max(float(values.min()), q1 - 1.5 * iqr_val)
    upper_whisker = min(float(values.max()), q3 + 1.5 * iqr_val)

    # Quartile box (IQR) - outline only
    box_points = [
        (center_x - box_width, q1),
        (center_x - box_width, q3),
        (center_x + box_width, q3),
        (center_x + box_width, q1),
        (center_x - box_width, q1),
    ]
    box_label = "Box (Q1-Q3)" if not added_box_legend else None
    chart.add(box_label, box_points, stroke=True, fill=False, show_dots=False, stroke_style=box_stroke_style)
    added_box_legend = True

    # Whisker lines (vertical lines from box to whisker ends)
    lower_whisker_line = [(center_x, q1), (center_x, lower_whisker)]
    upper_whisker_line = [(center_x, q3), (center_x, upper_whisker)]
    chart.add(None, lower_whisker_line, stroke=True, fill=False, show_dots=False, stroke_style=whisker_stroke_style)
    chart.add(None, upper_whisker_line, stroke=True, fill=False, show_dots=False, stroke_style=whisker_stroke_style)

    # Whisker caps (horizontal lines at ends)
    cap_width = box_width * 0.7
    lower_cap = [(center_x - cap_width, lower_whisker), (center_x + cap_width, lower_whisker)]
    upper_cap = [(center_x - cap_width, upper_whisker), (center_x + cap_width, upper_whisker)]
    chart.add(None, lower_cap, stroke=True, fill=False, show_dots=False, stroke_style=whisker_stroke_style)
    chart.add(None, upper_cap, stroke=True, fill=False, show_dots=False, stroke_style=whisker_stroke_style)

    # Median line (thicker, prominent)
    median_line = [(center_x - box_width, median), (center_x + box_width, median)]
    median_label = "Median" if not added_median_legend else None
    chart.add(median_label, median_line, stroke=True, fill=False, show_dots=False, stroke_style=median_stroke_style)
    added_median_legend = True

    # Strip plot - individual data points with jitter
    np.random.seed(42 + i)  # Different jitter per category but reproducible
    jitter = np.random.uniform(-strip_jitter, strip_jitter, len(values))
    strip_points = [(center_x + j, float(v)) for j, v in zip(jitter, values, strict=True)]
    strip_label = "Data Points" if not added_strip_legend else None
    chart.add(strip_label, strip_points, stroke=False, fill=False, show_dots=True, dots_size=12)
    added_strip_legend = True

# X-axis labels at box positions
chart.x_labels = ["", "Control", "Treatment A", "Treatment B", "Treatment C", ""]
chart.x_labels_major_count = 4

# Save outputs
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
