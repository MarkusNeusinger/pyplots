""" pyplots.ai
raincloud-basic: Basic Raincloud Plot
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-25
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
    [  # Bimodal - shows advantage of raincloud over box plots
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

# Create figure - HORIZONTAL orientation: x=values, y=categories
fig, ax = plt.subplots(figsize=(16, 9))

# Define colors - colorblind-accessible palette
palette = {"Control": "#306998", "Treatment A": "#E6A800", "Treatment B": "#4DAF4A"}
order = ["Control", "Treatment A", "Treatment B"]

# Map conditions to numeric positions for manual offset control
condition_positions = {cond: i for i, cond in enumerate(order)}
data["y_pos"] = data["Condition"].map(condition_positions)

# Layout offsets: Cloud on TOP, boxplot in MIDDLE, rain BELOW
cloud_offset = 0.2
rain_offset = -0.25

# Half-violin (cloud) on TOP - using seaborn's violinplot with horizontal orientation
# We need to manually create half-violins for proper raincloud layout
for i, condition in enumerate(order):
    subset = data[data["Condition"] == condition]["Reaction Time"].values
    color = palette[condition]

    # Calculate KDE for half-violin
    n = len(subset)
    std = np.std(subset)
    bw = 1.06 * std * n ** (-1 / 5)

    x_min, x_max = subset.min() - 30, subset.max() + 30
    x_vals = np.linspace(x_min, x_max, 200)

    # Gaussian kernel density estimation
    kde_vals = np.zeros_like(x_vals)
    for point in subset:
        kde_vals += np.exp(-0.5 * ((x_vals - point) / bw) ** 2) / (bw * np.sqrt(2 * np.pi))
    kde_vals /= n

    # Normalize and scale
    kde_scaled = kde_vals / kde_vals.max() * 0.35

    # Draw half-violin (cloud) on TOP
    ax.fill_between(
        x_vals,
        i + cloud_offset,
        i + cloud_offset + kde_scaled,
        alpha=0.7,
        color=color,
        edgecolor="white",
        linewidth=1.5,
    )

# Box plot (in the middle) - horizontal orientation
sns.boxplot(
    data=data,
    x="Reaction Time",
    y="Condition",
    hue="Condition",
    palette=palette,
    order=order,
    width=0.12,
    showfliers=False,
    linewidth=2,
    boxprops={"facecolor": "white", "edgecolor": "black"},
    medianprops={"color": "black", "linewidth": 2.5},
    whiskerprops={"linewidth": 2},
    capprops={"linewidth": 2},
    ax=ax,
    legend=False,
)

# Jittered strip points (rain) BELOW
for i, condition in enumerate(order):
    subset = data[data["Condition"] == condition]["Reaction Time"].values
    color = palette[condition]

    # Add jitter
    jitter = np.random.uniform(-0.06, 0.06, len(subset))

    ax.scatter(
        subset,
        i + rain_offset + jitter,
        s=70,
        alpha=0.6,
        color=color,
        edgecolor="white",
        linewidth=0.5,
        zorder=3,
    )

# Create custom legend
handles = [
    plt.scatter([], [], s=100, color=palette["Control"], label="Control", edgecolor="white"),
    plt.scatter([], [], s=100, color=palette["Treatment A"], label="Treatment A", edgecolor="white"),
    plt.scatter([], [], s=100, color=palette["Treatment B"], label="Treatment B", edgecolor="white"),
]
ax.legend(handles=handles, loc="upper right", fontsize=14, framealpha=0.9)

# Styling - HORIZONTAL orientation labels
ax.set_xlabel("Reaction Time (ms)", fontsize=20)
ax.set_ylabel("Condition", fontsize=20)
ax.set_title("raincloud-basic · seaborn · pyplots.ai", fontsize=24)

ax.tick_params(axis="both", labelsize=16)
ax.grid(True, axis="x", alpha=0.3, linestyle="--")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Adjust y-axis limits for cloud and rain visibility
ax.set_ylim(-0.6, 2.8)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
