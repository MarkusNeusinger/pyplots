"""pyplots.ai
bar-basic: Basic Bar Chart
Library: matplotlib | Python 3.13
Quality: pending | Created: 2025-12-23
"""

import matplotlib.pyplot as plt


# Data - Product sales by category
categories = ["Electronics", "Clothing", "Home & Garden", "Sports", "Books", "Toys"]
values = [45200, 32800, 28500, 21300, 18900, 15600]

# Create plot (4800x2700 px)
fig, ax = plt.subplots(figsize=(16, 9))

# Bar chart with Python Blue color
bars = ax.bar(categories, values, color="#306998", width=0.6, edgecolor="white", linewidth=1.5)

# Add value labels on top of bars
for bar, value in zip(bars, values, strict=True):
    height = bar.get_height()
    ax.annotate(
        f"${value:,}",
        xy=(bar.get_x() + bar.get_width() / 2, height),
        xytext=(0, 8),
        textcoords="offset points",
        ha="center",
        va="bottom",
        fontsize=16,
    )

# Labels and styling
ax.set_xlabel("Product Category", fontsize=20)
ax.set_ylabel("Sales ($)", fontsize=20)
ax.set_title("bar-basic · matplotlib · pyplots.ai", fontsize=24)

# Style tick labels
ax.tick_params(axis="both", labelsize=16)

# Subtle grid on y-axis only
ax.yaxis.grid(True, alpha=0.3, linestyle="--")
ax.set_axisbelow(True)

# Remove top and right spines for cleaner look
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Set y-axis to start at 0
ax.set_ylim(bottom=0)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
