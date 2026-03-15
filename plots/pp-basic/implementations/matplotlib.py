"""pyplots.ai
pp-basic: Probability-Probability (P-P) Plot
Library: matplotlib | Python 3.13
Quality: pending | Created: 2026-03-15
"""

from math import erfc, sqrt

import matplotlib.pyplot as plt
import numpy as np


# Data
np.random.seed(42)
sample_size = 200
observed = np.concatenate([np.random.normal(loc=50, scale=10, size=160), np.random.normal(loc=65, scale=8, size=40)])

observed_sorted = np.sort(observed)
empirical_cdf = np.arange(1, sample_size + 1) / (sample_size + 1)

mu, sigma = observed_sorted.mean(), observed_sorted.std()
theoretical_cdf = np.array([0.5 * erfc(-(x - mu) / (sigma * sqrt(2))) for x in observed_sorted])

# Plot
fig, ax = plt.subplots(figsize=(12, 12))

ax.plot([0, 1], [0, 1], color="#AAAAAA", linewidth=2, linestyle="--", zorder=1)

ax.scatter(
    theoretical_cdf, empirical_cdf, s=180, color="#306998", alpha=0.7, edgecolors="white", linewidth=0.5, zorder=2
)

# Style
ax.set_xlabel("Theoretical Cumulative Probability", fontsize=20)
ax.set_ylabel("Empirical Cumulative Probability", fontsize=20)
ax.set_title("pp-basic · matplotlib · pyplots.ai", fontsize=24, fontweight="medium")
ax.tick_params(axis="both", labelsize=16)
ax.set_xlim(-0.02, 1.02)
ax.set_ylim(-0.02, 1.02)
ax.set_aspect("equal")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.yaxis.grid(True, alpha=0.2, linewidth=0.8)
ax.xaxis.grid(True, alpha=0.2, linewidth=0.8)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
