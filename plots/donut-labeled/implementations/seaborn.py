"""
donut-labeled: Donut Chart with Percentage Labels
Library: seaborn
"""

import matplotlib.pyplot as plt
import numpy as np


# Data - Department budget allocation
categories = ["Engineering", "Marketing", "Operations", "Sales", "HR", "R&D"]
values = [35, 20, 15, 15, 8, 7]

# Color palette (from style guide)
colors = ["#306998", "#FFD43B", "#DC2626", "#059669", "#8B5CF6", "#F97316"]

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Create donut chart using matplotlib's pie with wedgeprops
wedges, texts = ax.pie(
    values, colors=colors, wedgeprops={"width": 0.45, "edgecolor": "white", "linewidth": 2}, startangle=90
)

# Add percentage labels on each segment
total = sum(values)
for i, (wedge, value) in enumerate(zip(wedges, values, strict=True)):
    # Calculate angle for label position
    angle = (wedge.theta2 + wedge.theta1) / 2
    # Position label in the middle of the wedge
    x = 0.725 * np.cos(np.radians(angle))
    y = 0.725 * np.sin(np.radians(angle))

    # Calculate percentage
    percentage = value / total * 100

    # Add percentage label
    ax.annotate(
        f"{percentage:.0f}%",
        xy=(x, y),
        ha="center",
        va="center",
        fontsize=16,
        fontweight="bold",
        color="white" if i in [0, 2, 4] else "black",
    )

# Add legend
ax.legend(
    wedges, categories, title="Department", loc="center left", bbox_to_anchor=(1, 0.5), fontsize=16, title_fontsize=18
)

# Title
ax.set_title("Budget Allocation by Department", fontsize=20, fontweight="bold", pad=20)

# Equal aspect ratio ensures the pie is drawn as a circle
ax.set_aspect("equal")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
