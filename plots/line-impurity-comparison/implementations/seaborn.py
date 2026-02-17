"""pyplots.ai
line-impurity-comparison: Gini Impurity vs Entropy Comparison
Library: seaborn 0.13.2 | Python 3.14.3
Quality: 82/100 | Created: 2026-02-17
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Data
p = np.linspace(0, 1, 100)

gini = 2 * p * (1 - p)
gini_normalized = gini / gini.max()

# Entropy with edge case handling (0 at p=0 and p=1)
entropy = np.zeros_like(p)
mask = (p > 0) & (p < 1)
entropy[mask] = -p[mask] * np.log2(p[mask]) - (1 - p[mask]) * np.log2(1 - p[mask])
entropy_normalized = entropy / entropy.max()

# Plot setup
sns.set_theme(
    style="whitegrid",
    rc={
        "axes.grid.axis": "y",
        "grid.alpha": 0.15,
        "grid.linewidth": 0.8,
        "axes.edgecolor": "#888888",
        "axes.linewidth": 1.2,
        "font.family": "sans-serif",
    },
)

fig, ax = plt.subplots(figsize=(16, 9))

palette = sns.color_palette(["#306998", "#E8833A"])

# Shaded region highlighting where curves diverge
ax.fill_between(p, gini_normalized, entropy_normalized, alpha=0.08, color="#306998", label="_nolegend_")

# Plot lines using seaborn with wide-form data
sns.lineplot(x=p, y=gini_normalized, color=palette[0], linewidth=3, linestyle="-", label="Gini: 2p(1−p)", ax=ax)
sns.lineplot(
    x=p,
    y=entropy_normalized,
    color=palette[1],
    linewidth=2.8,
    linestyle="--",
    label="Entropy: −p log₂p − (1−p) log₂(1−p)",
    ax=ax,
)

# Annotate maximum divergence region
divergence = np.abs(entropy_normalized - gini_normalized)
max_div_idx = np.argmax(divergence)
mid_y = (gini_normalized[max_div_idx] + entropy_normalized[max_div_idx]) / 2

ax.annotate(
    "Max divergence",
    xy=(p[max_div_idx], mid_y),
    xytext=(0.22, 0.2),
    fontsize=14,
    color="#555555",
    fontstyle="italic",
    arrowprops={"arrowstyle": "->", "color": "#999999", "lw": 1.5, "connectionstyle": "arc3,rad=0.2"},
)

# Annotate maximum impurity point at p=0.5
ax.plot(0.5, 1.0, "o", color="#333333", markersize=9, zorder=5)
ax.annotate(
    "Max impurity\np = 0.5",
    xy=(0.5, 1.0),
    xytext=(0.28, 0.85),
    fontsize=15,
    color="#333333",
    fontweight="medium",
    arrowprops={"arrowstyle": "->", "color": "#777777", "lw": 1.8, "connectionstyle": "arc3,rad=0.2"},
    bbox={"boxstyle": "round,pad=0.4", "facecolor": "#f8f8f8", "edgecolor": "#cccccc", "alpha": 0.95},
)

# Style
ax.set_xlabel("Probability (p)", fontsize=20, labelpad=12)
ax.set_ylabel("Impurity (normalized)", fontsize=20, labelpad=12)
ax.set_title("line-impurity-comparison · seaborn · pyplots.ai", fontsize=24, fontweight="medium", pad=20)
ax.tick_params(axis="both", labelsize=16)
ax.set_xlim(0, 1)
ax.set_ylim(-0.02, 1.08)

sns.despine(ax=ax, top=True, right=True)

# Legend
legend = ax.legend(
    title="Splitting Criterion",
    title_fontsize=18,
    fontsize=16,
    loc="upper right",
    framealpha=0.95,
    edgecolor="#dddddd",
    fancybox=True,
    borderpad=1.0,
)
legend.get_frame().set_linewidth(0.8)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
