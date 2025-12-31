"""pyplots.ai
scatter-animated-controls: Animated Scatter Plot with Play Controls
Library: seaborn | Python 3.13
Quality: pending | Created: 2025-12-31
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.lines import Line2D


# Data - Simulated country metrics over time (Gapminder-style)
np.random.seed(42)

regions = ["North", "South", "East", "West", "Central", "Island"]
years = [2000, 2005, 2010, 2015, 2020]
n_regions = len(regions)

# Generate realistic GDP and life expectancy trajectories
data = []
for i, region in enumerate(regions):
    # Base values with variation between regions
    base_gdp = 5000 + i * 8000 + np.random.rand() * 5000
    base_life = 55 + i * 5 + np.random.rand() * 10
    base_pop = (20 + i * 30 + np.random.rand() * 50) * 1e6

    for j, year in enumerate(years):
        # Growth over time with some noise
        gdp = base_gdp * (1 + 0.03 * j) ** 2 + np.random.randn() * 500
        life = base_life + j * 1.5 + np.random.randn() * 0.5
        pop = base_pop * (1 + 0.015 * j)

        data.append(
            {
                "Region": region,
                "Year": year,
                "GDP per Capita ($)": gdp,
                "Life Expectancy (years)": life,
                "Population": pop,
            }
        )

df = pd.DataFrame(data)

# Size mapping for population (scaled for visibility)
df["Size"] = (df["Population"] / df["Population"].max()) * 1000 + 200

# Create faceted plot - static representation of animation frames
sns.set_style("whitegrid")

g = sns.FacetGrid(df, col="Year", col_wrap=3, height=4.5, aspect=1.6, sharex=True, sharey=True)

# Custom color palette using Python colors first
colors = ["#306998", "#FFD43B", "#4ECDC4", "#FF6B6B", "#9B59B6", "#2ECC71"]

# Plot scatter for each year
g.map_dataframe(
    sns.scatterplot,
    x="GDP per Capita ($)",
    y="Life Expectancy (years)",
    hue="Region",
    size="Size",
    sizes=(200, 1200),
    alpha=0.85,
    palette=colors,
    legend=False,
    edgecolor="white",
    linewidth=1.5,
)

# Add region labels to each subplot
for ax, year in zip(g.axes.flat, years, strict=False):
    year_data = df[df["Year"] == year]
    for _, row in year_data.iterrows():
        ax.annotate(
            row["Region"][0],  # First letter of region
            (row["GDP per Capita ($)"], row["Life Expectancy (years)"]),
            fontsize=14,
            ha="center",
            va="center",
            fontweight="bold",
            color="white",
        )

# Style titles and labels
g.set_titles("Year: {col_name}", fontsize=22, fontweight="bold")
g.set_axis_labels("GDP per Capita ($)", "Life Expectancy (years)", fontsize=18)

for ax in g.axes.flat:
    ax.tick_params(axis="both", labelsize=14)
    ax.grid(True, alpha=0.3, linestyle="--")

# Add overall title
g.figure.suptitle("scatter-animated-controls · seaborn · pyplots.ai", fontsize=26, fontweight="bold", y=1.02)

# Create custom legend handles
legend_handles = [
    Line2D(
        [0],
        [0],
        marker="o",
        color="w",
        markerfacecolor=colors[i],
        markersize=14,
        label=regions[i],
        markeredgecolor="white",
        markeredgewidth=1.5,
    )
    for i in range(n_regions)
]

g.figure.legend(
    handles=legend_handles,
    loc="center right",
    fontsize=14,
    title="Region",
    title_fontsize=16,
    bbox_to_anchor=(0.99, 0.5),
    frameon=True,
    fancybox=True,
    shadow=True,
)

# Add subtitle explaining the static representation
g.figure.text(
    0.5,
    -0.01,
    "Static faceted view showing key time points (simulating animation frames)",
    ha="center",
    fontsize=14,
    style="italic",
    color="gray",
)

plt.tight_layout()
g.figure.set_size_inches(16, 9)
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
