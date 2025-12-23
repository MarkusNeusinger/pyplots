"""pyplots.ai
heatmap-basic: Basic Heatmap
Library: seaborn | Python 3.13
Quality: pending | Created: 2025-12-23
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Data - Monthly performance metrics across departments
np.random.seed(42)
departments = ["Sales", "Marketing", "Engineering", "Support", "Finance", "HR", "Operations"]
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Generate performance data (values 0-100)
data = np.random.randn(len(departments), len(months)) * 20 + 50
# Add patterns to demonstrate heatmap capabilities
data[0, :6] += 20  # Sales strong first half
data[2, 6:] += 25  # Engineering strong second half
data[4, :] = data[4, :] * 0.3 + 70  # Finance consistently stable
data[5, 3:9] -= 15  # HR dip mid-year
# Clip to valid performance range
data = np.clip(data, 5, 95)

# Plot - using square format for heatmap
fig, ax = plt.subplots(figsize=(12, 12))
sns.heatmap(
    data,
    annot=True,
    fmt=".0f",
    cmap="RdBu",
    center=50,
    xticklabels=months,
    yticklabels=departments,
    linewidths=1,
    linecolor="white",
    cbar_kws={"label": "Performance Score", "shrink": 0.75},
    annot_kws={"fontsize": 16},
    ax=ax,
    vmin=0,
    vmax=100,
)

# Style
ax.set_xlabel("Month", fontsize=20)
ax.set_ylabel("Department", fontsize=20)
ax.set_title("heatmap-basic · seaborn · pyplots.ai", fontsize=24, pad=20)
ax.tick_params(axis="both", labelsize=16)

# Adjust colorbar label size
cbar = ax.collections[0].colorbar
cbar.ax.tick_params(labelsize=14)
cbar.ax.set_ylabel("Performance Score", fontsize=18)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
