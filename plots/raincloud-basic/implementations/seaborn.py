"""pyplots.ai
raincloud-basic: Basic Raincloud Plot
Library: seaborn | Python 3.13
Quality: pending | Created: 2025-12-24
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Data - Reaction times (ms) for different experimental conditions
np.random.seed(42)

# Generate realistic reaction time data with different distributions
control = np.random.normal(450, 60, 80)
treatment_a = np.random.normal(380, 50, 80)  # Faster, less variable
treatment_b = np.concatenate(
    [  # Bimodal - shows advantage of raincloud
        np.random.normal(350, 30, 50),
        np.random.normal(480, 40, 30),
    ]
)

data = pd.DataFrame(
    {
        "Condition": ["Control"] * len(control)
        + ["Treatment A"] * len(treatment_a)
        + ["Treatment B"] * len(treatment_b),
        "Reaction Time": np.concatenate([control, treatment_a, treatment_b]),
    }
)

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Define colors - Python Blue and Yellow first, then accessible third color
colors = ["#306998", "#FFD43B", "#4DAF4A"]

# Half-violin (the "cloud") - shifted to right side
violin_parts = ax.violinplot(
    [data[data["Condition"] == cond]["Reaction Time"].values for cond in ["Control", "Treatment A", "Treatment B"]],
    positions=[1, 2, 3],
    widths=0.6,
    showextrema=False,
    showmedians=False,
    showmeans=False,
)

# Only show right half of violins and color them
for i, body in enumerate(violin_parts["bodies"]):
    m = np.mean(body.get_paths()[0].vertices[:, 0])
    body.get_paths()[0].vertices[:, 0] = np.clip(body.get_paths()[0].vertices[:, 0], m, np.inf)
    body.set_facecolor(colors[i])
    body.set_edgecolor("black")
    body.set_linewidth(1.5)
    body.set_alpha(0.7)

# Box plot (in the middle) - narrow
box_data = [
    data[data["Condition"] == cond]["Reaction Time"].values for cond in ["Control", "Treatment A", "Treatment B"]
]
bp = ax.boxplot(box_data, positions=[1, 2, 3], widths=0.15, patch_artist=True, showfliers=False)

# Style box plots
for box, median in zip(bp["boxes"], bp["medians"], strict=True):
    box.set_facecolor("white")
    box.set_edgecolor("black")
    box.set_linewidth(2)
    median.set_color("black")
    median.set_linewidth(2.5)

for whisker in bp["whiskers"]:
    whisker.set_linewidth(2)
for cap in bp["caps"]:
    cap.set_linewidth(2)

# Jittered strip points (the "rain") - on left side
for i, (cond, color) in enumerate(zip(["Control", "Treatment A", "Treatment B"], colors, strict=True)):
    y = data[data["Condition"] == cond]["Reaction Time"].values
    x = np.ones(len(y)) * (i + 1) - 0.25 + np.random.uniform(-0.08, 0.08, len(y))
    ax.scatter(x, y, s=80, alpha=0.6, color=color, edgecolor="white", linewidth=0.5, zorder=3)

# Styling
ax.set_ylabel("Reaction Time (ms)", fontsize=20)
ax.set_xlabel("Condition", fontsize=20)
ax.set_title("raincloud-basic · seaborn · pyplots.ai", fontsize=24)

ax.set_xticks([1, 2, 3])
ax.set_xticklabels(["Control", "Treatment A", "Treatment B"], fontsize=16)
ax.tick_params(axis="y", labelsize=16)

ax.set_xlim(0.4, 3.8)
ax.grid(True, axis="y", alpha=0.3, linestyle="--")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
