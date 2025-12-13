"""
bar-basic: Basic Bar Chart
Library: seaborn
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# Data
data = pd.DataFrame(
    {
        "category": ["Electronics", "Clothing", "Home & Garden", "Sports", "Books", "Toys"],
        "value": [45200, 38100, 29500, 22800, 18400, 15600],
    }
)

# Create plot
fig, ax = plt.subplots(figsize=(16, 9))
sns.barplot(data=data, x="category", y="value", color="#306998", ax=ax)

# Add value labels on top of bars
for container in ax.containers:
    ax.bar_label(container, fmt="${:,.0f}", fontsize=14, padding=5)

# Labels and styling
ax.set_xlabel("Product Category", fontsize=20)
ax.set_ylabel("Sales ($)", fontsize=20)
ax.set_title("Product Sales by Category", fontsize=20)
ax.tick_params(axis="both", labelsize=16)
ax.grid(True, axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
