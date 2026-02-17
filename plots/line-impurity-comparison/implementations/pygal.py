"""pyplots.ai
line-impurity-comparison: Gini Impurity vs Entropy Comparison
Library: pygal 3.1.0 | Python 3.14.3
Quality: 88/100 | Created: 2026-02-17
"""

import numpy as np
import pygal
from pygal.style import Style


# Data
p = np.linspace(0, 1, 200)

# Gini impurity: 2 * p * (1 - p), already in [0, 1]
gini = 2 * p * (1 - p)

# Entropy: -p*log2(p) - (1-p)*log2(1-p), normalized to [0, 1]
with np.errstate(divide="ignore", invalid="ignore"):
    entropy = -p * np.log2(p) - (1 - p) * np.log2(1 - p)
entropy = np.nan_to_num(entropy, nan=0.0)

# Style — publication-quality with font weight variation
custom_style = Style(
    background="white",
    plot_background="#fafafa",
    foreground="#2a2a2a",
    foreground_strong="#111111",
    foreground_subtle="#e0e0e0",
    colors=("#306998", "#D4773F", "#999999", "#306998"),
    opacity="1",
    opacity_hover="1",
    stroke_opacity="1",
    stroke_opacity_hover="1",
    stroke_width=8,
    stroke_width_hover=10,
    guide_stroke_color="#e0e0e0",
    guide_stroke_dasharray="4, 4",
    major_guide_stroke_color="#cccccc",
    major_guide_stroke_dasharray="0",
    title_font_size=74,
    label_font_size=48,
    major_label_font_size=44,
    legend_font_size=42,
    value_font_size=36,
    tooltip_font_size=32,
    font_family="Helvetica, Arial, sans-serif",
    label_font_family="Helvetica, Arial, sans-serif",
    major_label_font_family="Helvetica, Arial, sans-serif",
    legend_font_family="Helvetica, Arial, sans-serif",
    title_font_family="Helvetica, Arial, sans-serif",
    value_font_family="Helvetica, Arial, sans-serif",
)

# Plot — leveraging pygal XY configuration
chart = pygal.XY(
    width=4800,
    height=2700,
    title="line-impurity-comparison \u00b7 pygal \u00b7 pyplots.ai",
    x_title="Probability p (range 0 to 1)",
    y_title="Impurity Measure (normalized)",
    style=custom_style,
    show_dots=False,
    fill=False,
    show_y_guides=True,
    show_x_guides=False,
    show_minor_x_labels=False,
    legend_at_bottom=True,
    legend_at_bottom_columns=2,
    legend_box_size=30,
    truncate_legend=-1,
    xrange=(0, 1),
    range=(0, 1.08),
    x_labels=[0, 0.2, 0.4, 0.5, 0.6, 0.8, 1.0],
    y_labels=[0, 0.2, 0.4, 0.5, 0.6, 0.8, 1.0],
    show_y_labels=True,
    x_label_rotation=0,
    margin=80,
    margin_bottom=160,
    margin_left=220,
    margin_right=100,
    margin_top=100,
    interpolate="cubic",
    show_x_labels=True,
    print_values=False,
    print_zeroes=False,
    js=[],
)

# Gini impurity curve
gini_points = [(float(p[i]), float(gini[i])) for i in range(len(p))]
chart.add("Gini: 2p(1\u2212p)", gini_points, stroke_style={"width": 8})

# Entropy curve
entropy_points = [(float(p[i]), float(entropy[i])) for i in range(len(p))]
chart.add(
    "Entropy: \u2212p log\u2082p \u2212 (1\u2212p) log\u2082(1\u2212p)", entropy_points, stroke_style={"width": 8}
)

# Vertical marker at p=0.5 (max impurity for both)
chart.add(
    "Max impurity (p = 0.5)",
    [(0.5, 0.0), (0.5, 1.0)],
    stroke_style={"width": 3, "dasharray": "14, 10"},
    show_dots=True,
    dots_size=8,
)

# Annotation dot at peak — highlights the key insight where both curves peak
chart.add(
    None, [{"value": (0.5, 0.5), "label": "Gini peak = 0.50"}], stroke_style={"width": 0}, show_dots=True, dots_size=16
)

# Save as both SVG and PNG
chart.render_to_file("plot.svg")
chart.render_to_png("plot.png")
