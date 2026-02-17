"""pyplots.ai
ks-test-comparison: Kolmogorov-Smirnov Plot for Distribution Comparison
Library: seaborn 0.13.2 | Python 3.14.3
Quality: 86/100 | Created: 2026-02-17
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats


# Data - credit scoring: Good vs Bad customer score distributions
np.random.seed(42)
good_scores = np.random.beta(5, 2, size=300) * 600 + 350
bad_scores = np.random.beta(2, 4, size=200) * 600 + 350

# Compute K-S statistic
ks_stat, p_value = stats.ks_2samp(good_scores, bad_scores)

# Compute ECDFs manually for finding max distance point
good_sorted = np.sort(good_scores)
bad_sorted = np.sort(bad_scores)
all_values = np.sort(np.concatenate([good_sorted, bad_sorted]))
good_ecdf = np.searchsorted(good_sorted, all_values, side="right") / len(good_sorted)
bad_ecdf = np.searchsorted(bad_sorted, all_values, side="right") / len(bad_sorted)
distances = np.abs(good_ecdf - bad_ecdf)
max_idx = np.argmax(distances)
max_x = all_values[max_idx]
max_y_good = good_ecdf[max_idx]
max_y_bad = bad_ecdf[max_idx]

# Build DataFrame for seaborn-idiomatic plotting
df = pd.DataFrame(
    {
        "Credit Score (points)": np.concatenate([good_scores, bad_scores]),
        "Group": ["Good Customers"] * len(good_scores) + ["Bad Customers"] * len(bad_scores),
    }
)

# Style setup - use seaborn theme for distinctive look
sns.set_theme(
    style="whitegrid",
    rc={
        "axes.spines.top": False,
        "axes.spines.right": False,
        "grid.alpha": 0.15,
        "grid.linewidth": 0.6,
        "font.family": "sans-serif",
    },
)

# Higher-contrast, colorblind-safe palette
palette = {"Good Customers": "#1B6B93", "Bad Customers": "#D35400"}

fig, ax = plt.subplots(figsize=(16, 9))

# Use seaborn ecdfplot with hue for idiomatic grouped ECDF
sns.ecdfplot(data=df, x="Credit Score (points)", hue="Group", palette=palette, linewidth=3.5, ax=ax)

# Shaded fill between the two ECDFs near the max divergence point
# Narrow band around the max divergence location for visual emphasis
band_width = 60
band_mask = (all_values >= max_x - band_width) & (all_values <= max_x + band_width)
region_values = all_values[band_mask]
region_good = good_ecdf[band_mask]
region_bad = bad_ecdf[band_mask]
ax.fill_between(region_values, region_good, region_bad, alpha=0.15, color="#D35400", zorder=2, label="_nolegend_")

# Highlight K-S statistic: vertical line at max divergence
ax.plot(
    [max_x, max_x],
    [min(max_y_good, max_y_bad), max(max_y_good, max_y_bad)],
    color="#2D2D2D",
    linewidth=2.5,
    linestyle="--",
    zorder=5,
)

# Prominent dots at max divergence intersections
ax.scatter([max_x, max_x], [max_y_good, max_y_bad], color="#2D2D2D", s=160, zorder=6, edgecolors="white", linewidth=2)

# Annotate K-S statistic and p-value with refined styling
# Place annotation in the bottom-right empty region for clear separation
ax.annotate(
    f"K-S Statistic = {ks_stat:.3f}\np-value = {p_value:.2e}",
    xy=(max_x, (max_y_good + max_y_bad) / 2),
    xytext=(max_x + 120, 0.28),
    fontsize=16,
    fontweight="bold",
    color="#2D2D2D",
    ha="left",
    va="center",
    bbox={"boxstyle": "round,pad=0.6", "facecolor": "#F8F9FA", "edgecolor": "#95A5A6", "linewidth": 1.2, "alpha": 0.95},
    arrowprops={"arrowstyle": "-|>", "color": "#7F8C8D", "linewidth": 1.5, "connectionstyle": "arc3,rad=-0.2"},
)

# Axis styling
ax.set_xlabel("Credit Score (points)", fontsize=20, labelpad=10)
ax.set_ylabel("Cumulative Proportion", fontsize=20, labelpad=10)
ax.set_title(
    "Credit Score Distributions · ks-test-comparison · seaborn · pyplots.ai", fontsize=24, fontweight="semibold", pad=18
)
ax.tick_params(axis="both", labelsize=16)
ax.set_ylim(0, 1.04)
ax.xaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f"))
ax.yaxis.grid(True)
ax.xaxis.grid(False)

# Refine legend
legend = ax.get_legend()
legend.set_title(None)
for text in legend.get_texts():
    text.set_fontsize(16)
legend._loc = 2  # upper left

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
