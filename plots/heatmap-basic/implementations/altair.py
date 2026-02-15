""" pyplots.ai
heatmap-basic: Basic Heatmap
Library: altair 6.0.0 | Python 3.14.3
Quality: 87/100 | Updated: 2026-02-15
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - correlation matrix with realistic variables
np.random.seed(42)
variables = [
    "Temperature",
    "Humidity",
    "Wind Speed",
    "Pressure",
    "Visibility",
    "Cloud Cover",
    "Precipitation",
    "UV Index",
]

n_samples = 200
raw = np.random.randn(n_samples, len(variables))

# Inject realistic correlations with stronger relationships
raw[:, 1] += raw[:, 0] * 0.6  # Humidity ~ Temperature
raw[:, 5] += raw[:, 1] * 0.7  # Cloud Cover ~ Humidity
raw[:, 6] += raw[:, 5] * 0.65  # Precipitation ~ Cloud Cover (stronger)
raw[:, 4] -= raw[:, 5] * 0.9  # Visibility inversely ~ Cloud Cover (stronger)
raw[:, 7] -= raw[:, 5] * 0.7  # UV Index inversely ~ Cloud Cover (stronger)
raw[:, 7] += raw[:, 0] * 0.5  # UV Index ~ Temperature
raw[:, 3] -= raw[:, 0] * 0.4  # Pressure inversely ~ Temperature (stronger)
raw[:, 2] += raw[:, 3] * 0.3  # Wind Speed ~ Pressure

corr = np.corrcoef(raw.T)

# Build long-form dataframe
records = []
for i, row_var in enumerate(variables):
    for j, col_var in enumerate(variables):
        val = round(corr[i, j], 2)
        records.append({"x": col_var, "y": row_var, "value": val, "abs_value": abs(val)})

df = pd.DataFrame(records)

# Axis ordering
axis_order = list(variables)

# Plot - heatmap with colorblind-safe diverging color centered at 0
heatmap = (
    alt.Chart(df)
    .mark_rect(stroke="#ffffff", strokeWidth=1.5, cornerRadius=2)
    .encode(
        x=alt.X(
            "x:N",
            title="Weather Variable",
            sort=axis_order,
            axis=alt.Axis(
                labelFontSize=16, labelAngle=-30, orient="top", titleFontSize=20, titlePadding=12, labelPadding=8
            ),
        ),
        y=alt.Y(
            "y:N",
            title="Weather Variable",
            sort=axis_order,
            axis=alt.Axis(labelFontSize=16, titleFontSize=20, titlePadding=12, labelPadding=8),
        ),
        color=alt.Color(
            "value:Q",
            scale=alt.Scale(scheme="blueorange", domain=[-1, 1], domainMid=0),
            legend=alt.Legend(
                title="Correlation",
                titleFontSize=18,
                labelFontSize=16,
                gradientLength=350,
                gradientThickness=18,
                titlePadding=8,
                offset=12,
            ),
        ),
        tooltip=[
            alt.Tooltip("x:N", title="Variable X"),
            alt.Tooltip("y:N", title="Variable Y"),
            alt.Tooltip("value:Q", title="Correlation", format=".2f"),
        ],
    )
)

# Highlight cells with strong correlations using thicker borders
highlight = (
    alt.Chart(df[df["abs_value"] >= 0.7])
    .mark_rect(stroke="#333333", strokeWidth=2.5, filled=False, cornerRadius=2)
    .encode(x=alt.X("x:N", sort=axis_order), y=alt.Y("y:N", sort=axis_order))
)

# Text annotations with adaptive color
text = (
    alt.Chart(df)
    .mark_text(fontSize=16, fontWeight="bold")
    .encode(
        x=alt.X("x:N", sort=axis_order),
        y=alt.Y("y:N", sort=axis_order),
        text=alt.Text("value:Q", format=".2f"),
        color=alt.when((alt.datum.value > 0.55) | (alt.datum.value < -0.55))
        .then(alt.value("white"))
        .otherwise(alt.value("#333333")),
    )
)

# Combine and configure
chart = (
    (heatmap + highlight + text)
    .properties(
        width=1200,
        height=1200,
        title=alt.Title(
            "heatmap-basic · altair · pyplots.ai",
            subtitle="Pairwise Pearson correlation coefficients for 8 weather metrics",
            fontSize=28,
            subtitleFontSize=18,
            subtitleColor="#666666",
            anchor="start",
            offset=20,
        ),
    )
    .configure_axis(grid=False)
    .configure_view(strokeWidth=0)
)

# Save
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
