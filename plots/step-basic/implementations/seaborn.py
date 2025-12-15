"""
step-basic: Basic Step Plot
Library: seaborn
"""

import matplotlib.pyplot as plt
import numpy as np


# Data: Monthly cumulative sales over a year
np.random.seed(42)
months = np.arange(1, 13)
# Cumulative sales that increase in discrete jumps
monthly_increases = np.random.randint(15, 45, size=12) * 1000
cumulative_sales = np.cumsum(monthly_increases)

# Create figure (4800x2700 px at 300 dpi = 16x9 inches)
fig, ax = plt.subplots(figsize=(16, 9))

# Step plot using matplotlib's step function (seaborn uses matplotlib for line types)
ax.step(months, cumulative_sales, where="post", linewidth=3, color="#306998", label="Cumulative Sales")

# Add markers at data points to highlight where changes occur
ax.scatter(months, cumulative_sales, s=200, color="#FFD43B", edgecolor="#306998", linewidth=2, zorder=5)

# Labels and styling (scaled for 4800x2700)
ax.set_xlabel("Month", fontsize=20)
ax.set_ylabel("Cumulative Sales ($)", fontsize=20)
ax.set_title("step-basic · seaborn · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)

# Set x-axis to show all months
ax.set_xticks(months)
ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])

# Format y-axis with K notation for thousands
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x / 1000:.0f}K"))

# Grid for readability
ax.grid(True, alpha=0.3, linestyle="--")

# Legend
ax.legend(fontsize=16, loc="upper left")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
