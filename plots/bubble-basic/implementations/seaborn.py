"""pyplots.ai
bubble-basic: Basic Bubble Chart
Library: seaborn 0.13.2 | Python 3.14
Quality: /100 | Updated: 2026-02-15
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Data — World cities: GDP per capita vs life expectancy, bubble = population
np.random.seed(42)
n_cities = 40

gdp_per_capita = np.linspace(5, 85, n_cities) + np.random.normal(0, 5, n_cities)
gdp_per_capita = np.clip(gdp_per_capita, 5, 90)

life_expectancy = 60 + 0.22 * gdp_per_capita + np.random.normal(0, 2.5, n_cities)
life_expectancy = np.clip(life_expectancy, 58, 84)

population_millions = np.random.lognormal(mean=1.0, sigma=1.0, size=n_cities)
population_millions = np.clip(population_millions, 0.8, 30)

df = pd.DataFrame(
    {
        "gdp_per_capita": np.round(gdp_per_capita, 1),
        "life_expectancy": np.round(life_expectancy, 1),
        "population": np.round(population_millions, 1),
    }
)

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

sns.scatterplot(
    data=df,
    x="gdp_per_capita",
    y="life_expectancy",
    size="population",
    sizes=(120, 2000),
    alpha=0.55,
    color="#306998",
    edgecolor="white",
    linewidth=0.8,
    legend="brief",
    ax=ax,
)

# Adjust legend
legend = ax.get_legend()
legend.set_title("Population (M)")
legend.get_title().set_fontsize(16)
for text in legend.get_texts():
    text.set_fontsize(14)
legend.set_loc("upper left")
legend.set_frame_on(True)
legend.get_frame().set_alpha(0.9)
legend.get_frame().set_edgecolor("#cccccc")

# Style
ax.set_xlabel("GDP per Capita ($ thousands)", fontsize=20)
ax.set_ylabel("Life Expectancy (years)", fontsize=20)
ax.set_title("bubble-basic · seaborn · pyplots.ai", fontsize=24, fontweight="medium")
ax.tick_params(axis="both", labelsize=16)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.yaxis.grid(True, alpha=0.2, linewidth=0.8)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
