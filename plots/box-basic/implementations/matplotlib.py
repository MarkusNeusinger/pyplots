""" pyplots.ai
box-basic: Basic Box Plot
Library: matplotlib 3.10.8 | Python 3.13.11
Quality: 95/100 | Created: 2025-12-14
"""

import matplotlib.pyplot as plt
import numpy as np


# Data - simulating test scores across 4 departments
np.random.seed(42)
categories = ["Engineering", "Marketing", "Sales", "Support"]
colors = ["#306998", "#FFD43B", "#4B8BBE", "#E8A838"]

# Generate realistic distribution data for each category
data = [
    np.random.normal(75, 12, 100),  # Engineering: mean 75, std 12
    np.random.normal(82, 8, 100),  # Marketing: mean 82, std 8
    np.random.normal(70, 15, 100),  # Sales: mean 70, std 15
    np.random.normal(78, 10, 100),  # Support: mean 78, std 10
]

# Create plot (4800x2700 px)
fig, ax = plt.subplots(figsize=(16, 9))

# Create box plot with custom styling
bp = ax.boxplot(
    data,
    tick_labels=categories,
    patch_artist=True,
    widths=0.6,
    flierprops={"marker": "o", "markerfacecolor": "#666666", "markersize": 8, "alpha": 0.6},
    medianprops={"color": "#333333", "linewidth": 2.5},
    whiskerprops={"linewidth": 2},
    capprops={"linewidth": 2},
)

# Apply colors to each box
for patch, color in zip(bp["boxes"], colors, strict=True):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
    patch.set_linewidth(2)

# Labels and styling
ax.set_xlabel("Department", fontsize=20)
ax.set_ylabel("Performance Score", fontsize=20)
ax.set_title("box-basic · matplotlib · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)
ax.grid(True, alpha=0.3, linestyle="--", axis="y")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
