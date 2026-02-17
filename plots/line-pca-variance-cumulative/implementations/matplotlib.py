""" pyplots.ai
line-pca-variance-cumulative: Cumulative Explained Variance for PCA Component Selection
Library: matplotlib 3.10.8 | Python 3.14.3
Quality: 86/100 | Created: 2026-02-17
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from sklearn.datasets import load_wine
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


# Data
wine = load_wine()
X = StandardScaler().fit_transform(wine.data)
pca = PCA().fit(X)

variance = pca.explained_variance_ratio_
cumulative = np.cumsum(variance)
components = np.arange(1, len(cumulative) + 1)

# Thresholds
thresholds = [(0.90, "90%", "#D4A03C"), (0.95, "95%", "#C75B3B")]
n_at_threshold = [np.argmax(cumulative >= t) + 1 for t, _, _ in thresholds]

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

# Individual variance bars
ax.bar(components, variance, color="#306998", alpha=0.30, width=0.7, label="Individual variance", zorder=2)

# Cumulative line with styled markers
ax.plot(
    components,
    cumulative,
    color="#306998",
    linewidth=3,
    marker="o",
    markersize=10,
    markerfacecolor="white",
    markeredgecolor="#306998",
    markeredgewidth=2.5,
    label="Cumulative variance",
    zorder=5,
)

# Threshold lines with legend entries and crossing annotations
offsets = [(-4.5, -0.10), (-5.5, 0.04)]
for (t, label, color), n_comp, (dx, dy) in zip(thresholds, n_at_threshold, offsets, strict=True):
    ax.axhline(y=t, color=color, linestyle="--", linewidth=1.8, alpha=0.6, label=f"{label} threshold")
    ax.plot(n_comp, t, marker="D", color=color, markersize=13, zorder=6, markeredgecolor="white", markeredgewidth=1.5)
    ax.annotate(
        f"{n_comp} components → {label} variance",
        xy=(n_comp, t),
        xytext=(n_comp + dx, t + dy),
        fontsize=14,
        fontweight="medium",
        color=color,
        arrowprops={"arrowstyle": "-|>", "color": color, "lw": 1.5},
        bbox={"boxstyle": "round,pad=0.3", "facecolor": "white", "edgecolor": color, "alpha": 0.9},
        zorder=7,
    )

# Formatting
ax.set_xlabel("Number of Components", fontsize=20)
ax.set_ylabel("Explained Variance Ratio (%)", fontsize=20)
ax.set_title("line-pca-variance-cumulative · matplotlib · pyplots.ai", fontsize=24, fontweight="medium", pad=16)
ax.tick_params(axis="both", labelsize=16)
ax.set_xticks(components)
ax.set_xlim(0.3, len(components) + 0.7)
ax.set_ylim(0, 1.05)

# Y-axis percentage formatting using FuncFormatter
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:.0%}"))

# Visual refinement
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_linewidth(0.6)
ax.spines["left"].set_color("#888888")
ax.spines["bottom"].set_linewidth(0.6)
ax.spines["bottom"].set_color("#888888")
ax.yaxis.grid(True, alpha=0.15, linewidth=0.6, color="#999999")
ax.set_axisbelow(True)

# Legend in lower-right where there's empty space
ax.legend(fontsize=16, loc="lower right", framealpha=0.9, edgecolor="#cccccc", fancybox=True)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
