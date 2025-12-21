""" pyplots.ai
slope-basic: Basic Slope Chart (Slopegraph)
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-17
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D


# Data: Sales performance (in millions $) comparing Q1 vs Q4
np.random.seed(42)
entities = ["Product A", "Product B", "Product C", "Product D", "Product E", "Product F", "Product G", "Product H"]

# Generate realistic sales data showing mix of increases and decreases
q1_sales = [45, 32, 58, 27, 41, 53, 38, 62]
q4_sales = [52, 28, 71, 35, 38, 48, 55, 59]  # Some increase, some decrease

# Create DataFrame
df = pd.DataFrame({"entity": entities, "Q1": q1_sales, "Q4": q4_sales})

# Calculate change direction for color coding
df["change"] = df["Q4"] - df["Q1"]
df["direction"] = df["change"].apply(lambda x: "Increase" if x > 0 else "Decrease")

# Set up figure
fig, ax = plt.subplots(figsize=(16, 9))

# Color mapping for direction
colors = {"Increase": "#306998", "Decrease": "#FFD43B"}

# Plot lines connecting Q1 to Q4 for each entity
for _idx, row in df.iterrows():
    color = colors[row["direction"]]
    ax.plot([0, 1], [row["Q1"], row["Q4"]], color=color, linewidth=3, alpha=0.8)
    # Add markers at endpoints
    ax.scatter([0], [row["Q1"]], color=color, s=200, zorder=5)
    ax.scatter([1], [row["Q4"]], color=color, s=200, zorder=5)

# Add entity labels at both endpoints
for _idx, row in df.iterrows():
    color = colors[row["direction"]]
    # Left side labels (Q1)
    ax.annotate(
        f"{row['entity']} ({row['Q1']})",
        xy=(0, row["Q1"]),
        xytext=(-0.05, row["Q1"]),
        fontsize=14,
        ha="right",
        va="center",
        color=color,
        fontweight="bold",
    )
    # Right side labels (Q4)
    ax.annotate(
        f"{row['entity']} ({row['Q4']})",
        xy=(1, row["Q4"]),
        xytext=(1.05, row["Q4"]),
        fontsize=14,
        ha="left",
        va="center",
        color=color,
        fontweight="bold",
    )

# Configure axes
ax.set_xlim(-0.3, 1.3)
ax.set_ylim(min(q1_sales + q4_sales) - 5, max(q1_sales + q4_sales) + 5)

# Set x-axis ticks for time points
ax.set_xticks([0, 1])
ax.set_xticklabels(["Q1 2024", "Q4 2024"], fontsize=20, fontweight="bold")
ax.tick_params(axis="y", labelsize=16)

# Remove spines for cleaner look
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["bottom"].set_visible(False)

# Labels and title
ax.set_xlabel("")
ax.set_ylabel("Sales ($ millions)", fontsize=20)
ax.set_title("slope-basic · seaborn · pyplots.ai", fontsize=24, fontweight="bold")

# Add subtle grid for y-axis only
ax.yaxis.grid(True, alpha=0.3, linestyle="--")
ax.xaxis.grid(False)

# Add legend for direction
legend_elements = [
    Line2D([0], [0], color="#306998", linewidth=3, label="Increase"),
    Line2D([0], [0], color="#FFD43B", linewidth=3, label="Decrease"),
]
ax.legend(handles=legend_elements, loc="upper right", fontsize=14, framealpha=0.9)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
