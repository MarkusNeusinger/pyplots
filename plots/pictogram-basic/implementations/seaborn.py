""" pyplots.ai
pictogram-basic: Pictogram Chart (Isotype Visualization)
Library: seaborn 0.13.2 | Python 3.14.3
Quality: 76/100 | Created: 2026-03-10
"""

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Style
sns.set_style("white")

# Data — Fruit production (thousands of tonnes)
categories = ["Apples", "Oranges", "Bananas", "Grapes", "Strawberries"]
values = [35, 22, 18, 28, 12]
unit_value = 5
colors = ["#306998", "#E4873D", "#F2C53D", "#7A6DAC", "#C44E52"]

# Plot
fig, ax = plt.subplots(figsize=(16, 9))
marker_size = 900
spacing_x = 1.0
spacing_y = 1.2

for i, (_cat, val, color) in enumerate(zip(categories, values, colors, strict=True)):
    full_icons = int(val // unit_value)
    partial = (val % unit_value) / unit_value

    # Full icons
    if full_icons > 0:
        x_full = np.arange(full_icons) * spacing_x
        y_full = np.full(full_icons, i * spacing_y)
        ax.scatter(x_full, y_full, s=marker_size, marker="o", color=color, edgecolors="white", linewidth=1.5, zorder=3)

    # Partial icon (same size, lighter shade)
    if partial > 0:
        r, g, b = mcolors.to_rgb(color)
        faded = (r + (1 - r) * (1 - partial), g + (1 - g) * (1 - partial), b + (1 - b) * (1 - partial))
        ax.scatter(
            full_icons * spacing_x,
            i * spacing_y,
            s=marker_size,
            marker="o",
            color=faded,
            edgecolors="white",
            linewidth=1.5,
            zorder=3,
        )

# Labels and styling
ax.set_yticks([i * spacing_y for i in range(len(categories))])
ax.set_yticklabels(categories, fontsize=20, fontweight="medium")
ax.tick_params(axis="y", length=0, pad=10)
ax.tick_params(axis="x", which="both", bottom=False, labelbottom=False)

max_icons = max(val // unit_value for val in values) + 1
ax.set_xlim(-0.7, max_icons * spacing_x + 0.3)
ax.set_ylim(-0.8, (len(categories) - 1) * spacing_y + 0.8)

ax.set_title("pictogram-basic · seaborn · pyplots.ai", fontsize=24, fontweight="medium", pad=20)

sns.despine(left=True, bottom=True)

# Legend
ax.text(
    0.98,
    0.02,
    f"● = {unit_value},000 tonnes  (lighter = partial)",
    transform=ax.transAxes,
    fontsize=16,
    ha="right",
    va="bottom",
    color="#555555",
)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
