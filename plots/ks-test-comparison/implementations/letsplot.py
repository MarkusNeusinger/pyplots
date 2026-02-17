""" pyplots.ai
ks-test-comparison: Kolmogorov-Smirnov Plot for Distribution Comparison
Library: letsplot 4.8.2 | Python 3.14.3
Quality: 87/100 | Created: 2026-02-17
"""

import numpy as np
import pandas as pd
from lets_plot import *  # noqa: F403, F405
from scipy import stats


LetsPlot.setup_html()  # noqa: F405

# Data - Credit scoring: Good vs Bad customer score distributions
np.random.seed(42)
n_good = 500
n_bad = 300

good_scores = np.random.normal(loc=620, scale=80, size=n_good)
bad_scores = np.random.normal(loc=520, scale=90, size=n_bad)

# Clip to realistic credit score range to avoid extreme tails
good_scores = np.clip(good_scores, 300, 850)
bad_scores = np.clip(bad_scores, 300, 850)

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

# Shaded ribbon between the two ECDFs near the maximum divergence point
# Sample points around max divergence to show the gap region
ribbon_mask = (all_values >= max_x - 60) & (all_values <= max_x + 60)
ribbon_x = all_values[ribbon_mask]
ribbon_ymin = np.minimum(good_ecdf_at_all[ribbon_mask], bad_ecdf_at_all[ribbon_mask])
ribbon_ymax = np.maximum(good_ecdf_at_all[ribbon_mask], bad_ecdf_at_all[ribbon_mask])
df_ribbon = pd.DataFrame({"score": ribbon_x, "ymin": ribbon_ymin, "ymax": ribbon_ymax})

# Vertical line segment at maximum divergence
df_ks_line = pd.DataFrame({"score": [max_x, max_x], "ecdf": [min(max_good_y, max_bad_y), max(max_good_y, max_bad_y)]})

# Label for K-S statistic
ks_label_y = (max_good_y + max_bad_y) / 2
df_ks_label = pd.DataFrame({"score": [max_x + 25], "ecdf": [ks_label_y], "label": [f"D = {ks_stat:.3f}"]})

# Subtitle as annotation
subtitle_text = f"K-S Statistic: {ks_stat:.3f} | p-value: {p_value:.2e}"

# Plot
plot = (
    ggplot()  # noqa: F405
    # Shaded region between CDFs near maximum divergence
    + geom_ribbon(  # noqa: F405
        data=df_ribbon,
        mapping=aes(x="score", ymin="ymin", ymax="ymax"),  # noqa: F405
        fill="#7B68AE",
        alpha=0.25,
    )
    # Both ECDFs with color mapped to group for legend
    + geom_step(  # noqa: F405
        data=df_ecdf,
        mapping=aes(x="score", y="ecdf", color="group"),  # noqa: F405
        size=2.2,
    )
    # K-S statistic vertical line (purple for colorblind safety)
    + geom_line(  # noqa: F405
        data=df_ks_line,
        mapping=aes(x="score", y="ecdf"),  # noqa: F405
        color="#7B68AE",
        size=2.5,
        linetype="dashed",
    )
    # K-S statistic label
    + geom_text(  # noqa: F405
        data=df_ks_label,
        mapping=aes(x="score", y="ecdf", label="label"),  # noqa: F405
        color="#5B4A8E",
        size=14,
        fontface="bold",
    )
    + scale_color_manual(  # noqa: F405
        values={"Good Customers": "#306998", "Bad Customers": "#E85D4A"}
    )
    + labs(  # noqa: F405
        x="Credit Score",
        y="Cumulative Proportion",
        title="ks-test-comparison \u00b7 letsplot \u00b7 pyplots.ai",
        subtitle=subtitle_text,
        color="",
    )
    + scale_x_continuous(limits=[280, 850], breaks=list(range(300, 851, 100)))  # noqa: F405
    + scale_y_continuous(limits=[0, 1.05], breaks=[0, 0.25, 0.5, 0.75, 1.0])  # noqa: F405
    + ggsize(1600, 900)  # noqa: F405
    + theme_minimal()  # noqa: F405
    + theme(  # noqa: F405
        plot_title=element_text(size=24, face="bold"),  # noqa: F405
        plot_subtitle=element_text(size=18, color="#555555"),  # noqa: F405
        axis_title=element_text(size=20),  # noqa: F405
        axis_text=element_text(size=16),  # noqa: F405
        legend_text=element_text(size=16),  # noqa: F405
        legend_position="top",
        panel_grid_major=element_line(color="#D8D8D8", size=0.3, linetype="dashed"),  # noqa: F405
        panel_grid_minor=element_blank(),  # noqa: F405
        plot_background=element_rect(fill="#FAFAFA", color="#FAFAFA"),  # noqa: F405
        panel_background=element_rect(fill="#FAFAFA", color="#FAFAFA"),  # noqa: F405
    )
)

# Save PNG (scale 3x to get 4800 x 2700 px) and HTML
ggsave(plot, "plot.png", path=".", scale=3)  # noqa: F405
ggsave(plot, "plot.html", path=".")  # noqa: F405
