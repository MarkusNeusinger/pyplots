"""pyplots.ai
bar-basic: Basic Bar Chart
Library: seaborn 0.13.2 | Python 3.14
Quality: 89/100 | Created: 2025-12-23
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# Data - Product sales by category
data = pd.DataFrame(
    {
        "category": ["Electronics", "Clothing", "Home & Garden", "Sports", "Books", "Toys", "Groceries", "Automotive"],
        "sales": [218, 164, 89, 137, 41, 112, 187, 58],
    }
)

# Sort by sales descending for intentional ranking visualization
data = data.sort_values("sales", ascending=False).reset_index(drop=True)

# Mark top and bottom performers for color emphasis via seaborn's hue
top_val = data["sales"].max()
bottom_val = data["sales"].min()
data["emphasis"] = data["sales"].apply(
    lambda v: "top" if v == top_val else ("bottom" if v == bottom_val else "default")
)

# Palette mapped to emphasis groups — Python Blue base with storytelling accents
emphasis_palette = {"top": "#306998", "default": "#7BAFD4", "bottom": "#A3BFCF"}

# Create plot (4800x2700 px)
sns.set_context("talk", font_scale=1.1)
fig, ax = plt.subplots(figsize=(16, 9))
sns.barplot(
    data=data,
    x="category",
    y="sales",
    hue="emphasis",
    hue_order=["top", "default", "bottom"],
    palette=emphasis_palette,
    width=0.7,
    dodge=False,
    legend=False,
    ax=ax,
)

# Value labels on top of bars
for container in ax.containers:
    ax.bar_label(container, fmt="%d", fontsize=18, fontweight="bold", padding=5)

# Annotate top performer
top_row = data[data["emphasis"] == "top"].iloc[0]
top_idx = data.index[data["emphasis"] == "top"][0]
ax.annotate(
    f"Top seller — {top_row['sales']} units",
    xy=(top_idx, top_row["sales"]),
    xytext=(top_idx + 1.8, top_row["sales"] + 20),
    fontsize=16,
    fontweight="bold",
    color="#1A3A5C",
    arrowprops={"arrowstyle": "->", "color": "#1A3A5C", "lw": 2},
    ha="left",
    va="bottom",
)

# Annotate bottom performer
bottom_row = data[data["emphasis"] == "bottom"].iloc[0]
bottom_idx = data.index[data["emphasis"] == "bottom"][0]
ax.annotate(
    f"Lowest — {bottom_row['sales']} units",
    xy=(bottom_idx, bottom_row["sales"] + 18),
    xytext=(bottom_idx - 1.8, bottom_row["sales"] + 95),
    fontsize=14,
    color="#6B7B8D",
    arrowprops={"arrowstyle": "->", "color": "#6B7B8D", "lw": 1.5},
    ha="center",
    va="bottom",
)

# Labels and title
ax.set_xlabel("Product Category", fontsize=20)
ax.set_ylabel("Sales (units)", fontsize=20)
ax.set_title("bar-basic · seaborn · pyplots.ai", fontsize=24, fontweight="medium", pad=16)
ax.tick_params(axis="both", labelsize=16)

# Subtle grid and clean spines
ax.yaxis.grid(True, alpha=0.2, linewidth=0.8)
ax.set_axisbelow(True)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Increase y-axis upper limit to give room for annotations
y_max = data["sales"].max()
ax.set_ylim(0, y_max * 1.22)

fig.subplots_adjust(left=0.08, right=0.96, top=0.92, bottom=0.10)
plt.savefig("plot.png", dpi=300)
