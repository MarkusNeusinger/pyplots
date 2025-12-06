"""
bar-basic: Basic Bar Chart
Library: seaborn
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# Data
data = pd.DataFrame(
    {"category": ["Product A", "Product B", "Product C", "Product D", "Product E"], "value": [45, 78, 52, 91, 63]}
)

# Create plot
fig, ax = plt.subplots(figsize=(16, 9))
sns.barplot(
    data=data,
    x="category",
    y="value",
    hue="category",
    palette=["#306998", "#FFD43B", "#DC2626", "#059669", "#8B5CF6"],
    legend=False,
    ax=ax,
)

# Labels and styling
ax.set_xlabel("Category", fontsize=20)
ax.set_ylabel("Value", fontsize=20)
ax.set_title("Basic Bar Chart", fontsize=20)
ax.tick_params(axis="both", labelsize=16)
ax.yaxis.grid(True, alpha=0.3)
ax.set_axisbelow(True)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
