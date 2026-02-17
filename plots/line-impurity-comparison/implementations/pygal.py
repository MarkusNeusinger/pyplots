""" pyplots.ai
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

# Style
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#1a1a1a",
    foreground_subtle="#dddddd",
    colors=("#306998", "#D4773F", "#888888"),
    opacity="1",
    opacity_hover="1",
    stroke_opacity="1",
    stroke_opacity_hover="1",
    stroke_width=7,
    stroke_width_hover=9,
    guide_stroke_color="#dddddd",
    guide_stroke_dasharray="0",
    major_guide_stroke_color="#dddddd",
    major_guide_stroke_dasharray="0",
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=44,
    value_font_size=36,
    tooltip_font_size=32,
    font_family="sans-serif",
    label_font_family="sans-serif",
    major_label_font_family="sans-serif",
    legend_font_family="sans-serif",
    title_font_family="sans-serif",
)

# Plot
chart = pygal.XY(
    width=4800,
    height=2700,
    title="line-impurity-comparison \u00b7 pygal \u00b7 pyplots.ai",
    x_title="Probability p",
    y_title="Impurity Measure",
    style=custom_style,
    show_dots=False,
    fill=False,
    show_y_guides=True,
    show_x_guides=False,
    legend_at_bottom=True,
    legend_at_bottom_columns=3,
    truncate_legend=-1,
    xrange=(0, 1),
    range=(0, 1.05),
    x_labels=[0, 0.2, 0.4, 0.5, 0.6, 0.8, 1.0],
    x_label_rotation=0,
    margin=80,
    margin_bottom=220,
    margin_left=220,
    margin_right=100,
)

# Gini impurity curve
gini_points = [(float(p[i]), float(gini[i])) for i in range(len(p))]
chart.add("Gini: 2p(1\u2212p)", gini_points)

# Entropy curve
entropy_points = [(float(p[i]), float(entropy[i])) for i in range(len(p))]
chart.add("Entropy: \u2212p log\u2082p \u2212 (1\u2212p) log\u2082(1\u2212p)", entropy_points)

# Vertical marker at p=0.5 (max impurity for both)
chart.add(
    "Max impurity (p = 0.5)",
    [(0.5, 0.0), (0.5, 1.0)],
    stroke_style={"width": 3, "dasharray": "14, 10"},
    show_dots=True,
    dots_size=10,
)

# Save
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
