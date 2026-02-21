"""pyplots.ai
hexbin-basic: Basic Hexbin Plot
Library: altair 6.0.0 | Python 3.14.3
Quality: 83/100 | Updated: 2026-02-21
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
shift = (row_idx % 2) * 0.5
col_adj = np.round((longitude / dx) - shift).astype(int)

hex_cx = (col_adj + shift) * dx
hex_cy = row_idx * dy

counts = pd.DataFrame({"lon": hex_cx, "lat": hex_cy}).groupby(["lon", "lat"]).size().reset_index(name="count")

# Compute pixel size for hexagons to tile correctly
chart_width, chart_height = 1600, 900
lon_range = counts["lon"].max() - counts["lon"].min()
lat_range = counts["lat"].max() - counts["lat"].min()
hex_px_w = dx * (chart_width / lon_range) if lon_range > 0 else 1
hex_px_h = 2 * hex_radius * (chart_height / lat_range) if lat_range > 0 else 1
hex_area = hex_px_w * hex_px_h * 1.15

# Plot - hexagonal binning using mark_point with custom hexagon SVG path
hex_path = "M0,-1L0.866,-0.5L0.866,0.5L0,1L-0.866,0.5L-0.866,-0.5Z"

chart = (
    alt.Chart(counts)
    .mark_point(shape=hex_path, filled=True, strokeWidth=0.3, stroke="white")
    .encode(
        x=alt.X(
            "lon:Q",
            title="Longitude (\u00b0W)",
            scale=alt.Scale(zero=False),
            axis=alt.Axis(
                labelFontSize=18, titleFontSize=22, format=".2f", grid=True, gridOpacity=0.12, gridColor="#ccc"
            ),
        ),
        y=alt.Y(
            "lat:Q",
            title="Latitude (\u00b0N)",
            scale=alt.Scale(zero=False),
            axis=alt.Axis(
                labelFontSize=18,
                titleFontSize=22,
                format=".2f",
                tickCount=7,
                grid=True,
                gridOpacity=0.12,
                gridColor="#ccc",
            ),
        ),
        color=alt.Color(
            "count:Q",
            scale=alt.Scale(scheme="viridis", type="symlog"),
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
        title=alt.Title("hexbin-basic \u00b7 altair \u00b7 pyplots.ai", fontSize=28, anchor="middle", color="#222"),
    )
    .configure_view(strokeWidth=0, fill="#f9f9fb")
    .configure_axis(domainColor="#999", tickColor="#999", labelColor="#444", titleColor="#333")
)

# Save
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
