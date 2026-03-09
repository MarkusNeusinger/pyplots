"""pyplots.ai
heatmap-loss-triangle: Actuarial Loss Development Triangle
Library: matplotlib | Python 3.13
Quality: pending | Created: 2026-03-09
"""

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch


# Data
np.random.seed(42)

accident_years = list(range(2015, 2025))
development_periods = list(range(1, 11))
n_years = len(accident_years)
n_periods = len(development_periods)

# Age-to-age development factors (decreasing as claims mature)
dev_factors = [2.50, 1.60, 1.30, 1.15, 1.08, 1.05, 1.03, 1.02, 1.01]

# Generate cumulative paid claims triangle
# Start with initial claims for each accident year
initial_claims = np.array([4200, 4500, 4800, 5100, 5400, 5700, 6000, 6300, 6600, 7000], dtype=float)

triangle = np.full((n_years, n_periods), np.nan)
is_projected = np.full((n_years, n_periods), True)

# Fill the upper-left actual triangle
for i in range(n_years):
    triangle[i, 0] = initial_claims[i]
    n_actual = n_periods - i
    for j in range(1, n_actual):
        noise = 1 + np.random.uniform(-0.03, 0.03)
        triangle[i, j] = triangle[i, j - 1] * dev_factors[j - 1] * noise
    for j in range(n_actual):
        is_projected[i, j] = False

# Fill the lower-right projected triangle using chain-ladder
for i in range(1, n_years):
    n_actual = n_periods - i
    for j in range(n_actual, n_periods):
        triangle[i, j] = triangle[i, j - 1] * dev_factors[j - 1]

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

# Normalize colors by cumulative amount
valid_vals = triangle[~np.isnan(triangle)]
norm = mcolors.Normalize(vmin=valid_vals.min(), vmax=valid_vals.max())
cmap_actual = plt.cm.Blues
cmap_projected = plt.cm.Oranges

# Draw cells
for i in range(n_years):
    for j in range(n_periods):
        val = triangle[i, j]
        if np.isnan(val):
            continue

        projected = is_projected[i, j]
        cmap = cmap_projected if projected else cmap_actual
        facecolor = cmap(norm(val) * 0.7 + 0.15)

        rect = plt.Rectangle((j, n_years - 1 - i), 1, 1, facecolor=facecolor, edgecolor="white", linewidth=1.5)
        ax.add_patch(rect)

        # Annotate with formatted value
        text_val = f"{val:,.0f}"
        brightness = sum(facecolor[:3]) / 3
        text_color = "white" if brightness < 0.55 else "#333333"
        fontstyle = "italic" if projected else "normal"
        ax.text(
            j + 0.5,
            n_years - 1 - i + 0.5,
            text_val,
            ha="center",
            va="center",
            fontsize=10,
            color=text_color,
            fontstyle=fontstyle,
        )

# Development factors row at the bottom
for j in range(len(dev_factors)):
    ax.text(
        j + 1.0,
        -0.6,
        f"{dev_factors[j]:.2f}",
        ha="center",
        va="center",
        fontsize=10,
        color="#555555",
        fontweight="medium",
    )
ax.text(0.5, -0.6, "Dev\nFactor", ha="center", va="center", fontsize=9, color="#555555", fontweight="bold")

# Style
ax.set_xlim(0, n_periods)
ax.set_ylim(-1.2, n_years)
ax.set_xticks([j + 0.5 for j in range(n_periods)])
ax.set_xticklabels(development_periods, fontsize=14)
ax.set_yticks([i + 0.5 for i in range(n_years)])
ax.set_yticklabels(list(reversed(accident_years)), fontsize=14)
ax.set_xlabel("Development Period (Years)", fontsize=20)
ax.set_ylabel("Accident Year", fontsize=20)
ax.set_title("heatmap-loss-triangle \u00b7 matplotlib \u00b7 pyplots.ai", fontsize=24, fontweight="medium", pad=20)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.tick_params(axis="both", length=0)

# Legend
legend_elements = [
    Patch(facecolor=cmap_actual(0.5), edgecolor="white", label="Actual (Observed)"),
    Patch(facecolor=cmap_projected(0.5), edgecolor="white", label="Projected (Estimated)"),
]
ax.legend(
    handles=legend_elements,
    loc="lower left",
    fontsize=14,
    frameon=True,
    fancybox=True,
    shadow=False,
    edgecolor="#cccccc",
    facecolor="white",
    bbox_to_anchor=(0.0, -0.15),
)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
