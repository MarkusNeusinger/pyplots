"""
bar-basic: Basic Bar Chart
Library: matplotlib
"""

import matplotlib.pyplot as plt
import pandas as pd


# Data
data = pd.DataFrame(
    {"category": ["Product A", "Product B", "Product C", "Product D", "Product E"], "value": [45, 78, 52, 91, 63]}
)

# Create plot
fig, ax = plt.subplots(figsize=(16, 9))
ax.bar(data["category"], data["value"], color="#306998", edgecolor="white", linewidth=1)

# Labels and styling
ax.set_xlabel("Category", fontsize=20)
ax.set_ylabel("Value", fontsize=20)
ax.set_title("Basic Bar Chart", fontsize=20)
ax.tick_params(axis="both", labelsize=16)
ax.grid(axis="y", alpha=0.3)
ax.set_axisbelow(True)
ax.set_ylim(bottom=0)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
