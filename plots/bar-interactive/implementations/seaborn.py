"""pyplots.ai
bar-interactive: Interactive Bar Chart with Hover and Click
Library: seaborn | Python 3.13
Quality: pending | Created: 2025-01-07
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Data - Sales by product category
np.random.seed(42)
categories = ["Electronics", "Clothing", "Home & Garden", "Sports", "Books", "Toys"]
values = np.array([4850, 3200, 2750, 2100, 1850, 1450])
percentages = values / values.sum() * 100

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Create bar chart with seaborn
colors = ["#306998", "#FFD43B", "#306998", "#FFD43B", "#306998", "#FFD43B"]
sns.barplot(x=categories, y=values, hue=categories, palette=colors, legend=False, ax=ax)

# Add value labels on bars (simulating hover tooltip data)
for i, (val, pct) in enumerate(zip(values, percentages, strict=True)):
    ax.annotate(
        f"${val:,}\n({pct:.1f}%)",
        xy=(i, val),
        ha="center",
        va="bottom",
        fontsize=16,
        fontweight="bold",
        color="#333333",
    )

# Add interactivity indicator text
ax.annotate(
    "Static visualization (seaborn)\nFor interactivity, use: plotly, bokeh, altair",
    xy=(0.98, 0.98),
    xycoords="axes fraction",
    ha="right",
    va="top",
    fontsize=14,
    style="italic",
    color="#666666",
    bbox={"boxstyle": "round,pad=0.5", "facecolor": "#f0f0f0", "edgecolor": "#cccccc"},
)

# Styling
ax.set_xlabel("Product Category", fontsize=20)
ax.set_ylabel("Sales Revenue ($)", fontsize=20)
ax.set_title("bar-interactive · seaborn · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)
ax.set_ylim(0, max(values) * 1.25)
ax.grid(True, axis="y", alpha=0.3, linestyle="--")

# Remove top and right spines for cleaner look
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
