"""pyplots.ai
line-pca-variance-cumulative: Cumulative Explained Variance for PCA Component Selection
Library: matplotlib | Python 3.13
Quality: pending | Created: 2026-02-17
"""

import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_wine
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


# Data
wine = load_wine()
X = StandardScaler().fit_transform(wine.data)
pca = PCA().fit(X)

explained_variance_ratio = pca.explained_variance_ratio_
cumulative_variance = np.cumsum(explained_variance_ratio)
components = np.arange(1, len(cumulative_variance) + 1)

# Thresholds
thresholds = [0.90, 0.95]
threshold_labels = ["90%", "95%"]
threshold_colors = ["#D4A03C", "#C75B3B"]

# Find components needed for each threshold
components_at_threshold = []
for t in thresholds:
    n = np.argmax(cumulative_variance >= t) + 1
    components_at_threshold.append(n)

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

ax.bar(components, explained_variance_ratio, color="#306998", alpha=0.35, width=0.7, label="Individual variance")

ax.plot(
    components,
    cumulative_variance,
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

# Threshold lines and markers
for t, label, color, n_comp in zip(
    thresholds, threshold_labels, threshold_colors, components_at_threshold, strict=True
):
    ax.axhline(y=t, color=color, linestyle="--", linewidth=2, alpha=0.7)
    ax.text(components[-1] + 0.3, t, label, fontsize=16, color=color, va="center", fontweight="medium")
    ax.plot(n_comp, t, marker="D", color=color, markersize=12, zorder=6, markeredgecolor="white", markeredgewidth=1.5)

# Style
ax.set_xlabel("Number of Components", fontsize=20)
ax.set_ylabel("Explained Variance Ratio", fontsize=20)
ax.set_title("line-pca-variance-cumulative \u00b7 matplotlib \u00b7 pyplots.ai", fontsize=24, fontweight="medium")
ax.tick_params(axis="both", labelsize=16)
ax.set_xticks(components)
ax.set_xlim(0.4, len(components) + 1.4)
ax.set_ylim(0, 1.05)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.yaxis.grid(True, alpha=0.2, linewidth=0.8)
ax.legend(fontsize=16, loc="center right")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
