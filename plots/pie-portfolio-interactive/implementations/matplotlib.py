""" pyplots.ai
pie-portfolio-interactive: Interactive Portfolio Allocation Chart
Library: matplotlib 3.10.8 | Python 3.13.11
Quality: 88/100 | Created: 2026-01-20
"""

import matplotlib.pyplot as plt
import numpy as np


# Data - Portfolio allocation with asset classes
np.random.seed(42)

# Main asset categories with sub-holdings
categories = {
    "Equities": {"US Large Cap": 25.0, "International": 15.0, "Emerging Markets": 8.0},
    "Fixed Income": {"Government Bonds": 18.0, "Corporate Bonds": 12.0},
    "Alternatives": {"Real Estate": 10.0, "Commodities": 7.0},
    "Cash": {"Money Market": 5.0},
}

# Flatten for outer ring (individual holdings)
holdings = []
weights = []
category_colors = []
category_names = []

# Color scheme by asset class (colorblind-safe)
color_map = {
    "Equities": ["#306998", "#4A8BC2", "#6AA7D6"],  # Blues
    "Fixed Income": ["#2E8B57", "#3CB371"],  # Greens
    "Alternatives": ["#CD853F", "#D2691E"],  # Browns/oranges
    "Cash": ["#708090"],  # Gray
}

for category, assets in categories.items():
    for asset, weight in assets.items():
        holdings.append(asset)
        weights.append(weight)
        colors = color_map[category]
        idx = list(assets.keys()).index(asset)
        category_colors.append(colors[idx % len(colors)])
        category_names.append(category)

# Category totals for inner ring
category_totals = {cat: sum(assets.values()) for cat, assets in categories.items()}
cat_labels = list(category_totals.keys())
cat_weights = list(category_totals.values())
cat_colors = ["#306998", "#2E8B57", "#CD853F", "#708090"]

# Create plot
fig, ax = plt.subplots(figsize=(12, 12))

# Outer ring - individual holdings
outer_wedges, outer_texts, outer_autotexts = ax.pie(
    weights,
    labels=holdings,
    colors=category_colors,
    autopct=lambda pct: f"{pct:.1f}%" if pct > 5 else "",
    pctdistance=0.85,
    labeldistance=1.15,
    startangle=90,
    radius=1.0,
    wedgeprops={"linewidth": 2, "edgecolor": "white", "width": 0.4},
    textprops={"fontsize": 14},
)

# Style autopct text
for autotext in outer_autotexts:
    autotext.set_fontsize(12)
    autotext.set_fontweight("bold")
    autotext.set_color("white")

# Inner ring - asset categories
inner_wedges, inner_texts, inner_autotexts = ax.pie(
    cat_weights,
    labels=None,
    colors=cat_colors,
    autopct=lambda pct: f"{pct:.0f}%",
    pctdistance=0.75,
    startangle=90,
    radius=0.6,
    wedgeprops={"linewidth": 2, "edgecolor": "white", "width": 0.35},
    textprops={"fontsize": 16, "fontweight": "bold"},
)

# Style inner autopct text
for autotext in inner_autotexts:
    autotext.set_fontsize(14)
    autotext.set_fontweight("bold")
    autotext.set_color("white")

# Add center text
ax.text(0, 0, "Portfolio\nAllocation", ha="center", va="center", fontsize=18, fontweight="bold")

# Create legend for categories
legend_handles = [plt.Rectangle((0, 0), 1, 1, facecolor=color, edgecolor="white", linewidth=2) for color in cat_colors]
legend_labels = [f"{cat} ({weight:.0f}%)" for cat, weight in zip(cat_labels, cat_weights, strict=True)]
ax.legend(
    legend_handles, legend_labels, loc="lower center", bbox_to_anchor=(0.5, -0.08), ncol=4, fontsize=14, frameon=False
)

ax.set_title("pie-portfolio-interactive · matplotlib · pyplots.ai", fontsize=24, fontweight="bold", pad=20)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
