""" pyplots.ai
ks-test-comparison: Kolmogorov-Smirnov Plot for Distribution Comparison
Library: seaborn 0.13.2 | Python 3.14.3
Quality: 87/100 | Created: 2026-02-17
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats


# Data - credit scoring: Good vs Bad customer score distributions
# Moderate overlap for educational K-S demonstration (~0.35-0.50 statistic)
np.random.seed(42)
good_scores = np.random.beta(5, 3, size=300) * 500 + 350
bad_scores = np.random.beta(3, 4, size=200) * 500 + 350

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
# Apply different linestyles for accessibility beyond color alone
sns.ecdfplot(data=df, x="Credit Score (points)", hue="Group", palette=palette, linewidth=3.5, ax=ax)

# Set distinct linestyles on the ECDF lines for colorblind accessibility
lines = ax.get_lines()
if len(lines) >= 2:
    lines[0].set_linestyle("-")  # Good Customers: solid
    lines[1].set_linestyle("--")  # Bad Customers: dashed

# Subtle shaded fill between the two ECDFs near the max divergence point
# Tight band (±25 points) for balanced layout without dominating the plot
band_half = 25
band_mask = (all_values >= max_x - band_half) & (all_values <= max_x + band_half)
region_values = all_values[band_mask]
region_good = good_ecdf[band_mask]
region_bad = bad_ecdf[band_mask]
ax.fill_between(region_values, region_good, region_bad, alpha=0.12, color="#D35400", zorder=2, label="_nolegend_")

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
mid_y = (max_y_good + max_y_bad) / 2
ax.annotate(
    f"K-S Statistic = {ks_stat:.3f}\np-value = {p_value:.2e}",
    xy=(max_x, mid_y),
    xytext=(max_x + 100, 0.25),
    fontsize=16,
    fontweight="bold",
    color="#2D2D2D",
    ha="left",
    va="center",
    bbox={"boxstyle": "round,pad=0.6", "facecolor": "#F8F9FA", "edgecolor": "#95A5A6", "linewidth": 1.2, "alpha": 0.95},
    arrowprops={"arrowstyle": "-|>", "color": "#7F8C8D", "linewidth": 1.5, "connectionstyle": "arc3,rad=-0.2"},
)

# Small label next to divergence line for storytelling
ax.text(
    max_x + 5,
    max(max_y_good, max_y_bad) + 0.02,
    "max distance",
    fontsize=12,
    fontstyle="italic",
    color="#555555",
    va="bottom",
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

# Refine legend using public API
legend = ax.get_legend()
legend.set_title(None)
for text in legend.get_texts():
    text.set_fontsize(16)
legend.set_loc("upper left")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
