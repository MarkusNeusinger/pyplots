""" pyplots.ai
contour-map-geographic: Contour Lines on Geographic Map
Library: altair 6.0.0 | Python 3.13.11
Quality: 82/100 | Created: 2026-01-17
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - Generate temperature-like data for Europe region
np.random.seed(42)

# Create dense grid covering wider Europe region to fill map canvas
lon_range = np.linspace(-25, 55, 120)
lat_range = np.linspace(30, 72, 80)
lon_grid, lat_grid = np.meshgrid(lon_range, lat_range)

# Generate temperature pattern (decreases with latitude, varies with longitude)
temperature = (
    30
    - 0.6 * (lat_grid - 30)  # Cooler as you go north
    + 3 * np.sin((lon_grid + 10) / 15)  # East-west variation (Gulf Stream effect)
    + 2 * np.cos(lat_grid / 10)  # Additional pattern
    - 5 * np.exp(-((lat_grid - 47) ** 2 + (lon_grid - 10) ** 2) / 100)  # Alps cold spot
    - 3 * np.exp(-((lat_grid - 65) ** 2 + (lon_grid - 25) ** 2) / 150)  # Scandinavian cold
    + np.random.normal(0, 0.3, lon_grid.shape)  # Minimal noise for smoother contours
)

# Clip to realistic range
temperature = np.clip(temperature, -15, 35)

# Create DataFrame
df = pd.DataFrame(
    {"longitude": lon_grid.flatten(), "latitude": lat_grid.flatten(), "temperature": temperature.flatten()}
)

# Define contour levels for labeling
contour_levels = [-10, -5, 0, 5, 10, 15, 20, 25, 30]

# Load world countries for geographic context
countries = alt.topo_feature("https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json", "countries")

# Map projection settings - centered on Europe with better coverage
projection_params = {"type": "mercator", "scale": 550, "center": [15, 52]}

# Base map - world countries with subtle styling
base = (
    alt.Chart(countries)
    .mark_geoshape(fill="#F0F0F0", stroke="#CCCCCC", strokeWidth=0.5)
    .project(**projection_params)
    .properties(width=1600, height=900)
)

# Create smooth filled contour visualization using small circles for seamless appearance
filled_contours = (
    alt.Chart(df)
    .mark_circle(size=180, opacity=0.9)
    .encode(
        longitude="longitude:Q",
        latitude="latitude:Q",
        color=alt.Color(
            "temperature:Q",
            scale=alt.Scale(scheme="redyellowblue", reverse=True, domain=[-10, 30]),
            legend=alt.Legend(
                title="Temperature (°C)",
                titleFontSize=20,
                labelFontSize=16,
                gradientLength=450,
                gradientThickness=30,
                orient="right",
                offset=20,
            ),
        ),
        tooltip=[
            alt.Tooltip("longitude:Q", format=".1f", title="Longitude"),
            alt.Tooltip("latitude:Q", format=".1f", title="Latitude"),
            alt.Tooltip("temperature:Q", format=".1f", title="Temperature (°C)"),
        ],
    )
    .project(**projection_params)
    .properties(width=1600, height=900)
)

# Create contour line data by identifying boundary points between temperature bins
contour_data = []
for level in contour_levels[1:-1]:  # Skip extreme ends
    mask = np.abs(df["temperature"] - level) < 0.6
    level_points = df[mask].copy()
    level_points["contour_value"] = level
    level_points["contour_label"] = f"{level}°C"
    contour_data.append(level_points)

contour_df = pd.concat(contour_data, ignore_index=True)

# Contour lines layer - small dark points forming isolines
contour_lines = (
    alt.Chart(contour_df)
    .mark_circle(size=8, opacity=0.7)
    .encode(longitude="longitude:Q", latitude="latitude:Q", color=alt.value("#2D2D2D"))
    .project(**projection_params)
    .properties(width=1600, height=900)
)

# Create contour labels at strategic positions
# Sample representative points along each contour level for labeling
label_data = []
for level in [0, 10, 20]:
    level_points = contour_df[contour_df["contour_value"] == level]
    if len(level_points) > 0:
        # Select points at different longitudes for label placement
        for target_lon in [-10, 10, 30]:
            closest_idx = (level_points["longitude"] - target_lon).abs().idxmin()
            point = level_points.loc[closest_idx].copy()
            label_data.append({"longitude": point["longitude"], "latitude": point["latitude"], "label": f"{level}°C"})

label_df = pd.DataFrame(label_data)

# Contour value labels
contour_labels = (
    alt.Chart(label_df)
    .mark_text(fontSize=16, fontWeight="bold", fill="#1a1a1a", stroke="#FFFFFF", strokeWidth=2)
    .encode(longitude="longitude:Q", latitude="latitude:Q", text="label:N")
    .project(**projection_params)
    .properties(width=1600, height=900)
)

# Layer all components: base map, filled contours, contour lines, labels
chart = (
    alt.layer(base, filled_contours, contour_lines, contour_labels)
    .properties(
        width=1600,
        height=900,
        title=alt.Title(
            "European Temperature Contours · contour-map-geographic · altair · pyplots.ai",
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
