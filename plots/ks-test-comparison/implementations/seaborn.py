"""pyplots.ai
ks-test-comparison: Kolmogorov-Smirnov Plot for Distribution Comparison
Library: seaborn | Python 3.13
Quality: pending | Created: 2026-02-17
"""

import matplotlib.pyplot as plt
import numpy as np
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

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

sns.ecdfplot(data=good_scores, ax=ax, linewidth=3, color="#306998", label="Good Customers")
sns.ecdfplot(data=bad_scores, ax=ax, linewidth=3, color="#E3724B", label="Bad Customers")

# Highlight K-S statistic: vertical line at max divergence
ax.plot(
    [max_x, max_x],
    [min(max_y_good, max_y_bad), max(max_y_good, max_y_bad)],
    color="#2D2D2D",
    linewidth=2.5,
    linestyle="--",
    zorder=5,
)
ax.scatter([max_x, max_x], [max_y_good, max_y_bad], color="#2D2D2D", s=120, zorder=6, edgecolors="white", linewidth=1.5)

# Annotate K-S statistic and p-value
ax.annotate(
    f"K-S Statistic = {ks_stat:.3f}\np-value = {p_value:.2e}",
    xy=(max_x, (max_y_good + max_y_bad) / 2),
    xytext=(max_x + 40, 0.5),
    fontsize=16,
    fontweight="bold",
    color="#2D2D2D",
    ha="left",
    va="center",
    bbox={"boxstyle": "round,pad=0.5", "facecolor": "white", "edgecolor": "#CCCCCC", "alpha": 0.9},
    arrowprops={"arrowstyle": "->", "color": "#2D2D2D", "linewidth": 1.5},
)

# Style
ax.set_xlabel("Credit Score", fontsize=20)
ax.set_ylabel("Cumulative Proportion", fontsize=20)
ax.set_title("Credit Score Distributions · ks-test-comparison · seaborn · pyplots.ai", fontsize=24, fontweight="medium")
ax.tick_params(axis="both", labelsize=16)
ax.set_ylim(0, 1.02)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.yaxis.grid(True, alpha=0.2, linewidth=0.8)
ax.legend(fontsize=16, frameon=False, loc="upper left")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
