""" pyplots.ai
bar-drilldown: Column Chart with Hierarchical Drilling
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 82/100 | Created: 2026-01-16
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Set random seed for reproducibility
np.random.seed(42)

# Hierarchical data: Company sales by region, country, and city
data = {
    "id": ["NA", "EU", "APAC", "USA", "CAN", "MEX", "UK", "DE", "FR", "JP", "CN", "AU", "NYC", "LA", "CHI"],
    "name": [
        "North America",
        "Europe",
        "Asia Pacific",
        "USA",
        "Canada",
        "Mexico",
        "UK",
        "Germany",
        "France",
        "Japan",
        "China",
        "Australia",
        "New York",
        "Los Angeles",
        "Chicago",
    ],
    "value": [850, 620, 530, 480, 220, 150, 230, 250, 140, 180, 230, 120, 200, 150, 130],
    "parent": [None, None, None, "NA", "NA", "NA", "EU", "EU", "EU", "APAC", "APAC", "APAC", "USA", "USA", "USA"],
}

df = pd.DataFrame(data)

# Set seaborn style with subtle grid
sns.set_style("whitegrid", {"grid.alpha": 0.3, "grid.linestyle": "--"})

# Create figure with three subplots - use constrained_layout for better spacing
fig, axes = plt.subplots(1, 3, figsize=(16, 9), constrained_layout=True)

# Use colorblind-safe palette for accessibility
cb_palette = sns.color_palette("colorblind", 10)
level1_colors = [cb_palette[0], cb_palette[1], cb_palette[2]]  # Blue, Orange, Green
level2_colors = [cb_palette[4], cb_palette[5], cb_palette[8]]  # Purple, Brown, Light Blue
level3_colors = [cb_palette[3], cb_palette[6], cb_palette[7]]  # Red, Pink, Gray

# Unified Y-axis limit across all panels for consistent comparison
y_max = 1000

# Left plot: Root level (Level 1 - Regions)
root_df = df[df["parent"].isna()].copy()
sns.barplot(
    data=root_df, x="name", y="value", hue="name", palette=level1_colors, ax=axes[0], legend=False, edgecolor="white"
)

# Add value labels and click indicators on bars
for i, (_, row) in enumerate(root_df.iterrows()):
    axes[0].text(i, row["value"] + 30, f"${row['value']}M", ha="center", va="bottom", fontsize=18, fontweight="bold")
    # Add click indicator arrow inside bar
    axes[0].annotate(
        "\u25bc", xy=(i, row["value"] * 0.12), ha="center", va="center", fontsize=20, color="white", fontweight="bold"
    )

axes[0].set_xlabel("Region", fontsize=20)
axes[0].set_ylabel("Sales ($ Millions)", fontsize=20)
axes[0].set_title("Level 1: All Regions\n\u2193 Click bar to drill down", fontsize=18, fontweight="bold", color="#333")
axes[0].tick_params(axis="both", labelsize=16)
axes[0].set_ylim(0, y_max)
axes[0].grid(True, alpha=0.3, linestyle="--")

# Middle plot: Level 2 - Drilled into North America
na_children = df[df["parent"] == "NA"].copy()
sns.barplot(
    data=na_children,
    x="name",
    y="value",
    hue="name",
    palette=level2_colors,
    ax=axes[1],
    legend=False,
    edgecolor="white",
)

for i, (_, row) in enumerate(na_children.iterrows()):
    axes[1].text(i, row["value"] + 30, f"${row['value']}M", ha="center", va="bottom", fontsize=18, fontweight="bold")
    axes[1].annotate(
        "\u25bc", xy=(i, row["value"] * 0.12), ha="center", va="center", fontsize=20, color="white", fontweight="bold"
    )

axes[1].set_xlabel("Country", fontsize=20)
axes[1].set_ylabel("Sales ($ Millions)", fontsize=20)
axes[1].set_title(
    "Level 2: All \u203a North America\n\u2193 Click bar to drill down", fontsize=18, fontweight="bold", color="#333"
)
axes[1].tick_params(axis="both", labelsize=16)
axes[1].set_ylim(0, y_max)
axes[1].grid(True, alpha=0.3, linestyle="--")

# Right plot: Level 3 - Drilled into USA (deepest level)
usa_children = df[df["parent"] == "USA"].copy()
sns.barplot(
    data=usa_children,
    x="name",
    y="value",
    hue="name",
    palette=level3_colors,
    ax=axes[2],
    legend=False,
    edgecolor="white",
)

for i, (_, row) in enumerate(usa_children.iterrows()):
    axes[2].text(i, row["value"] + 30, f"${row['value']}M", ha="center", va="bottom", fontsize=18, fontweight="bold")

axes[2].set_xlabel("City", fontsize=20)
axes[2].set_ylabel("Sales ($ Millions)", fontsize=20)
axes[2].set_title(
    "Level 3: All \u203a NA \u203a USA\n\u2714 Deepest level reached", fontsize=18, fontweight="bold", color="#333"
)
axes[2].tick_params(axis="both", labelsize=16)
axes[2].set_ylim(0, y_max)
axes[2].grid(True, alpha=0.3, linestyle="--")

# Main title
fig.suptitle("bar-drilldown \u00b7 seaborn \u00b7 pyplots.ai", fontsize=26, fontweight="bold", y=1.02)

# Add legend explaining the drilldown indicators
fig.text(
    0.5,
    -0.02,
    "\u25bc = Click to drill down  |  Colors indicate hierarchy level  |  Breadcrumb: All \u203a Region \u203a Country \u203a City",
    ha="center",
    va="top",
    fontsize=16,
    style="italic",
    color="#555",
)

plt.savefig("plot.png", dpi=300, bbox_inches="tight")
