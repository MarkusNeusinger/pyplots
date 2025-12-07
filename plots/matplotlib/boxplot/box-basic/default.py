"""
box-basic: Basic Box Plot
Library: matplotlib
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Data
np.random.seed(42)
data = pd.DataFrame(
    {
        "group": ["A"] * 50 + ["B"] * 50 + ["C"] * 50 + ["D"] * 50,
        "value": np.concatenate(
            [
                np.random.normal(50, 10, 50),
                np.random.normal(60, 15, 50),
                np.random.normal(45, 8, 50),
                np.random.normal(70, 20, 50),
            ]
        ),
    }
)

# Prepare data for boxplot (list of arrays, one per group)
groups = data["group"].unique()
box_data = [data[data["group"] == g]["value"].values for g in groups]

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

bp = ax.boxplot(
    box_data,
    tick_labels=groups,
    patch_artist=True,
    widths=0.6,
    flierprops={"marker": "o", "markerfacecolor": "#306998", "markersize": 6, "alpha": 0.6},
    medianprops={"color": "#DC2626", "linewidth": 2},
    whiskerprops={"color": "#306998", "linewidth": 1.5},
    capprops={"color": "#306998", "linewidth": 1.5},
    boxprops={"linewidth": 1.5},
)

# Color the boxes
colors = ["#306998", "#FFD43B", "#059669", "#8B5CF6"]
for patch, color in zip(bp["boxes"], colors, strict=False):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

# Labels and styling
ax.set_xlabel("Group", fontsize=20)
ax.set_ylabel("Value", fontsize=20)
ax.set_title("Basic Box Plot", fontsize=20)
ax.tick_params(axis="both", labelsize=16)
ax.grid(True, axis="y", alpha=0.3, linestyle="--")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
