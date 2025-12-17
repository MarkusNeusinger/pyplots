"""
pyramid-basic: Basic Pyramid Chart
Library: matplotlib
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter


# Data - Population pyramid by age group
age_groups = ["0-9", "10-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80+"]
male = np.array([48, 52, 58, 62, 55, 50, 42, 28, 12])
female = np.array([46, 50, 56, 60, 57, 52, 45, 35, 18])

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

y = np.arange(len(age_groups))
bar_height = 0.7

# Left bars (male) - extend to the left (negative values)
ax.barh(y, -male, height=bar_height, color="#306998", label="Male", edgecolor="white", linewidth=1)

# Right bars (female) - extend to the right (positive values)
ax.barh(y, female, height=bar_height, color="#FFD43B", label="Female", edgecolor="white", linewidth=1)

# Styling
ax.set_yticks(y)
ax.set_yticklabels(age_groups)
ax.set_xlabel("Population (millions)", fontsize=20)
ax.set_ylabel("Age Group", fontsize=20)
ax.set_title("Population Pyramid · pyramid-basic · matplotlib · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)

# Symmetric x-axis for fair comparison
max_val = max(male.max(), female.max())
ax.set_xlim(-max_val * 1.15, max_val * 1.15)

# Format x-ticks to show absolute values
ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{abs(int(x))}"))

# Add center line
ax.axvline(x=0, color="gray", linewidth=1.5, alpha=0.5)

# Legend
ax.legend(fontsize=16, loc="upper right")

# Grid
ax.grid(True, alpha=0.3, linestyle="--", axis="x")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
