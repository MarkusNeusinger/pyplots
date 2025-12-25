"""pyplots.ai
bar-stacked: Stacked Bar Chart
Library: seaborn | Python 3.13
Quality: pending | Created: 2025-12-25
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Data - Monthly sales by product category (realistic business scenario)
np.random.seed(42)

categories = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
products = ["Electronics", "Clothing", "Home & Garden", "Sports"]

# Create realistic sales data (in thousands)
data = {
    "Month": categories * len(products),
    "Product": [p for p in products for _ in categories],
    "Sales": [
        # Electronics - highest, growing trend
        120,
        135,
        145,
        160,
        175,
        190,
        # Clothing - seasonal variation
        85,
        70,
        95,
        110,
        90,
        75,
        # Home & Garden - spring/summer peak
        45,
        55,
        80,
        95,
        85,
        60,
        # Sports - summer peak
        35,
        40,
        55,
        70,
        85,
        65,
    ],
}

df = pd.DataFrame(data)

# Pivot data for stacking
pivot_df = df.pivot(index="Month", columns="Product", values="Sales")
pivot_df = pivot_df[products]  # Maintain order
pivot_df = pivot_df.reindex(categories)  # Maintain month order

# Create plot
fig, ax = plt.subplots(figsize=(16, 9))

# Python-themed color palette (blue and yellow first, then complementary)
colors = ["#306998", "#FFD43B", "#4B8BBE", "#FFE873"]

# Create stacked bar chart using matplotlib's bar with seaborn styling
sns.set_style("whitegrid")
sns.set_context("talk", font_scale=1.2)

# Stack bars manually for full control
bottom = np.zeros(len(categories))
bar_width = 0.6

for i, product in enumerate(products):
    ax.bar(
        categories,
        pivot_df[product].values,
        bottom=bottom,
        width=bar_width,
        label=product,
        color=colors[i],
        edgecolor="white",
        linewidth=1.5,
    )
    bottom += pivot_df[product].values

# Add total labels on top of each stack
totals = pivot_df.sum(axis=1)
for i, total in enumerate(totals):
    ax.text(i, total + 8, f"${int(total)}K", ha="center", va="bottom", fontsize=16, fontweight="bold")

# Styling
ax.set_xlabel("Month", fontsize=20)
ax.set_ylabel("Sales (Thousands $)", fontsize=20)
ax.set_title("bar-stacked · seaborn · pyplots.ai", fontsize=24, fontweight="bold")
ax.tick_params(axis="both", labelsize=16)

# Legend
ax.legend(
    title="Product Category",
    title_fontsize=18,
    fontsize=16,
    loc="upper left",
    bbox_to_anchor=(1.02, 1),
    frameon=True,
    edgecolor="gray",
)

# Grid styling
ax.yaxis.grid(True, alpha=0.3, linestyle="--")
ax.xaxis.grid(False)
ax.set_axisbelow(True)

# Remove top and right spines
sns.despine()

# Adjust y-axis to accommodate total labels
ax.set_ylim(0, max(totals) * 1.15)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
