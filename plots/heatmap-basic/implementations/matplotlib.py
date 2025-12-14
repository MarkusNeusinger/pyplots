"""
heatmap-basic: Basic Heatmap
Library: matplotlib
"""

import matplotlib.pyplot as plt
import numpy as np


# Data - correlation-like matrix with meaningful labels
np.random.seed(42)
categories = ["Sales", "Marketing", "Support", "Dev", "HR", "Finance", "Ops", "Legal"]
n = len(categories)

# Generate a correlation-like symmetric matrix
raw = np.random.randn(n, n)
data = (raw + raw.T) / 2  # Make symmetric
np.fill_diagonal(data, 1)  # Perfect correlation on diagonal
data = np.clip(data, -1, 1)  # Clip to valid correlation range

# Create plot (4800x2700 px)
fig, ax = plt.subplots(figsize=(16, 9))

# Heatmap with diverging colormap for positive/negative values
im = ax.imshow(data, cmap="RdBu_r", vmin=-1, vmax=1, aspect="auto")

# Add colorbar
cbar = fig.colorbar(im, ax=ax, shrink=0.8, pad=0.02)
cbar.ax.tick_params(labelsize=16)
cbar.set_label("Correlation", fontsize=18)

# Set ticks and labels
ax.set_xticks(np.arange(n))
ax.set_yticks(np.arange(n))
ax.set_xticklabels(categories, fontsize=16, rotation=45, ha="right")
ax.set_yticklabels(categories, fontsize=16)

# Add value annotations in cells
for i in range(n):
    for j in range(n):
        value = data[i, j]
        # Use white text on dark cells, black on light cells
        text_color = "white" if abs(value) > 0.5 else "black"
        ax.text(j, i, f"{value:.2f}", ha="center", va="center", fontsize=14, color=text_color)

# Labels and title
ax.set_xlabel("Department", fontsize=20)
ax.set_ylabel("Department", fontsize=20)
ax.set_title("heatmap-basic · matplotlib · pyplots.ai", fontsize=24)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
