"""pyplots.ai
raincloud-basic: Basic Raincloud Plot
Library: matplotlib | Python 3.13
Quality: pending | Created: 2025-12-24
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch


# Data: Reaction times (ms) for three experimental conditions
np.random.seed(42)

# Control group: Normal distribution centered around 350ms
control = np.random.normal(350, 50, 80)

# Treatment A: Faster responses, slightly bimodal
treatment_a = np.concatenate([np.random.normal(280, 30, 50), np.random.normal(320, 20, 30)])

# Treatment B: Mixed results with some outliers
treatment_b = np.concatenate(
    [
        np.random.normal(300, 40, 60),
        np.random.normal(400, 25, 15),  # Slower subgroup
        np.array([500, 520, 480]),  # Outliers
    ]
)

categories = ["Control", "Treatment A", "Treatment B"]
data = [control, treatment_a, treatment_b]
colors = ["#306998", "#FFD43B", "#4CAF50"]

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Offset parameters
box_width = 0.12
jitter_offset = 0.2

for i, (d, color) in enumerate(zip(data, colors, strict=True)):
    pos = i + 1

    # Calculate KDE for half-violin (Silverman's rule for bandwidth)
    n = len(d)
    std = np.std(d)
    bw = 1.06 * std * n ** (-1 / 5)

    y_min, y_max = d.min() - 30, d.max() + 30
    y_vals = np.linspace(y_min, y_max, 200)

    # Gaussian kernel density estimation
    kde_vals = np.zeros_like(y_vals)
    for point in d:
        kde_vals += np.exp(-0.5 * ((y_vals - point) / bw) ** 2) / (bw * np.sqrt(2 * np.pi))
    kde_vals /= n

    # Normalize and scale violin width
    kde_scaled = kde_vals / kde_vals.max() * 0.35

    # Draw half-violin (cloud) on the left side
    ax.fill_betweenx(y_vals, pos - kde_scaled, pos, alpha=0.7, color=color, edgecolor="white", linewidth=1.5)

    # Draw box plot in the middle (narrow)
    bp = ax.boxplot([d], positions=[pos], widths=box_width, vert=True, patch_artist=True, showfliers=False, zorder=3)

    # Style box plot
    bp["boxes"][0].set_facecolor("white")
    bp["boxes"][0].set_edgecolor("#333333")
    bp["boxes"][0].set_linewidth(2)
    bp["medians"][0].set_color("#333333")
    bp["medians"][0].set_linewidth(2.5)
    bp["whiskers"][0].set_color("#333333")
    bp["whiskers"][0].set_linewidth(1.5)
    bp["whiskers"][1].set_color("#333333")
    bp["whiskers"][1].set_linewidth(1.5)
    bp["caps"][0].set_color("#333333")
    bp["caps"][0].set_linewidth(1.5)
    bp["caps"][1].set_color("#333333")
    bp["caps"][1].set_linewidth(1.5)

    # Draw jittered points (rain) on the right side
    jitter = np.random.uniform(-0.05, 0.05, len(d))
    ax.scatter(
        pos + jitter_offset + jitter, d, s=80, alpha=0.6, color=color, edgecolor="white", linewidth=0.5, zorder=2
    )

# Styling
ax.set_xticks([1, 2, 3])
ax.set_xticklabels(categories, fontsize=18)
ax.set_ylabel("Reaction Time (ms)", fontsize=20)
ax.set_xlabel("Experimental Condition", fontsize=20)
ax.set_title("raincloud-basic · matplotlib · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)

# Set y-axis range with padding
all_data = np.concatenate(data)
ax.set_ylim(all_data.min() - 40, all_data.max() + 40)
ax.set_xlim(0.3, 3.7)

# Subtle grid on y-axis only
ax.yaxis.grid(True, alpha=0.3, linestyle="--")
ax.set_axisbelow(True)

# Custom legend
legend_elements = [
    Patch(facecolor=c, edgecolor="white", alpha=0.7, label=cat) for c, cat in zip(colors, categories, strict=True)
]
ax.legend(handles=legend_elements, fontsize=16, loc="upper right", framealpha=0.9, edgecolor="none")

# Clean up spines
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_linewidth(1.5)
ax.spines["bottom"].set_linewidth(1.5)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
