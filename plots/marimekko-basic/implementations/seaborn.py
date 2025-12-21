""" pyplots.ai
marimekko-basic: Basic Marimekko Chart
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 93/100 | Created: 2025-12-16
"""

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Data: Market share by region (x-category) and product line (y-category)
data = {
    "Region": [
        "North America",
        "North America",
        "North America",
        "Europe",
        "Europe",
        "Europe",
        "Asia Pacific",
        "Asia Pacific",
        "Asia Pacific",
        "Latin America",
        "Latin America",
        "Latin America",
    ],
    "Product": ["Software", "Hardware", "Services"] * 4,
    "Revenue": [
        45,
        30,
        25,  # North America: $100M total
        35,
        25,
        20,  # Europe: $80M total
        50,
        40,
        30,  # Asia Pacific: $120M total
        15,
        10,
        15,
    ],  # Latin America: $40M total
}

df = pd.DataFrame(data)

# Calculate totals per region for bar widths
region_totals = df.groupby("Region")["Revenue"].sum()
region_order = ["North America", "Europe", "Asia Pacific", "Latin America"]
region_totals = region_totals.reindex(region_order)
total_revenue = region_totals.sum()

# Calculate widths (proportional to region totals)
widths = (region_totals / total_revenue).values
cumulative_widths = np.concatenate([[0], np.cumsum(widths)[:-1]])

# Colors for products (Python Blue, Python Yellow, and additional colorblind-safe)
colors = {"Software": "#306998", "Hardware": "#FFD43B", "Services": "#6BAA75"}
products = ["Software", "Hardware", "Services"]

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Draw Marimekko bars
for i, region in enumerate(region_order):
    region_data = df[df["Region"] == region].set_index("Product")["Revenue"]
    region_total = region_data.sum()

    # Calculate heights as proportions within each region
    heights = (region_data / region_total).reindex(products).values
    cumulative_heights = np.concatenate([[0], np.cumsum(heights)[:-1]])

    x_start = cumulative_widths[i]
    bar_width = widths[i]

    for j, product in enumerate(products):
        rect = mpatches.Rectangle(
            (x_start, cumulative_heights[j]),
            bar_width,
            heights[j],
            facecolor=colors[product],
            edgecolor="white",
            linewidth=2,
        )
        ax.add_patch(rect)

        # Add value labels for larger segments
        if heights[j] > 0.15:
            value = region_data[product]
            ax.text(
                x_start + bar_width / 2,
                cumulative_heights[j] + heights[j] / 2,
                f"${value}M",
                ha="center",
                va="center",
                fontsize=14,
                fontweight="bold",
                color="white" if product == "Software" else "black",
            )

# Set axis properties
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

# X-axis: region labels centered under each bar
x_centers = cumulative_widths + widths / 2
ax.set_xticks(x_centers)
ax.set_xticklabels(region_order, fontsize=16)

# Add width percentages below region names
for center, width in zip(x_centers, widths, strict=True):
    ax.text(center, -0.08, f"({width * 100:.0f}%)", ha="center", va="top", fontsize=12, color="gray")

# Y-axis as percentage
ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
ax.set_yticklabels(["0%", "25%", "50%", "75%", "100%"], fontsize=16)

# Labels
ax.set_xlabel("Region (width = share of total revenue)", fontsize=20)
ax.set_ylabel("Product Mix (%)", fontsize=20)
ax.set_title("marimekko-basic · seaborn · pyplots.ai", fontsize=24)

# Legend
legend_patches = [mpatches.Patch(color=colors[p], label=p) for p in products]
ax.legend(handles=legend_patches, loc="upper right", fontsize=14, framealpha=0.9)

# Grid (subtle horizontal lines)
ax.yaxis.grid(True, alpha=0.3, linestyle="--")
ax.set_axisbelow(True)

# Remove top and right spines
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
