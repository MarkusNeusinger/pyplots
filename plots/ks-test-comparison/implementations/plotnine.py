"""pyplots.ai
ks-test-comparison: Kolmogorov-Smirnov Plot for Distribution Comparison
Library: plotnine 0.15.3 | Python 3.14.3
Quality: 81/100 | Created: 2026-02-17
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    annotate,
    element_blank,
    element_line,
    element_rect,
    element_text,
    geom_rect,
    geom_segment,
    geom_step,
    ggplot,
    labs,
    scale_color_manual,
    scale_x_continuous,
    scale_y_continuous,
    theme,
    theme_minimal,
)
from scipy import stats


# Data
np.random.seed(42)
good_scores = np.random.beta(5, 2, 300) * 800 + 200
bad_scores = np.random.beta(2, 4, 300) * 800 + 200

# K-S test
ks_stat, p_value = stats.ks_2samp(good_scores, bad_scores)

# Compute ECDFs
good_sorted = np.sort(good_scores)
bad_sorted = np.sort(bad_scores)
good_ecdf = np.arange(1, len(good_sorted) + 1) / len(good_sorted)
bad_ecdf = np.arange(1, len(bad_sorted) + 1) / len(bad_sorted)

# Find the point of maximum divergence
all_values = np.sort(np.concatenate([good_sorted, bad_sorted]))
good_cdf_at_all = np.searchsorted(good_sorted, all_values, side="right") / len(good_sorted)
bad_cdf_at_all = np.searchsorted(bad_sorted, all_values, side="right") / len(bad_sorted)
differences = np.abs(good_cdf_at_all - bad_cdf_at_all)
max_idx = np.argmax(differences)
max_x = all_values[max_idx]
max_y_good = good_cdf_at_all[max_idx]
max_y_bad = bad_cdf_at_all[max_idx]

# Build DataFrames for step plots
df_good = pd.DataFrame({"score": good_sorted, "ecdf": good_ecdf, "group": "Good Customers"})
df_bad = pd.DataFrame({"score": bad_sorted, "ecdf": bad_ecdf, "group": "Bad Customers"})
df = pd.concat([df_good, df_bad], ignore_index=True)

# Shaded region highlighting the max divergence zone
y_lo = min(max_y_good, max_y_bad)
y_hi = max(max_y_good, max_y_bad)
band_half_width = 18
df_shade = pd.DataFrame(
    {"xmin": [max_x - band_half_width], "xmax": [max_x + band_half_width], "ymin": [y_lo], "ymax": [y_hi]}
)

# Max distance segment
df_segment = pd.DataFrame({"x": [max_x], "xend": [max_x], "y": [y_lo], "yend": [y_hi]})

# Axis ranges
x_min = min(good_sorted.min(), bad_sorted.min())
x_max = max(good_sorted.max(), bad_sorted.max())
x_pad = (x_max - x_min) * 0.04

# Plot
plot = (
    ggplot(df, aes(x="score", y="ecdf", color="group"))
    # Shaded region between the two CDFs at max divergence
    + geom_rect(
        aes(xmin="xmin", xmax="xmax", ymin="ymin", ymax="ymax"),
        data=df_shade,
        fill="#E74C3C",
        alpha=0.12,
        inherit_aes=False,
    )
    # Max divergence vertical line - bold and prominent
    + geom_segment(
        aes(x="x", xend="xend", y="y", yend="yend"),
        data=df_segment,
        color="#C0392B",
        size=1.8,
        linetype="dashed",
        inherit_aes=False,
    )
    # ECDF step functions
    + geom_step(size=2)
    # D label near max divergence line
    + annotate(
        "text",
        x=max_x + 20,
        y=(max_y_good + max_y_bad) / 2,
        label=f"D = {ks_stat:.3f}",
        size=14,
        ha="left",
        va="center",
        color="#C0392B",
        fontweight="bold",
    )
    # Statistical summary - positioned in lower-center to use empty space
    + annotate(
        "label",
        x=x_min + 0.50 * (x_max - x_min),
        y=0.08,
        label=f"K-S Statistic = {ks_stat:.3f}\np-value = {p_value:.2e}",
        size=14,
        ha="left",
        va="center",
        color="#C0392B",
        fontweight="bold",
        fill="#FDF2F0",
        alpha=0.9,
        label_size=0.8,
        boxstyle="round",
    )
    + scale_color_manual(values={"Good Customers": "#306998", "Bad Customers": "#E8873D"})
    + scale_y_continuous(limits=(0, 1.0), breaks=np.arange(0, 1.1, 0.2))
    + scale_x_continuous(limits=(x_min - x_pad, x_max + x_pad * 3))
    + labs(
        x="Credit Score",
        y="Cumulative Proportion",
        color="Customer Type",
        title="ks-test-comparison · plotnine · pyplots.ai",
    )
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        text=element_text(size=14),
        axis_title=element_text(size=20, margin={"t": 12, "r": 12}),
        axis_text=element_text(size=16),
        plot_title=element_text(size=24, weight="bold", margin={"b": 12}),
        legend_title=element_text(size=18, weight="bold"),
        legend_text=element_text(size=16),
        legend_position=(0.18, 0.82),
        legend_background=element_rect(fill="white", alpha=0.8),
        panel_grid_major_x=element_blank(),
        panel_grid_minor=element_blank(),
        panel_grid_major_y=element_line(color="#DDDDDD", alpha=0.4, size=0.5),
        axis_line=element_line(color="#888888", size=0.5),
        panel_border=element_blank(),
        plot_margin_right=0.04,
    )
)

# Save
plot.save("plot.png", dpi=300)
