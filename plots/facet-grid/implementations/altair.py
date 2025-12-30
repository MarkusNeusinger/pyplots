"""pyplots.ai
facet-grid: Faceted Grid Plot
Library: altair | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - Plant growth measurements across light and water conditions
np.random.seed(42)

conditions = []
for light in ["Low Light", "Medium Light", "High Light"]:
    for water in ["Dry", "Moderate", "Wet"]:
        n = 30
        base_growth = {"Low Light": 4, "Medium Light": 10, "High Light": 16}[light]
        water_factor = {"Dry": 0.6, "Moderate": 1.0, "Wet": 0.8}[water]

        days = np.arange(1, n + 1)
        growth = base_growth * water_factor * (1 - np.exp(-days / 12)) + np.random.randn(n) * 1.2
        growth = np.maximum(growth, 0)

        for d, g in zip(days, growth, strict=True):
            conditions.append({"Day": d, "Growth (cm)": g, "Light": light, "Water": water})

df = pd.DataFrame(conditions)

# Create faceted scatter chart with row and column faceting
chart = (
    alt.Chart(df)
    .mark_point(size=150, filled=True, opacity=0.8)
    .encode(
        x=alt.X("Day:Q", title="Days Since Planting", scale=alt.Scale(domain=[0, 32])),
        y=alt.Y("Growth (cm):Q", title="Plant Height (cm)", scale=alt.Scale(domain=[0, 18])),
        color=alt.Color(
            "Light:N",
            scale=alt.Scale(
                domain=["Low Light", "Medium Light", "High Light"], range=["#306998", "#FFD43B", "#4CAF50"]
            ),
            legend=alt.Legend(titleFontSize=18, labelFontSize=16, symbolSize=200),
        ),
        tooltip=["Day:Q", "Growth (cm):Q", "Light:N", "Water:N"],
    )
    .facet(
        row=alt.Row("Light:N", title=None, header=alt.Header(labelFontSize=20, labelFontWeight="bold", labelAngle=0)),
        column=alt.Column("Water:N", title=None, header=alt.Header(labelFontSize=20, labelFontWeight="bold")),
    )
    .properties(title=alt.Title("facet-grid · altair · pyplots.ai", fontSize=32, anchor="middle", dy=-10))
    .configure_axis(labelFontSize=16, titleFontSize=18, gridOpacity=0.3)
    .configure_view(strokeWidth=1, stroke="#888888")
    .resolve_scale(y="shared", x="shared")
)

# Save outputs
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
