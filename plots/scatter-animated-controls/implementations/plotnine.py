""" pyplots.ai
scatter-animated-controls: Animated Scatter Plot with Play Controls
Library: plotnine 0.15.2 | Python 3.13.11
Quality: 90/100 | Created: 2025-12-31
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    element_blank,
    element_line,
    element_rect,
    element_text,
    facet_wrap,
    geom_point,
    ggplot,
    labs,
    scale_color_brewer,
    scale_size_continuous,
    scale_x_continuous,
    scale_y_continuous,
    theme,
    theme_minimal,
)


# Data - Simulated country metrics over time (Gapminder-style)
np.random.seed(42)

countries = ["Nordland", "Australis", "Eastoria", "Pacifica", "Centralia", "Westmark"]
regions = ["Europe", "Americas", "Asia", "Asia", "Africa", "Europe"]
years = list(range(2000, 2021, 2))  # 11 time points: 2000-2020 every 2 years
n_countries = len(countries)
n_years = len(years)

# Generate base values for each country with distinct trajectories
base_gdp = np.array([25000, 12000, 8000, 3000, 1500, 35000])
base_life_exp = np.array([76, 72, 65, 58, 52, 79])
base_population = np.array([10, 45, 200, 130, 90, 25])  # in millions

data = []
for i, country in enumerate(countries):
    for j, year in enumerate(years):
        # Different growth patterns per region
        if regions[i] == "Asia":
            gdp_growth = 1 + 0.08 * j + np.random.uniform(-0.02, 0.02)  # Fast growth
        elif regions[i] == "Africa":
            gdp_growth = 1 + 0.04 * j + np.random.uniform(-0.03, 0.03)  # Moderate with volatility
        else:
            gdp_growth = 1 + 0.025 * j + np.random.uniform(-0.01, 0.01)  # Steady growth

        gdp = base_gdp[i] * gdp_growth

        # Life expectancy increases at different rates
        life_gain = 0.4 if regions[i] == "Africa" else 0.25
        life_exp = base_life_exp[i] + life_gain * j + np.random.uniform(-0.3, 0.3)

        # Population growth varies
        pop_rate = 0.025 if regions[i] in ["Asia", "Africa"] else 0.008
        pop_growth = 1 + pop_rate * j + np.random.uniform(-0.005, 0.005)
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

# Create faceted scatter plot showing key time points
# Select 6 key time points for facets (fills 2x3 grid perfectly)
key_years = [2000, 2004, 2008, 2012, 2016, 2020]
df_faceted = df[df["year"].isin(key_years)].copy()

plot = (
    ggplot(df_faceted, aes(x="gdp_per_capita", y="life_expectancy", color="region", size="population"))
    + geom_point(alpha=0.85)
    + facet_wrap("~year", ncol=3)
    + labs(
        x="GDP per Capita (USD)",
        y="Life Expectancy (years)",
        title="scatter-animated-controls · plotnine · pyplots.ai",
        color="Region",
        size="Population (M)",
    )
    + scale_color_brewer(type="qual", palette="Dark2")
    + scale_size_continuous(range=(4, 18), breaks=[25, 100, 200])
    + scale_x_continuous(breaks=[0, 30000, 60000], labels=["0", "30k", "60k"], limits=(-2000, 65000))
    + scale_y_continuous(breaks=[55, 65, 75, 85], limits=(50, 88))
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        text=element_text(size=12),
        axis_title=element_text(size=18),
        axis_text=element_text(size=10),
        axis_text_x=element_text(size=9),
        plot_title=element_text(size=22, ha="center", weight="bold"),
        legend_text=element_text(size=12),
        legend_title=element_text(size=14, weight="bold"),
        legend_position="right",
        legend_box_spacing=0.4,
        strip_text=element_text(size=16, weight="bold"),
        strip_background=element_rect(fill="#e8e8e8", color="#cccccc", size=0.5),
        panel_spacing_x=0.15,
        panel_spacing_y=0.15,
        panel_grid_major=element_line(color="#dddddd", size=0.4),
        panel_grid_minor=element_blank(),
        panel_background=element_rect(fill="#fafafa"),
    )
)

# Save plot
plot.save("plot.png", dpi=300, verbose=False)
