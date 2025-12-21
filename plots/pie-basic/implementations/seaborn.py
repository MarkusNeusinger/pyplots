""" pyplots.ai
pie-basic: Basic Pie Chart
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 100/100 | Created: 2025-12-14
"""

import matplotlib.pyplot as plt
import seaborn as sns


# Set seaborn style for aesthetics
sns.set_theme(style="whitegrid")

# Data - Market share distribution (5 categories, good for pie chart)
categories = ["Product A", "Product B", "Product C", "Product D", "Product E"]
values = [35, 25, 20, 12, 8]

# Colors - Python Blue first, then colorblind-safe palette
colors = ["#306998", "#FFD43B", "#4ECDC4", "#FF6B6B", "#95E1D3"]

# Slight explosion for emphasis on largest slice
explode = [0.05, 0, 0, 0, 0]

# Create figure (4800x2700 px at 300 dpi)
fig, ax = plt.subplots(figsize=(16, 9))

# Create pie chart
wedges, texts, autotexts = ax.pie(
    values,
    labels=categories,
    autopct="%1.1f%%",
    startangle=90,
    explode=explode,
    colors=colors,
    wedgeprops={"edgecolor": "white", "linewidth": 2},
    textprops={"fontsize": 18},
    pctdistance=0.6,
)

# Style percentage labels
for autotext in autotexts:
    autotext.set_fontsize(16)
    autotext.set_fontweight("bold")
    autotext.set_color("white")

# Style category labels
for text in texts:
    text.set_fontsize(18)

# Equal aspect ratio ensures circular pie
ax.set_aspect("equal")

# Title
ax.set_title("pie-basic · seaborn · pyplots.ai", fontsize=24, fontweight="bold", pad=20)

# Legend
ax.legend(
    wedges,
    [f"{cat}: {val}%" for cat, val in zip(categories, values, strict=True)],
    title="Categories",
    loc="center left",
    bbox_to_anchor=(1.0, 0.5),
    fontsize=16,
    title_fontsize=18,
)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, facecolor="white", edgecolor="none")
