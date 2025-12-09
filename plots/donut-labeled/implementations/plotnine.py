"""
donut-labeled: Donut Chart with Percentage Labels
Library: plotnine

Note: plotnine does not support coord_polar() required for pie/donut charts.
This implementation uses matplotlib directly while following PyPlots.ai style.
"""

import matplotlib.pyplot as plt
import pandas as pd


# Data - departmental budget allocation
data = pd.DataFrame(
    {"category": ["Engineering", "Marketing", "Operations", "Sales", "R&D", "HR"], "value": [32, 22, 18, 14, 9, 5]}
)

# Calculate percentages
total = data["value"].sum()
data["percentage"] = data["value"] / total * 100

# PyPlots.ai color palette
colors = [
    "#306998",  # Python Blue
    "#FFD43B",  # Python Yellow
    "#DC2626",  # Signal Red
    "#059669",  # Teal Green
    "#8B5CF6",  # Violet
    "#F97316",  # Orange
]

# Create figure (16:9 aspect ratio for 4800x2700 at 300 dpi)
fig, ax = plt.subplots(figsize=(16, 9), facecolor="white")
ax.set_facecolor("white")

# Create pie chart (outer ring of donut)
wedges, texts, autotexts = ax.pie(
    data["value"],
    autopct=lambda pct: f"{pct:.1f}%",
    startangle=90,
    colors=colors[: len(data)],
    textprops={"fontsize": 16, "fontweight": "bold"},
    wedgeprops={"linewidth": 2, "edgecolor": "white", "width": 0.45},
    pctdistance=0.75,
)

# Style percentage labels for visibility
for i, autotext in enumerate(autotexts):
    autotext.set_fontsize(16)
    autotext.set_fontweight("bold")
    # Use white for dark backgrounds, dark for light backgrounds
    if colors[i] == "#FFD43B":  # Yellow needs dark text
        autotext.set_color("#333333")
    else:
        autotext.set_color("white")

# Add center circle to create donut effect (55% of radius)
center_circle = plt.Circle((0, 0), 0.55, fc="white", ec="white", linewidth=0)
ax.add_patch(center_circle)

# Add legend
ax.legend(
    wedges,
    data["category"],
    title="Department",
    loc="center left",
    bbox_to_anchor=(1.0, 0.5),
    fontsize=16,
    title_fontsize=20,
    frameon=True,
    facecolor="white",
    edgecolor="gray",
)

# Title
ax.set_title("Budget Allocation by Department", fontsize=20, fontweight="semibold", pad=20)

# Ensure circular shape
ax.set_aspect("equal")

# Adjust layout
plt.tight_layout()

# Save
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
