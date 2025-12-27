"""pyplots.ai
scatter-size-mapped: Bubble Chart
Library: lets-plot | Python 3.13
Quality: pending | Created: 2025-12-27
"""

import numpy as np
import pandas as pd
from lets_plot import *  # noqa: F403
from lets_plot.export import ggsave as export_ggsave


LetsPlot.setup_html()  # noqa: F405

# Data - Country economic indicators
np.random.seed(42)
n_countries = 40

regions = ["Europe", "Asia", "Americas", "Africa", "Oceania"]
region_weights = [10, 12, 8, 7, 3]

# Generate realistic data with regional patterns
data = []
for _ in range(n_countries):
    region_idx = np.random.choice(len(regions), p=np.array(region_weights) / sum(region_weights))
    region = regions[region_idx]

    # GDP per capita varies by region
    gdp_base = {"Europe": 45000, "Asia": 25000, "Americas": 30000, "Africa": 8000, "Oceania": 50000}
    gdp = gdp_base[region] + np.random.normal(0, gdp_base[region] * 0.4)
    gdp = np.clip(gdp, 1000, 80000)

    # Life expectancy correlates with GDP
    life_exp_base = 55 + (gdp / 80000) * 30
    life_exp = life_exp_base + np.random.normal(0, 3)
    life_exp = np.clip(life_exp, 50, 85)

    # Population (log-normal distribution)
    pop = np.exp(np.random.normal(17, 1.5))  # Log-normal for wide range
    pop = np.clip(pop, 500000, 1400000000)

    data.append({"region": region, "gdp_per_capita": gdp, "life_expectancy": life_exp, "population": pop})

df = pd.DataFrame(data)

# Calculate bubble sizes (scaled for visibility)
df["pop_millions"] = df["population"] / 1e6

# Color palette for regions (colorblind-safe)
region_colors = ["#306998", "#FFD43B", "#2ECC71", "#E74C3C", "#9B59B6"]

# Create bubble chart
plot = (
    ggplot(df, aes(x="gdp_per_capita", y="life_expectancy", size="pop_millions", color="region"))  # noqa: F405
    + geom_point(alpha=0.65)  # noqa: F405
    + scale_size(range=[3, 22], name="Population (M)")  # noqa: F405
    + scale_color_manual(values=region_colors, name="Region")  # noqa: F405
    + scale_x_continuous(format="${.0f}")  # noqa: F405
    + labs(  # noqa: F405
        x="GDP per Capita (USD)", y="Life Expectancy (years)", title="scatter-size-mapped · letsplot · pyplots.ai"
    )
    + theme_minimal()  # noqa: F405
    + theme(  # noqa: F405
        plot_title=element_text(size=24),  # noqa: F405
        axis_title=element_text(size=20),  # noqa: F405
        axis_text=element_text(size=16),  # noqa: F405
        legend_title=element_text(size=18),  # noqa: F405
        legend_text=element_text(size=14),  # noqa: F405
        panel_grid=element_line(color="#E0E0E0", size=0.5, linetype="dashed"),  # noqa: F405
    )
    + ggsize(1600, 900)  # noqa: F405
)

# Save PNG (scale 3x to get 4800 × 2700 px)
export_ggsave(plot, filename="plot.png", path=".", scale=3)

# Save HTML for interactive version
export_ggsave(plot, filename="plot.html", path=".")
