""" pyplots.ai
ks-test-comparison: Kolmogorov-Smirnov Plot for Distribution Comparison
Library: letsplot 4.8.2 | Python 3.14.3
Quality: 78/100 | Created: 2026-02-17
"""

import numpy as np
import pandas as pd
from lets_plot import *  # noqa: F403
from lets_plot.export import ggsave as export_ggsave
from scipy import stats


LetsPlot.setup_html()  # noqa: F405

# Data - Credit scoring: Good vs Bad customer score distributions
np.random.seed(42)
n_good = 500
n_bad = 300

good_scores = np.random.normal(loc=620, scale=80, size=n_good)
bad_scores = np.random.normal(loc=520, scale=90, size=n_bad)

# Compute ECDFs
good_sorted = np.sort(good_scores)
good_ecdf = np.arange(1, len(good_sorted) + 1) / len(good_sorted)

bad_sorted = np.sort(bad_scores)
bad_ecdf = np.arange(1, len(bad_sorted) + 1) / len(bad_sorted)

# K-S test
ks_stat, p_value = stats.ks_2samp(good_scores, bad_scores)

# Find the point of maximum divergence
all_values = np.sort(np.concatenate([good_sorted, bad_sorted]))
good_ecdf_at_all = np.searchsorted(good_sorted, all_values, side="right") / len(good_sorted)
bad_ecdf_at_all = np.searchsorted(bad_sorted, all_values, side="right") / len(bad_sorted)
differences = np.abs(good_ecdf_at_all - bad_ecdf_at_all)
max_idx = np.argmax(differences)
max_x = all_values[max_idx]
max_good_y = good_ecdf_at_all[max_idx]
max_bad_y = bad_ecdf_at_all[max_idx]

# Build DataFrames for each ECDF with group column for combined legend
df_good = pd.DataFrame({"score": good_sorted, "ecdf": good_ecdf, "group": "Good Customers"})
df_bad = pd.DataFrame({"score": bad_sorted, "ecdf": bad_ecdf, "group": "Bad Customers"})
df_ecdf = pd.concat([df_good, df_bad], ignore_index=True)

# Vertical line segment at maximum divergence
df_ks_line = pd.DataFrame({"score": [max_x, max_x], "ecdf": [min(max_good_y, max_bad_y), max(max_good_y, max_bad_y)]})

# Label for K-S statistic
ks_label_y = (max_good_y + max_bad_y) / 2
df_ks_label = pd.DataFrame({"score": [max_x + 20], "ecdf": [ks_label_y], "label": [f"D = {ks_stat:.3f}"]})

# Plot
plot = (
    ggplot()  # noqa: F405
    # Both ECDFs with color mapped to group for legend
    + geom_step(  # noqa: F405
        data=df_ecdf,
        mapping=aes(x="score", y="ecdf", color="group"),  # noqa: F405
        size=1.8,
    )
    # K-S statistic vertical line
    + geom_line(  # noqa: F405
        data=df_ks_line,
        mapping=aes(x="score", y="ecdf"),  # noqa: F405
        color="#2CA02C",
        size=2.0,
        linetype="dashed",
    )
    # K-S statistic label
    + geom_text(  # noqa: F405
        data=df_ks_label,
        mapping=aes(x="score", y="ecdf", label="label"),  # noqa: F405
        color="#2CA02C",
        size=13,
        fontface="bold",
    )
    + scale_color_manual(values={"Good Customers": "#306998", "Bad Customers": "#E85D4A"})  # noqa: F405
    + labs(  # noqa: F405
        x="Credit Score",
        y="Cumulative Proportion",
        title=f"ks-test-comparison \u00b7 letsplot \u00b7 pyplots.ai\nK-S Statistic: {ks_stat:.3f} | p-value: {p_value:.2e}",
        color="",
    )
    + scale_y_continuous(limits=[0, 1.05], breaks=[0, 0.25, 0.5, 0.75, 1.0])  # noqa: F405
    + ggsize(1600, 900)  # noqa: F405
    + theme_minimal()  # noqa: F405
    + theme(  # noqa: F405
        plot_title=element_text(size=22),  # noqa: F405
        axis_title=element_text(size=20),  # noqa: F405
        axis_text=element_text(size=16),  # noqa: F405
        legend_text=element_text(size=16),  # noqa: F405
        legend_position="top",
        panel_grid_major=element_line(color="#CCCCCC", size=0.5, linetype="dashed"),  # noqa: F405
        panel_grid_minor=element_blank(),  # noqa: F405
    )
)

# Save PNG (scale 3x to get 4800 x 2700 px) and HTML
export_ggsave(plot, filename="plot.png", path=".", scale=3)
export_ggsave(plot, filename="plot.html", path=".")
