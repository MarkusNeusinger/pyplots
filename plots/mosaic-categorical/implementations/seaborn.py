""" pyplots.ai
mosaic-categorical: Mosaic Plot for Categorical Association Analysis
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 78/100 | Created: 2026-01-11
"""

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import seaborn as sns


# Load Titanic dataset using seaborn
df = sns.load_dataset("titanic")

# Set seaborn style for consistent aesthetics
sns.set_style("whitegrid")
sns.set_context("talk", font_scale=1.1)

# Create contingency table from seaborn dataset
contingency_df = df.groupby(["class", "survived"], observed=True).size().unstack(fill_value=0)
contingency = contingency_df.values

categories_1 = ["First", "Second", "Third"]
categories_2 = ["Survived", "Did Not Survive"]

# Calculate proportions for mosaic
row_totals = contingency.sum(axis=1)
total = contingency.sum()
col_widths = row_totals / total
col_heights = contingency / row_totals[:, None]

# Color palette using seaborn colorblind palette converted to Python colors
colors = sns.color_palette(["#306998", "#FFD43B"])

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Gap between rectangles
gap = 0.02

# Draw mosaic rectangles
x_start = 0
for i, cat1 in enumerate(categories_1):
    width = col_widths[i] - gap
    y_start = 0

    for j in range(len(categories_2)):
        # Note: contingency has [Not Survived, Survived], need to reverse for display
        actual_j = 1 - j  # Flip so Survived is on bottom
        height = col_heights[i, actual_j] - gap / 2

        # Color: Blue for survived (j=0 displayed at bottom), Yellow for not survived
        color = colors[j]

        # Draw rectangle with seaborn-influenced styling
        rect = mpatches.FancyBboxPatch(
            (x_start + gap / 2, y_start + gap / 4),
            width,
            height,
            boxstyle="round,pad=0,rounding_size=0.01",
            facecolor=color,
            edgecolor="white",
            linewidth=3,
        )
        ax.add_patch(rect)

        # Add frequency label in center of rectangle
        freq = contingency[i, actual_j]
        cx = x_start + gap / 2 + width / 2
        cy = y_start + gap / 4 + height / 2

        # Only show label if rectangle is large enough
        if height > 0.08:
            ax.text(cx, cy, f"{freq}", ha="center", va="center", fontsize=20, fontweight="bold", color="white")

        y_start += height + gap / 2

    # Add class label below each column
    cx = x_start + gap / 2 + width / 2
    ax.text(cx, -0.08, cat1, ha="center", va="top", fontsize=18, fontweight="bold")

    x_start += col_widths[i]

# Calculate average y positions for row labels
avg_survived_height = col_heights[:, 1].mean()  # Index 1 = Survived in original data
avg_not_survived_height = col_heights[:, 0].mean()  # Index 0 = Not Survived

survived_y = avg_survived_height / 2
not_survived_y = avg_survived_height + avg_not_survived_height / 2

# Add row labels on the left side
ax.text(-0.04, survived_y, "Survived", ha="right", va="center", fontsize=18, fontweight="bold")
ax.text(-0.04, not_survived_y, "Did Not\nSurvive", ha="right", va="center", fontsize=18, fontweight="bold")

# Set axis properties
ax.set_xlim(-0.18, 1.02)
ax.set_ylim(-0.15, 1.05)
ax.set_aspect("equal")
ax.axis("off")

# Add title
ax.set_title(
    "Titanic Passenger Survival by Class · mosaic-categorical · seaborn · pyplots.ai",
    fontsize=24,
    fontweight="bold",
    pad=20,
)

# Add legend using seaborn color palette
legend_elements = [
    mpatches.Patch(facecolor="#306998", edgecolor="white", linewidth=2, label="Survived"),
    mpatches.Patch(facecolor="#FFD43B", edgecolor="white", linewidth=2, label="Did Not Survive"),
]
ax.legend(handles=legend_elements, loc="upper right", fontsize=16, framealpha=0.95, edgecolor="gray")

# Add axis labels
ax.text(0.5, -0.13, "Passenger Class", ha="center", va="top", fontsize=20, fontweight="bold")
ax.text(-0.15, 0.5, "Survival Status", ha="right", va="center", fontsize=20, fontweight="bold", rotation=90)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
