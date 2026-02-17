""" pyplots.ai
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

# Compute ECDFs for both samples
good_sorted = np.sort(good_scores)
bad_sorted = np.sort(bad_scores)
n_good = len(good_sorted)
n_bad = len(bad_sorted)
good_ecdf_y = np.arange(1, n_good + 1) / n_good
bad_ecdf_y = np.arange(1, n_bad + 1) / n_bad

# Run KS test
ks_stat, p_value = stats.ks_2samp(good_scores, bad_scores)

# Find the point of maximum divergence
# Evaluate both ECDFs on a combined sorted grid
all_values = np.sort(np.concatenate([good_sorted, bad_sorted]))
good_ecdf_on_grid = np.searchsorted(good_sorted, all_values, side="right") / n_good
bad_ecdf_on_grid = np.searchsorted(bad_sorted, all_values, side="right") / n_bad
diffs = np.abs(good_ecdf_on_grid - bad_ecdf_on_grid)
max_idx = np.argmax(diffs)
max_x = all_values[max_idx]
max_y_good = good_ecdf_on_grid[max_idx]
max_y_bad = bad_ecdf_on_grid[max_idx]

# Build step function data for Good customers ECDF
good_xy = []
for i in range(n_good):
    if i == 0:
        good_xy.append((good_sorted[i], 0))
    else:
        good_xy.append((good_sorted[i], good_ecdf_y[i - 1]))
    good_xy.append((good_sorted[i], good_ecdf_y[i]))
good_xy.append((good_sorted[-1] + 10, 1.0))

# Build step function data for Bad customers ECDF
bad_xy = []
for i in range(n_bad):
    if i == 0:
        bad_xy.append((bad_sorted[i], 0))
    else:
        bad_xy.append((bad_sorted[i], bad_ecdf_y[i - 1]))
    bad_xy.append((bad_sorted[i], bad_ecdf_y[i]))
bad_xy.append((bad_sorted[-1] + 10, 1.0))

# KS statistic vertical line at point of maximum divergence
ks_line = [
    {"value": (max_x, min(max_y_good, max_y_bad)), "label": f"KS Statistic = {ks_stat:.3f}"},
    {"value": (max_x, max(max_y_good, max_y_bad)), "label": f"p-value = {p_value:.2e}"},
]

# Custom style for 4800x2700 canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#CCCCCC",
    colors=("#306998", "#E8590C", "#D4380D"),
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=42,
    value_font_size=36,
    tooltip_font_size=36,
    stroke_width=4,
    opacity=0.9,
    opacity_hover=1.0,
)

# Create XY chart
chart = pygal.XY(
    style=custom_style,
    width=4800,
    height=2700,
    title="ks-test-comparison \u00b7 pygal \u00b7 pyplots.ai",
    x_title="Credit Score",
    y_title="Cumulative Proportion",
    show_dots=False,
    stroke_style={"width": 4},
    show_x_guides=True,
    show_y_guides=True,
    range=(0, 1.05),
    legend_at_bottom=True,
    legend_at_bottom_columns=3,
    legend_box_size=28,
    truncate_legend=-1,
    margin=50,
    margin_top=80,
    margin_bottom=200,
)

# Add ECDFs
chart.add("Good Customers", good_xy)
chart.add("Bad Customers", bad_xy)

# Add KS statistic line at point of maximum divergence
chart.add(
    f"KS = {ks_stat:.3f}, p = {p_value:.2e}",
    ks_line,
    show_dots=True,
    dots_size=12,
    stroke_style={"width": 6},
    stroke_dasharray="12,6",
)

# Save
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
