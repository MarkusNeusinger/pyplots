""" pyplots.ai
bar-race-animated: Animated Bar Chart Race
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 91/100 | Created: 2026-01-11
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Data: Simulated company market values over 8 years
np.random.seed(42)

companies = [
    "TechCorp",
    "GlobalSoft",
    "DataSystems",
    "CloudNet",
    "InnovateTech",
    "SmartSolutions",
    "FutureLogic",
    "ByteWorks",
    "QuantumLabs",
    "CyberFlow",
]
years = list(range(2016, 2024))
n_companies = len(companies)

# Generate realistic market values with trends and volatility
base_values = np.array([120, 95, 85, 110, 60, 75, 45, 55, 35, 40])
growth_rates = np.array([0.15, 0.08, 0.05, 0.20, 0.25, 0.12, 0.18, 0.10, 0.30, 0.22])

data_rows = []
for i, company in enumerate(companies):
    for j, year in enumerate(years):
        noise = np.random.normal(0, 8)
        value = base_values[i] * (1 + growth_rates[i]) ** j + noise
        value = max(10, value)
        data_rows.append({"Company": company, "Year": year, "Value": value})

df = pd.DataFrame(data_rows)

# Select 6 key snapshots for small multiples
snapshot_years = [2016, 2018, 2020, 2022, 2023, 2023]  # Duplicate last for grid

# Create small multiples grid
fig, axes = plt.subplots(2, 3, figsize=(16, 9))
axes = axes.flatten()

# Color palette for consistent entity tracking
palette = sns.color_palette("tab10", n_companies)
company_colors = dict(zip(companies, palette, strict=False))

# Global x-axis limit for all panels (for better comparison)
x_max = df["Value"].max() * 1.18

for idx, year in enumerate(snapshot_years[:5]):
    ax = axes[idx]

    # Filter and sort data for this year
    year_data = df[df["Year"] == year].copy()
    year_data = year_data.sort_values("Value", ascending=True)

    # Create horizontal bar chart
    sns.barplot(
        data=year_data,
        y="Company",
        x="Value",
        hue="Company",
        palette=company_colors,
        ax=ax,
        legend=False,
        edgecolor="white",
        linewidth=1.5,
    )

    # Add value labels at end of bars
    for i, (_, row) in enumerate(year_data.iterrows()):
        ax.text(row["Value"] + 5, i, f"${row['Value']:.0f}B", va="center", fontsize=11, fontweight="bold")

    # Styling
    ax.set_title(f"{year}", fontsize=22, fontweight="bold", pad=12)
    ax.set_xlabel("Market Value (Billion $)", fontsize=15)
    ax.set_ylabel("")
    ax.tick_params(axis="y", labelsize=13)
    ax.tick_params(axis="x", labelsize=12)
    ax.set_xlim(0, x_max)
    ax.grid(axis="x", alpha=0.3, linestyle="--")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

# Use 6th panel for legend
ax_legend = axes[5]
ax_legend.axis("off")

# Create legend handles
handles = [plt.Rectangle((0, 0), 1, 1, facecolor=company_colors[c], edgecolor="white") for c in companies]
ax_legend.legend(
    handles, companies, loc="center", fontsize=14, title="Companies", title_fontsize=16, frameon=False, ncol=2
)

# Add overall title
fig.suptitle(
    "Tech Company Market Values · bar-race-animated · seaborn · pyplots.ai", fontsize=24, fontweight="bold", y=0.98
)

plt.tight_layout(rect=[0, 0, 1, 0.94])
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
