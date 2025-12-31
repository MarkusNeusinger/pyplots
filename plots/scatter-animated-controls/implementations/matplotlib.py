""" pyplots.ai
scatter-animated-controls: Animated Scatter Plot with Play Controls
Library: matplotlib 3.10.8 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-31
"""

import matplotlib.pyplot as plt
import numpy as np


# Data - Simulated country data inspired by Gapminder
np.random.seed(42)

# 8 countries tracked over 20 years
n_countries = 8
n_years = 20
years = np.arange(2000, 2000 + n_years)

countries = ["Country A", "Country B", "Country C", "Country D", "Country E", "Country F", "Country G", "Country H"]

# Base values for each country (GDP per capita in thousands, life expectancy)
base_gdp = np.array([5, 15, 25, 8, 35, 12, 45, 20])
base_life = np.array([55, 65, 72, 58, 78, 62, 80, 68])
base_pop = np.array([50, 120, 80, 200, 30, 150, 25, 90])  # Population in millions

# Growth rates (GDP grows, life expectancy improves)
gdp_growth = np.array([0.06, 0.04, 0.03, 0.055, 0.02, 0.045, 0.015, 0.035])
life_growth = np.array([0.4, 0.25, 0.15, 0.35, 0.1, 0.3, 0.08, 0.2])
pop_growth = np.array([0.02, 0.01, 0.005, 0.025, 0.003, 0.015, 0.002, 0.008])

# Generate data for all years
gdp_data = np.zeros((n_countries, n_years))
life_data = np.zeros((n_countries, n_years))
pop_data = np.zeros((n_countries, n_years))

for i in range(n_countries):
    for t in range(n_years):
        noise_gdp = np.random.randn() * 0.5
        noise_life = np.random.randn() * 0.3
        gdp_data[i, t] = base_gdp[i] * (1 + gdp_growth[i]) ** t + noise_gdp
        life_data[i, t] = min(85, base_life[i] + life_growth[i] * t + noise_life)
        pop_data[i, t] = base_pop[i] * (1 + pop_growth[i]) ** t

# Colors for countries (colorblind-safe palette - avoiding similar yellows)
colors = ["#306998", "#E69F00", "#CC79A7", "#56B4E9", "#009E73", "#D55E00", "#0072B2", "#882255"]

# Select 4 key time points to show evolution
key_years_idx = [0, 6, 13, 19]  # 2000, 2006, 2013, 2019
key_years = years[key_years_idx]

# Create faceted plot - 2x2 grid showing key time points
fig, axes = plt.subplots(2, 2, figsize=(16, 9))
axes = axes.flatten()

for idx, (ax, year_idx) in enumerate(zip(axes, key_years_idx, strict=True)):
    year = years[year_idx]

    # Plot each country
    for i in range(n_countries):
        # Size based on population (scaled for visibility)
        size = pop_data[i, year_idx] * 3

        ax.scatter(
            gdp_data[i, year_idx],
            life_data[i, year_idx],
            s=size,
            c=colors[i],
            alpha=0.7,
            edgecolors="white",
            linewidth=1.5,
            label=countries[i] if idx == 0 else None,
        )

        # Add country labels for larger bubbles
        if pop_data[i, year_idx] > 80:
            ax.annotate(
                countries[i].split()[-1],
                (gdp_data[i, year_idx], life_data[i, year_idx]),
                fontsize=10,
                ha="center",
                va="center",
                fontweight="bold",
                color="white",
            )

    # Year displayed prominently as watermark
    ax.text(
        0.5,
        0.5,
        str(year),
        transform=ax.transAxes,
        fontsize=72,
        color="gray",
        alpha=0.15,
        ha="center",
        va="center",
        fontweight="bold",
    )

    # Panel title
    ax.set_title(f"Year {year}", fontsize=20, fontweight="bold")

    # Axis labels
    ax.set_xlabel("GDP per Capita (thousands $)", fontsize=20)
    ax.set_ylabel("Life Expectancy (years)", fontsize=20)
    ax.tick_params(axis="both", labelsize=16)

    # Consistent axis limits across all panels
    ax.set_xlim(0, 80)
    ax.set_ylim(50, 88)

    # Grid
    ax.grid(True, alpha=0.3, linestyle="--")

# Main title with play control annotation
fig.suptitle("scatter-animated-controls · matplotlib · pyplots.ai", fontsize=24, fontweight="bold", y=0.98)

# Add subtitle explaining the visualization
fig.text(
    0.5,
    0.93,
    "GDP vs Life Expectancy Over Time (bubble size = population)",
    ha="center",
    fontsize=16,
    style="italic",
    color="gray",
)

# Add legend - positioned in bottom right of figure
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(
    handles,
    labels,
    loc="lower center",
    ncol=4,
    fontsize=12,
    frameon=True,
    fancybox=True,
    shadow=True,
    bbox_to_anchor=(0.5, -0.02),
)

# Add prominent animation control panel
control_box = fig.add_axes([0.3, 0.01, 0.4, 0.035])
control_box.set_xlim(0, 10)
control_box.set_ylim(0, 1)
control_box.axis("off")

# Play button
control_box.add_patch(plt.Rectangle((0.2, 0.15), 0.8, 0.7, facecolor="#306998", edgecolor="#1a3d5c", linewidth=2))
control_box.text(0.6, 0.5, "▶", ha="center", va="center", fontsize=16, color="white", fontweight="bold")

# Pause button
control_box.add_patch(plt.Rectangle((1.2, 0.15), 0.8, 0.7, facecolor="#666666", edgecolor="#444444", linewidth=2))
control_box.text(1.6, 0.5, "||", ha="center", va="center", fontsize=14, color="white", fontweight="bold")

# Timeline slider
control_box.add_patch(plt.Rectangle((2.5, 0.35), 7, 0.3, facecolor="#E0E0E0", edgecolor="#999999", linewidth=1))
# Progress indicator
control_box.add_patch(plt.Rectangle((2.5, 0.35), 5.25, 0.3, facecolor="#306998", edgecolor="none"))
# Slider handle
control_box.add_patch(plt.Circle((7.75, 0.5), 0.25, facecolor="white", edgecolor="#306998", linewidth=2))

# Year labels on timeline
control_box.text(2.5, 0.1, "2000", ha="center", va="top", fontsize=10, color="#666666")
control_box.text(9.5, 0.1, "2019", ha="center", va="top", fontsize=10, color="#666666")
control_box.text(7.75, 0.9, "2015", ha="center", va="bottom", fontsize=11, color="#306998", fontweight="bold")

plt.tight_layout(rect=[0, 0.05, 1, 0.92])
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
