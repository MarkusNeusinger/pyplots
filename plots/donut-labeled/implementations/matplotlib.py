"""
donut-labeled: Donut Chart with Percentage Labels
Library: matplotlib
"""

import matplotlib.pyplot as plt


# Data - Department budget allocation
categories = ["Marketing", "Engineering", "Operations", "Sales", "HR", "R&D"]
values = [25, 30, 15, 18, 7, 5]

# Colors from style guide palette
colors = ["#306998", "#FFD43B", "#DC2626", "#059669", "#8B5CF6", "#F97316"]

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Create donut chart with wedgeprops for inner radius (donut hole)
wedges, texts, autotexts = ax.pie(
    values,
    labels=None,
    autopct="%1.1f%%",
    startangle=90,
    colors=colors,
    wedgeprops={"width": 0.45, "edgecolor": "white", "linewidth": 2},
    pctdistance=0.75,
    textprops={"fontsize": 16, "fontweight": "bold", "color": "white"},
)

# Style percentage labels
for autotext in autotexts:
    autotext.set_fontsize(16)
    autotext.set_fontweight("bold")

# Add legend
ax.legend(
    wedges,
    categories,
    title="Department",
    loc="center left",
    bbox_to_anchor=(1, 0, 0.5, 1),
    fontsize=16,
    title_fontsize=18,
)

# Title
ax.set_title("Department Budget Allocation", fontsize=20, fontweight="bold", pad=20)

# Equal aspect ratio ensures circular shape
ax.set_aspect("equal")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
