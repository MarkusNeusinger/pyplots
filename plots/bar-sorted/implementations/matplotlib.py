""" pyplots.ai
bar-sorted: Sorted Bar Chart
Library: matplotlib 3.10.8 | Python 3.13.11
Quality: 94/100 | Created: 2025-12-30
"""

import matplotlib.pyplot as plt
import numpy as np


# Data: Sales performance by product category
np.random.seed(42)
categories = [
    "Electronics",
    "Furniture",
    "Office Supplies",
    "Software",
    "Accessories",
    "Networking",
    "Storage",
    "Printing",
]
values = np.random.randint(150, 800, size=len(categories))

# Sort by value (descending)
sorted_indices = np.argsort(values)[::-1]
sorted_categories = [categories[i] for i in sorted_indices]
sorted_values = values[sorted_indices]

# Create figure (horizontal bars work better for readability)
fig, ax = plt.subplots(figsize=(16, 9))

# Plot horizontal bars
bars = ax.barh(sorted_categories, sorted_values, color="#306998", edgecolor="white", linewidth=1.5)

# Add value labels on bars
for bar, value in zip(bars, sorted_values, strict=True):
    ax.text(
        value + 10,
        bar.get_y() + bar.get_height() / 2,
        f"${value}K",
        va="center",
        ha="left",
        fontsize=16,
        color="#333333",
    )

# Invert y-axis so largest is at top
ax.invert_yaxis()

# Styling
ax.set_xlabel("Sales Revenue ($ thousands)", fontsize=20)
ax.set_ylabel("Product Category", fontsize=20)
ax.set_title("bar-sorted · matplotlib · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)

# Subtle grid on x-axis only
ax.grid(True, axis="x", alpha=0.3, linestyle="--")
ax.set_axisbelow(True)

# Remove top and right spines for cleaner look
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Extend x-axis to fit value labels
ax.set_xlim(0, max(sorted_values) * 1.15)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
