"""pyplots.ai
pie-drilldown: Drilldown Pie Chart with Click Navigation
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 72/100 | Created: 2025-12-31
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# Set seaborn style
sns.set_theme(style="whitegrid", palette="colorblind")

# Data - Sales hierarchy: Region -> Category breakdown
# Main level (regions)
main_data = pd.DataFrame(
    {"region": ["North America", "Europe", "Asia Pacific", "Latin America"], "sales": [45000, 32000, 28000, 15000]}
)
main_data["percentage"] = main_data["sales"] / main_data["sales"].sum() * 100

# Drilldown data for "North America" (shown as example)
drilldown_data = pd.DataFrame(
    {
        "category": ["Electronics", "Clothing", "Home & Garden", "Sports", "Books"],
        "sales": [18000, 12000, 8000, 4500, 2500],
    }
)
drilldown_data["percentage"] = drilldown_data["sales"] / drilldown_data["sales"].sum() * 100

# Colors
main_colors = ["#306998", "#4B8BBE", "#FFD43B", "#FFE873"]
drilldown_colors = ["#306998", "#4B8BBE", "#5A9FD4", "#FFD43B", "#FFE873"]

# Create figure with two subplots showing drilldown concept
fig, axes = plt.subplots(1, 2, figsize=(16, 9))

# Left chart - Main level (all regions) using seaborn barplot
ax1 = axes[0]
sns.barplot(
    data=main_data,
    x="region",
    y="sales",
    hue="region",
    palette=main_colors,
    ax=ax1,
    legend=False,
    edgecolor="white",
    linewidth=2,
)

# Add value labels on bars
for i, (_idx, row) in enumerate(main_data.iterrows()):
    ax1.text(
        i,
        row["sales"] + 1000,
        f"${row['sales']:,}\n({row['percentage']:.1f}%)",
        ha="center",
        fontsize=14,
        fontweight="bold",
    )

# Highlight North America with annotation
ax1.annotate(
    "Click to\ndrill down →",
    xy=(0, main_data.iloc[0]["sales"]),
    xytext=(0.8, 40000),
    fontsize=12,
    arrowprops={"arrowstyle": "->", "color": "#306998", "lw": 2},
    bbox={"boxstyle": "round,pad=0.3", "facecolor": "#FFD43B", "edgecolor": "#306998", "alpha": 0.9},
)

ax1.set_title("All Regions", fontsize=22, fontweight="bold", pad=20)
ax1.set_xlabel("Region", fontsize=18)
ax1.set_ylabel("Sales ($)", fontsize=18)
ax1.tick_params(axis="both", labelsize=14)
ax1.set_ylim(0, 55000)

# Rotate x-axis labels for better readability
plt.setp(ax1.get_xticklabels(), rotation=15, ha="right")

# Right chart - Drilldown view (North America breakdown) using seaborn barplot
ax2 = axes[1]
sns.barplot(
    data=drilldown_data,
    x="category",
    y="sales",
    hue="category",
    palette=drilldown_colors,
    ax=ax2,
    legend=False,
    edgecolor="white",
    linewidth=2,
)

# Add value labels on bars
for i, (_idx, row) in enumerate(drilldown_data.iterrows()):
    ax2.text(
        i,
        row["sales"] + 400,
        f"${row['sales']:,}\n({row['percentage']:.1f}%)",
        ha="center",
        fontsize=14,
        fontweight="bold",
    )

ax2.set_title("North America Breakdown", fontsize=22, fontweight="bold", pad=20)
ax2.set_xlabel("Category", fontsize=18)
ax2.set_ylabel("Sales ($)", fontsize=18)
ax2.tick_params(axis="both", labelsize=14)
ax2.set_ylim(0, 22000)

# Rotate x-axis labels for better readability
plt.setp(ax2.get_xticklabels(), rotation=15, ha="right")

# Add breadcrumb trail above drilldown chart
ax2.annotate(
    "All > North America",
    xy=(0.7, 1.12),
    xycoords="axes fraction",
    fontsize=14,
    ha="center",
    bbox={"boxstyle": "round,pad=0.4", "facecolor": "#f0f0f0", "edgecolor": "#306998", "alpha": 0.9},
)

# Add back button indicator
ax2.annotate(
    "← Back",
    xy=(0.1, 1.12),
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
