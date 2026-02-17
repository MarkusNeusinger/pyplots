"""pyplots.ai
line-pca-variance-cumulative: Cumulative Explained Variance for PCA Component Selection
Library: pygal 3.1.0 | Python 3.14.3
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - Realistic PCA variance ratios for a 13-feature dataset (Wine-like)
eigenvalues = np.array([4.73, 2.51, 1.45, 0.92, 0.85, 0.64, 0.55, 0.35, 0.29, 0.21, 0.17, 0.13, 0.08])
explained_variance_ratio = eigenvalues / eigenvalues.sum()
individual_variance = explained_variance_ratio * 100
cumulative_variance = np.cumsum(explained_variance_ratio) * 100
n_components = len(cumulative_variance)
component_labels = [str(i) for i in range(1, n_components + 1)]

# Detect elbow point: where slope drops below 35% of max slope
slopes = np.diff(cumulative_variance)
elbow_idx = int(np.argmax(slopes < slopes[0] * 0.35))

# Find threshold crossings
cross_90 = int(np.searchsorted(cumulative_variance, 90))
cross_95 = int(np.searchsorted(cumulative_variance, 95))

# Custom style - refined palette, colorblind-safe (blue + purple + teal + steel)
custom_style = Style(
    background="white",
    plot_background="#F8F9FA",
    foreground="#2C3E50",
    foreground_strong="#1A252F",
    foreground_subtle="#D5DAE0",
    colors=("#306998", "#9B59B6", "#16A085", "#5D8AA8"),
    opacity=1.0,
    opacity_hover=1.0,
    stroke_opacity=1.0,
    stroke_opacity_hover=1.0,
    stroke_width=6,
    stroke_width_hover=8,
    dot_opacity=1.0,
    title_font_size=64,
    label_font_size=44,
    major_label_font_size=44,
    legend_font_size=38,
    value_font_size=38,
    tooltip_font_size=32,
    title_font_family="sans-serif",
    label_font_family="sans-serif",
    value_font_family="sans-serif",
)

# Chart with refined configuration
chart = pygal.Line(
    width=4800,
    height=2700,
    title="line-pca-variance-cumulative · pygal · pyplots.ai",
    x_title="Number of Components",
    y_title="Cumulative Explained Variance (%)",
    style=custom_style,
    show_dots=True,
    dots_size=10,
    show_only_major_dots=False,
    show_y_guides=True,
    show_x_guides=False,
    legend_at_bottom=True,
    legend_at_bottom_columns=4,
    legend_box_size=28,
    truncate_legend=-1,
    range=(0, 103),
    secondary_range=(0, 45),
    margin=30,
    margin_bottom=100,
    margin_left=140,
    margin_right=140,
    print_values=True,
    print_values_position="top",
    value_formatter=lambda x: "",
    spacing=20,
    x_labels_major_count=13,
    show_minor_x_labels=False,
    tooltip_fancy_mode=True,
    tooltip_border_radius=8,
)

# X-axis and Y-axis labels
chart.x_labels = component_labels

# Y-axis: key percentages with major labels at thresholds
chart.y_labels = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 100]
chart.y_labels_major = [90, 95]
chart.show_minor_y_labels = True

# Annotation formatters for key data points
annotations = {elbow_idx: lambda x: f"◆ Elbow ({x:.0f}%)", cross_90: lambda x: "90% ——→", cross_95: lambda x: "95% ——→"}

# Cumulative variance line with per-point annotations at key locations
cumulative_values = [
    {"value": round(v, 1), "formatter": annotations.get(i, lambda x: "")} for i, v in enumerate(cumulative_variance)
]

chart.add("Cumulative Variance", cumulative_values, stroke_style={"width": 8, "linecap": "round", "linejoin": "round"})

# 90% threshold line (dashed, purple - colorblind-safe vs blue)
chart.add(
    "90% Threshold",
    [{"value": 90, "formatter": lambda x: ""} for _ in range(n_components)],
    show_dots=False,
    stroke_style={"width": 7, "dasharray": "24, 12"},
)

# 95% threshold line (dashed, teal - colorblind-safe vs both blue and purple)
chart.add(
    "95% Threshold",
    [{"value": 95, "formatter": lambda x: ""} for _ in range(n_components)],
    show_dots=False,
    stroke_style={"width": 7, "dasharray": "10, 8"},
)

# Individual variance bars on secondary Y-axis (steel blue, lighter opacity)
individual_values = [{"value": round(v, 1), "formatter": lambda x: f"{x:.1f}%"} for v in individual_variance]
chart.add(
    "Individual Variance",
    individual_values,
    secondary=True,
    stroke_style={"width": 14, "linecap": "round"},
    show_dots=False,
    fill=False,
)

# Save
chart.render_to_png("plot.png")
