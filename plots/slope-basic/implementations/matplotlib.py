"""pyplots.ai
slope-basic: Basic Slope Chart
Library: matplotlib | Python 3.13
Quality: pending | Created: 2025-12-23
"""

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


# Data: Sales figures (in millions $) for products comparing Q1 vs Q4
products = ["Product A", "Product B", "Product C", "Product D", "Product E", "Product F", "Product G", "Product H"]
q1_sales = [12.5, 8.3, 15.2, 6.8, 10.1, 9.4, 7.2, 11.8]
q4_sales = [14.8, 6.1, 18.5, 9.2, 8.7, 12.3, 10.5, 10.2]

# Calculate changes to determine colors
changes = [q4 - q1 for q1, q4 in zip(q1_sales, q4_sales, strict=True)]

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Plot each slope line
x_positions = [0, 1]
for product, q1, q4, change in zip(products, q1_sales, q4_sales, changes, strict=True):
    # Color by direction: blue for increase, yellow/orange for decrease
    color = "#306998" if change >= 0 else "#FFD43B"
    ax.plot(x_positions, [q1, q4], marker="o", markersize=12, linewidth=3, color=color)

    # Labels at both endpoints
    ax.text(-0.05, q1, f"{product}: ${q1:.1f}M", ha="right", va="center", fontsize=14, color=color, fontweight="bold")
    ax.text(1.05, q4, f"${q4:.1f}M", ha="left", va="center", fontsize=14, color=color, fontweight="bold")

# Style the axes
ax.set_xlim(-0.6, 1.6)
ax.set_xticks(x_positions)
ax.set_xticklabels(["Q1 2024", "Q4 2024"], fontsize=20, fontweight="bold")
ax.set_ylabel("Sales (Millions $)", fontsize=20)
ax.set_title("slope-basic · matplotlib · pyplots.ai", fontsize=24)

# Remove spines and set grid
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.tick_params(axis="y", labelsize=16)
ax.tick_params(axis="x", length=0)
ax.grid(True, axis="y", alpha=0.3, linestyle="--")

# Add legend for color coding
legend_elements = [
    Line2D([0], [0], color="#306998", linewidth=3, label="Increase"),
    Line2D([0], [0], color="#FFD43B", linewidth=3, label="Decrease"),
]
ax.legend(handles=legend_elements, loc="upper right", fontsize=16)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
