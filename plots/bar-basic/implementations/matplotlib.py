"""pyplots.ai
bar-basic: Basic Bar Chart
Library: matplotlib 3.10.8 | Python 3.14
Quality: /100 | Updated: 2026-02-14
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


# Data - Product sales by category (mixed order for natural variation)
categories = ["Electronics", "Clothing", "Home & Garden", "Sports", "Books", "Toys"]
values = [45200, 32800, 28500, 38700, 18900, 24100]

# Create plot (4800x2700 px)
fig, ax = plt.subplots(figsize=(16, 9))

# Bar chart with Python Blue color
bars = ax.bar(categories, values, color="#306998", width=0.6, edgecolor="white", linewidth=1.5)

# Value labels using bar_label with callable formatter
ax.bar_label(bars, fmt=lambda v: f"${v:,.0f}", padding=8, fontsize=16)

# Y-axis dollar formatting via FuncFormatter
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))

# Labels and styling
ax.set_xlabel("Product Category", fontsize=20)
ax.set_ylabel("Sales", fontsize=20)
ax.set_title("bar-basic \u00b7 matplotlib \u00b7 pyplots.ai", fontsize=24, fontweight="medium")

# Style tick labels
ax.tick_params(axis="both", labelsize=16)

# Subtle grid on y-axis only
ax.yaxis.grid(True, alpha=0.2, linewidth=0.8)
ax.set_axisbelow(True)

# Remove top and right spines for cleaner look
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Set y-axis to start at 0 with headroom for labels
ax.set_ylim(bottom=0, top=max(values) * 1.15)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
