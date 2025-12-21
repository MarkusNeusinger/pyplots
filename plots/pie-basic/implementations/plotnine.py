""" pyplots.ai
pie-basic: Basic Pie Chart
Library: plotnine 0.15.1 | Python 3.13.11
Quality: 88/100 | Created: 2025-12-14
"""

import matplotlib.pyplot as plt
import pandas as pd


# Data - Market share distribution
data = pd.DataFrame(
    {"category": ["Product A", "Product B", "Product C", "Product D", "Product E"], "value": [35, 25, 20, 12, 8]}
)

# Colors - Python Blue first, then colorblind-safe palette
colors = ["#306998", "#FFD43B", "#4ECDC4", "#E76F51", "#9B59B6"]

# Explode the largest slice slightly for emphasis
explode = [0.05, 0, 0, 0, 0]

# Create figure with plotnine-style sizing
fig, ax = plt.subplots(figsize=(16, 9))

# Create pie chart
wedges, texts, autotexts = ax.pie(
    data["value"],
    labels=data["category"],
    colors=colors,
    explode=explode,
    autopct="%1.1f%%",
    startangle=90,
    pctdistance=0.6,
    labeldistance=1.15,
)

# Style text elements for 4800x2700 canvas
for text in texts:
    text.set_fontsize(18)
for autotext in autotexts:
    autotext.set_fontsize(16)
    autotext.set_fontweight("bold")
    autotext.set_color("white")

# Title in pyplots format
ax.set_title("pie-basic · plotnine · pyplots.ai", fontsize=24, fontweight="bold", pad=20)

# Add legend
ax.legend(
    wedges,
    data["category"],
    title="Category",
    loc="center left",
    bbox_to_anchor=(1, 0.5),
    fontsize=16,
    title_fontsize=18,
)

# Equal aspect ratio ensures circular pie
ax.set_aspect("equal")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
