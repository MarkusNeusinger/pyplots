""" pyplots.ai
pp-basic: Probability-Probability (P-P) Plot
Library: seaborn 0.13.2 | Python 3.14.3
Quality: 79/100 | Created: 2026-03-15
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy import stats


# Data
np.random.seed(42)
sample_size = 200
normal_component = np.random.normal(loc=50, scale=10, size=int(sample_size * 0.85))
skewed_component = np.random.exponential(scale=5, size=int(sample_size * 0.15)) + 55
observed = np.concatenate([normal_component, skewed_component])

sorted_data = np.sort(observed)
empirical_cdf = np.arange(1, len(sorted_data) + 1) / (len(sorted_data) + 1)

mu, sigma = stats.norm.fit(sorted_data)
theoretical_cdf = stats.norm.cdf(sorted_data, loc=mu, scale=sigma)

# Plot
fig, ax = plt.subplots(figsize=(10, 10))

sns.scatterplot(
    x=theoretical_cdf, y=empirical_cdf, ax=ax, color="#306998", s=200, alpha=0.7, edgecolor="white", linewidth=0.5
)

ax.plot([0, 1], [0, 1], color="#C84B31", linewidth=2.5, linestyle="--", alpha=0.8, zorder=0)

# Style
ax.set_xlabel("Theoretical Cumulative Probability", fontsize=20)
ax.set_ylabel("Empirical Cumulative Probability", fontsize=20)
ax.set_title("pp-basic · seaborn · pyplots.ai", fontsize=24, fontweight="medium")
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
