""" pyplots.ai
line-impurity-comparison: Gini Impurity vs Entropy Comparison
Library: seaborn 0.13.2 | Python 3.14.3
Quality: 82/100 | Created: 2026-02-17
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Data
p = np.linspace(0, 1, 100)

gini = 2 * p * (1 - p)
gini_normalized = gini / np.max(gini)

# Entropy with edge case handling (0 at p=0 and p=1)
entropy = np.zeros_like(p)
mask = (p > 0) & (p < 1)
entropy[mask] = -p[mask] * np.log2(p[mask]) - (1 - p[mask]) * np.log2(1 - p[mask])
entropy_normalized = entropy / np.max(entropy)

df = pd.DataFrame(
    {
        "Probability (p)": np.tile(p, 2),
        "Impurity": np.concatenate([gini_normalized, entropy_normalized]),
        "Criterion": ["Gini: 2p(1−p)"] * len(p) + ["Entropy: −p log₂p − (1−p) log₂(1−p)"] * len(p),
    }
)

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

palette = ["#306998", "#E8833A"]

sns.lineplot(
    data=df,
    x="Probability (p)",
    y="Impurity",
    hue="Criterion",
    style="Criterion",
    dashes=[(1, 0), (6, 2)],
    linewidth=3.5,
    palette=palette,
    ax=ax,
)

# Annotate maximum impurity point at p=0.5
ax.plot(0.5, 1.0, "o", color="#444444", markersize=10, zorder=5)
ax.annotate(
    "Max impurity\np = 0.5",
    xy=(0.5, 1.0),
    xytext=(0.72, 0.78),
    fontsize=16,
    color="#444444",
    arrowprops={"arrowstyle": "->", "color": "#888888", "lw": 2, "connectionstyle": "arc3,rad=-0.2"},
    bbox={"boxstyle": "round,pad=0.4", "facecolor": "white", "edgecolor": "#cccccc", "alpha": 0.9},
)

# Style
ax.set_xlabel("Probability (p)", fontsize=20)
ax.set_ylabel("Impurity (normalized)", fontsize=20)
ax.set_title("line-impurity-comparison · seaborn · pyplots.ai", fontsize=24, fontweight="medium")
ax.tick_params(axis="both", labelsize=16)
ax.set_xlim(0, 1)
ax.set_ylim(-0.02, 1.08)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.yaxis.grid(True, alpha=0.2, linewidth=0.8)

# Legend
ax.legend(title="Splitting Criterion", title_fontsize=18, fontsize=16, loc="upper left", framealpha=0.9)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
