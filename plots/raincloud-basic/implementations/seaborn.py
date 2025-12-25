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

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Define colors - colorblind-accessible palette
palette = {"Control": "#306998", "Treatment A": "#E6A800", "Treatment B": "#4DAF4A"}
order = ["Control", "Treatment A", "Treatment B"]

# Half-violin (the "cloud") - on right side using split parameter
# seaborn's violinplot with split=True creates half-violins when combined with hue
# We'll create a dummy split variable to achieve this effect
data["Side"] = "right"  # All on one side for half-violin effect

sns.violinplot(
    data=data,
    x="Condition",
    y="Reaction Time",
    hue="Side",
    palette=["#306998"],  # Will be overridden per category
    order=order,
    inner=None,
    cut=0,
    width=0.6,
    linewidth=1.5,
    split=True,
    ax=ax,
    legend=False,
)

# Color each violin properly since split only allows single hue
for i, condition in enumerate(order):
    # Find the violin collection for this condition
    for collection in ax.collections:
        if hasattr(collection, "get_paths") and collection.get_paths():
            path = collection.get_paths()[0]
            vertices = path.vertices
            center_x = i  # The x position of this category
            # Check if this collection belongs to this category
            if np.abs(np.mean(vertices[:, 0]) - center_x) < 0.5:
                collection.set_facecolor(palette[condition])
                collection.set_alpha(0.7)
                # Clip to right half (cloud on right side)
                vertices[:, 0] = np.clip(vertices[:, 0], center_x, np.inf)
                break

# Box plot (in the middle) - narrow box showing summary statistics
sns.boxplot(
    data=data,
    x="Condition",
    y="Reaction Time",
    hue="Condition",
    palette=palette,
    order=order,
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

# Jittered strip points (the "rain") - on left side
sns.stripplot(
    data=data,
    x="Condition",
    y="Reaction Time",
    hue="Condition",
    palette=palette,
    order=order,
    size=7,
    alpha=0.6,
    jitter=0.08,
    edgecolor="white",
    linewidth=0.5,
    ax=ax,
    zorder=3,
    legend=False,
)

# Shift strip points to the left (the "rain" below the cloud)
point_collections = [c for c in ax.collections if hasattr(c, "get_offsets") and len(c.get_offsets()) > 0]

# The strip collections are the last 3 added (one per condition)
n_conditions = len(order)
for collection in point_collections[-n_conditions:]:
    offsets = collection.get_offsets().copy()
    if len(offsets) > 0:
        # Shift x coordinates to the left by 0.25
        offsets[:, 0] = offsets[:, 0] - 0.25
        collection.set_offsets(offsets)

# Create custom legend - positioned at upper left to avoid overlap with clouds
handles = [
    plt.scatter([], [], s=100, color=palette["Control"], label="Control", edgecolor="white"),
    plt.scatter([], [], s=100, color=palette["Treatment A"], label="Treatment A", edgecolor="white"),
    plt.scatter([], [], s=100, color=palette["Treatment B"], label="Treatment B", edgecolor="white"),
]
ax.legend(handles=handles, loc="upper left", fontsize=14, framealpha=0.9)

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
