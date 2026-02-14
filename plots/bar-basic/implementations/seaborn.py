"""pyplots.ai
bar-basic: Basic Bar Chart
Library: seaborn 0.13.2 | Python 3.14
Quality: /100 | Updated: 2026-02-14
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# Style - leverage seaborn's built-in context scaling
sns.set_context("talk", font_scale=1.1)

# Data - Product sales by category (wider spread for clear ranking)
data = pd.DataFrame(
    {
        "category": ["Electronics", "Clothing", "Home & Garden", "Sports", "Books", "Toys", "Groceries", "Automotive"],
        "sales": [218, 156, 73, 134, 41, 95, 187, 62],
    }
)

# Create plot (4800x2700 px)
fig, ax = plt.subplots(figsize=(16, 9))
sns.barplot(data=data, x="category", y="sales", color="#306998", width=0.7, ax=ax)

# Value labels on top of bars
for container in ax.containers:
    ax.bar_label(container, fmt="%d", fontsize=18, fontweight="bold", padding=5)

# Labels and title
ax.set_xlabel("Product Category", fontsize=20)
ax.set_ylabel("Sales (units)", fontsize=20)
ax.set_title("bar-basic · seaborn · pyplots.ai", fontsize=24, fontweight="medium")
ax.tick_params(axis="both", labelsize=16)

# Subtle grid and clean spines
ax.yaxis.grid(True, alpha=0.2, linewidth=0.8)
ax.set_axisbelow(True)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
