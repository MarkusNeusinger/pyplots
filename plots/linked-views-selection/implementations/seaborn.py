"""pyplots.ai
linked-views-selection: Multiple Linked Views with Selection Sync
Library: seaborn | Python 3.13
Quality: pending | Created: 2026-01-08
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Data - Iris-like multivariate dataset with categorical groups
np.random.seed(42)

categories = ["Group A", "Group B", "Group C"]

# Generate clustered data for each category
data = []
centers = [(5.0, 3.5), (6.5, 2.8), (7.5, 3.2)]
spreads = [(0.4, 0.3), (0.5, 0.4), (0.6, 0.3)]

for i, (cat, center, spread) in enumerate(zip(categories, centers, spreads, strict=True)):
    n = 50
    x = np.random.normal(center[0], spread[0], n)
    y = np.random.normal(center[1], spread[1], n)
    value = np.random.normal(2.5 + i * 0.8, 0.4, n)
    for j in range(n):
        data.append({"x": x[j], "y": y[j], "category": cat, "value": value[j]})

df = pd.DataFrame(data)

# Simulate a selection: select points where x > 6.0 (roughly Group B and C cluster)
df["selected"] = df["x"] > 6.0

# Define colors for selection state
color_selected = "#306998"  # Python Blue
color_unselected = "#CCCCCC"  # Gray for unselected

# Create multi-panel figure with linked views
fig = plt.figure(figsize=(16, 9))

# Layout: 2x2 grid with scatter, histogram, bar chart, and value distribution
gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.25)

ax1 = fig.add_subplot(gs[0, 0])  # Scatter plot (main selection view)
ax2 = fig.add_subplot(gs[0, 1])  # Histogram of value (filtered)
ax3 = fig.add_subplot(gs[1, 0])  # Bar chart by category
ax4 = fig.add_subplot(gs[1, 1])  # Y distribution

# --- Panel 1: Scatter plot with selection region ---
# Plot unselected points first (gray, lower opacity)
unselected = df[~df["selected"]]
selected = df[df["selected"]]

sns.scatterplot(data=unselected, x="x", y="y", color=color_unselected, s=150, alpha=0.4, ax=ax1, legend=False)
sns.scatterplot(data=selected, x="x", y="y", color=color_selected, s=150, alpha=0.9, ax=ax1, legend=False)

# Add vertical line showing selection threshold
ax1.axvline(x=6.0, color="#FFD43B", linestyle="--", linewidth=2.5, label="Selection: x > 6.0")
ax1.legend(fontsize=14, loc="upper left")
ax1.set_xlabel("X Value", fontsize=18)
ax1.set_ylabel("Y Value", fontsize=18)
ax1.set_title("Scatter Plot (Selection Source)", fontsize=20, fontweight="bold")
ax1.tick_params(axis="both", labelsize=14)
ax1.grid(True, alpha=0.3, linestyle="--")

# --- Panel 2: Histogram of 'value' showing selected vs unselected ---
bins = np.linspace(df["value"].min(), df["value"].max(), 15)

ax2.hist(
    unselected["value"],
    bins=bins,
    color=color_unselected,
    alpha=0.5,
    label="Unselected",
    edgecolor="white",
    linewidth=1,
)
ax2.hist(
    selected["value"], bins=bins, color=color_selected, alpha=0.8, label="Selected", edgecolor="white", linewidth=1
)
ax2.legend(fontsize=14)
ax2.set_xlabel("Value", fontsize=18)
ax2.set_ylabel("Count", fontsize=18)
ax2.set_title("Value Distribution (Linked)", fontsize=20, fontweight="bold")
ax2.tick_params(axis="both", labelsize=14)
ax2.grid(True, alpha=0.3, linestyle="--", axis="y")

# --- Panel 3: Bar chart showing selection count by category ---
selection_counts = df.groupby("category")["selected"].agg(["sum", "count"]).reset_index()
selection_counts.columns = ["category", "selected_count", "total_count"]
selection_counts["unselected_count"] = selection_counts["total_count"] - selection_counts["selected_count"]

x_pos = np.arange(len(categories))
width = 0.5

# Stacked bar chart
ax3.bar(
    x_pos,
    selection_counts["unselected_count"],
    width,
    color=color_unselected,
    alpha=0.5,
    label="Unselected",
    edgecolor="white",
    linewidth=1.5,
)
ax3.bar(
    x_pos,
    selection_counts["selected_count"],
    width,
    bottom=selection_counts["unselected_count"],
    color=color_selected,
    alpha=0.9,
    label="Selected",
    edgecolor="white",
    linewidth=1.5,
)

ax3.set_xticks(x_pos)
ax3.set_xticklabels(categories, fontsize=14)
ax3.legend(fontsize=14)
ax3.set_xlabel("Category", fontsize=18)
ax3.set_ylabel("Count", fontsize=18)
ax3.set_title("Category Breakdown (Linked)", fontsize=20, fontweight="bold")
ax3.tick_params(axis="both", labelsize=14)
ax3.grid(True, alpha=0.3, linestyle="--", axis="y")

# --- Panel 4: Y value distribution using KDE ---
sns.kdeplot(
    data=unselected, x="y", color=color_unselected, linewidth=3, alpha=0.6, label="Unselected", ax=ax4, fill=True
)
sns.kdeplot(data=selected, x="y", color=color_selected, linewidth=3, alpha=0.8, label="Selected", ax=ax4, fill=True)
ax4.legend(fontsize=14)
ax4.set_xlabel("Y Value", fontsize=18)
ax4.set_ylabel("Density", fontsize=18)
ax4.set_title("Y Distribution (Linked)", fontsize=20, fontweight="bold")
ax4.tick_params(axis="both", labelsize=14)
ax4.grid(True, alpha=0.3, linestyle="--")

# Main title with selection info
n_selected = selected.shape[0]
n_total = df.shape[0]
fig.suptitle("linked-views-selection · seaborn · pyplots.ai", fontsize=26, fontweight="bold", y=1.02)
fig.text(
    0.5,
    0.96,
    f"Selection: {n_selected}/{n_total} points where x > 6.0",
    fontsize=16,
    ha="center",
    style="italic",
    color="#555555",
)

plt.tight_layout(rect=[0, 0, 1, 0.94])
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
