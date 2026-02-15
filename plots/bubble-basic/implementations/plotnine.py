""" pyplots.ai
bubble-basic: Basic Bubble Chart
Library: plotnine 0.15.3 | Python 3.14.3
Quality: 80/100 | Updated: 2026-02-15
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    element_blank,
    element_line,
    element_text,
    geom_point,
    ggplot,
    labs,
    scale_size_area,
    scale_x_continuous,
    scale_y_continuous,
    theme,
    theme_minimal,
)


# Data
np.random.seed(42)
n_cities = 40
gdp_per_capita = np.random.lognormal(mean=10.2, sigma=0.5, size=n_cities) / 1000
life_expectancy = 55 + 20 * (1 - np.exp(-gdp_per_capita / 40)) + np.random.normal(0, 2, n_cities)
population = np.random.lognormal(mean=2.5, sigma=1.0, size=n_cities)

df = pd.DataFrame(
    {"gdp_per_capita": gdp_per_capita, "life_expectancy": np.clip(life_expectancy, 50, 88), "population": population}
)

# Plot
plot = (
    ggplot(df, aes(x="gdp_per_capita", y="life_expectancy", size="population"))
    + geom_point(color="#306998", alpha=0.6)
    + scale_size_area(max_size=20, name="Population (M)")
    + scale_x_continuous(labels=lambda lst: [f"${v:.0f}k" for v in lst])
    + scale_y_continuous(labels=lambda lst: [f"{v:.0f}" for v in lst])
    + labs(
        x="GDP per Capita (USD thousands)",
        y="Life Expectancy (years)",
        title="bubble-basic \u00b7 plotnine \u00b7 pyplots.ai",
    )
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        text=element_text(size=14),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        plot_title=element_text(size=24),
        legend_title=element_text(size=18),
        legend_text=element_text(size=16),
        panel_grid_major=element_line(alpha=0.2),
        panel_grid_minor=element_blank(),
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
