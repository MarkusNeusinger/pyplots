""" pyplots.ai
scatter-size-mapped: Bubble Chart
Library: matplotlib 3.10.8 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-27
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D


# Data - Country economic indicators
np.random.seed(42)

# Generate 40 countries across different regions
n_countries = 40

# Regions with different economic profiles
regions = ["Americas", "Europe", "Asia", "Africa", "Oceania"]
region_colors = {
    "Americas": "#306998",  # Python Blue
    "Europe": "#FFD43B",  # Python Yellow
    "Asia": "#E74C3C",  # Red (colorblind-safe distinct)
    "Africa": "#2ECC71",  # Green
    "Oceania": "#9B59B6",  # Purple
}

# Assign regions (weighted distribution)
region_weights = [8, 10, 12, 8, 2]  # 40 total
region_list = []
for region, count in zip(regions, region_weights, strict=True):
    region_list.extend([region] * count)
np.random.shuffle(region_list)

# Generate economic data based on region profiles
gdp_per_capita = []
life_expectancy = []
population = []

for region in region_list:
    if region == "Europe":
        gdp = np.random.uniform(30000, 75000)
        life = np.random.uniform(77, 84)
        pop = np.random.uniform(5e6, 85e6)
    elif region == "Americas":
        gdp = np.random.uniform(8000, 65000)
        life = np.random.uniform(70, 82)
        pop = np.random.uniform(10e6, 330e6)
    elif region == "Asia":
        gdp = np.random.uniform(2000, 55000)
        life = np.random.uniform(65, 85)
        pop = np.random.uniform(20e6, 1400e6)
    elif region == "Africa":
        gdp = np.random.uniform(1000, 15000)
        life = np.random.uniform(52, 72)
        pop = np.random.uniform(10e6, 200e6)
    else:  # Oceania
        gdp = np.random.uniform(25000, 60000)
        life = np.random.uniform(78, 84)
        pop = np.random.uniform(5e6, 30e6)

    gdp_per_capita.append(gdp)
    life_expectancy.append(life)
    population.append(pop)

gdp_per_capita = np.array(gdp_per_capita)
life_expectancy = np.array(life_expectancy)
population = np.array(population)

# Scale bubble sizes using log scale for visibility (population spans many orders of magnitude)
# Map to range suitable for visualization: 50-800 for 40 points
pop_log = np.log10(population)
size_min, size_max = 80, 800
sizes = (pop_log - pop_log.min()) / (pop_log.max() - pop_log.min()) * (size_max - size_min) + size_min

# Colors based on region
colors = [region_colors[r] for r in region_list]

# Create plot
fig, ax = plt.subplots(figsize=(16, 9))

# Plot each region separately for legend
for region in regions:
    mask = np.array([r == region for r in region_list])
    if mask.any():
        ax.scatter(
            gdp_per_capita[mask],
            life_expectancy[mask],
            s=sizes[mask],
            c=region_colors[region],
            alpha=0.6,
            edgecolors="white",
            linewidth=1.5,
            label=region,
        )

# Labels and styling
ax.set_xlabel("GDP per Capita (USD)", fontsize=20)
ax.set_ylabel("Life Expectancy (years)", fontsize=20)
ax.set_title("scatter-size-mapped · matplotlib · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)
ax.grid(True, alpha=0.3, linestyle="--")

# Format x-axis with thousands separator
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x / 1000:.0f}k"))

# Legend for regions
region_legend = ax.legend(title="Region", fontsize=14, title_fontsize=16, loc="upper left", framealpha=0.9)
ax.add_artist(region_legend)

# Size legend showing population scale
size_legend_pops = [10e6, 100e6, 500e6, 1000e6]
size_legend_labels = ["10M", "100M", "500M", "1B"]
size_legend_sizes = []
for pop in size_legend_pops:
    log_pop = np.log10(pop)
    s = (log_pop - pop_log.min()) / (pop_log.max() - pop_log.min()) * (size_max - size_min) + size_min
    size_legend_sizes.append(s)

# Create size legend handles
size_handles = [
    Line2D(
        [0],
        [0],
        marker="o",
        color="w",
        markerfacecolor="gray",
        markersize=np.sqrt(s) / 2,
        alpha=0.6,
        label=label,
        linestyle="None",
    )
    for s, label in zip(size_legend_sizes, size_legend_labels, strict=True)
]

size_legend = ax.legend(
    handles=size_handles, title="Population", fontsize=14, title_fontsize=16, loc="lower right", framealpha=0.9
)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
