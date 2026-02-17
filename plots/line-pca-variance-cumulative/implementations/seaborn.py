""" pyplots.ai
line-pca-variance-cumulative: Cumulative Explained Variance for PCA Component Selection
Library: seaborn 0.13.2 | Python 3.14.3
Quality: 82/100 | Created: 2026-02-17
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.datasets import load_wine
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


# Data
wine = load_wine()
X_scaled = StandardScaler().fit_transform(wine.data)

pca = PCA()
pca.fit(X_scaled)

n_components = np.arange(1, len(pca.explained_variance_ratio_) + 1)
individual_variance = pca.explained_variance_ratio_ * 100
cumulative_variance = np.cumsum(individual_variance)

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

# Individual variance as subtle bars
ax.bar(n_components, individual_variance, color="#306998", alpha=0.25, width=0.6, label="Individual Variance")

# Cumulative variance line
sns.lineplot(
    x=n_components,
    y=cumulative_variance,
    ax=ax,
    color="#306998",
    linewidth=3,
    marker="o",
    markersize=12,
    markerfacecolor="white",
    markeredgecolor="#306998",
    markeredgewidth=2.5,
    label="Cumulative Variance",
)

# Threshold reference lines
thresholds = [(95, "#E74C3C", "95%"), (90, "#F39C12", "90%")]
for threshold, color, label in thresholds:
    ax.axhline(y=threshold, color=color, linestyle="--", linewidth=2, alpha=0.7)
    ax.text(n_components[-1] + 0.3, threshold, label, fontsize=16, color=color, fontweight="bold", va="center")

# Mark where cumulative variance first exceeds 95%
idx_95 = np.argmax(cumulative_variance >= 95)
ax.plot(
    n_components[idx_95],
    cumulative_variance[idx_95],
    "o",
    markersize=18,
    markerfacecolor="#E74C3C",
    markeredgecolor="white",
    markeredgewidth=2.5,
    zorder=5,
)
ax.annotate(
    f"{int(n_components[idx_95])} components\n({cumulative_variance[idx_95]:.1f}%)",
    xy=(n_components[idx_95], cumulative_variance[idx_95]),
    xytext=(n_components[idx_95] - 3, cumulative_variance[idx_95] - 12),
    fontsize=16,
    fontweight="bold",
    color="#E74C3C",
    arrowprops={"arrowstyle": "->", "color": "#E74C3C", "lw": 2},
)

# Style
ax.set_xlabel("Number of Principal Components", fontsize=20)
ax.set_ylabel("Explained Variance (%)", fontsize=20)
ax.set_title("Wine Dataset PCA · line-pca-variance-cumulative · seaborn · pyplots.ai", fontsize=24, fontweight="medium")
ax.tick_params(axis="both", labelsize=16)
ax.set_xticks(n_components)
ax.set_xlim(0.4, n_components[-1] + 1.5)
ax.set_ylim(0, 105)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.yaxis.grid(True, alpha=0.2, linewidth=0.8)

# Legend
ax.legend(fontsize=15, loc="center right", framealpha=0.9)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
