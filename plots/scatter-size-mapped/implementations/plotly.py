"""pyplots.ai
scatter-size-mapped: Bubble Chart
Library: plotly | Python 3.13
Quality: pending | Created: 2025-12-27
"""

import numpy as np
import plotly.graph_objects as go


# Data: Generate synthetic country economic indicators
np.random.seed(42)

# Create data for different regions with distinct characteristics
regions = {
    "Europe": {"gdp_range": (35000, 65000), "life_range": (78, 84), "pop_range": (5e6, 85e6), "n": 12},
    "Asia": {"gdp_range": (3000, 55000), "life_range": (65, 85), "pop_range": (10e6, 1400e6), "n": 10},
    "Americas": {"gdp_range": (8000, 70000), "life_range": (70, 82), "pop_range": (10e6, 350e6), "n": 10},
    "Africa": {"gdp_range": (1000, 15000), "life_range": (55, 75), "pop_range": (10e6, 210e6), "n": 8},
    "Oceania": {"gdp_range": (40000, 60000), "life_range": (80, 84), "pop_range": (5e6, 30e6), "n": 5},
}

gdp_data = []
life_data = []
pop_data = []
region_data = []

for region, params in regions.items():
    n = params["n"]
    gdp = np.random.uniform(*params["gdp_range"], n)
    life = np.random.uniform(*params["life_range"], n)
    pop = np.random.uniform(*params["pop_range"], n)

    gdp_data.extend(gdp)
    life_data.extend(life)
    pop_data.extend(pop)
    region_data.extend([region] * n)

gdp_data = np.array(gdp_data)
life_data = np.array(life_data)
pop_data = np.array(pop_data)

# Scale bubble sizes using log scale for better visibility (population spans many orders of magnitude)
size_scaled = np.log10(pop_data) * 8

# Color palette: colorblind-safe, starting with Python Blue
colors = {
    "Europe": "#306998",  # Python Blue
    "Asia": "#FFD43B",  # Python Yellow
    "Americas": "#2CA02C",  # Green
    "Africa": "#E377C2",  # Pink
    "Oceania": "#17BECF",  # Cyan
}

# Create figure
fig = go.Figure()

# Add traces for each region
for region in regions.keys():
    mask = np.array([r == region for r in region_data])
    fig.add_trace(
        go.Scatter(
            x=gdp_data[mask],
            y=life_data[mask],
            mode="markers",
            name=region,
            marker=dict(
                size=size_scaled[mask], color=colors[region], opacity=0.65, line=dict(width=1.5, color="white")
            ),
            hovertemplate="<b>%{text}</b><br>"
            + "GDP per Capita: $%{x:,.0f}<br>"
            + "Life Expectancy: %{y:.1f} years<br>"
            + "Population: %{customdata:,.0f}<extra></extra>",
            text=[region] * np.sum(mask),
            customdata=pop_data[mask],
        )
    )

# Update layout with proper sizing for 4800x2700 px output
fig.update_layout(
    title=dict(text="scatter-size-mapped · plotly · pyplots.ai", font=dict(size=32), x=0.5, xanchor="center"),
    xaxis=dict(
        title=dict(text="GDP per Capita (USD)", font=dict(size=24)),
        tickfont=dict(size=18),
        tickformat="$,.0f",
        showgrid=True,
        gridwidth=1,
        gridcolor="rgba(128, 128, 128, 0.2)",
    ),
    yaxis=dict(
        title=dict(text="Life Expectancy (Years)", font=dict(size=24)),
        tickfont=dict(size=18),
        showgrid=True,
        gridwidth=1,
        gridcolor="rgba(128, 128, 128, 0.2)",
    ),
    template="plotly_white",
    legend=dict(
        font=dict(size=18),
        title=dict(text="Region", font=dict(size=20)),
        itemsizing="constant",
        bordercolor="rgba(128, 128, 128, 0.3)",
        borderwidth=1,
    ),
    margin=dict(l=80, r=80, t=100, b=80),
)

# Add size legend annotation
fig.add_annotation(
    text="Bubble size = Population (log scale)",
    xref="paper",
    yref="paper",
    x=0.02,
    y=-0.08,
    showarrow=False,
    font=dict(size=16, color="gray"),
)

# Save as PNG (4800 x 2700 px using scale=3)
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Save as HTML for interactivity
fig.write_html("plot.html", include_plotlyjs="cdn")
