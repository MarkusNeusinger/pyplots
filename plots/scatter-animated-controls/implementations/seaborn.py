""" pyplots.ai
scatter-animated-controls: Animated Scatter Plot with Play Controls
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-31
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

# Generate diverse GDP and life expectancy trajectories to show different patterns
data = []
for i, region in enumerate(regions):
    # Base values with significant variation between regions
    base_gdp = 5000 + i * 10000 + np.random.rand() * 8000
    base_life = 50 + i * 6 + np.random.rand() * 12
    base_pop = (20 + i * 40 + np.random.rand() * 60) * 1e6

    for j, year in enumerate(years):
        # Diverse growth patterns for different regions
        if region == "North":
            # Steady high growth
            gdp = base_gdp * (1.08**j) + np.random.randn() * 1000
            life = base_life + j * 2.0 + np.random.randn() * 0.3
        elif region == "South":
            # Rapid catch-up growth
            gdp = base_gdp * (1.15**j) + np.random.randn() * 800
            life = base_life + j * 2.5 + np.random.randn() * 0.4
        elif region == "East":
            # Volatile - boom then stagnation
            growth = 1.12 if j < 3 else 1.02
            gdp = base_gdp * (growth**j) + np.random.randn() * 1500
            life = base_life + j * 1.8 + np.random.randn() * 0.5
        elif region == "West":
            # Mature economy - slow steady growth
            gdp = base_gdp * (1.03**j) + np.random.randn() * 600
            life = base_life + j * 0.8 + np.random.randn() * 0.2
        elif region == "Central":
            # Economic decline then recovery
            if j < 2:
                gdp = base_gdp * (0.95**j) + np.random.randn() * 1200
            else:
                gdp = base_gdp * 0.9 * (1.10 ** (j - 2)) + np.random.randn() * 1000
            life = base_life + j * 1.2 + np.random.randn() * 0.6
        else:  # Island
            # Tourism boom - exponential growth
            gdp = base_gdp * (1.20**j) + np.random.randn() * 2000
            life = base_life + j * 1.5 + np.random.randn() * 0.4

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
sns.set_context("talk", font_scale=1.3)

# Use 2 rows x 3 cols layout to leave space for legend below
g = sns.FacetGrid(df, col="Year", col_wrap=5, height=4.0, aspect=1.2, sharex=True, sharey=True)

# Custom color palette with good contrast
colors = ["#306998", "#E69F00", "#56B4E9", "#D55E00", "#9B59B6", "#009E73"]

# Plot scatter for each year
g.map_dataframe(
    sns.scatterplot,
    x="GDP per Capita ($)",
    y="Life Expectancy (years)",
    hue="Region",
    size="Size",
    sizes=(300, 1400),
    alpha=0.85,
    palette=colors,
    legend=False,
    edgecolor="white",
    linewidth=2,
)

# Add prominent year labels in background and region labels
for ax, year in zip(g.axes.flat, years, strict=False):
    # Large year text in background (spec requirement)
    ax.text(
        0.5,
        0.5,
        str(year),
        transform=ax.transAxes,
        fontsize=72,
        fontweight="bold",
        color="#E0E0E0",
        ha="center",
        va="center",
        zorder=0,
    )
    # Region labels on bubbles
    year_data = df[df["Year"] == year]
    for _, row in year_data.iterrows():
        ax.annotate(
            row["Region"][0],  # First letter of region
            (row["GDP per Capita ($)"], row["Life Expectancy (years)"]),
            fontsize=16,
            ha="center",
            va="center",
            fontweight="bold",
            color="white",
            zorder=10,
        )

# Style titles and labels with increased font sizes
g.set_titles("{col_name}", fontsize=28, fontweight="bold")
g.set_axis_labels("GDP per Capita ($)", "Life Expectancy (years)", fontsize=22)

for ax in g.axes.flat:
    ax.tick_params(axis="both", labelsize=16)
    ax.grid(True, alpha=0.25, linestyle="--", zorder=1)

# Add overall title
g.figure.suptitle("scatter-animated-controls · seaborn · pyplots.ai", fontsize=30, fontweight="bold", y=1.02)

# Create custom legend handles with larger markers
legend_handles = [
    Line2D(
        [0],
        [0],
        marker="o",
        color="w",
        markerfacecolor=colors[i],
        markersize=18,
        label=regions[i],
        markeredgecolor="white",
        markeredgewidth=2,
    )
    for i in range(n_regions)
]

# Place legend at bottom center to avoid overlap with panels
g.figure.legend(
    handles=legend_handles,
    loc="lower center",
    fontsize=16,
    title="Region",
    title_fontsize=18,
    ncol=6,
    bbox_to_anchor=(0.5, -0.02),
    frameon=True,
    fancybox=True,
    shadow=True,
)

# Add subtitle explaining the static representation
g.figure.text(
    0.5,
    -0.08,
    "Static faceted view showing key time points (simulating animation frames)",
    ha="center",
    fontsize=16,
    style="italic",
    color="gray",
)

plt.tight_layout()
g.figure.set_size_inches(16, 9)
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
