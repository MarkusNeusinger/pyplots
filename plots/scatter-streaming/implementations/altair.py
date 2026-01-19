""" pyplots.ai
scatter-streaming: Streaming Scatter Plot
Library: altair 6.0.0 | Python 3.13.11
Quality: 91/100 | Created: 2026-01-19
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - simulated streaming sensor data with timestamps
np.random.seed(42)
n_points = 200

# Generate timestamps simulating arrival over time (last 200 seconds of data)
timestamps = pd.date_range(end=pd.Timestamp.now(), periods=n_points, freq="s")

# Simulate sensor readings with some correlation and noise
# x: temperature-like readings (20-30 range)
# y: humidity-like readings (40-80 range) with correlation to x
base_x = np.cumsum(np.random.randn(n_points) * 0.3) + 25
x = np.clip(base_x, 20, 30)
y = 60 + (x - 25) * 4 + np.random.randn(n_points) * 5
y = np.clip(y, 40, 80)

# Calculate point age for opacity encoding (0 = oldest, 1 = newest)
point_age = np.linspace(0, 1, n_points)

# Create DataFrame
df = pd.DataFrame(
    {
        "x": x,
        "y": y,
        "timestamp": timestamps,
        "age": point_age,
        "opacity": 0.2 + 0.8 * point_age,  # Range from 0.2 to 1.0
    }
)

# Create streaming scatter plot with opacity encoding for point age
chart = (
    alt.Chart(df)
    .mark_circle(strokeWidth=0)
    .encode(
        x=alt.X("x:Q", title="Temperature (°C)", scale=alt.Scale(domain=[19, 31])),
        y=alt.Y("y:Q", title="Humidity (%)", scale=alt.Scale(domain=[35, 85])),
        opacity=alt.Opacity("opacity:Q", legend=None),
        color=alt.Color(
            "age:Q",
            scale=alt.Scale(scheme="blues", domain=[0, 1]),
            legend=alt.Legend(
                title="Recency",
                titleFontSize=18,
                labelFontSize=14,
                labelExpr="datum.value == 0 ? 'Old' : datum.value == 1 ? 'New' : ''",
                gradientLength=200,
                gradientThickness=20,
            ),
        ),
        size=alt.value(200),
        tooltip=[
            alt.Tooltip("x:Q", title="Temperature", format=".1f"),
            alt.Tooltip("y:Q", title="Humidity", format=".1f"),
            alt.Tooltip("timestamp:T", title="Time"),
        ],
    )
    .properties(
        width=1600, height=900, title=alt.Title("scatter-streaming · altair · pyplots.ai", fontSize=28, anchor="middle")
    )
    .configure_axis(labelFontSize=18, titleFontSize=22, gridColor="#e0e0e0", gridOpacity=0.5)
    .configure_view(strokeWidth=0)
)

# Save as PNG and HTML
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
