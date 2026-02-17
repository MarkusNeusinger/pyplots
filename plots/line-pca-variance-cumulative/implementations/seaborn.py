"""pyplots.ai
line-pca-variance-cumulative: Cumulative Explained Variance for PCA Component Selection
Library: seaborn 0.13.2 | Python 3.14.3
Quality: 82/100 | Created: 2026-02-17
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
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

df = pd.DataFrame(
    {
        "Component": np.tile(n_components, 2),
        "Variance (%)": np.concatenate([cumulative_variance, individual_variance]),
        "Type": ["Cumulative"] * len(n_components) + ["Individual"] * len(n_components),
    }
)

# Plot
sns.set_theme(
    style="whitegrid",
    rc={
        "axes.spines.top": False,
        "axes.spines.right": False,
        "grid.alpha": 0.2,
        "grid.linewidth": 0.8,
        "axes.grid.axis": "y",
    },
)

fig, ax = plt.subplots(figsize=(16, 9))

# Individual variance as subtle bars using seaborn
sns.barplot(
    data=df[df["Type"] == "Individual"],
    x="Component",
    y="Variance (%)",
    hue="Type",
    palette={"Individual": "#306998"},
    alpha=0.25,
    width=0.55,
    legend=False,
    ax=ax,
)

# Cumulative variance line using seaborn
sns.lineplot(
    data=df[df["Type"] == "Cumulative"],
    x="Component",
    y="Variance (%)",
    hue="Type",
    palette={"Cumulative": "#306998"},
    linewidth=3,
    marker="o",
    markersize=12,
    markeredgewidth=2.5,
    legend=False,
    ax=ax,
)

# Style markers: white fill with blue edge
line = ax.lines[0]
line.set_markerfacecolor("white")
line.set_markeredgecolor("#306998")

# Build legend from the seaborn-drawn elements
legend_elements = [
    Line2D(
        [0],
        [0],
        color="#306998",
        linewidth=3,
        marker="o",
        markerfacecolor="white",
        markeredgecolor="#306998",
        markeredgewidth=2.5,
        markersize=10,
        label="Cumulative Variance",
    ),
    Patch(facecolor="#306998", alpha=0.25, label="Individual Variance"),
]
ax.legend(handles=legend_elements, fontsize=15, loc="lower right", framealpha=0.9)

# Threshold reference lines with distinct patterns for colorblind accessibility
thresholds = [
    (95, "#C0392B", "95%", (5, 3)),  # dashed
    (90, "#8E44AD", "90%", (2, 3, 5, 3)),  # dash-dot
]
for threshold, color, label, dash_pattern in thresholds:
    ax.axhline(y=threshold, color=color, linestyle="--", linewidth=2, alpha=0.7, dashes=dash_pattern)
    ax.text(0.5, threshold + 1.3, label, fontsize=15, color=color, fontweight="bold", va="bottom", ha="center")

# Mark where cumulative variance first exceeds 95%
idx_95 = int(np.argmax(cumulative_variance >= 95))
comp_95 = n_components[idx_95]
val_95 = cumulative_variance[idx_95]

ax.plot(
    idx_95,
    val_95,
    "o",
    markersize=18,
    markerfacecolor="#C0392B",
    markeredgecolor="white",
    markeredgewidth=2.5,
    zorder=5,
)

# Annotation positioned below the marker to avoid overlap with line/data
ax.annotate(
    f"{comp_95} components ({val_95:.1f}%)",
    xy=(idx_95, val_95),
    xytext=(idx_95 - 2, 58),
    fontsize=16,
    fontweight="bold",
    color="#C0392B",
    arrowprops={"arrowstyle": "->", "color": "#C0392B", "lw": 2, "connectionstyle": "arc3,rad=0.15"},
)

# Style
ax.set_xlabel("Number of Principal Components", fontsize=20)
ax.set_ylabel("Explained Variance (%)", fontsize=20)
ax.set_title("line-pca-variance-cumulative · seaborn · pyplots.ai", fontsize=24, fontweight="medium", pad=16)
ax.tick_params(axis="both", labelsize=16)
ax.set_xlim(-0.6, len(n_components) - 0.5)
ax.set_ylim(0, 105)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
