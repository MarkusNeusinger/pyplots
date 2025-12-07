"""
box-basic: Basic Box Plot
Library: seaborn
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


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

# Custom color palette using style guide colors
colors = ["#306998", "#FFD43B", "#DC2626", "#059669"]

# Create plot
fig, ax = plt.subplots(figsize=(16, 9))
sns.boxplot(
    data=data,
    x="group",
    y="value",
    hue="group",
    palette=colors,
    legend=False,
    ax=ax,
    linewidth=2,
    flierprops={"marker": "o", "markersize": 8, "alpha": 0.7},
)

# Labels and styling
ax.set_xlabel("Group", fontsize=20)
ax.set_ylabel("Value", fontsize=20)
ax.set_title("Basic Box Plot", fontsize=20)
ax.tick_params(axis="both", labelsize=16)
ax.grid(True, alpha=0.3, axis="y")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
