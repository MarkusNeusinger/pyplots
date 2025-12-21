""" pyplots.ai
donut-basic: Basic Donut Chart
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-14
"""

import matplotlib.pyplot as plt
import seaborn as sns


# Set seaborn style for clean aesthetics
sns.set_style("whitegrid")
sns.set_context("talk", font_scale=1.2)

# Data - budget allocation example
categories = ["Marketing", "Operations", "Development", "Sales", "Support"]
values = [25, 20, 30, 15, 10]
total = sum(values)

# Colors using Python Blue as primary, then colorblind-safe palette
colors = ["#306998", "#FFD43B", "#4ECDC4", "#FF6B6B", "#9B59B6"]

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Create pie chart with hole in center for donut effect
wedges, texts, autotexts = ax.pie(
    values,
    labels=categories,
    colors=colors,
    autopct=lambda pct: f"{pct:.1f}%",
    startangle=90,
    pctdistance=0.75,
    wedgeprops={"width": 0.5, "edgecolor": "white", "linewidth": 2},
    textprops={"fontsize": 18},
)

# Style percentage labels
for autotext in autotexts:
    autotext.set_fontsize(16)
    autotext.set_fontweight("bold")
    autotext.set_color("white")

# Add center text with total
ax.text(0, 0, f"Total\n${total}K", ha="center", va="center", fontsize=28, fontweight="bold", color="#306998")

# Equal aspect ratio ensures circular shape
ax.set_aspect("equal")

# Title
ax.set_title("donut-basic · seaborn · pyplots.ai", fontsize=24, fontweight="bold", pad=20)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
