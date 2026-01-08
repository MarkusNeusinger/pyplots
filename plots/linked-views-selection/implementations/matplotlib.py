"""pyplots.ai
linked-views-selection: Multiple Linked Views with Selection Sync
Library: matplotlib | Python 3.13
Quality: pending | Created: 2025-01-08
"""

import matplotlib.pyplot as plt
import numpy as np


# Data - Simulated multivariate dataset
np.random.seed(42)
n_points = 150

# Create 3 clusters with different characteristics
cluster_sizes = [50, 50, 50]
categories = np.repeat(["Cluster A", "Cluster B", "Cluster C"], cluster_sizes)

# Generate x, y coordinates for each cluster
x = np.concatenate(
    [
        np.random.normal(2, 0.8, 50),  # Cluster A
        np.random.normal(5, 0.6, 50),  # Cluster B
        np.random.normal(4, 1.0, 50),  # Cluster C
    ]
)

y = np.concatenate(
    [
        np.random.normal(3, 0.7, 50),  # Cluster A
        np.random.normal(6, 0.5, 50),  # Cluster B
        np.random.normal(2, 0.9, 50),  # Cluster C
    ]
)

# Additional value dimension for histogram
value = np.concatenate(
    [
        np.random.normal(25, 5, 50),  # Cluster A
        np.random.normal(45, 8, 50),  # Cluster B
        np.random.normal(35, 6, 50),  # Cluster C
    ]
)

# Simulate a selection - select Cluster B as "selected"
# This demonstrates linked highlighting across all views
selected_mask = categories == "Cluster B"
unselected_mask = ~selected_mask

# Colors - Python Blue for selected, gray for unselected
selected_color = "#306998"
unselected_color = "#CCCCCC"

# Create figure with 3 subplots (linked views)
fig, axes = plt.subplots(1, 3, figsize=(16, 9))

# View 1: Scatter Plot (x vs y)
ax1 = axes[0]
ax1.scatter(
    x[unselected_mask],
    y[unselected_mask],
    s=120,
    c=unselected_color,
    alpha=0.4,
    edgecolors="white",
    linewidth=0.5,
    label="Unselected",
)
ax1.scatter(
    x[selected_mask],
    y[selected_mask],
    s=180,
    c=selected_color,
    alpha=0.9,
    edgecolors="white",
    linewidth=1,
    label="Selected (Cluster B)",
)
ax1.set_xlabel("X Coordinate", fontsize=18)
ax1.set_ylabel("Y Coordinate", fontsize=18)
ax1.set_title("Scatter Plot View", fontsize=20, fontweight="bold")
ax1.tick_params(axis="both", labelsize=14)
ax1.grid(True, alpha=0.3, linestyle="--")
ax1.legend(fontsize=14, loc="upper left")

# View 2: Histogram of Values
ax2 = axes[1]
bins = np.linspace(10, 70, 20)
ax2.hist(
    value[unselected_mask],
    bins=bins,
    color=unselected_color,
    alpha=0.5,
    edgecolor="white",
    linewidth=0.5,
    label="Unselected",
)
ax2.hist(
    value[selected_mask], bins=bins, color=selected_color, alpha=0.85, edgecolor="white", linewidth=1, label="Selected"
)
ax2.set_xlabel("Value Distribution", fontsize=18)
ax2.set_ylabel("Frequency", fontsize=18)
ax2.set_title("Histogram View", fontsize=20, fontweight="bold")
ax2.tick_params(axis="both", labelsize=14)
ax2.grid(True, alpha=0.3, linestyle="--", axis="y")
ax2.legend(fontsize=14, loc="upper right")

# View 3: Bar Chart by Category
ax3 = axes[2]
unique_categories = ["Cluster A", "Cluster B", "Cluster C"]
category_counts = [np.sum(categories == cat) for cat in unique_categories]
selected_counts = [np.sum((categories == cat) & selected_mask) for cat in unique_categories]

bar_positions = np.arange(len(unique_categories))
bar_width = 0.6

# Draw bars - highlight selected category
bar_colors = [selected_color if cat == "Cluster B" else unselected_color for cat in unique_categories]

ax3.bar(bar_positions, category_counts, width=bar_width, color=bar_colors, alpha=0.85, edgecolor="white", linewidth=1.5)

# Add selection count annotations
for i, (count, sel_count) in enumerate(zip(category_counts, selected_counts, strict=True)):
    if sel_count > 0:
        ax3.annotate(
            f"{sel_count} selected",
            xy=(bar_positions[i], count + 2),
            ha="center",
            fontsize=14,
            fontweight="bold",
            color=selected_color,
        )

ax3.set_xlabel("Category", fontsize=18)
ax3.set_ylabel("Count", fontsize=18)
ax3.set_title("Category Distribution", fontsize=20, fontweight="bold")
ax3.set_xticks(bar_positions)
ax3.set_xticklabels(unique_categories, fontsize=14)
ax3.tick_params(axis="y", labelsize=14)
ax3.grid(True, alpha=0.3, linestyle="--", axis="y")
ax3.set_ylim(0, 65)

# Main title with selection info
n_selected = np.sum(selected_mask)
fig.suptitle(
    f"linked-views-selection · matplotlib · pyplots.ai\nSelection: {n_selected} of {n_points} points (Cluster B)",
    fontsize=24,
    fontweight="bold",
    y=0.98,
)

# Add explanatory annotation
fig.text(
    0.5,
    0.02,
    "Selecting Cluster B in scatter plot highlights corresponding data in all views",
    ha="center",
    fontsize=14,
    style="italic",
    color="#666666",
)

plt.tight_layout(rect=[0, 0.05, 1, 0.92])
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
