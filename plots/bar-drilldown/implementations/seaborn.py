"""pyplots.ai
bar-drilldown: Column Chart with Hierarchical Drilling
Library: seaborn | Python 3.13
Quality: pending | Created: 2026-01-16
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# Hierarchical data: Company sales by region and country
# Root level: Regions
# Second level: Countries within each region
data = {
    "id": ["NA", "EU", "APAC", "USA", "CAN", "MEX", "UK", "DE", "FR", "JP", "CN", "AU"],
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
    ],
    "value": [850, 620, 530, 480, 220, 150, 230, 250, 140, 180, 230, 120],
    "parent": [None, None, None, "NA", "NA", "NA", "EU", "EU", "EU", "APAC", "APAC", "APAC"],
}

df = pd.DataFrame(data)

# Create figure with two subplots showing drill-down concept
fig, axes = plt.subplots(1, 2, figsize=(16, 9))

# Left plot: Root level (Regions)
root_df = df[df["parent"].isna()].copy()
sns.barplot(
    data=root_df, x="name", y="value", hue="name", palette=["#306998", "#FFD43B", "#4B8BBE"], ax=axes[0], legend=False
)

# Add value labels on bars
for i, (_, row) in enumerate(root_df.iterrows()):
    axes[0].text(i, row["value"] + 15, f"${row['value']}M", ha="center", va="bottom", fontsize=14, fontweight="bold")

axes[0].set_xlabel("Region", fontsize=20)
axes[0].set_ylabel("Sales ($ Millions)", fontsize=20)
axes[0].set_title("Level 1: All Regions\n(Click to drill down)", fontsize=20)
axes[0].tick_params(axis="both", labelsize=16)
axes[0].set_ylim(0, 1000)


# Right plot: Drilled into North America (simulated drill-down)
na_children = df[df["parent"] == "NA"].copy()
colors = ["#306998", "#4B8BBE", "#646464"]
sns.barplot(data=na_children, x="name", y="value", hue="name", palette=colors, ax=axes[1], legend=False)

# Add value labels on bars
for i, (_, row) in enumerate(na_children.iterrows()):
    axes[1].text(i, row["value"] + 10, f"${row['value']}M", ha="center", va="bottom", fontsize=14, fontweight="bold")

axes[1].set_xlabel("Country", fontsize=20)
axes[1].set_ylabel("Sales ($ Millions)", fontsize=20)
axes[1].set_title("Level 2: All > North America\n(Breadcrumb navigation)", fontsize=20)
axes[1].tick_params(axis="both", labelsize=16)
axes[1].set_ylim(0, 600)


# Main title
fig.suptitle("bar-drilldown · seaborn · pyplots.ai", fontsize=24, fontweight="bold", y=0.98)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
