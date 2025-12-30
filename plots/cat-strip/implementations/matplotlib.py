""" pyplots.ai
cat-strip: Categorical Strip Plot
Library: matplotlib 3.10.8 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-30
"""

import matplotlib.pyplot as plt
import numpy as np


# Data - Performance scores across different departments
np.random.seed(42)

categories = ["Engineering", "Marketing", "Sales", "Support", "Design"]
n_per_category = 25

# Generate data with different distributions per category
data = {
    "Engineering": np.random.normal(75, 12, n_per_category),
    "Marketing": np.random.normal(68, 15, n_per_category),
    "Sales": np.random.normal(82, 10, n_per_category),
    "Support": np.random.normal(70, 8, n_per_category),
    "Design": np.random.normal(78, 14, n_per_category),
}

# Prepare data for plotting
all_values = []
all_categories = []
for cat in categories:
    all_values.extend(data[cat])
    all_categories.extend([cat] * n_per_category)

# Create numeric positions for categories
category_positions = {cat: i for i, cat in enumerate(categories)}
x_positions = np.array([category_positions[cat] for cat in all_categories])

# Add jitter to x positions
jitter = np.random.uniform(-0.25, 0.25, len(x_positions))
x_jittered = x_positions + jitter

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

# Color by category using Python colors
colors = ["#306998", "#FFD43B", "#4B8BBE", "#FFE873", "#646464"]
point_colors = [colors[int(x)] for x in x_positions]

ax.scatter(x_jittered, all_values, c=point_colors, s=150, alpha=0.7, edgecolors="white", linewidths=0.5)

# Styling
ax.set_xticks(range(len(categories)))
ax.set_xticklabels(categories)
ax.set_xlabel("Department", fontsize=20)
ax.set_ylabel("Performance Score", fontsize=20)
ax.set_title("cat-strip · matplotlib · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)
ax.grid(True, alpha=0.3, linestyle="--", axis="y")

# Set y-axis limits with padding
ax.set_ylim(min(all_values) - 5, max(all_values) + 5)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
