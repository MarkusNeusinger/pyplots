"""
pie-basic: Basic Pie Chart
Library: seaborn

Note: Seaborn does not have a native pie chart function. This implementation uses
matplotlib's pie chart with seaborn's styling context for consistent aesthetics.
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# PyPlots.ai color palette
PYPLOTS_COLORS = [
    "#306998",  # Python Blue
    "#FFD43B",  # Python Yellow
    "#DC2626",  # Signal Red
    "#059669",  # Teal Green
    "#8B5CF6",  # Violet
    "#F97316",  # Orange
]

# Data from spec
data = pd.DataFrame(
    {"category": ["Product A", "Product B", "Product C", "Product D", "Other"], "value": [35, 25, 20, 15, 5]}
)

# Set seaborn style for consistent aesthetics
sns.set_theme(style="white")

# Create figure (16:9 aspect ratio for 4800x2700 at 300 DPI)
fig, ax = plt.subplots(figsize=(16, 9))

# Extract data
categories = data["category"].tolist()
values = data["value"].tolist()

# Use PyPlots colors
colors = PYPLOTS_COLORS[: len(categories)]

# Create pie chart
wedges, texts, autotexts = ax.pie(
    values,
    autopct="%1.1f%%",
    startangle=90,
    colors=colors,
    wedgeprops={"edgecolor": "white", "linewidth": 2},
    textprops={"fontsize": 16},
    pctdistance=0.7,
)

# Style percentage labels
for autotext in autotexts:
    autotext.set_fontsize(16)
    autotext.set_fontweight("bold")
    autotext.set_color("white")

# Ensure circular shape
ax.set_aspect("equal")

# Add legend
ax.legend(
    wedges,
    categories,
    title="Category",
    loc="center left",
    bbox_to_anchor=(1.0, 0.5),
    fontsize=16,
    title_fontsize=16,
    frameon=True,
    facecolor="white",
    edgecolor="gray",
)

# Title
ax.set_title("Market Share Distribution", fontsize=20, fontweight="semibold", pad=20)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
