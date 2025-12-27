"""pyplots.ai
scatter-size-mapped: Bubble Chart
Library: plotnine | Python 3.13
Quality: pending | Created: 2025-12-27
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    element_text,
    geom_point,
    ggplot,
    labs,
    scale_color_manual,
    scale_size_continuous,
    theme,
    theme_minimal,
)


# Data - Country economic indicators
np.random.seed(42)

regions = ["Europe", "Asia", "Americas", "Africa"]
region_colors = {"Europe": "#306998", "Asia": "#FFD43B", "Americas": "#4CAF50", "Africa": "#E57373"}

# Generate realistic country data
n_countries = 40
data = {"country": [f"Country_{i}" for i in range(n_countries)], "region": np.random.choice(regions, n_countries)}

# GDP per capita varies by region (1,000 - 80,000)
gdp_base = {"Europe": 40000, "Asia": 25000, "Americas": 30000, "Africa": 8000}
data["gdp_per_capita"] = [max(1000, min(80000, gdp_base[r] + np.random.normal(0, 15000))) for r in data["region"]]

# Life expectancy correlates with GDP (50 - 85)
data["life_expectancy"] = [
    max(50, min(85, 55 + (gdp / 80000) * 25 + np.random.normal(0, 3))) for gdp in data["gdp_per_capita"]
]

# Population (log scale, 1M - 1.4B)
data["population"] = np.exp(np.random.uniform(np.log(1e6), np.log(1.4e9), n_countries))

df = pd.DataFrame(data)

# Create bubble chart
plot = (
    ggplot(df, aes(x="gdp_per_capita", y="life_expectancy", size="population", color="region"))
    + geom_point(alpha=0.6)
    + scale_size_continuous(
        range=(3, 20), breaks=[1e7, 1e8, 5e8, 1e9], labels=["10M", "100M", "500M", "1B"], name="Population"
    )
    + scale_color_manual(values=region_colors, name="Region")
    + labs(x="GDP per Capita (USD)", y="Life Expectancy (Years)", title="scatter-size-mapped · plotnine · pyplots.ai")
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        text=element_text(size=14),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        plot_title=element_text(size=24),
        legend_text=element_text(size=14),
        legend_title=element_text(size=16),
    )
)

# Save plot
plot.save("plot.png", dpi=300)
