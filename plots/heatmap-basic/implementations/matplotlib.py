"""pyplots.ai
heatmap-basic: Basic Heatmap
Library: matplotlib 3.10.8 | Python 3.14.3
Quality: /100 | Updated: 2026-02-15
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import TwoSlopeNorm


# Data - department correlation matrix with realistic patterns
departments = ["Sales", "Marketing", "Support", "Dev", "HR", "Finance", "Ops", "Legal"]
n = len(departments)

# Craft realistic correlations: related departments correlate more strongly
data = np.array(
    [
        [1.00, 0.82, 0.35, 0.12, -0.05, 0.61, 0.44, 0.08],  # Sales
        [0.82, 1.00, 0.28, 0.18, 0.10, 0.48, 0.30, 0.05],  # Marketing
        [0.35, 0.28, 1.00, 0.55, 0.22, -0.10, 0.60, 0.15],  # Support
        [0.12, 0.18, 0.55, 1.00, 0.08, -0.25, 0.42, -0.12],  # Dev
        [-0.05, 0.10, 0.22, 0.08, 1.00, 0.30, 0.18, 0.52],  # HR
        [0.61, 0.48, -0.10, -0.25, 0.30, 1.00, 0.35, 0.40],  # Finance
        [0.44, 0.30, 0.60, 0.42, 0.18, 0.35, 1.00, 0.20],  # Ops
        [0.08, 0.05, 0.15, -0.12, 0.52, 0.40, 0.20, 1.00],  # Legal
    ]
)

# Plot (square format for matrix visualization)
fig, ax = plt.subplots(figsize=(12, 12))

# Heatmap with diverging colormap centered at zero
norm = TwoSlopeNorm(vmin=-1, vcenter=0, vmax=1)
im = ax.matshow(data, cmap="RdBu_r", norm=norm)

# Colorbar
cbar = fig.colorbar(im, ax=ax, shrink=0.78, pad=0.02, aspect=30)
cbar.ax.tick_params(labelsize=16)
cbar.set_label("Correlation Coefficient", fontsize=18, labelpad=12)
cbar.outline.set_visible(False)

# Tick labels
ax.set_xticks(np.arange(n))
ax.set_yticks(np.arange(n))
ax.set_xticklabels(departments, fontsize=16, rotation=45, ha="left")
ax.set_yticklabels(departments, fontsize=16)
ax.xaxis.set_ticks_position("bottom")
ax.tick_params(axis="both", length=0)

# Cell value annotations with adaptive text color
for i in range(n):
    for j in range(n):
        value = data[i, j]
        text_color = "white" if abs(value) > 0.55 else "black"
        ax.text(j, i, f"{value:.2f}", ha="center", va="center", fontsize=14, color=text_color, fontweight="bold")

# Subtle cell borders
for i in range(n + 1):
    ax.axhline(i - 0.5, color="white", linewidth=1.5)
    ax.axvline(i - 0.5, color="white", linewidth=1.5)

# Labels and title
ax.set_xlabel("Department", fontsize=20, labelpad=12)
ax.set_ylabel("Department", fontsize=20, labelpad=12)
ax.set_title(
    "Department Correlation · heatmap-basic · matplotlib · pyplots.ai", fontsize=24, fontweight="medium", pad=15
)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
