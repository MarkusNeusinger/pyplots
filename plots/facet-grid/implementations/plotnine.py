""" pyplots.ai
facet-grid: Faceted Grid Plot
Library: plotnine 0.15.2 | Python 3.13.11
Quality: 72/100 | Created: 2025-12-30
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    element_line,
    element_text,
    facet_grid,
    geom_point,
    ggplot,
    labs,
    scale_color_brewer,
    theme,
    theme_minimal,
)


# Data - Plant growth study with soil type and light conditions
np.random.seed(42)

# Create faceting variables
soil_types = ["Sandy", "Loamy", "Clay"]
light_levels = ["Low", "Medium", "High"]
species = ["Basil", "Tomato", "Fern"]

# Generate realistic data for each combination
data = []
for soil in soil_types:
    for light in light_levels:
        # Base growth depends on soil and light
        soil_effect = {"Sandy": -5, "Loamy": 0, "Clay": 3}[soil]
        light_effect = {"Low": -8, "Medium": 0, "High": 10}[light]

        for sp in species:
            species_effect = {"Basil": 0, "Tomato": 5, "Fern": -3}[sp]
            n_points = 15

            # Water amount (x-axis)
            water = np.random.uniform(30, 60, n_points)

            # Growth depends on water, soil, light, and species
            base_growth = 20 + 0.8 * water + soil_effect + light_effect + species_effect
            growth = base_growth + np.random.randn(n_points) * 5

            for i in range(n_points):
                data.append(
                    {"water": water[i], "growth": growth[i], "soil_type": soil, "light_level": light, "species": sp}
                )

df = pd.DataFrame(data)

# Ensure correct ordering of categorical variables
df["soil_type"] = pd.Categorical(df["soil_type"], categories=soil_types, ordered=True)
df["light_level"] = pd.Categorical(df["light_level"], categories=light_levels, ordered=True)

# Plot - Faceted grid showing growth patterns across soil and light conditions
plot = (
    ggplot(df, aes(x="water", y="growth", color="species"))
    + geom_point(size=4, alpha=0.7)
    + facet_grid("soil_type ~ light_level")
    + scale_color_brewer(type="qual", palette="Set2")
    + labs(title="facet-grid \u00b7 plotnine \u00b7 pyplots.ai", x="Water (mL/day)", y="Growth (cm)")
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        plot_title=element_text(size=24, face="bold", ha="center"),
        axis_title=element_text(size=18),
        axis_text=element_text(size=14),
        strip_text_x=element_text(size=16, face="bold"),
        strip_text_y=element_text(size=16, face="bold", angle=0),
        legend_title=element_text(size=16),
        legend_text=element_text(size=14),
        legend_position="right",
        panel_grid_major=element_line(color="#cccccc", alpha=0.3),
        panel_grid_minor=element_line(color="#eeeeee", alpha=0.2),
        panel_spacing=0.15,
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
