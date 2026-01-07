"""pyplots.ai
line-animated-progressive: Animated Line Plot Over Time
Library: altair | Python 3.13
Quality: pending | Created: 2025-01-07
"""

import altair as alt
import numpy as np
import pandas as pd


# Data: Monthly temperature readings over 3 years
np.random.seed(42)
dates = pd.date_range("2022-01-01", periods=36, freq="ME")
# Seasonal pattern with slight upward trend
base_temp = 15 + 10 * np.sin(np.linspace(0, 6 * np.pi, 36))  # Seasonal cycle
trend = np.linspace(0, 2, 36)  # Slight warming trend
noise = np.random.normal(0, 1.5, 36)
temperatures = base_temp + trend + noise

df = pd.DataFrame({"date": dates, "temperature": temperatures, "order": range(len(dates))})

# Create base line chart showing full data with gradient-like effect via point markers
# The markers suggest progression direction (smaller/lighter to larger/darker)
line = (
    alt.Chart(df)
    .mark_line(color="#306998", strokeWidth=4, opacity=0.9)
    .encode(
        x=alt.X("date:T", title="Date", axis=alt.Axis(labelFontSize=18, titleFontSize=22, format="%b %Y")),
        y=alt.Y(
            "temperature:Q",
            title="Temperature (°C)",
            axis=alt.Axis(labelFontSize=18, titleFontSize=22),
            scale=alt.Scale(domain=[0, 35]),
        ),
    )
)

# Add points with size gradient to show progression direction (smaller at start, larger at end)
points = (
    alt.Chart(df)
    .mark_circle(opacity=0.8)
    .encode(
        x="date:T",
        y="temperature:Q",
        size=alt.Size("order:Q", scale=alt.Scale(range=[30, 200]), legend=None),
        color=alt.Color("order:Q", scale=alt.Scale(scheme="blues"), legend=None),
        tooltip=[
            alt.Tooltip("date:T", title="Date", format="%B %Y"),
            alt.Tooltip("temperature:Q", title="Temperature (°C)", format=".1f"),
        ],
    )
)

# Add a highlight on the final point (most recent)
final_point = (
    alt.Chart(df.tail(1))
    .mark_circle(size=400, color="#FFD43B", stroke="#306998", strokeWidth=3, opacity=1.0)
    .encode(x="date:T", y="temperature:Q")
)

# Add annotation arrow indicating progression direction
arrow_data = pd.DataFrame({"x": [df["date"].iloc[5]], "y": [32], "text": ["← Progression →"]})

arrow_text = (
    alt.Chart(arrow_data)
    .mark_text(fontSize=18, fontWeight="bold", color="#306998", opacity=0.7)
    .encode(x="x:T", y="y:Q", text="text:N")
)

# Combine all layers
chart = (
    (line + points + final_point + arrow_text)
    .properties(
        width=1600,
        height=900,
        title=alt.Title(
            "Monthly Temperature Readings · line-animated-progressive · altair · pyplots.ai",
            fontSize=28,
            fontWeight="bold",
            anchor="middle",
        ),
    )
    .configure_axis(labelFontSize=18, titleFontSize=22, gridOpacity=0.3)
    .configure_view(strokeWidth=0)
)

# Save static PNG
chart.save("plot.png", scale_factor=3.0)

# Save interactive HTML with animation slider
# Create animated chart with slider for frame-by-frame progression
df_animated = []
for i in range(1, len(df) + 1):
    subset = df.head(i).copy()
    subset["frame"] = i
    df_animated.append(subset)

df_animated = pd.concat(df_animated, ignore_index=True)

# Animation slider
slider = alt.binding_range(min=1, max=len(df), step=1, name="Progress: ")
selection = alt.param(name="frame", value=len(df), bind=slider)

line_animated = (
    alt.Chart(df_animated)
    .mark_line(color="#306998", strokeWidth=4)
    .encode(
        x=alt.X("date:T", title="Date", axis=alt.Axis(labelFontSize=16, titleFontSize=20, format="%b %Y")),
        y=alt.Y(
            "temperature:Q",
            title="Temperature (°C)",
            axis=alt.Axis(labelFontSize=16, titleFontSize=20),
            scale=alt.Scale(domain=[0, 35]),
        ),
    )
    .transform_filter(alt.datum.frame <= selection)
)

points_animated = (
    alt.Chart(df_animated)
    .mark_circle(size=100, color="#306998", opacity=0.7)
    .encode(
        x="date:T",
        y="temperature:Q",
        tooltip=[
            alt.Tooltip("date:T", title="Date", format="%B %Y"),
            alt.Tooltip("temperature:Q", title="Temperature (°C)", format=".1f"),
        ],
    )
    .transform_filter(alt.datum.frame <= selection)
)

# Highlight current point (the latest in the current frame)
current_point = (
    alt.Chart(df_animated)
    .mark_circle(size=300, color="#FFD43B", stroke="#306998", strokeWidth=3)
    .encode(x="date:T", y="temperature:Q")
    .transform_filter(alt.datum.frame == selection)
    .transform_filter(alt.datum.order == alt.datum.frame - 1)
)

chart_animated = (
    (line_animated + points_animated + current_point)
    .properties(
        width=900,
        height=500,
        title=alt.Title(
            "line-animated-progressive · altair · pyplots.ai",
            fontSize=24,
            fontWeight="bold",
            anchor="middle",
            subtitle="Use slider to animate the progressive line reveal",
        ),
    )
    .add_params(selection)
    .configure_axis(labelFontSize=16, titleFontSize=20, gridOpacity=0.3)
    .configure_view(strokeWidth=0)
)

chart_animated.save("plot.html")
