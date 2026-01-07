""" pyplots.ai
bar-interactive: Interactive Bar Chart with Hover and Click
Library: matplotlib 3.10.8 | Python 3.13.11
Quality: 87/100 | Created: 2026-01-07
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle


# Data - Product sales with hover/click details
np.random.seed(42)
categories = ["Electronics", "Clothing", "Home & Garden", "Sports", "Books", "Toys", "Automotive", "Health"]
values = np.array([87500, 64200, 52300, 48700, 35600, 42100, 31200, 28900])
percentages = values / values.sum() * 100
prev_values = values * (0.85 + np.random.rand(len(categories)) * 0.3)
growth = ((values - prev_values) / prev_values * 100).round(1)

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Colors - Python Blue as primary, highlighted bar in different color
colors = ["#306998"] * len(categories)
highlight_idx = 0  # Simulating hover on first bar
colors[highlight_idx] = "#FFD43B"  # Python Yellow for highlighted bar

# Create bars with edge styling for definition
bars = ax.bar(categories, values, color=colors, edgecolor="#1a3a52", linewidth=2, width=0.7)

# Add hover tooltip annotation for the highlighted bar (demonstrating interactivity)
tooltip_x = highlight_idx
tooltip_y = values[highlight_idx]
tooltip_text = (
    f"Category: {categories[highlight_idx]}\n"
    f"Sales: ${values[highlight_idx]:,}\n"
    f"Share: {percentages[highlight_idx]:.1f}%\n"
    f"Growth: {'+' if growth[highlight_idx] > 0 else ''}{growth[highlight_idx]}%\n"
    f"[Click to drill down]"
)

# Create tooltip box
bbox_props = {"boxstyle": "round,pad=0.5", "facecolor": "white", "edgecolor": "#306998", "linewidth": 2, "alpha": 0.95}
ax.annotate(
    tooltip_text,
    xy=(tooltip_x, tooltip_y),
    xytext=(tooltip_x + 0.8, tooltip_y + 8000),
    fontsize=14,
    ha="left",
    va="bottom",
    bbox=bbox_props,
    arrowprops={"arrowstyle": "->", "color": "#306998", "lw": 2},
)

# Add value labels on top of each bar
for bar, val in zip(bars, values, strict=True):
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        height + 1500,
        f"${val / 1000:.0f}K",
        ha="center",
        va="bottom",
        fontsize=14,
        fontweight="bold",
        color="#1a3a52",
    )

# Highlight effect - add subtle glow to highlighted bar
highlight_bar = bars[highlight_idx]
glow = Rectangle(
    (highlight_bar.get_x() - 0.05, 0),
    highlight_bar.get_width() + 0.1,
    highlight_bar.get_height(),
    facecolor="none",
    edgecolor="#FFD43B",
    linewidth=4,
    alpha=0.5,
)
ax.add_patch(glow)

# Styling
ax.set_xlabel("Product Category", fontsize=20)
ax.set_ylabel("Sales Revenue ($)", fontsize=20)
ax.set_title("bar-interactive · matplotlib · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)
ax.tick_params(axis="x", rotation=15)

# Format y-axis with dollar amounts
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x / 1000:.0f}K"))

# Grid
ax.grid(True, alpha=0.3, linestyle="--", axis="y")
ax.set_axisbelow(True)

# Set y-axis limit to accommodate annotations
ax.set_ylim(0, max(values) * 1.35)

# Add legend explaining the interaction
legend_elements = [
    plt.Rectangle((0, 0), 1, 1, facecolor="#306998", edgecolor="#1a3a52", label="Normal bar"),
    plt.Rectangle((0, 0), 1, 1, facecolor="#FFD43B", edgecolor="#1a3a52", label="Hovered bar (highlighted)"),
]
ax.legend(handles=legend_elements, loc="upper right", fontsize=14)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
