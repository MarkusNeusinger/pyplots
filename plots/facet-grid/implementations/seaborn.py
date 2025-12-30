"""pyplots.ai
facet-grid: Faceted Grid Plot
Library: seaborn | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import numpy as np
import pandas as pd
import seaborn as sns


# Data - Plant growth experiment across conditions
np.random.seed(42)

# Create experimental data: plant growth by water level and light exposure
water_levels = ["Low", "Medium", "High"]
light_conditions = ["Shade", "Partial", "Full Sun"]
n_per_group = 40

data = []
for water in water_levels:
    for light in light_conditions:
        # Base growth varies by conditions
        base_growth = 10 + (water_levels.index(water) * 8) + (light_conditions.index(light) * 5)
        base_height = 5 + (water_levels.index(water) * 3) + (light_conditions.index(light) * 2)

        # Generate correlated height and leaf count
        heights = np.random.normal(base_height, 1.5, n_per_group)
        leaf_counts = base_growth + heights * 1.5 + np.random.normal(0, 2, n_per_group)

        for height, leaf in zip(heights, leaf_counts, strict=True):
            data.append(
                {"Height (cm)": max(1, height), "Leaf Count": max(1, leaf), "Water Level": water, "Light": light}
            )

df = pd.DataFrame(data)

# Create faceted grid plot
sns.set_context("talk", font_scale=1.3)
g = sns.FacetGrid(
    df,
    col="Light",
    row="Water Level",
    col_order=light_conditions,
    row_order=water_levels,
    height=4,
    aspect=1.3,
    margin_titles=True,
)

# Map scatter plot to each facet
g.map_dataframe(sns.scatterplot, x="Height (cm)", y="Leaf Count", s=150, alpha=0.7, color="#306998")

# Add regression line to each facet
g.map_dataframe(sns.regplot, x="Height (cm)", y="Leaf Count", scatter=False, color="#FFD43B", line_kws={"linewidth": 3})

# Customize appearance
g.set_titles(col_template="{col_name}", row_template="{row_name}", size=20)
g.set_axis_labels("Height (cm)", "Leaf Count", fontsize=18)

# Adjust tick label sizes
for ax in g.axes.flat:
    ax.tick_params(axis="both", labelsize=14)
    ax.grid(True, alpha=0.3, linestyle="--")

# Add main title
g.figure.suptitle("facet-grid · seaborn · pyplots.ai", fontsize=26, y=1.02)

# Adjust layout
g.tight_layout()

# Save plot
g.savefig("plot.png", dpi=300, bbox_inches="tight")
