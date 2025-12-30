"""pyplots.ai
facet-grid: Faceted Grid Plot
Library: plotnine | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    element_rect,
    element_text,
    facet_grid,
    geom_point,
    ggplot,
    labs,
    scale_color_manual,
    theme,
    theme_minimal,
)


# Data - Plant growth experiment with different treatments and conditions
np.random.seed(42)

# Create experimental data: plant growth under different light and water conditions
light_levels = ["Low Light", "Medium Light", "High Light"]
water_levels = ["Low Water", "High Water"]

data = []
for light in light_levels:
    for water in water_levels:
        n_plants = 25
        # Base growth depends on conditions
        base_growth = {"Low Light": 5, "Medium Light": 12, "High Light": 18}[light]
        water_boost = {"Low Water": 0, "High Water": 4}[water]

        # Generate plant data
        for _ in range(n_plants):
            initial_size = np.random.uniform(2, 6)
            growth_rate = base_growth + water_boost + np.random.normal(0, 2)
            final_size = initial_size + growth_rate + np.random.normal(0, 1.5)
            data.append(
                {
                    "Initial Size (cm)": initial_size,
                    "Final Size (cm)": max(final_size, initial_size),
                    "Light Condition": light,
                    "Water Condition": water,
                }
            )

df = pd.DataFrame(data)

# Create faceted grid plot
plot = (
    ggplot(df, aes(x="Initial Size (cm)", y="Final Size (cm)", color="Light Condition"))
    + geom_point(size=4, alpha=0.7)
    + facet_grid("Water Condition ~ Light Condition")
    + scale_color_manual(values=["#306998", "#FFD43B", "#4CAF50"])
    + labs(
        x="Initial Size (cm)", y="Final Size (cm)", title="facet-grid · plotnine · pyplots.ai", color="Light Condition"
    )
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        plot_title=element_text(size=24, ha="center"),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        legend_text=element_text(size=16),
        legend_title=element_text(size=18),
        strip_text=element_text(size=18, weight="bold"),
        strip_background=element_rect(fill="#E8E8E8", color="#CCCCCC"),
        panel_spacing=0.3,
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
