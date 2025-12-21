""" pyplots.ai
bar-basic: Basic Bar Chart
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 94/100 | Created: 2025-12-13
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# Data - Product sales by category
data = pd.DataFrame(
    {
        "category": ["Electronics", "Clothing", "Home & Garden", "Sports", "Books", "Toys"],
        "value": [145, 98, 76, 112, 54, 89],
    }
)

# Create plot (4800x2700 px)
fig, ax = plt.subplots(figsize=(16, 9))
sns.barplot(data=data, x="category", y="value", color="#306998", width=0.7, ax=ax)

# Add value labels on top of bars
for container in ax.containers:
    ax.bar_label(container, fmt="%d", fontsize=18, fontweight="bold", padding=5)

# Labels and styling
ax.set_xlabel("Product Category", fontsize=20)
ax.set_ylabel("Sales (units)", fontsize=20)
ax.set_title("bar-basic · seaborn · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)
ax.grid(True, axis="y", alpha=0.3, linestyle="--")

# Remove top and right spines for cleaner look
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
