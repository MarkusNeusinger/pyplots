"""pyplots.ai
scatter-size-mapped: Bubble Chart
Library: altair | Python 3.13
Quality: pending | Created: 2025-12-27
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - Country economic indicators
np.random.seed(42)

regions = ["Americas", "Europe", "Asia", "Africa", "Oceania"]
region_colors = {
    "Americas": "#306998",
    "Europe": "#FFD43B",
    "Asia": "#E57373",
    "Africa": "#81C784",
    "Oceania": "#BA68C8",
}

# Generate realistic country data
n_countries = 40
data = {
    "Country": [f"Country_{i + 1}" for i in range(n_countries)],
    "Region": np.random.choice(regions, n_countries, p=[0.2, 0.25, 0.3, 0.15, 0.1]),
}

# GDP per capita varies by region (realistic ranges)
gdp_base = {"Americas": 35000, "Europe": 45000, "Asia": 25000, "Africa": 8000, "Oceania": 40000}
data["GDP per Capita (USD)"] = [np.clip(gdp_base[r] + np.random.randn() * 20000, 1000, 80000) for r in data["Region"]]

# Life expectancy correlates with GDP
data["Life Expectancy (Years)"] = [
    np.clip(55 + (gdp / 80000) * 30 + np.random.randn() * 3, 50, 85) for gdp in data["GDP per Capita (USD)"]
]

# Population (log-distributed)
data["Population"] = np.random.lognormal(mean=17, sigma=1.5, size=n_countries).astype(int)
data["Population"] = np.clip(data["Population"], 500000, 1400000000)

df = pd.DataFrame(data)

# Create bubble chart
chart = (
    alt.Chart(df)
    .mark_circle(opacity=0.6, stroke="white", strokeWidth=1)
    .encode(
        x=alt.X("GDP per Capita (USD):Q", title="GDP per Capita (USD)", scale=alt.Scale(domain=[0, 85000])),
        y=alt.Y("Life Expectancy (Years):Q", title="Life Expectancy (Years)", scale=alt.Scale(domain=[48, 88])),
        size=alt.Size(
            "Population:Q",
            title="Population",
            scale=alt.Scale(range=[100, 3000], type="sqrt"),
            legend=alt.Legend(
                title="Population", titleFontSize=18, labelFontSize=16, symbolSize=400, orient="right", format=".2s"
            ),
        ),
        color=alt.Color(
            "Region:N",
            scale=alt.Scale(domain=list(region_colors.keys()), range=list(region_colors.values())),
            legend=alt.Legend(title="Region", titleFontSize=18, labelFontSize=16, symbolSize=400, orient="right"),
        ),
        tooltip=["Country:N", "Region:N", "GDP per Capita (USD):Q", "Life Expectancy (Years):Q", "Population:Q"],
    )
    .properties(
        width=1600,
        height=900,
        title=alt.Title(text="scatter-size-mapped · altair · pyplots.ai", fontSize=28, anchor="middle"),
    )
    .configure_axis(labelFontSize=18, titleFontSize=22, gridOpacity=0.3, gridDash=[3, 3])
    .configure_view(strokeWidth=0)
    .configure_legend(titleFontSize=18, labelFontSize=16)
)

# Save as PNG (4800 x 2700 with scale_factor=3)
chart.save("plot.png", scale_factor=3.0)

# Save as HTML for interactivity
chart.save("plot.html")
