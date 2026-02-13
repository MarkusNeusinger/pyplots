"""pyplots.ai
histogram-basic: Basic Histogram
Library: seaborn 0.13.2 | Python 3.14.0
Quality: /100 | Updated: 2026-02-13
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Data - simulated exam scores with realistic right skew
np.random.seed(42)
values = np.concatenate(
    [
        np.random.normal(loc=72, scale=10, size=400),
        np.random.normal(loc=90, scale=4, size=80),
        np.random.uniform(30, 50, size=20),
    ]
)

# Plot
fig, ax = plt.subplots(figsize=(16, 9))
sns.histplot(values, bins=30, kde=True, color="#306998", edgecolor="white", linewidth=1.2, alpha=0.85, ax=ax)

# Style
ax.set_xlabel("Exam Score (points)", fontsize=20)
ax.set_ylabel("Frequency (count)", fontsize=20)
ax.set_title("histogram-basic \u00b7 seaborn \u00b7 pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.yaxis.grid(True, alpha=0.2, linewidth=0.8)
ax.set_ylim(bottom=0)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
