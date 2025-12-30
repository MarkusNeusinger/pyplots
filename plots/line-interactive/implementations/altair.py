""" pyplots.ai
line-interactive: Interactive Line Chart with Hover and Zoom
Library: altair 6.0.0 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-30
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - Daily temperature readings for a city over one year
np.random.seed(42)
dates = pd.date_range("2024-01-01", periods=365, freq="D")

# Create realistic seasonal temperature pattern (Northern Hemisphere)
day_of_year = np.arange(365)
# Base seasonal pattern (coldest in January, warmest in July)
seasonal = 15 * np.sin(2 * np.pi * (day_of_year - 80) / 365)  # offset by ~80 days
# Add baseline and daily random variation
temperature = 12 + seasonal + np.random.normal(0, 3, 365)

df = pd.DataFrame({"Date": dates, "Temperature (°C)": temperature.round(1), "Month": dates.strftime("%B")})

# Create interactive selection for zoom/pan (named to avoid deduplication warning)
brush = alt.selection_interval(name="range_selector", encodings=["x"])

# Base chart encoding
base = alt.Chart(df).encode(
    x=alt.X("Date:T", title="Date", axis=alt.Axis(labelFontSize=18, titleFontSize=22)),
    y=alt.Y(
        "Temperature (°C):Q",
        title="Temperature (°C)",
        scale=alt.Scale(domain=[df["Temperature (°C)"].min() - 2, df["Temperature (°C)"].max() + 2]),
        axis=alt.Axis(labelFontSize=18, titleFontSize=22),
    ),
    tooltip=[
        alt.Tooltip("Date:T", title="Date", format="%B %d, %Y"),
        alt.Tooltip("Temperature (°C):Q", title="Temperature", format=".1f"),
        alt.Tooltip("Month:N", title="Month"),
    ],
)

# Main chart: line filtered by brush selection (zoom view)
main_line = base.mark_line(color="#306998", strokeWidth=2.5).properties(width=1500, height=680).transform_filter(brush)

# Points overlay for hover interaction
main_points = base.mark_point(color="#306998", size=50, filled=True, opacity=0.6).transform_filter(brush)

# Main chart combines line and points
main_chart = (main_line + main_points).properties(
    title=alt.Title("Daily Temperature 2024 · line-interactive · altair · pyplots.ai", fontSize=28, anchor="middle")
)

# Overview chart for range selection (shows full data)
overview = (
    base.mark_line(color="#306998", strokeWidth=1.5)
    .properties(width=1500, height=100, title=alt.Title("Drag to select range", fontSize=16, anchor="middle"))
    .add_params(brush)
)

# Combine main and overview charts
combined = (
    alt.vconcat(main_chart, overview)
    .configure_axis(labelFontSize=16, titleFontSize=20, gridOpacity=0.3)
    .configure_view(strokeWidth=0)
    .resolve_scale(y="independent")
)

# Save as PNG and HTML
combined.save("plot.png", scale_factor=3.0)
combined.save("plot.html")
