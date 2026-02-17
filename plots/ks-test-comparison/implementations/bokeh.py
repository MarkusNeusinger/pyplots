"""pyplots.ai
ks-test-comparison: Kolmogorov-Smirnov Plot for Distribution Comparison
Library: bokeh | Python 3.13
Quality: pending | Created: 2026-02-17
"""

import numpy as np
from bokeh.io import export_png, save
from bokeh.models import ColumnDataSource, Label, Legend
from bokeh.plotting import figure
from bokeh.resources import CDN
from scipy import stats


# Data — Credit scoring: Good vs Bad customer score distributions
np.random.seed(42)
good_scores = np.random.beta(5, 2, 400) * 600 + 300  # Good customers: higher scores
bad_scores = np.random.beta(2, 4, 350) * 600 + 300  # Bad customers: lower scores

# Compute ECDFs
good_sorted = np.sort(good_scores)
good_ecdf = np.arange(1, len(good_sorted) + 1) / len(good_sorted)

bad_sorted = np.sort(bad_scores)
bad_ecdf = np.arange(1, len(bad_sorted) + 1) / len(bad_sorted)

# K-S test
ks_stat, p_value = stats.ks_2samp(good_scores, bad_scores)

# Find point of maximum divergence
all_values = np.sort(np.concatenate([good_scores, bad_scores]))
good_ecdf_at = np.searchsorted(good_sorted, all_values, side="right") / len(good_sorted)
bad_ecdf_at = np.searchsorted(bad_sorted, all_values, side="right") / len(bad_sorted)
diffs = np.abs(good_ecdf_at - bad_ecdf_at)
max_idx = np.argmax(diffs)
max_x = all_values[max_idx]
max_y_good = good_ecdf_at[max_idx]
max_y_bad = bad_ecdf_at[max_idx]

# Build step function arrays for Good customers
good_x_step = np.repeat(good_sorted, 2)[1:]
good_y_step = np.repeat(good_ecdf, 2)[:-1]
good_x_step = np.concatenate([[good_sorted[0]], good_x_step])
good_y_step = np.concatenate([[0], good_y_step])

# Build step function arrays for Bad customers
bad_x_step = np.repeat(bad_sorted, 2)[1:]
bad_y_step = np.repeat(bad_ecdf, 2)[:-1]
bad_x_step = np.concatenate([[bad_sorted[0]], bad_x_step])
bad_y_step = np.concatenate([[0], bad_y_step])

good_source = ColumnDataSource(data={"x": good_x_step, "y": good_y_step})
bad_source = ColumnDataSource(data={"x": bad_x_step, "y": bad_y_step})

# Plot
p = figure(
    width=4800,
    height=2700,
    title="ks-test-comparison · bokeh · pyplots.ai",
    x_axis_label="Credit Score",
    y_axis_label="Cumulative Proportion",
    y_range=(-0.02, 1.08),
    toolbar_location=None,
)

# Draw ECDF step lines
good_line = p.line(x="x", y="y", source=good_source, line_width=5, line_color="#306998", alpha=0.9)
bad_line = p.line(x="x", y="y", source=bad_source, line_width=5, line_color="#E8833A", alpha=0.9)

# Highlight maximum divergence with a vertical segment
ks_y_lower = min(max_y_good, max_y_bad)
ks_y_upper = max(max_y_good, max_y_bad)
ks_segment_source = ColumnDataSource(data={"x0": [max_x], "y0": [ks_y_lower], "x1": [max_x], "y1": [ks_y_upper]})
ks_line = p.segment(
    x0="x0", y0="y0", x1="x1", y1="y1", source=ks_segment_source, line_width=5, line_color="#D62728", line_dash="solid"
)

# Endpoint markers for the K-S segment
p.scatter(x=[max_x, max_x], y=[ks_y_lower, ks_y_upper], size=16, color="#D62728", marker="circle")

# Annotation: K-S statistic and p-value
p_text = "p < 0.001" if p_value < 0.001 else f"p = {p_value:.4f}"
ks_label = Label(
    x=max_x,
    y=(ks_y_lower + ks_y_upper) / 2,
    text=f"D = {ks_stat:.3f},  {p_text}",
    text_font_size="24pt",
    text_color="#D62728",
    text_font_style="bold",
    text_baseline="middle",
    x_offset=20,
)
p.add_layout(ks_label)

# Legend
legend = Legend(
    items=[
        ("Good Customers (ECDF)", [good_line]),
        ("Bad Customers (ECDF)", [bad_line]),
        ("Max Distance (K-S Statistic)", [ks_line]),
    ],
    location="top_left",
)
legend.label_text_font_size = "20pt"
legend.background_fill_alpha = 0.85
legend.border_line_alpha = 0.0
legend.padding = 15
legend.spacing = 8
p.add_layout(legend)

# Style
p.title.text_font_size = "28pt"
p.xaxis.axis_label_text_font_size = "22pt"
p.yaxis.axis_label_text_font_size = "22pt"
p.xaxis.major_label_text_font_size = "18pt"
p.yaxis.major_label_text_font_size = "18pt"

p.xgrid.grid_line_alpha = 0.2
p.ygrid.grid_line_alpha = 0.2

p.outline_line_color = None
p.background_fill_color = "white"
p.border_fill_color = "white"

# Save
export_png(p, filename="plot.png")
save(p, filename="plot.html", resources=CDN, title="ks-test-comparison · bokeh · pyplots.ai")
