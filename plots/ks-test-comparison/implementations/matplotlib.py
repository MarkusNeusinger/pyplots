"""pyplots.ai
ks-test-comparison: Kolmogorov-Smirnov Plot for Distribution Comparison
Library: matplotlib | Python 3.13
Quality: pending | Created: 2026-02-17
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


# Data
np.random.seed(42)
good_customers = np.random.beta(5, 2, 500) * 100
bad_customers = np.random.beta(2, 4, 500) * 100

# K-S test
ks_stat, p_value = stats.ks_2samp(good_customers, bad_customers)

# Compute ECDFs
good_sorted = np.sort(good_customers)
bad_sorted = np.sort(bad_customers)
good_ecdf = np.arange(1, len(good_sorted) + 1) / len(good_sorted)
bad_ecdf = np.arange(1, len(bad_sorted) + 1) / len(bad_sorted)

# Find maximum distance point
all_values = np.sort(np.concatenate([good_sorted, bad_sorted]))
good_cdf_at_all = np.searchsorted(good_sorted, all_values, side="right") / len(good_sorted)
bad_cdf_at_all = np.searchsorted(bad_sorted, all_values, side="right") / len(bad_sorted)
differences = np.abs(good_cdf_at_all - bad_cdf_at_all)
max_idx = np.argmax(differences)
max_x = all_values[max_idx]
max_y_good = good_cdf_at_all[max_idx]
max_y_bad = bad_cdf_at_all[max_idx]

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

ax.step(good_sorted, good_ecdf, where="post", linewidth=2.5, color="#306998", label="Good Customers")
ax.step(bad_sorted, bad_ecdf, where="post", linewidth=2.5, color="#D4533B", label="Bad Customers")

# K-S distance line
ax.plot([max_x, max_x], [max_y_bad, max_y_good], color="#2D2D2D", linewidth=2.5, linestyle="--", zorder=5)
ax.scatter([max_x, max_x], [max_y_bad, max_y_good], color="#2D2D2D", s=80, zorder=6, edgecolors="white", linewidth=0.5)

# K-S statistic annotation
mid_y = (max_y_good + max_y_bad) / 2
ax.annotate(
    f"D = {ks_stat:.3f}",
    xy=(max_x, mid_y),
    xytext=(max_x + 6, mid_y),
    fontsize=18,
    fontweight="bold",
    color="#2D2D2D",
    arrowprops={"arrowstyle": "-", "color": "#2D2D2D", "linewidth": 1.5},
    va="center",
)

# P-value text
ax.text(
    0.97,
    0.05,
    "p-value < 0.001" if p_value < 0.001 else f"p-value = {p_value:.4f}",
    transform=ax.transAxes,
    fontsize=16,
    ha="right",
    va="bottom",
    color="#555555",
)

# Style
ax.set_xlabel("Credit Score", fontsize=20)
ax.set_ylabel("Cumulative Proportion", fontsize=20)
ax.set_title("ks-test-comparison · matplotlib · pyplots.ai", fontsize=24, fontweight="medium")
ax.tick_params(axis="both", labelsize=16)
ax.set_ylim(0, 1.02)
ax.legend(fontsize=16, loc="upper left", framealpha=0.9)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.yaxis.grid(True, alpha=0.2, linewidth=0.8)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
