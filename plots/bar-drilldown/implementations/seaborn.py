""" pyplots.ai
bar-drilldown: Column Chart with Hierarchical Drilling
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 72/100 | Created: 2026-01-16
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Set random seed for reproducibility
np.random.seed(42)

# Hierarchical data: Company sales by region, country, and city
# Root level (Level 1): Regions
# Second level (Level 2): Countries within each region
# Third level (Level 3): Cities within each country
data = {
    "id": [
        "NA",
        "EU",
        "APAC",
        "USA",
        "CAN",
        "MEX",
        "UK",
        "DE",
        "FR",
        "JP",
        "CN",
        "AU",
        "NYC",
        "LA",
        "CHI",
        "TOR",
        "VAN",
        "MXC",
    ],
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
        "Toronto",
        "Vancouver",
        "Mexico City",
    ],
    "value": [850, 620, 530, 480, 220, 150, 230, 250, 140, 180, 230, 120, 200, 150, 130, 120, 100, 90],
    "parent": [
        None,
        None,
        None,
        "NA",
        "NA",
        "NA",
        "EU",
        "EU",
        "EU",
        "APAC",
        "APAC",
        "APAC",
        "USA",
        "USA",
        "USA",
        "CAN",
        "CAN",
        "MEX",
    ],
}

df = pd.DataFrame(data)

# Create figure with three subplots showing 3-level drill-down concept
fig, axes = plt.subplots(1, 3, figsize=(16, 9))

# Define distinct color palettes for better accessibility
level1_colors = ["#2E86AB", "#F6AE2D", "#A23B72"]  # Blue, Yellow, Magenta
level2_colors = ["#2E86AB", "#E55934", "#1B998B"]  # Blue, Red-Orange, Teal
level3_colors = ["#2E86AB", "#8338EC", "#06D6A0"]  # Blue, Purple, Green

# Left plot: Root level (Level 1 - Regions)
root_df = df[df["parent"].isna()].copy()
sns.barplot(data=root_df, x="name", y="value", hue="name", palette=level1_colors, ax=axes[0], legend=False)

# Add value labels on bars
for i, (_, row) in enumerate(root_df.iterrows()):
    axes[0].text(i, row["value"] + 20, f"${row['value']}M", ha="center", va="bottom", fontsize=12, fontweight="bold")

axes[0].set_xlabel("Region", fontsize=18)
axes[0].set_ylabel("Sales ($ Millions)", fontsize=18)
axes[0].set_title("Level 1: All Regions", fontsize=18, fontweight="bold")
axes[0].tick_params(axis="both", labelsize=14)
axes[0].set_ylim(0, 1000)
axes[0].grid(axis="y", alpha=0.3, linestyle="--")
axes[0].text(
    0.5,
    -0.12,
    "Click to drill down",
    ha="center",
    va="top",
    fontsize=12,
    fontstyle="italic",
    transform=axes[0].transAxes,
    color="#666666",
)

# Middle plot: Level 2 - Drilled into North America
na_children = df[df["parent"] == "NA"].copy()
sns.barplot(data=na_children, x="name", y="value", hue="name", palette=level2_colors, ax=axes[1], legend=False)

for i, (_, row) in enumerate(na_children.iterrows()):
    axes[1].text(i, row["value"] + 12, f"${row['value']}M", ha="center", va="bottom", fontsize=12, fontweight="bold")

axes[1].set_xlabel("Country", fontsize=18)
axes[1].set_ylabel("Sales ($ Millions)", fontsize=18)
axes[1].set_title("Level 2: All > North America", fontsize=18, fontweight="bold")
axes[1].tick_params(axis="both", labelsize=14)
axes[1].set_ylim(0, 600)
axes[1].grid(axis="y", alpha=0.3, linestyle="--")
axes[1].text(
    0.5,
    -0.12,
    "Click to drill down",
    ha="center",
    va="top",
    fontsize=12,
    fontstyle="italic",
    transform=axes[1].transAxes,
    color="#666666",
)

# Right plot: Level 3 - Drilled into USA
usa_children = df[df["parent"] == "USA"].copy()
sns.barplot(data=usa_children, x="name", y="value", hue="name", palette=level3_colors, ax=axes[2], legend=False)

for i, (_, row) in enumerate(usa_children.iterrows()):
    axes[2].text(i, row["value"] + 5, f"${row['value']}M", ha="center", va="bottom", fontsize=12, fontweight="bold")

axes[2].set_xlabel("City", fontsize=18)
axes[2].set_ylabel("Sales ($ Millions)", fontsize=18)
axes[2].set_title("Level 3: All > NA > USA", fontsize=18, fontweight="bold")
axes[2].tick_params(axis="both", labelsize=14)
axes[2].set_ylim(0, 250)
axes[2].grid(axis="y", alpha=0.3, linestyle="--")
axes[2].text(
    0.5,
    -0.12,
    "Deepest level",
    ha="center",
    va="top",
    fontsize=12,
    fontstyle="italic",
    transform=axes[2].transAxes,
    color="#666666",
)

# Main title
fig.suptitle("bar-drilldown \u00b7 seaborn \u00b7 pyplots.ai", fontsize=24, fontweight="bold", y=0.98)

plt.tight_layout(rect=[0, 0.02, 1, 0.94])
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
