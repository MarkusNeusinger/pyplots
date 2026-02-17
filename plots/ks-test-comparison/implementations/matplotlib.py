"""pyplots.ai
ks-test-comparison: Kolmogorov-Smirnov Plot for Distribution Comparison
Library: matplotlib 3.10.8 | Python 3.14.3
Quality: 84/100 | Created: 2026-02-17
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

# ECDF step lines with distinct linestyles for colorblind accessibility
ax.step(
    good_sorted,
    good_ecdf,
    where="post",
    linewidth=2.8,
    color="#306998",
    label="Good Customers",
    linestyle="-",
    zorder=3,
)
ax.step(
    bad_sorted, bad_ecdf, where="post", linewidth=2.8, color="#D4533B", label="Bad Customers", linestyle="--", zorder=3
)

# Shaded region at maximum distance to emphasize the K-S gap
ax.fill_betweenx([max_y_bad, max_y_good], max_x - 1.5, max_x + 1.5, color="#306998", alpha=0.10, zorder=1)

# K-S distance line
ax.plot([max_x, max_x], [max_y_bad, max_y_good], color="#2D2D2D", linewidth=2.5, linestyle=":", zorder=5)
ax.scatter([max_x, max_x], [max_y_bad, max_y_good], color="#2D2D2D", s=120, zorder=6, edgecolors="white", linewidth=1.2)

# K-S statistic annotation — positioned close to the distance line
mid_y = (max_y_good + max_y_bad) / 2
ax.annotate(
    f"D = {ks_stat:.3f}",
    xy=(max_x, mid_y),
    xytext=(max_x + 4, mid_y + 0.04),
    fontsize=18,
    fontweight="bold",
    color="#2D2D2D",
    arrowprops={"arrowstyle": "->", "color": "#555555", "linewidth": 1.5, "connectionstyle": "arc3,rad=-0.15"},
    va="center",
    bbox={"boxstyle": "round,pad=0.3", "facecolor": "white", "edgecolor": "#CCCCCC", "alpha": 0.9},
)

# P-value text
p_text = "p-value < 0.001" if p_value < 0.001 else f"p-value = {p_value:.4f}"
ax.text(
    0.97,
    0.05,
    p_text,
    transform=ax.transAxes,
    fontsize=16,
    ha="right",
    va="bottom",
    color="#555555",
    fontstyle="italic",
)

# Style
ax.set_xlabel("Credit Score (0–100)", fontsize=20)
ax.set_ylabel("Cumulative Proportion", fontsize=20)
ax.set_title("ks-test-comparison · matplotlib · pyplots.ai", fontsize=24, fontweight="medium", pad=16)
ax.tick_params(axis="both", labelsize=16)
ax.set_ylim(-0.02, 1.04)
ax.set_xlim(-2, 102)
ax.legend(fontsize=16, loc="upper left", framealpha=0.9, edgecolor="#CCCCCC")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_linewidth(0.6)
ax.spines["bottom"].set_linewidth(0.6)
ax.yaxis.grid(True, alpha=0.15, linewidth=0.6, color="#AAAAAA")
ax.set_facecolor("#FAFAFA")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
