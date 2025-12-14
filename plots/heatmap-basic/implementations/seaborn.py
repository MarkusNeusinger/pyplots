"""
heatmap-basic: Basic Heatmap
Library: seaborn
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Data - Monthly performance metrics across departments
np.random.seed(42)
departments = ["Sales", "Marketing", "Engineering", "Support", "Finance", "HR", "Operations"]
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Generate performance data (values ranging from -50 to 100)
data = np.random.randn(len(departments), len(months)) * 30 + 50
# Add some structure to make patterns visible
data[0, :6] += 20  # Sales good first half
data[2, 6:] += 25  # Engineering good second half
data[4, :] = data[4, :] * 0.5 + 60  # Finance stable

# Plot
fig, ax = plt.subplots(figsize=(16, 9))
sns.heatmap(
    data,
    annot=True,
    fmt=".0f",
    cmap="RdBu",
    center=50,
    xticklabels=months,
    yticklabels=departments,
    linewidths=0.5,
    linecolor="white",
    cbar_kws={"label": "Performance Score", "shrink": 0.8},
    annot_kws={"fontsize": 14},
    ax=ax,
)

# Style
ax.set_xlabel("Month", fontsize=20)
ax.set_ylabel("Department", fontsize=20)
ax.set_title("heatmap-basic · seaborn · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)

# Adjust colorbar label size
cbar = ax.collections[0].colorbar
cbar.ax.tick_params(labelsize=14)
cbar.ax.set_ylabel("Performance Score", fontsize=16)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
