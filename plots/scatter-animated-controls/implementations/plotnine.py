"""pyplots.ai
scatter-animated-controls: Animated Scatter Plot with Play Controls
Library: plotnine | Python 3.13
Quality: pending | Created: 2025-12-31
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    element_rect,
    element_text,
    facet_wrap,
    geom_point,
    ggplot,
    labs,
    scale_color_brewer,
    scale_size_continuous,
    scale_x_continuous,
    theme,
    theme_minimal,
)


# Data - Simulated country metrics over time (Gapminder-style)
np.random.seed(42)

countries = ["Country A", "Country B", "Country C", "Country D", "Country E", "Country F"]
regions = ["North", "South", "East", "East", "West", "West"]
years = [2000, 2005, 2010, 2015, 2020]
n_countries = len(countries)
n_years = len(years)

# Generate base values for each country
base_gdp = np.array([5000, 8000, 15000, 25000, 35000, 45000])
base_life_exp = np.array([55, 60, 68, 72, 75, 78])
base_population = np.array([50, 120, 80, 200, 150, 100])  # in millions

data = []
for i, country in enumerate(countries):
    for j, year in enumerate(years):
        # GDP grows over time with some noise
        gdp_growth = 1 + 0.05 * j + np.random.uniform(-0.02, 0.02)
        gdp = base_gdp[i] * gdp_growth

        # Life expectancy increases slowly
        life_exp = base_life_exp[i] + 1.5 * j + np.random.uniform(-0.5, 0.5)

        # Population grows
        pop_growth = 1 + 0.02 * j + np.random.uniform(-0.01, 0.01)
        population = base_population[i] * pop_growth

        data.append(
            {
                "country": country,
                "region": regions[i],
                "year": year,
                "gdp_per_capita": gdp,
                "life_expectancy": life_exp,
                "population": population,
            }
        )

df = pd.DataFrame(data)

# Create faceted scatter plot (static alternative to animation)
plot = (
    ggplot(df, aes(x="gdp_per_capita", y="life_expectancy", color="region", size="population"))
    + geom_point(alpha=0.8)
    + facet_wrap("~year", ncol=3)
    + labs(
        x="GDP per Capita (USD)",
        y="Life Expectancy (years)",
        title="scatter-animated-controls · plotnine · pyplots.ai",
        color="Region",
        size="Population (millions)",
    )
    + scale_color_brewer(type="qual", palette="Set2")
    + scale_size_continuous(range=(3, 12))
    + scale_x_continuous(breaks=[10000, 30000, 50000], labels=lambda x: [f"{int(v / 1000)}k" for v in x])
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        text=element_text(size=14),
        axis_title=element_text(size=20),
        axis_text=element_text(size=14),
        axis_text_x=element_text(angle=45, hjust=1),
        plot_title=element_text(size=24, ha="center"),
        legend_text=element_text(size=14),
        legend_title=element_text(size=16),
        strip_text=element_text(size=18, weight="bold"),
        strip_background=element_rect(fill="#f0f0f0", color="none"),
        panel_spacing=0.3,
    )
)

# Save plot
plot.save("plot.png", dpi=300, verbose=False)
