"""pyplots.ai
pie-drilldown: Drilldown Pie Chart with Click Navigation
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 72/100 | Created: 2025-12-31
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


np.random.seed(42)

# Set seaborn style for consistent theming
sns.set_theme(style="whitegrid", palette="colorblind")

# Data - Sales hierarchy: Region -> Category breakdown
# Main level (regions)
main_labels = ["North America", "Europe", "Asia Pacific", "Latin America"]
main_values = [45000, 32000, 28000, 15000]
main_total = sum(main_values)

# Drilldown data for "North America" (shown as example of drill-down view)
drill_labels = ["Electronics", "Clothing", "Home & Garden", "Sports", "Books"]
drill_values = [18000, 12000, 8000, 4500, 2500]
drill_total = sum(drill_values)

# Use seaborn color palette
main_colors = sns.color_palette("colorblind", n_colors=len(main_labels))
drill_colors = sns.color_palette("Blues_r", n_colors=len(drill_labels))

# Create figure with two subplots showing drilldown concept
fig, axes = plt.subplots(1, 2, figsize=(16, 9))

# Left chart - Main level pie chart (all regions)
ax1 = axes[0]

# Explode the first slice to show it's selected for drilldown
explode_main = [0.08, 0, 0, 0]

_, _, autotexts1 = ax1.pie(
    main_values,
    labels=main_labels,
    colors=main_colors,
    autopct=lambda pct: f"{pct:.1f}%\n(${int(pct * main_total / 100):,})",
    explode=explode_main,
    startangle=140,
    pctdistance=0.55,
    labeldistance=1.18,
    wedgeprops={"edgecolor": "white", "linewidth": 2},
    textprops={"fontsize": 14},
)

# Style the percentage labels
for autotext in autotexts1:
    autotext.set_fontsize(12)
    autotext.set_fontweight("bold")
    autotext.set_color("white")

# Add click indicator annotation pointing to North America
ax1.annotate(
    "Click to\ndrill down",
    xy=(0.25, 0.45),
    xycoords="axes fraction",
    fontsize=12,
    ha="center",
    fontweight="bold",
    bbox={"boxstyle": "round,pad=0.4", "facecolor": "#FFD43B", "edgecolor": "#306998", "alpha": 0.9},
    arrowprops={"arrowstyle": "->", "color": "#306998", "lw": 2, "connectionstyle": "arc3,rad=0.2"},
    xytext=(0.05, 0.25),
)

ax1.set_title("All Regions", fontsize=22, fontweight="bold", pad=15)

# Right chart - Drilldown pie chart (North America breakdown)
ax2 = axes[1]

_, _, autotexts2 = ax2.pie(
    drill_values,
    labels=drill_labels,
    colors=drill_colors,
    autopct=lambda pct: f"{pct:.1f}%\n(${int(pct * drill_total / 100):,})",
    startangle=45,
    pctdistance=0.55,
    labeldistance=1.20,
    wedgeprops={"edgecolor": "white", "linewidth": 2},
    textprops={"fontsize": 14},
)

# Style the percentage labels
for autotext in autotexts2:
    autotext.set_fontsize(11)
    autotext.set_fontweight("bold")
    autotext.set_color("white")

ax2.set_title("North America Breakdown", fontsize=22, fontweight="bold", pad=15)

# Add breadcrumb trail above drilldown chart
ax2.annotate(
    "All > North America",
    xy=(0.5, 1.08),
    xycoords="axes fraction",
    fontsize=14,
    ha="center",
    bbox={"boxstyle": "round,pad=0.4", "facecolor": "#f0f0f0", "edgecolor": "#306998", "alpha": 0.9},
)

# Add back button indicator
ax2.annotate(
    "← Back",
    xy=(0.05, 1.08),
    xycoords="axes fraction",
    fontsize=13,
    ha="left",
    color="#306998",
    fontweight="bold",
    bbox={"boxstyle": "round,pad=0.3", "facecolor": "white", "edgecolor": "#306998"},
)

# Add arrow between charts to show drilldown flow
fig.patches.extend(
    [plt.Arrow(0.48, 0.5, 0.04, 0, width=0.06, transform=fig.transFigure, facecolor="#306998", edgecolor="white")]
)

# Main title
fig.suptitle("pie-drilldown · seaborn · pyplots.ai", fontsize=26, fontweight="bold", y=0.98)

# Subtitle explaining the visualization
fig.text(
    0.5,
    0.02,
    "Static representation of drilldown: Click any slice to explore subcategories",
    ha="center",
    fontsize=14,
    style="italic",
    color="#666666",
)

plt.tight_layout(rect=[0, 0.05, 1, 0.93])
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
