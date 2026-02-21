""" pyplots.ai
violin-basic: Basic Violin Plot
Library: matplotlib 3.10.8 | Python 3.14.3
Quality: 88/100 | Updated: 2026-02-21
"""

import matplotlib.pyplot as plt
import numpy as np


# Data - simulated test scores (0-100) across different schools
np.random.seed(42)
categories = ["School A", "School B", "School C", "School D"]
data = [
    np.clip(np.random.normal(75, 10, 150), 0, 100),  # School A: centered around 75
    np.clip(np.random.normal(85, 6, 150), 0, 100),  # School B: high scores, tight cluster
    np.clip(np.random.normal(62, 15, 150), 0, 100),  # School C: lower average, wide spread
    np.clip(
        np.concatenate([np.random.normal(70, 5, 80), np.random.normal(88, 4, 70)]), 0, 100
    ),  # School D: bimodal (two subgroups)
]

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

# Violin plot with built-in quartile lines and facecolor/linecolor params
parts = ax.violinplot(
    data,
    positions=range(len(categories)),
    quantiles=[[0.25, 0.5, 0.75]] * len(categories),
    showmeans=False,
    showmedians=False,
    showextrema=False,
    bw_method=0.3,
    widths=0.75,
)

# Style violin bodies with shade intensity by median value
medians = [np.median(d) for d in data]
median_min, median_max = min(medians), max(medians)
base_blue = np.array([0x30, 0x69, 0x98]) / 255  # Python Blue #306998

for i, pc in enumerate(parts["bodies"]):
    t = (medians[i] - median_min) / (median_max - median_min) if median_max > median_min else 0.5
    pc.set_facecolor(base_blue * (0.6 + 0.4 * t))
    pc.set_edgecolor("#1e4a6e")
    pc.set_alpha(0.75)
    pc.set_linewidth(2)

# Style quantile lines: white for Q1/Q3, yellow for median
parts["cquantiles"].set_colors(["white", "#FFD43B", "white"] * len(categories))
parts["cquantiles"].set_linewidths([2, 3.5, 2] * len(categories))

# Labels and styling
ax.set_xticks(range(len(categories)))
ax.set_xticklabels(categories)
ax.set_xlabel("School", fontsize=20)
ax.set_ylabel("Test Score (points)", fontsize=20)
ax.set_title("violin-basic \u00b7 matplotlib \u00b7 pyplots.ai", fontsize=24, fontweight="medium")
ax.tick_params(axis="both", labelsize=16)

# Spine removal and grid per library rules
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.yaxis.grid(True, alpha=0.2, linewidth=0.8)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
