"""
donut-basic: Basic Donut Chart
Library: plotnine

Note: plotnine doesn't support coord_polar for pie/donut charts.
Using matplotlib directly with plotnine-style aesthetics.
"""

import matplotlib.pyplot as plt
import pandas as pd


# Data - Budget allocation example
data = pd.DataFrame(
    {
        "category": ["Housing", "Food", "Transport", "Entertainment", "Savings", "Utilities"],
        "value": [1800, 600, 400, 300, 500, 200],
    }
)

# Calculate total for center label
total = data["value"].sum()

# Colors - Python Blue first, then colorblind-safe palette
colors = ["#306998", "#FFD43B", "#4ECDC4", "#E76F51", "#9B59B6", "#3498DB"]

# Create figure with plotnine-style sizing
fig, ax = plt.subplots(figsize=(16, 9))

# Create pie chart (will become donut with center circle)
wedges, texts, autotexts = ax.pie(
    data["value"],
    labels=data["category"],
    colors=colors,
    autopct="%1.1f%%",
    startangle=90,
    pctdistance=0.75,
    labeldistance=1.15,
    wedgeprops={"width": 0.5, "edgecolor": "white", "linewidth": 2},
)

# Style text elements for 4800x2700 canvas
for text in texts:
    text.set_fontsize(18)
for autotext in autotexts:
    autotext.set_fontsize(14)
    autotext.set_fontweight("bold")
    autotext.set_color("white")

# Add center circle for donut effect with total value
center_circle = plt.Circle((0, 0), 0.35, fc="white")
ax.add_patch(center_circle)

# Add text in center showing total
ax.text(0, 0.05, "Total", ha="center", va="center", fontsize=20, fontweight="bold", color="#306998")
ax.text(0, -0.12, f"${total:,}", ha="center", va="center", fontsize=24, fontweight="bold", color="#306998")

# Title in pyplots format
ax.set_title("donut-basic · plotnine · pyplots.ai", fontsize=24, fontweight="bold", pad=20)

# Equal aspect ratio ensures circular donut
ax.set_aspect("equal")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
