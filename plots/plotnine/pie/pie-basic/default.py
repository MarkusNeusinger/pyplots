"""
pie-basic: Basic Pie Chart
Library: plotnine

Note: plotnine does not support coord_polar() required for pie charts.
This implementation uses matplotlib directly while following PyPlots.ai style.
"""

import matplotlib.pyplot as plt
import pandas as pd


# Data
data = pd.DataFrame(
    {"category": ["Product A", "Product B", "Product C", "Product D", "Other"], "value": [35, 25, 20, 15, 5]}
)

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

# Create pie chart
wedges, texts, autotexts = ax.pie(
    data["value"],
    autopct="%1.1f%%",
    startangle=90,
    colors=colors[: len(data)],
    textprops={"fontsize": 16, "fontweight": "bold", "color": "white"},
    wedgeprops={"linewidth": 2, "edgecolor": "white"},
)

# Style percentage labels
for autotext in autotexts:
    autotext.set_fontsize(16)
    autotext.set_fontweight("bold")
    autotext.set_color("white")

# Add legend
ax.legend(
    wedges,
    data["category"],
    title="Category",
    loc="center left",
    bbox_to_anchor=(1.0, 0.5),
    fontsize=16,
    title_fontsize=20,
    frameon=True,
    facecolor="white",
    edgecolor="gray",
)

# Title
ax.set_title("Basic Pie Chart", fontsize=20, fontweight="semibold", pad=20)

# Ensure circular shape
ax.set_aspect("equal")

# Adjust layout
plt.tight_layout()

# Save
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
