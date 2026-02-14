""" pyplots.ai
box-basic: Basic Box Plot
Library: matplotlib 3.10.8 | Python 3.14
Quality: 82/100 | Created: 2025-12-23
"""

import matplotlib.pyplot as plt
import numpy as np


# Data - simulating test scores (0-100 scale) across 5 departments
np.random.seed(42)
categories = ["Engineering", "Marketing", "Sales", "Support", "Design"]
colors = ["#306998", "#FFD43B", "#E8A838", "#8B5CF6", "#4ECDC4"]

# Generate realistic distributions with varied characteristics and clamped to 0-100
data = [
    np.clip(np.random.normal(74, 10, 80), 15, 100),  # Engineering: solid, moderate spread
    np.clip(np.random.normal(85, 6, 90), 15, 100),  # Marketing: high scores, tight cluster
    np.clip(np.random.normal(68, 14, 70), 15, 100),  # Sales: lower, widest spread
    np.clip(np.random.normal(78, 9, 85), 15, 100),  # Support: above average, moderate
    np.clip(np.random.normal(80, 11, 60), 15, 100),  # Design: high with some spread
]

# Inject deliberate outliers for feature coverage
data[0] = np.append(data[0], [38, 99])  # Engineering: one low, one high outlier
data[2] = np.append(data[2], [22, 25, 98])  # Sales: two low outliers, one high

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

bp = ax.boxplot(
    data,
    tick_labels=categories,
    patch_artist=True,
    widths=0.55,
    showmeans=True,
    meanprops={"marker": "D", "markerfacecolor": "white", "markeredgecolor": "#333333", "markersize": 9, "zorder": 5},
    flierprops={
        "marker": "o",
        "markerfacecolor": "#666666",
        "markersize": 8,
        "alpha": 0.6,
        "markeredgecolor": "white",
        "markeredgewidth": 0.5,
    },
    medianprops={"color": "#333333", "linewidth": 2.5},
    whiskerprops={"linewidth": 2, "color": "#555555"},
    capprops={"linewidth": 2, "color": "#555555"},
)

# Apply colors to each box
for patch, color in zip(bp["boxes"], colors, strict=True):
    patch.set_facecolor(color)
    patch.set_alpha(0.75)
    patch.set_edgecolor("#333333")
    patch.set_linewidth(2)

# Style
ax.set_xlabel("Department", fontsize=20)
ax.set_ylabel("Score (0–100)", fontsize=20)
ax.set_title("box-basic · matplotlib · pyplots.ai", fontsize=24, fontweight="medium")
ax.tick_params(axis="both", labelsize=16)
ax.set_ylim(10, 105)
ax.yaxis.grid(True, alpha=0.2, linewidth=0.8)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
