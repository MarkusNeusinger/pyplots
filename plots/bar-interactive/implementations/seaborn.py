"""pyplots.ai
bar-interactive: Interactive Bar Chart with Hover and Click
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 84/100 | Created: 2026-01-07
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize


# Data - Sales by product category with multiple samples (for error bars)
np.random.seed(42)
categories = ["Electronics", "Clothing", "Home & Garden", "Sports", "Books", "Toys"]
base_values = np.array([4850, 3200, 2750, 2100, 1850, 1450])

# Generate multiple samples per category to enable seaborn's statistical features
data_records = []
for cat, base_val in zip(categories, base_values, strict=True):
    # Create 10 samples around the base value with some variance
    samples = base_val + np.random.normal(0, base_val * 0.08, 10)
    for sample in samples:
        data_records.append({"category": cat, "sales": sample})

df = pd.DataFrame(data_records)

# Calculate summary statistics for annotations
summary = df.groupby("category")["sales"].agg(["mean", "std"]).reset_index()
summary["category"] = pd.Categorical(summary["category"], categories=categories, ordered=True)
summary = summary.sort_values("category")
total = summary["mean"].sum()
summary["pct"] = summary["mean"] / total * 100

# Create figure with space for colorbar
fig, ax = plt.subplots(figsize=(16, 9))

# Create sequential colormap based on values
cmap = plt.cm.Blues
norm = Normalize(vmin=min(base_values) * 0.8, vmax=max(base_values) * 1.1)
colors = [cmap(norm(val)) for val in base_values]

# Create bar chart with seaborn using statistical aggregation (shows mean + SD)
sns.barplot(
    data=df,
    x="category",
    y="sales",
    order=categories,
    hue="category",
    hue_order=categories,
    palette=colors,
    errorbar="sd",  # Show standard deviation as error bars
    capsize=0.15,
    err_kws={"linewidth": 2.5},
    legend=True,
    ax=ax,
)

# Configure legend
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels, title="Product Category", title_fontsize=16, fontsize=14, loc="upper right", framealpha=0.9)

# Add colorbar to explain color intensity encoding
sm = ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax, shrink=0.7, aspect=25, pad=0.02)
cbar.set_label("Sales Magnitude ($)", fontsize=18)
cbar.ax.tick_params(labelsize=14)

# Add value annotations on bars (simulating hover tooltip data)
for i, (_cat, row) in enumerate(summary.iterrows()):
    mean_val = row["mean"]
    std_val = row["std"]
    pct_val = row["pct"]
    # Format annotation like an interactive tooltip
    # Position above error bar with extra clearance to avoid overlap
    ax.annotate(
        f"${mean_val:,.0f} ± {std_val:,.0f}\n({pct_val:.1f}% of total)",
        xy=(i, mean_val + std_val + 200),
        ha="center",
        va="bottom",
        fontsize=15,
        fontweight="bold",
        color="#333333",
        bbox={"boxstyle": "round,pad=0.3", "facecolor": "white", "edgecolor": "#888888", "alpha": 0.9},
    )

# Styling
ax.set_xlabel("Product Category", fontsize=20)
ax.set_ylabel("Sales Revenue ($)", fontsize=20)
ax.set_title("bar-interactive · seaborn · pyplots.ai", fontsize=24, fontweight="bold")
ax.tick_params(axis="both", labelsize=16)
ax.set_ylim(0, df["sales"].max() * 1.4)
ax.grid(True, axis="y", alpha=0.3, linestyle="--")

# Remove top and right spines for cleaner look
sns.despine(ax=ax)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
