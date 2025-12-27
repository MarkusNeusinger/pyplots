""" pyplots.ai
scatter-size-mapped: Bubble Chart
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-27
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Data: Country economic indicators
np.random.seed(42)

regions = ["Americas", "Europe", "Asia", "Africa", "Oceania"]
region_colors = {
    "Americas": "#306998",
    "Europe": "#FFD43B",
    "Asia": "#E34A33",
    "Africa": "#31A354",
    "Oceania": "#756BB1",
}

# Generate 40 countries with realistic distributions per region
data = []
region_params = {
    "Americas": {"gdp_range": (8000, 65000), "life_range": (65, 80), "pop_range": (3e6, 350e6)},
    "Europe": {"gdp_range": (15000, 70000), "life_range": (75, 84), "pop_range": (1e6, 85e6)},
    "Asia": {"gdp_range": (2000, 60000), "life_range": (60, 85), "pop_range": (5e6, 1400e6)},
    "Africa": {"gdp_range": (1000, 15000), "life_range": (50, 75), "pop_range": (2e6, 220e6)},
    "Oceania": {"gdp_range": (10000, 55000), "life_range": (70, 83), "pop_range": (0.5e6, 26e6)},
}

n_per_region = [10, 10, 10, 7, 3]  # Total 40 countries

for region, n in zip(regions, n_per_region, strict=True):
    params = region_params[region]
    for _ in range(n):
        gdp = np.random.uniform(*params["gdp_range"])
        life = np.random.uniform(*params["life_range"])
        pop = np.exp(np.random.uniform(np.log(params["pop_range"][0]), np.log(params["pop_range"][1])))
        data.append({"GDP per Capita ($)": gdp, "Life Expectancy (years)": life, "Population": pop, "Region": region})

df = pd.DataFrame(data)

# Scale population for bubble size (log scale for better visibility)
df["size"] = np.log10(df["Population"]) * 40

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

sns.scatterplot(
    data=df,
    x="GDP per Capita ($)",
    y="Life Expectancy (years)",
    size="size",
    sizes=(50, 600),
    hue="Region",
    palette=region_colors,
    alpha=0.6,
    ax=ax,
    legend="brief",
)

# Styling
ax.set_title("scatter-size-mapped \u00b7 seaborn \u00b7 pyplots.ai", fontsize=24, fontweight="bold", pad=20)
ax.set_xlabel("GDP per Capita ($)", fontsize=20)
ax.set_ylabel("Life Expectancy (years)", fontsize=20)
ax.tick_params(axis="both", labelsize=16)
ax.grid(True, alpha=0.3, linestyle="--")

# Format x-axis with thousands separator
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"{x:,.0f}"))

# Adjust legend - keep only region labels
handles, labels = ax.get_legend_handles_labels()
# Find region handles (skip the first 'size' label group)
region_handles = []
region_labels = []
for handle, label in zip(handles, labels, strict=False):
    if label in regions:
        region_handles.append(handle)
        region_labels.append(label)

# Create custom size legend handles
size_legend_pops = [1e6, 10e6, 100e6, 1e9]
size_legend_labels = ["1M", "10M", "100M", "1B"]

size_handles = []
for pop in size_legend_pops:
    size_val = np.log10(pop) * 40
    # Map to the scatter size range
    mapped_size = 50 + (size_val - df["size"].min()) / (df["size"].max() - df["size"].min()) * (600 - 50)
    h = ax.scatter([], [], s=mapped_size * 0.5, c="gray", alpha=0.5, edgecolors="none")
    size_handles.append(h)

# Create two legends
legend1 = ax.legend(
    region_handles, region_labels, title="Region", title_fontsize=16, fontsize=14, loc="lower right", framealpha=0.9
)
ax.add_artist(legend1)

legend2 = ax.legend(
    size_handles,
    size_legend_labels,
    title="Population",
    title_fontsize=16,
    fontsize=14,
    loc="upper left",
    framealpha=0.9,
)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
