"""pyplots.ai
ks-test-comparison: Kolmogorov-Smirnov Plot for Distribution Comparison
Library: pygal 3.1.0 | Python 3.14.3
Quality: 68/100 | Created: 2026-02-17
"""

import numpy as np
import pygal
from pygal.style import Style
from scipy import stats


# Data - Credit scoring: Good vs Bad customer score distributions
np.random.seed(42)
good_scores = np.random.normal(loc=650, scale=80, size=300)
bad_scores = np.random.normal(loc=500, scale=90, size=300)

# Compute ECDFs using numpy vectorized operations
good_sorted = np.sort(good_scores)
bad_sorted = np.sort(bad_scores)
n_good, n_bad = len(good_sorted), len(bad_sorted)
good_ecdf_y = np.arange(1, n_good + 1) / n_good
bad_ecdf_y = np.arange(1, n_bad + 1) / n_bad

# Run KS test
ks_stat, p_value = stats.ks_2samp(good_scores, bad_scores)

# Find the point of maximum divergence on a combined grid
all_values = np.sort(np.concatenate([good_sorted, bad_sorted]))
good_ecdf_on_grid = np.searchsorted(good_sorted, all_values, side="right") / n_good
bad_ecdf_on_grid = np.searchsorted(bad_sorted, all_values, side="right") / n_bad
diffs = np.abs(good_ecdf_on_grid - bad_ecdf_on_grid)
max_idx = np.argmax(diffs)
max_x = all_values[max_idx]
max_y_good = good_ecdf_on_grid[max_idx]
max_y_bad = bad_ecdf_on_grid[max_idx]

# Build step-function data using numpy repeat (vectorized, no loops)
good_x_steps = np.repeat(good_sorted, 2)
good_y_steps = np.empty_like(good_x_steps)
good_y_steps[0::2] = np.concatenate([[0], good_ecdf_y[:-1]])
good_y_steps[1::2] = good_ecdf_y
good_xy = list(zip(good_x_steps.tolist(), good_y_steps.tolist(), strict=True))

bad_x_steps = np.repeat(bad_sorted, 2)
bad_y_steps = np.empty_like(bad_x_steps)
bad_y_steps[0::2] = np.concatenate([[0], bad_ecdf_y[:-1]])
bad_y_steps[1::2] = bad_ecdf_y
bad_xy = list(zip(bad_x_steps.tolist(), bad_y_steps.tolist(), strict=True))

# Shared font family for consistency
_font = "Helvetica, Arial, sans-serif"

# Custom style — distinct palette: blue for Good, orange for Bad, dark green for KS
custom_style = Style(
    background="white",
    plot_background="#fafafa",
    foreground="#2a2a2a",
    foreground_strong="#111111",
    foreground_subtle="#e0e0e0",
    colors=(
        "#306998",  # Good Customers — Python Blue
        "#E8590C",  # Bad Customers — burnt orange
        "#1a7a3a",  # KS vertical line — dark green (high contrast vs both)
        "#1a7a3a",  # KS annotation dot (bottom) — matches KS line
        "#1a7a3a",  # KS annotation dot (top) — matches KS line
    ),
    opacity="0.95",
    opacity_hover="1",
    stroke_opacity="1",
    stroke_opacity_hover="1",
    stroke_width=7,
    guide_stroke_color="#e8e8e8",
    guide_stroke_dasharray="4, 6",
    major_guide_stroke_color="#d0d0d0",
    major_guide_stroke_dasharray="0",
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=42,
    value_font_size=40,
    value_label_font_size=40,
    tooltip_font_size=36,
    font_family=_font,
    label_font_family=_font,
    major_label_font_family=_font,
    legend_font_family=_font,
    title_font_family=_font,
    value_font_family=_font,
    value_label_font_family=_font,
)

# Create XY chart with refined layout
chart = pygal.XY(
    style=custom_style,
    width=4800,
    height=2700,
    title="ks-test-comparison \u00b7 pygal \u00b7 pyplots.ai",
    x_title="Credit Score (points)",
    y_title="Cumulative Proportion",
    show_dots=False,
    fill=False,
    show_x_guides=False,
    show_y_guides=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=2,
    legend_box_size=28,
    truncate_legend=-1,
    range=(0, 1.05),
    print_values=False,
    print_labels=True,
    print_zeroes=False,
    margin=60,
    margin_top=90,
    margin_bottom=180,
    margin_left=180,
    margin_right=100,
    js=[],
)

# Series 1: Good Customers ECDF — prominent blue line
chart.add("Good Customers", good_xy, stroke_style={"width": 8})

# Series 2: Bad Customers ECDF — prominent orange line
chart.add("Bad Customers", bad_xy, stroke_style={"width": 8})

# Series 3: KS vertical line — dark green dashed, thick for focal point
ks_line_points = [(max_x, min(max_y_good, max_y_bad)), (max_x, max(max_y_good, max_y_bad))]
chart.add(None, ks_line_points, stroke_style={"width": 6, "dasharray": "14, 8"}, show_dots=False)

# Series 4: KS annotation dot at bottom of divergence
chart.add(
    None,
    [{"value": (max_x, min(max_y_good, max_y_bad)), "label": f"D = {ks_stat:.3f}"}],
    stroke_style={"width": 0},
    show_dots=True,
    dots_size=18,
)

# Series 5: KS annotation dot at top of divergence with p-value
chart.add(
    None,
    [{"value": (max_x, max(max_y_good, max_y_bad)), "label": f"p = {p_value:.2e}"}],
    stroke_style={"width": 0},
    show_dots=True,
    dots_size=18,
)

# Save
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
