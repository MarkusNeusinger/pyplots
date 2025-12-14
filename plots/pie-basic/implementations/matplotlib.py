"""
pie-basic: Basic Pie Chart
Library: matplotlib
"""

import matplotlib.pyplot as plt


# Data - Market share distribution
categories = ["Product A", "Product B", "Product C", "Product D", "Product E"]
values = [35, 25, 20, 12, 8]

# Colors - Python Blue first, then harmonious colorblind-safe colors
colors = ["#306998", "#FFD43B", "#4ECDC4", "#FF6B6B", "#95A5A6"]

# Explode the largest slice slightly for emphasis
explode = [0.05, 0, 0, 0, 0]

# Create plot (4800x2700 px)
fig, ax = plt.subplots(figsize=(16, 9))

wedges, texts, autotexts = ax.pie(
    values,
    labels=categories,
    autopct="%1.1f%%",
    explode=explode,
    colors=colors,
    startangle=90,
    textprops={"fontsize": 18},
    wedgeprops={"linewidth": 2, "edgecolor": "white"},
)

# Style percentage labels
for autotext in autotexts:
    autotext.set_fontsize(16)
    autotext.set_fontweight("bold")
    autotext.set_color("white")

# Add title
ax.set_title("pie-basic · matplotlib · pyplots.ai", fontsize=24, pad=20)

# Add legend
ax.legend(
    wedges, categories, title="Categories", loc="center left", bbox_to_anchor=(1, 0.5), fontsize=16, title_fontsize=18
)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
