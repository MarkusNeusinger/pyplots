"""
line-basic: Basic Line Plot
Library: seaborn
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# Data
data = pd.DataFrame({"time": [1, 2, 3, 4, 5, 6, 7], "value": [10, 15, 13, 18, 22, 19, 25]})

# Create plot
fig, ax = plt.subplots(figsize=(16, 9))
sns.lineplot(data=data, x="time", y="value", ax=ax, color="#306998", linewidth=2, marker="o", markersize=8)

# Labels and styling
ax.set_xlabel("Time", fontsize=20)
ax.set_ylabel("Value", fontsize=20)
ax.set_title("Basic Line Plot", fontsize=20)
ax.tick_params(axis="both", labelsize=16)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
