"""pyplots.ai
heatmap-basic: Basic Heatmap
Library: altair 6.0.0 | Python 3.14.3
Quality: /100 | Updated: 2026-02-15
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

# Inject realistic correlations
raw[:, 1] += raw[:, 0] * 0.6  # Humidity ~ Temperature
raw[:, 5] += raw[:, 1] * 0.7  # Cloud Cover ~ Humidity
raw[:, 6] += raw[:, 5] * 0.5  # Precipitation ~ Cloud Cover
raw[:, 4] -= raw[:, 5] * 0.8  # Visibility inversely ~ Cloud Cover
raw[:, 7] -= raw[:, 5] * 0.6  # UV Index inversely ~ Cloud Cover
raw[:, 3] -= raw[:, 0] * 0.3  # Pressure inversely ~ Temperature

corr = np.corrcoef(raw.T)

# Build long-form dataframe
records = []
for i, row_var in enumerate(variables):
    for j, col_var in enumerate(variables):
        records.append({"x": col_var, "y": row_var, "value": round(corr[i, j], 2)})

df = pd.DataFrame(records)

# Axis ordering
axis_order = list(variables)

# Plot - heatmap with diverging color centered at 0
heatmap = (
    alt.Chart(df)
    .mark_rect(stroke="#ffffff", strokeWidth=1.5)
    .encode(
        x=alt.X("x:N", title=None, sort=axis_order, axis=alt.Axis(labelFontSize=16, labelAngle=0, orient="top")),
        y=alt.Y("y:N", title=None, sort=axis_order, axis=alt.Axis(labelFontSize=16)),
        color=alt.Color(
            "value:Q",
            scale=alt.Scale(scheme="redblue", domain=[-1, 1], domainMid=0),
            legend=alt.Legend(
                title="Correlation", titleFontSize=18, labelFontSize=16, gradientLength=300, gradientThickness=16
            ),
        ),
        tooltip=[
            alt.Tooltip("x:N", title="Variable X"),
            alt.Tooltip("y:N", title="Variable Y"),
            alt.Tooltip("value:Q", title="Correlation", format=".2f"),
        ],
    )
)

# Text annotations with adaptive color
text = (
    alt.Chart(df)
    .mark_text(fontSize=16, fontWeight="bold")
    .encode(
        x=alt.X("x:N", sort=axis_order),
        y=alt.Y("y:N", sort=axis_order),
        text=alt.Text("value:Q", format=".2f"),
        color=alt.when((alt.datum.value > 0.6) | (alt.datum.value < -0.6))
        .then(alt.value("white"))
        .otherwise(alt.value("#333333")),
    )
)

# Combine and configure
chart = (
    (heatmap + text)
    .properties(
        width=1200,
        height=1200,
        title=alt.Title(
            "Weather Metrics Correlation · heatmap-basic · altair · pyplots.ai", fontSize=28, anchor="start", offset=20
        ),
    )
    .configure_axis(grid=False)
    .configure_view(strokeWidth=0)
)

# Save
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
