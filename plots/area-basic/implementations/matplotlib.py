"""
area-basic: Basic Area Chart
Library: matplotlib
"""

import matplotlib.pyplot as plt
import pandas as pd


# Data - Monthly sales from spec
data = pd.DataFrame(
    {
        "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        "sales": [120, 135, 148, 162, 175, 195, 210, 198, 185, 170, 158, 190],
    }
)

# Create plot
fig, ax = plt.subplots(figsize=(16, 9))

# Plot area chart - use numeric x-axis for proper fill_between
x = range(len(data))
ax.fill_between(x, data["sales"], alpha=0.5, color="#306998")
ax.plot(x, data["sales"], color="#306998", linewidth=2)

# Set x-tick labels to month names
ax.set_xticks(x)
ax.set_xticklabels(data["month"])

# Labels and styling
ax.set_xlabel("Month", fontsize=20)
ax.set_ylabel("Sales", fontsize=20)
ax.set_title("Basic Area Chart", fontsize=20)
ax.tick_params(axis="both", labelsize=16)
ax.grid(True, alpha=0.3, linestyle="--")

# Set y-axis to start from 0 for proper area representation
ax.set_ylim(bottom=0)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
