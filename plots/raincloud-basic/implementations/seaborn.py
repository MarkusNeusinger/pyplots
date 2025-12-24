"""pyplots.ai
raincloud-basic: Basic Raincloud Plot
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 88/100 | Created: 2025-12-24
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


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

# Define colors - improved yellow (#E6A800) for better contrast
palette = {"Control": "#306998", "Treatment A": "#E6A800", "Treatment B": "#4DAF4A"}

# Half-violin (the "cloud") - using seaborn violinplot with split
# We use inner=None and cut=0 for clean half-violins
sns.violinplot(
    data=data,
    x="Condition",
    y="Reaction Time",
    hue="Condition",
    palette=palette,
    inner=None,
    cut=0,
    width=0.6,
    linewidth=1.5,
    alpha=0.7,
    ax=ax,
    legend=False,
)

# Clip violins to show only right half (the "cloud" effect)
for violin in ax.collections:
    if hasattr(violin, "get_paths") and violin.get_paths():
        path = violin.get_paths()[0]
        vertices = path.vertices
        m = np.mean(vertices[:, 0])
        vertices[:, 0] = np.clip(vertices[:, 0], m, np.inf)

# Box plot (in the middle) - narrow, using seaborn boxplot
sns.boxplot(
    data=data,
    x="Condition",
    y="Reaction Time",
    hue="Condition",
    palette=palette,
    width=0.15,
    showfliers=False,
    linewidth=2,
    boxprops={"facecolor": "white", "edgecolor": "black"},
    medianprops={"color": "black", "linewidth": 2.5},
    whiskerprops={"linewidth": 2},
    capprops={"linewidth": 2},
    ax=ax,
    legend=False,
)

# Jittered strip points (the "rain") - on left side using seaborn stripplot
# Shift points to the left by adjusting after plotting
order = ["Control", "Treatment A", "Treatment B"]
for i, cond in enumerate(order):
    subset = data[data["Condition"] == cond]
    y = subset["Reaction Time"].values
    # Position points to left of box (at i - 0.25)
    x = np.ones(len(y)) * i - 0.25 + np.random.uniform(-0.08, 0.08, len(y))
    ax.scatter(
        x,
        y,
        s=80,
        alpha=0.6,
        color=palette[cond],
        edgecolor="white",
        linewidth=0.5,
        zorder=3,
        label=cond if i == 0 else None,
    )

# Create custom legend
handles = [
    plt.scatter([], [], s=100, color=palette["Control"], label="Control", edgecolor="white"),
    plt.scatter([], [], s=100, color=palette["Treatment A"], label="Treatment A", edgecolor="white"),
    plt.scatter([], [], s=100, color=palette["Treatment B"], label="Treatment B", edgecolor="white"),
]
ax.legend(handles=handles, loc="upper right", fontsize=14, framealpha=0.9)

# Styling
ax.set_ylabel("Reaction Time (ms)", fontsize=20)
ax.set_xlabel("Condition", fontsize=20)
ax.set_title("raincloud-basic · seaborn · pyplots.ai", fontsize=24)

ax.tick_params(axis="both", labelsize=16)
ax.grid(True, axis="y", alpha=0.3, linestyle="--")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
