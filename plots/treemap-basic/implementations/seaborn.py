"""
treemap-basic: Basic Treemap
Library: seaborn
"""

import matplotlib.pyplot as plt
import seaborn as sns
import squarify


# Set seaborn style for consistent aesthetics
sns.set_style("whitegrid")

# Data: Budget allocation by department and project
categories = [
    "Engineering",
    "Engineering",
    "Engineering",
    "Marketing",
    "Marketing",
    "Sales",
    "Sales",
    "Operations",
    "Operations",
    "HR",
    "HR",
    "Finance",
]
subcategories = [
    "Development",
    "QA",
    "DevOps",
    "Digital Ads",
    "Content",
    "Direct",
    "Channel",
    "Logistics",
    "Support",
    "Recruiting",
    "Training",
    "Accounting",
]
values = [350, 120, 80, 200, 150, 180, 120, 140, 100, 90, 60, 110]

# Create color palette - one color per main category
unique_categories = list(dict.fromkeys(categories))  # Preserve order
palette = sns.color_palette("Set2", n_colors=len(unique_categories))
category_colors = {cat: palette[i] for i, cat in enumerate(unique_categories)}
colors = [category_colors[cat] for cat in categories]

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Draw treemap rectangles
squarify.plot(
    sizes=values,
    label=[f"{sub}\n${val}K" for sub, val in zip(subcategories, values, strict=True)],
    color=colors,
    alpha=0.85,
    ax=ax,
    text_kwargs={"fontsize": 14, "fontweight": "bold", "color": "white"},
    pad=True,
)

# Add subtle borders
for rect in ax.patches:
    rect.set_edgecolor("white")
    rect.set_linewidth(2)

# Remove axes for cleaner look
ax.axis("off")

# Title and styling
ax.set_title("Budget Allocation · treemap-basic · seaborn · pyplots.ai", fontsize=24, fontweight="bold", pad=20)

# Create legend for main categories
legend_handles = [
    plt.Rectangle((0, 0), 1, 1, facecolor=category_colors[cat], alpha=0.85, edgecolor="white", linewidth=2)
    for cat in unique_categories
]
ax.legend(
    legend_handles,
    unique_categories,
    loc="upper right",
    fontsize=14,
    title="Department",
    title_fontsize=16,
    framealpha=0.9,
    fancybox=True,
)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
