"""pyplots.ai
ks-test-comparison: Kolmogorov-Smirnov Plot for Distribution Comparison
Library: plotnine | Python 3.13
Quality: pending | Created: 2026-02-17
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    annotate,
    element_blank,
    element_line,
    element_text,
    geom_segment,
    geom_step,
    ggplot,
    labs,
    scale_color_manual,
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

# Max distance segment
df_segment = pd.DataFrame(
    {"x": [max_x], "xend": [max_x], "y": [min(max_y_good, max_y_bad)], "yend": [max(max_y_good, max_y_bad)]}
)

# Annotation text
annotation_text = f"K-S Statistic = {ks_stat:.3f}\np-value = {p_value:.2e}"
annotation_x = min(good_sorted.min(), bad_sorted.min()) + 0.65 * (
    max(good_sorted.max(), bad_sorted.max()) - min(good_sorted.min(), bad_sorted.min())
)

# Plot
plot = (
    ggplot(df, aes(x="score", y="ecdf", color="group"))
    + geom_step(size=1.5)
    + geom_segment(
        aes(x="x", xend="xend", y="y", yend="yend"),
        data=df_segment,
        color="#E74C3C",
        size=1.2,
        linetype="dashed",
        inherit_aes=False,
    )
    + annotate(
        "text", x=annotation_x, y=0.15, label=annotation_text, size=14, ha="left", fontweight="bold", color="#333333"
    )
    + annotate(
        "text",
        x=max_x + 15,
        y=(max_y_good + max_y_bad) / 2,
        label=f"D = {ks_stat:.3f}",
        size=12,
        ha="left",
        color="#E74C3C",
        fontweight="bold",
    )
    + scale_color_manual(values={"Good Customers": "#306998", "Bad Customers": "#E8873D"})
    + scale_y_continuous(limits=(0, 1), breaks=np.arange(0, 1.1, 0.2))
    + labs(
        x="Credit Score",
        y="Cumulative Proportion",
        color="Distribution",
        title="ks-test-comparison · plotnine · pyplots.ai",
    )
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        text=element_text(size=14),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        plot_title=element_text(size=24, weight="bold"),
        legend_title=element_text(size=18),
        legend_text=element_text(size=16),
        legend_position=(0.15, 0.85),
        panel_grid_major_x=element_blank(),
        panel_grid_minor=element_blank(),
        panel_grid_major_y=element_line(color="#cccccc", alpha=0.25),
    )
)

# Save
plot.save("plot.png", dpi=300)
