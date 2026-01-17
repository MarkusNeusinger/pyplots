"""pyplots.ai
contour-map-geographic: Contour Lines on Geographic Map
Library: altair | Python 3.13
Quality: pending | Created: 2025-01-17
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - Generate temperature-like data for Europe region
np.random.seed(42)

# Create dense grid covering Europe for smooth appearance
lon_range = np.linspace(-10, 40, 80)
lat_range = np.linspace(35, 70, 60)
lon_grid, lat_grid = np.meshgrid(lon_range, lat_range)

# Generate temperature pattern (decreases with latitude, varies with longitude)
temperature = (
    28
    - 0.55 * (lat_grid - 35)  # Cooler as you go north
    + 4 * np.sin((lon_grid + 5) / 12)  # East-west variation (Gulf Stream effect)
    + 2 * np.cos(lat_grid / 8)  # Additional pattern
    - 6 * np.exp(-((lat_grid - 47) ** 2 + (lon_grid - 10) ** 2) / 80)  # Alps cold spot
    + np.random.normal(0, 0.8, lon_grid.shape)  # Reduced noise for smoother contours
)

# Create DataFrame with binned temperatures for contour-like effect
df = pd.DataFrame(
    {"longitude": lon_grid.flatten(), "latitude": lat_grid.flatten(), "temperature": temperature.flatten()}
)

# Bin temperatures to create discrete contour levels
contour_levels = [-10, -5, 0, 5, 10, 15, 20, 25, 30]
df["temp_bin"] = pd.cut(df["temperature"], bins=contour_levels, labels=False)
df["temp_level"] = pd.cut(
    df["temperature"], bins=contour_levels, labels=["-7.5", "-2.5", "2.5", "7.5", "12.5", "17.5", "22.5", "27.5"]
).astype(float)

# Load world countries for geographic context
countries = alt.topo_feature("https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json", "countries")

# Base map - world countries with subtle styling
base = (
    alt.Chart(countries)
    .mark_geoshape(fill="#E8E8E8", stroke="#CCCCCC", strokeWidth=0.3)
    .project(type="mercator", scale=650, center=[15, 52], clipExtent=[[0, 0], [1600, 900]])
    .properties(width=1600, height=900)
)

# Create filled contour visualization using square marks for seamless appearance
# This approximates filled contours by using overlapping squares colored by temperature
filled_contours = (
    alt.Chart(df)
    .mark_square(size=350, opacity=0.85)
    .encode(
        longitude="longitude:Q",
        latitude="latitude:Q",
        color=alt.Color(
            "temp_level:Q",
            scale=alt.Scale(scheme="redyellowblue", reverse=True, domain=[-10, 30]),
            legend=alt.Legend(
                title="Temperature (°C)",
                titleFontSize=18,
                labelFontSize=14,
                gradientLength=400,
                gradientThickness=25,
                orient="right",
                offset=10,
            ),
        ),
        tooltip=[
            alt.Tooltip("longitude:Q", format=".1f", title="Longitude"),
            alt.Tooltip("latitude:Q", format=".1f", title="Latitude"),
            alt.Tooltip("temperature:Q", format=".1f", title="Temperature (°C)"),
        ],
    )
    .project(type="mercator", scale=650, center=[15, 52], clipExtent=[[0, 0], [1600, 900]])
    .properties(width=1600, height=900)
)

# Create contour lines by identifying points near level boundaries
contour_data = []
for level in [0, 5, 10, 15, 20, 25]:
    mask = np.abs(df["temperature"] - level) < 0.8
    level_points = df[mask].copy()
    level_points["contour_value"] = level
    contour_data.append(level_points)

contour_df = pd.concat(contour_data, ignore_index=True)

# Contour lines layer - darker points to show level boundaries
contour_lines = (
    alt.Chart(contour_df)
    .mark_point(size=15, opacity=0.6, filled=True)
    .encode(longitude="longitude:Q", latitude="latitude:Q", color=alt.value("#333333"))
    .project(type="mercator", scale=650, center=[15, 52], clipExtent=[[0, 0], [1600, 900]])
    .properties(width=1600, height=900)
)

# Layer all components: base map, filled contours, contour lines
chart = (
    alt.layer(base, filled_contours, contour_lines)
    .properties(
        width=1600,
        height=900,
        title=alt.Title(
            "European Temperature · contour-map-geographic · altair · pyplots.ai",
            fontSize=28,
            anchor="middle",
            color="#333333",
        ),
    )
    .configure_view(strokeWidth=0)
)

# Save outputs
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
