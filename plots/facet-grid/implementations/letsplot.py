"""pyplots.ai
facet-grid: Faceted Grid Plot
Library: lets-plot | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import numpy as np
import pandas as pd
from lets_plot import *


LetsPlot.setup_html()

# Data - Plant growth experiment across conditions
np.random.seed(42)

# Create factorial design: 2 soil types x 3 light levels
soil_types = ["Sandy", "Clay"]
light_levels = ["Low", "Medium", "High"]

data = []
for soil in soil_types:
    for light in light_levels:
        n_plants = 25
        # Base growth depends on conditions
        base_growth = {"Low": 8, "Medium": 15, "High": 22}[light]
        soil_bonus = 2 if soil == "Clay" else 0

        # Generate plant data
        water = np.random.uniform(50, 150, n_plants)
        growth = base_growth + soil_bonus + water * 0.1 + np.random.normal(0, 2, n_plants)

        for w, g in zip(water, growth):
            data.append({"Water (mL/day)": w, "Growth (cm)": max(0, g), "Soil Type": soil, "Light Level": light})

df = pd.DataFrame(data)

# Create faceted grid plot - scatter with trend
plot = (
    ggplot(df, aes(x="Water (mL/day)", y="Growth (cm)"))
    + geom_point(color="#306998", size=4, alpha=0.7)
    + geom_smooth(method="lm", color="#FFD43B", size=1.5)
    + facet_grid(x="Soil Type", y="Light Level")
    + labs(title="facet-grid · letsplot · pyplots.ai", x="Water (mL/day)", y="Growth (cm)")
    + theme_minimal()
    + theme(
        plot_title=element_text(size=24),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        strip_text=element_text(size=18),
    )
    + ggsize(1600, 900)
)

# Save outputs
ggsave(plot, "plot.png", path=".", scale=3)
ggsave(plot, "plot.html", path=".")
