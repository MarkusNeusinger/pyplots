"""pyplots.ai
line-impurity-comparison: Gini Impurity vs Entropy Comparison
Library: matplotlib | Python 3.13
Quality: pending | Created: 2026-02-17
"""

import matplotlib.pyplot as plt
import numpy as np


# Data
p = np.linspace(0, 1, 200)

gini = 2 * p * (1 - p)

entropy = np.zeros_like(p)
mask = (p > 0) & (p < 1)
entropy[mask] = -p[mask] * np.log2(p[mask]) - (1 - p[mask]) * np.log2(1 - p[mask])

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

ax.plot(p, gini, linewidth=3, color="#306998", label="Gini Impurity:  $2p(1-p)$")
ax.plot(
    p,
    entropy,
    linewidth=3,
    color="#C1694F",
    linestyle="--",
    label="Entropy (normalized):  $-p\\,\\log_2 p - (1-p)\\,\\log_2(1-p)$",
)

# Annotate maximum at p=0.5
ax.annotate(
    "Maximum impurity\n$p = 0.5$",
    xy=(0.5, 1.0),
    xytext=(0.68, 0.82),
    fontsize=16,
    color="#444444",
    arrowprops={"arrowstyle": "->", "color": "#888888", "lw": 1.5},
    ha="left",
)

ax.plot(0.5, 2 * 0.5 * 0.5, "o", color="#306998", markersize=10, zorder=5)
ax.plot(0.5, 1.0, "o", color="#C1694F", markersize=10, zorder=5)

# Style
ax.set_xlabel("Probability $p$", fontsize=20)
ax.set_ylabel("Impurity Measure", fontsize=20)
ax.set_title("line-impurity-comparison · matplotlib · pyplots.ai", fontsize=24, fontweight="medium")
ax.tick_params(axis="both", labelsize=16)
ax.legend(fontsize=16, loc="upper left", framealpha=0.9)
ax.set_xlim(-0.02, 1.02)
ax.set_ylim(-0.02, 1.08)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.yaxis.grid(True, alpha=0.2, linewidth=0.8)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
