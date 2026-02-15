""" pyplots.ai
heatmap-basic: Basic Heatmap
Library: matplotlib 3.10.8 | Python 3.14.3
Quality: 89/100 | Updated: 2026-02-15
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import TwoSlopeNorm


# Data - department correlation matrix with realistic patterns
departments = ["Sales", "Marketing", "Support", "Dev", "HR", "Finance", "Ops", "Legal"]
n = len(departments)

data = np.array(
    [
        [1.00, 0.82, 0.35, 0.12, -0.15, 0.61, 0.44, 0.08],  # Sales
        [0.82, 1.00, 0.28, 0.18, 0.10, 0.48, 0.30, -0.20],  # Marketing
        [0.35, 0.28, 1.00, 0.55, 0.22, -0.38, 0.60, 0.15],  # Support
        [0.12, 0.18, 0.55, 1.00, -0.10, -0.65, 0.42, -0.30],  # Dev
        [-0.15, 0.10, 0.22, -0.10, 1.00, 0.30, -0.08, 0.52],  # HR
        [0.61, 0.48, -0.38, -0.65, 0.30, 1.00, 0.05, 0.40],  # Finance
        [0.44, 0.30, 0.60, 0.42, -0.08, 0.05, 1.00, 0.20],  # Ops
        [0.08, -0.20, 0.15, -0.30, 0.52, 0.40, 0.20, 1.00],  # Legal
    ]
)

# Plot - square figure for 3600x3600 at 300 dpi
fig, ax = plt.subplots(figsize=(12, 12))

# Heatmap with imshow - idiomatic for grid-aligned data
norm = TwoSlopeNorm(vmin=-1, vcenter=0, vmax=1)
im = ax.imshow(data, cmap="coolwarm", norm=norm, aspect="equal")

# Remove all spines for a modern, clean look
for spine in ax.spines.values():
    spine.set_visible(False)

# Cell edges via grid lines for clean separation
ax.set_xticks(np.arange(n + 1) - 0.5, minor=True)
ax.set_yticks(np.arange(n + 1) - 0.5, minor=True)
ax.grid(which="minor", color="white", linewidth=2)
ax.tick_params(which="minor", bottom=False, left=False)

# Tick labels centered on cells
ax.set_xticks(np.arange(n))
ax.set_yticks(np.arange(n))
ax.set_xticklabels(departments, fontsize=16, rotation=45, ha="right")
ax.set_yticklabels(departments, fontsize=16)
ax.tick_params(axis="both", length=0)

# Colorbar with clean styling
cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03, aspect=30)
cbar.ax.tick_params(labelsize=16)
cbar.set_label("Correlation Coefficient", fontsize=18, labelpad=12)
cbar.outline.set_visible(False)

# Cell annotations with adaptive text color and emphasis on strong correlations
for i in range(n):
    for j in range(n):
        value = data[i, j]
        # Adaptive text color for readability
        text_color = "white" if abs(value) > 0.55 else "#333333"
        # Emphasize strong off-diagonal correlations (|r| >= 0.6) with larger, bolder text
        is_strong = abs(value) >= 0.6 and i != j
        ax.text(
            j,
            i,
            f"{value:.2f}",
            ha="center",
            va="center",
            fontsize=16 if is_strong else 13,
            color=text_color,
            fontweight="bold" if is_strong else "medium",
        )

# Labels and title
ax.set_xlabel("Department", fontsize=20, labelpad=12)
ax.set_ylabel("Department", fontsize=20, labelpad=12)
ax.set_title("heatmap-basic · matplotlib · pyplots.ai", fontsize=24, fontweight="medium", pad=20)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
