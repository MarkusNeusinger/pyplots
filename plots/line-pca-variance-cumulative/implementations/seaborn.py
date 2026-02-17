""" pyplots.ai
line-pca-variance-cumulative: Cumulative Explained Variance for PCA Component Selection
Library: seaborn 0.13.2 | Python 3.14.3
Quality: 88/100 | Created: 2026-02-17
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
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

# Find where cumulative variance crosses 95%
idx_95 = int(np.argmax(cumulative_variance >= 95))
comp_95 = n_components[idx_95]
val_95 = cumulative_variance[idx_95]

# Tidy dataframes for seaborn
df_bar = pd.DataFrame({"Component": n_components, "Variance (%)": individual_variance, "Type": "Individual"})
df_line = pd.DataFrame({"Component": n_components, "Variance (%)": cumulative_variance, "Type": "Cumulative"})

# Seaborn theme with custom context
sns.set_theme(
    style="whitegrid",
    context="talk",
    font_scale=1.1,
    rc={
        "axes.spines.top": False,
        "axes.spines.right": False,
        "grid.alpha": 0.15,
        "grid.linewidth": 0.6,
        "axes.grid.axis": "y",
        "axes.edgecolor": "#444444",
        "axes.linewidth": 1.2,
        "font.family": "sans-serif",
    },
)

# Cohesive color scheme from seaborn palette
main_palette = sns.color_palette("deep")
blue = main_palette[0]
orange = main_palette[1]
green = main_palette[2]

fig, ax = plt.subplots(figsize=(16, 9))

# Individual variance bars using seaborn barplot with hue
sns.barplot(
    data=df_bar,
    x="Component",
    y="Variance (%)",
    hue="Type",
    palette={"Individual": blue},
    alpha=0.2,
    width=0.5,
    legend=False,
    ax=ax,
)

# Cumulative variance line using seaborn lineplot with hue
sns.lineplot(
    data=df_line,
    x="Component",
    y="Variance (%)",
    hue="Type",
    palette={"Cumulative": blue},
    linewidth=3,
    marker="o",
    markersize=12,
    markeredgewidth=2.5,
    ax=ax,
)

# Style cumulative line markers: white fill with blue edge
line = ax.lines[0]
line.set_markerfacecolor("white")
line.set_markeredgecolor(blue)

# Build legend from seaborn lineplot handle + manual bar entry
handles, labels = ax.get_legend_handles_labels()
bar_patch = plt.Rectangle((0, 0), 1, 1, fc=blue, alpha=0.2, label="Individual Variance")
handles.append(bar_patch)
labels.append("Individual Variance")
labels[0] = "Cumulative Variance"
ax.legend(
    handles=handles, labels=labels, fontsize=15, loc="lower right", framealpha=0.9, edgecolor="#cccccc", fancybox=True
)

# Threshold lines with colorblind-friendly colors from seaborn deep palette
ax.axhline(y=95, color=orange, linestyle="--", linewidth=2, alpha=0.65, dashes=(6, 3))
ax.axhline(y=90, color=green, linestyle="--", linewidth=2, alpha=0.65, dashes=(3, 2, 6, 2))

# Threshold labels: 95% on the left, 90% on the right to avoid overlap with each other and data
ax.text(0.3, 95.8, "95%", fontsize=15, color=orange, fontweight="bold", va="bottom", ha="center")
ax.text(0.3, 89.2, "90%", fontsize=15, color=green, fontweight="bold", va="top", ha="center")

# Highlight the 95% crossing point
ax.plot(
    idx_95, val_95, "o", markersize=18, markerfacecolor=orange, markeredgecolor="white", markeredgewidth=2.5, zorder=5
)

# Annotation with boxed text and curved arrow for storytelling
ax.annotate(
    f"{comp_95} components explain {val_95:.1f}%",
    xy=(idx_95, val_95),
    xytext=(idx_95 - 4, 58),
    fontsize=15,
    fontweight="bold",
    color=orange,
    arrowprops={"arrowstyle": "-|>", "color": orange, "lw": 2.2, "connectionstyle": "arc3,rad=0.25"},
    bbox={"boxstyle": "round,pad=0.4", "facecolor": "white", "edgecolor": orange, "alpha": 0.9},
)

# Subtle shading below 90% to highlight the insufficient-components region
ax.axhspan(0, 90, color=green, alpha=0.03)

# Axis styling
ax.set_xlabel("Number of Principal Components", fontsize=20)
ax.set_ylabel("Explained Variance (%)", fontsize=20)
ax.set_title("line-pca-variance-cumulative · seaborn · pyplots.ai", fontsize=24, fontweight="medium", pad=16)
ax.tick_params(axis="both", labelsize=16)
ax.set_xlim(-0.6, len(n_components) - 0.4)
ax.set_ylim(0, 105)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
