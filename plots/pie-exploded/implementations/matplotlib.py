"""pyplots.ai
pie-exploded: Exploded Pie Chart
Library: matplotlib | Python 3.13
Quality: pending | Created: 2025-12-25
"""

import matplotlib.pyplot as plt


# Data - Market share analysis with leading company emphasized
categories = ["TechCorp", "DataSoft", "CloudNet", "AIVentures", "Others"]
values = [35, 25, 18, 12, 10]
explode = [0.1, 0, 0, 0, 0]  # Explode the market leader

# Colors - Python Blue first, then colorblind-safe palette
colors = ["#306998", "#FFD43B", "#4DAF4A", "#984EA3", "#FF7F00"]

# Create plot - square format for pie chart
fig, ax = plt.subplots(figsize=(12, 12))

wedges, texts, autotexts = ax.pie(
    values,
    explode=explode,
    labels=categories,
    colors=colors,
    autopct="%1.1f%%",
    startangle=90,
    wedgeprops={"linewidth": 2, "edgecolor": "white"},
    textprops={"fontsize": 20},
    pctdistance=0.6,
)

# Style percentage labels
for autotext in autotexts:
    autotext.set_fontsize(18)
    autotext.set_fontweight("bold")
    autotext.set_color("white")

# Title
ax.set_title("pie-exploded · matplotlib · pyplots.ai", fontsize=24, fontweight="bold", pad=20)

# Legend
ax.legend(
    wedges, categories, title="Companies", loc="center left", bbox_to_anchor=(1, 0.5), fontsize=16, title_fontsize=18
)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
