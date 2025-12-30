"""pyplots.ai
facet-grid: Faceted Grid Plot
Library: plotly | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import numpy as np
import pandas as pd
import plotly.express as px


# Data: Plant growth experiment across different conditions
np.random.seed(42)

# Create realistic multi-factorial experiment data
conditions = []
for light in ["Low Light", "Medium Light", "High Light"]:
    for soil in ["Sandy", "Loamy"]:
        n_plants = 25
        # Base growth varies by light and soil
        light_effect = {"Low Light": 5, "Medium Light": 12, "High Light": 18}[light]
        soil_effect = {"Sandy": -2, "Loamy": 2}[soil]

        base_growth = light_effect + soil_effect
        water = np.linspace(10, 50, n_plants) + np.random.normal(0, 3, n_plants)
        growth = base_growth + water * 0.4 + np.random.normal(0, 3, n_plants)

        for w, g in zip(water, growth):
            conditions.append(
                {"Water (mL/day)": w, "Growth (cm)": max(0, g), "Light Condition": light, "Soil Type": soil}
            )

df = pd.DataFrame(conditions)

# Create faceted scatter plot
fig = px.scatter(
    df,
    x="Water (mL/day)",
    y="Growth (cm)",
    facet_row="Soil Type",
    facet_col="Light Condition",
    color="Soil Type",
    color_discrete_sequence=["#306998", "#FFD43B"],
    opacity=0.7,
)

# Update layout for 4800x2700 canvas
fig.update_layout(
    title=dict(text="facet-grid · plotly · pyplots.ai", font=dict(size=32), x=0.5, xanchor="center"),
    template="plotly_white",
    font=dict(size=18),
    legend=dict(font=dict(size=20), title=dict(font=dict(size=22))),
    margin=dict(l=100, r=100, t=150, b=100),
)

# Update axes for readability
fig.update_xaxes(title_font=dict(size=22), tickfont=dict(size=18), gridcolor="rgba(0,0,0,0.1)", gridwidth=1)

fig.update_yaxes(title_font=dict(size=22), tickfont=dict(size=18), gridcolor="rgba(0,0,0,0.1)", gridwidth=1)

# Update facet annotation font sizes
fig.for_each_annotation(lambda a: a.update(font=dict(size=22)))

# Update marker size for visibility
fig.update_traces(marker=dict(size=14, line=dict(width=1, color="white")))

# Save as PNG and HTML
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html")
