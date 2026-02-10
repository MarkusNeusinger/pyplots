""" pyplots.ai
scatter-basic: Basic Scatter Plot
Library: altair 6.0.0 | Python 3.14.2
Quality: /100 | Updated: 2026-02-10
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - Daily temperature vs ice cream sales for a beach town
np.random.seed(42)
n = 120
temperature = np.random.normal(24, 7, n).clip(5, 42)
sales = temperature * 12 + np.random.normal(0, 35, n) + 50
sales = sales.clip(20, None)

df = pd.DataFrame(
    {"Temperature (Celsius)": np.round(temperature, 1), "Ice Cream Sales (USD)": np.round(sales, 0).astype(int)}
)

# Plot
chart = (
    alt.Chart(df)
    .mark_circle(size=220, opacity=0.72, stroke="#1a3a5c", strokeWidth=0.8)
    .encode(
        x=alt.X(
            "Temperature (Celsius):Q",
            scale=alt.Scale(domain=[0, 45], nice=True),
            axis=alt.Axis(labelFontSize=18, titleFontSize=22, tickCount=10, gridOpacity=0.25, gridDash=[4, 4]),
        ),
        y=alt.Y(
            "Ice Cream Sales (USD):Q",
            scale=alt.Scale(domain=[0, 600], nice=True),
            axis=alt.Axis(labelFontSize=18, titleFontSize=22, gridOpacity=0.25, gridDash=[4, 4]),
        ),
        color=alt.Color(
            "Temperature (Celsius):Q",
            scale=alt.Scale(scheme="turbo", domain=[5, 42]),
            legend=alt.Legend(
                title="Temp (C)",
                titleFontSize=16,
                labelFontSize=14,
                gradientLength=260,
                gradientThickness=18,
                orient="right",
            ),
        ),
        tooltip=[
            alt.Tooltip("Temperature (Celsius):Q", format=".1f"),
            alt.Tooltip("Ice Cream Sales (USD):Q", format=",.0f"),
        ],
    )
    .properties(
        width=1600,
        height=900,
        title=alt.Title(
            "scatter-basic \u00b7 altair \u00b7 pyplots.ai",
            fontSize=28,
            fontWeight="bold",
            anchor="start",
            offset=16,
            subtitle="Daily temperature vs ice cream sales in a coastal town",
            subtitleFontSize=18,
            subtitleColor="#555555",
        ),
    )
    .configure_view(strokeWidth=0)
    .configure_axis(domainColor="#888888", tickColor="#888888", labelColor="#333333", titleColor="#222222")
)

# Save
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
