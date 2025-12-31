""" pyplots.ai
pie-drilldown: Drilldown Pie Chart with Click Navigation
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 72/100 | Created: 2025-12-31
"""

import matplotlib.pyplot as plt


# Data - Sales hierarchy: Region -> Category breakdown
# Main level (regions)
main_categories = ["North America", "Europe", "Asia Pacific", "Latin America"]
main_values = [45000, 32000, 28000, 15000]

# Drilldown data for "North America" (shown as example)
drilldown_categories = ["Electronics", "Clothing", "Home & Garden", "Sports", "Books"]
drilldown_values = [18000, 12000, 8000, 4500, 2500]

# Colors - Python palette
main_colors = ["#306998", "#4B8BBE", "#FFD43B", "#FFE873"]
drilldown_colors = ["#306998", "#4B8BBE", "#5A9FD4", "#FFD43B", "#FFE873"]

# Create figure with two pie charts showing drilldown concept
fig, axes = plt.subplots(1, 2, figsize=(16, 9))

# Left pie - Main level (all regions)
ax1 = axes[0]
wedges1, texts1, autotexts1 = ax1.pie(
    main_values,
    labels=main_categories,
    colors=main_colors,
    autopct=lambda pct: f"{pct:.1f}%\n(${int(pct / 100 * sum(main_values)):,})",
    startangle=90,
    explode=[0.05, 0, 0, 0],  # Highlight North America
    textprops={"fontsize": 14, "fontweight": "bold"},
    wedgeprops={"linewidth": 2, "edgecolor": "white"},
    pctdistance=0.6,
)
ax1.set_title("All Regions", fontsize=22, fontweight="bold", pad=20)

# Style percentage labels
for autotext in autotexts1:
    autotext.set_fontsize(12)
    autotext.set_color("white")
    autotext.set_fontweight("bold")

# Add annotation showing this is clickable
ax1.annotate(
    "Click to drill down →",
    xy=(0.3, 0.4),
    xytext=(0.8, 0.8),
    fontsize=12,
    arrowprops={"arrowstyle": "->", "color": "#306998", "lw": 2},
    bbox={"boxstyle": "round,pad=0.3", "facecolor": "#FFD43B", "edgecolor": "#306998", "alpha": 0.9},
)

# Right pie - Drilldown view (North America breakdown)
ax2 = axes[1]
wedges2, texts2, autotexts2 = ax2.pie(
    drilldown_values,
    labels=drilldown_categories,
    colors=drilldown_colors,
    autopct=lambda pct: f"{pct:.1f}%\n(${int(pct / 100 * sum(drilldown_values)):,})",
    startangle=90,
    textprops={"fontsize": 14, "fontweight": "bold"},
    wedgeprops={"linewidth": 2, "edgecolor": "white"},
    pctdistance=0.6,
)
ax2.set_title("North America Breakdown", fontsize=22, fontweight="bold", pad=20)

# Style percentage labels
for autotext in autotexts2:
    autotext.set_fontsize(12)
    autotext.set_color("white")
    autotext.set_fontweight("bold")

# Add breadcrumb trail above drilldown chart
ax2.annotate(
    "All > North America",
    xy=(0, 1.15),
    xycoords="axes fraction",
    fontsize=14,
    ha="center",
    bbox={"boxstyle": "round,pad=0.4", "facecolor": "#f0f0f0", "edgecolor": "#306998", "alpha": 0.9},
)

# Add back button indicator
ax2.annotate(
    "← Back",
    xy=(-0.3, 1.15),
    xycoords="axes fraction",
    fontsize=12,
    ha="center",
    color="#306998",
    fontweight="bold",
    bbox={"boxstyle": "round,pad=0.3", "facecolor": "white", "edgecolor": "#306998"},
)

# Main title
fig.suptitle("pie-drilldown · seaborn · pyplots.ai", fontsize=26, fontweight="bold", y=0.98)

# Subtitle explaining the visualization
fig.text(
    0.5,
    0.02,
    "Static representation: Left shows main categories, right shows drilldown view of North America",
    ha="center",
    fontsize=14,
    style="italic",
    color="#666666",
)

plt.tight_layout(rect=[0, 0.05, 1, 0.93])
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
