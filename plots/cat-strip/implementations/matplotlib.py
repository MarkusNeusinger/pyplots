"""pyplots.ai
cat-strip: Categorical Strip Plot
Library: matplotlib | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import matplotlib.pyplot as plt
import numpy as np


# Data - Product quality scores across manufacturing plants
np.random.seed(42)

categories = ["Plant A", "Plant B", "Plant C", "Plant D", "Plant E"]
n_per_category = 25

# Generate different distributions for each plant to show variety
data = {
    "Plant A": np.random.normal(85, 5, n_per_category),  # High quality, consistent
    "Plant B": np.random.normal(75, 8, n_per_category),  # Medium quality, variable
    "Plant C": np.random.normal(90, 3, n_per_category),  # Very high quality, tight
    "Plant D": np.random.normal(70, 12, n_per_category),  # Lower quality, wide spread
    "Plant E": np.random.normal(80, 6, n_per_category),  # Good quality, moderate
}

# Add some outliers for visual interest
data["Plant B"] = np.append(data["Plant B"], [55, 95])
data["Plant D"] = np.append(data["Plant D"], [40, 45])

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Plot each category with jitter
colors = ["#306998", "#FFD43B", "#4A90A4", "#E07B39", "#6B8E23"]

for i, (category, values) in enumerate(data.items()):
    # Apply horizontal jitter
    jitter = np.random.uniform(-0.2, 0.2, len(values))
    x_positions = np.full(len(values), i) + jitter

    ax.scatter(x_positions, values, s=150, alpha=0.7, color=colors[i], edgecolors="white", linewidth=1, label=category)

# Styling
ax.set_xticks(range(len(categories)))
ax.set_xticklabels(categories)
ax.set_xlabel("Manufacturing Plant", fontsize=20)
ax.set_ylabel("Quality Score (0-100)", fontsize=20)
ax.set_title("cat-strip · matplotlib · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)
ax.grid(True, alpha=0.3, linestyle="--", axis="y")

# Set y-axis limits to show full range with some padding
ax.set_ylim(30, 105)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
