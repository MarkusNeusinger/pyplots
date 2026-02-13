""" pyplots.ai
histogram-basic: Basic Histogram
Library: matplotlib 3.10.8 | Python 3.14.0
Quality: 85/100 | Created: 2025-12-23
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgba


# Data - Simulate exam scores with slight left skew (realistic grade distribution)
np.random.seed(42)
base = np.random.normal(loc=72, scale=12, size=450)
high_cluster = np.random.normal(loc=88, scale=4, size=50)
scores = np.clip(np.concatenate([base, high_cluster]), 0, 100)

# Plot
fig, ax = plt.subplots(figsize=(16, 9))
n, bins, patches = ax.hist(scores, bins=25, color="#306998", edgecolor="white", linewidth=1.5, alpha=0.85)

# Shade bars by height using patch manipulation (matplotlib-distinctive)
max_count = max(n)
base_color = to_rgba("#306998")
for count, patch in zip(n, patches, strict=True):
    intensity = 0.5 + 0.5 * (count / max_count)
    patch.set_facecolor((*base_color[:3], intensity * 0.85))

# Labels and styling
ax.set_xlabel("Exam Score (points)", fontsize=20)
ax.set_ylabel("Frequency (count)", fontsize=20)
ax.set_title("histogram-basic \u00b7 matplotlib \u00b7 pyplots.ai", fontsize=24, fontweight="medium")
ax.tick_params(axis="both", labelsize=16)

# Spine removal (library convention: remove top + right)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Subtle y-axis grid
ax.yaxis.grid(True, alpha=0.2, linewidth=0.8)
ax.set_axisbelow(True)

# Ensure y-axis starts at zero
ax.set_ylim(bottom=0)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
