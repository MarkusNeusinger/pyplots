"""pyplots.ai
bar-categorical: Categorical Count Bar Chart
Library: matplotlib | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Data - survey responses for product preference
np.random.seed(42)
categories = ["Product A", "Product B", "Product C", "Product D", "Product E"]
probabilities = [0.30, 0.25, 0.20, 0.15, 0.10]  # Different frequencies for variety
raw_data = np.random.choice(categories, size=500, p=probabilities)

# Count frequencies
df = pd.DataFrame({"Category": raw_data})
counts = df["Category"].value_counts().sort_values(ascending=False)

# Create plot (4800x2700 px at 300 dpi = 16x9 inches)
fig, ax = plt.subplots(figsize=(16, 9))

# Bar chart with Python Blue
bars = ax.bar(counts.index, counts.values, color="#306998", edgecolor="#1e4a6e", linewidth=2)

# Add value labels on top of bars
for bar, value in zip(bars, counts.values, strict=True):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 5,
        str(value),
        ha="center",
        va="bottom",
        fontsize=18,
        fontweight="bold",
    )

# Styling
ax.set_xlabel("Product Category", fontsize=20)
ax.set_ylabel("Count (Frequency)", fontsize=20)
ax.set_title("bar-categorical · matplotlib · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)
ax.grid(True, axis="y", alpha=0.3, linestyle="--")

# Remove top and right spines for cleaner look
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
