""" pyplots.ai
hexbin-basic: Basic Hexbin Plot
Library: altair 6.0.0 | Python 3.14.3
Quality: /100 | Updated: 2026-02-21
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - GPS coordinates showing traffic density in a metropolitan area
np.random.seed(42)

n_points = 5000

# Downtown core - highest density
downtown_lon = np.random.randn(n_points // 2) * 0.008 + (-122.335)
downtown_lat = np.random.randn(n_points // 2) * 0.006 + 47.608

# Shopping district - secondary hotspot
shopping_lon = np.random.randn(n_points // 3) * 0.005 + (-122.315)
shopping_lat = np.random.randn(n_points // 3) * 0.004 + 47.622

# Industrial zone - sparse traffic
industrial_lon = np.random.randn(n_points // 6) * 0.004 + (-122.355)
industrial_lat = np.random.randn(n_points // 6) * 0.003 + 47.635

longitude = np.concatenate([downtown_lon, shopping_lon, industrial_lon])
latitude = np.concatenate([downtown_lat, shopping_lat, industrial_lat])

# Hexagonal binning - compute hex grid positions and counts
hex_radius = 0.002
dx = hex_radius * np.sqrt(3)
dy = hex_radius * 1.5

col_idx = np.round(longitude / dx).astype(int)
row_idx = np.round(latitude / dy).astype(int)

# Offset odd rows for hexagonal staggering
shift = (row_idx % 2) * 0.5
col_adj = np.round((longitude / dx) - shift).astype(int)

hex_cx = (col_adj + shift) * dx
hex_cy = row_idx * dy

hex_keys = list(zip(hex_cx, hex_cy, strict=True))
hex_counts = pd.Series(hex_keys).value_counts()

hex_df = pd.DataFrame(
    {"lon": [k[0] for k in hex_counts.index], "lat": [k[1] for k in hex_counts.index], "count": hex_counts.values}
)

# Compute pixel size for hexagons to tile correctly
chart_width = 1600
chart_height = 900
lon_range = hex_df["lon"].max() - hex_df["lon"].min()
lat_range = hex_df["lat"].max() - hex_df["lat"].min()
px_per_lon = chart_width / lon_range if lon_range > 0 else 1
px_per_lat = chart_height / lat_range if lat_range > 0 else 1
hex_px_width = dx * px_per_lon
hex_px_height = 2 * hex_radius * px_per_lat
hex_area = hex_px_width * hex_px_height * 1.15

# Plot - hexagonal binning using mark_point with custom hexagon SVG path
hex_path = "M0,-1L0.866,-0.5L0.866,0.5L0,1L-0.866,0.5L-0.866,-0.5Z"

chart = (
    alt.Chart(hex_df)
    .mark_point(shape=hex_path, filled=True, strokeWidth=0.3, stroke="white")
    .encode(
        x=alt.X(
            "lon:Q",
            title="Longitude (\u00b0W)",
            scale=alt.Scale(zero=False),
            axis=alt.Axis(labelFontSize=18, titleFontSize=22, format=".2f", grid=True, gridOpacity=0.15),
        ),
        y=alt.Y(
            "lat:Q",
            title="Latitude (\u00b0N)",
            scale=alt.Scale(zero=False),
            axis=alt.Axis(labelFontSize=18, titleFontSize=22, format=".3f", grid=True, gridOpacity=0.15),
        ),
        color=alt.Color(
            "count:Q",
            scale=alt.Scale(scheme="viridis"),
            legend=alt.Legend(
                title="Vehicle Count", titleFontSize=20, labelFontSize=16, gradientLength=350, gradientThickness=25
            ),
        ),
        size=alt.value(hex_area),
        tooltip=[
            alt.Tooltip("lon:Q", title="Longitude", format=".3f"),
            alt.Tooltip("lat:Q", title="Latitude", format=".3f"),
            alt.Tooltip("count:Q", title="Vehicles"),
        ],
    )
    .properties(
        width=chart_width,
        height=chart_height,
        title=alt.Title("hexbin-basic \u00b7 altair \u00b7 pyplots.ai", fontSize=28, anchor="middle"),
    )
    .configure_view(strokeWidth=0)
    .configure_axis(domainColor="#888")
)

# Save
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
