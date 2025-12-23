""" pyplots.ai
hexbin-basic: Basic Hexbin Plot
Library: altair 6.0.0 | Python 3.13.11
Quality: 52/100 | Created: 2025-12-23
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - GPS coordinates showing traffic density in a metropolitan area
# Simulating vehicle GPS pings across different urban zones
np.random.seed(42)

n_points = 5000

# Downtown core - highest density (longitude/latitude offsets from city center)
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


# Hexagonal binning function - computes hex bin centers and counts
def hexbin_aggregate(x, y, gridsize=25):
    """Aggregate points into hexagonal bins and return bin centers with counts."""
    x_min, x_max = x.min(), x.max()
    y_min = y.min()

    # Hex geometry parameters
    hex_width = (x_max - x_min) / gridsize
    hex_height = hex_width * np.sqrt(3) / 2

    bin_counts = {}

    for xi, yi in zip(x, y, strict=True):
        # Offset coordinates for hexagonal grid
        col = int((xi - x_min) / hex_width)
        row_offset = (col % 2) * hex_height / 2
        row = int((yi - y_min - row_offset) / hex_height)

        # Snap to hex center
        cx = x_min + col * hex_width + hex_width / 2
        cy = y_min + row * hex_height + row_offset + hex_height / 2

        key = (round(cx, 6), round(cy, 6))
        bin_counts[key] = bin_counts.get(key, 0) + 1

    # Convert to list of hex centers with counts
    hex_data = [{"hex_x": cx, "hex_y": cy, "count": count} for (cx, cy), count in bin_counts.items()]

    return pd.DataFrame(hex_data), hex_width


# Compute hexagonal bins
hex_df, hex_size = hexbin_aggregate(longitude, latitude, gridsize=30)

# Custom SVG path for a flat-topped hexagon (unit size, will be scaled)
hex_path = "M 0 -1 L 0.866 -0.5 L 0.866 0.5 L 0 1 L -0.866 0.5 L -0.866 -0.5 Z"

# Plot - hexagonal binning using mark_point with custom hexagon SVG path
chart = (
    alt.Chart(hex_df)
    .mark_point(shape=hex_path, filled=True, strokeWidth=0.5, stroke="white", opacity=0.9)
    .encode(
        x=alt.X(
            "hex_x:Q",
            title="Longitude (°W)",
            scale=alt.Scale(domain=[longitude.min() - 0.005, longitude.max() + 0.005]),
            axis=alt.Axis(labelFontSize=18, titleFontSize=22, format=".2f", grid=True, gridOpacity=0.3),
        ),
        y=alt.Y(
            "hex_y:Q",
            title="Latitude (°N)",
            scale=alt.Scale(domain=[latitude.min() - 0.003, latitude.max() + 0.003]),
            axis=alt.Axis(labelFontSize=18, titleFontSize=22, format=".3f", grid=True, gridOpacity=0.3),
        ),
        color=alt.Color(
            "count:Q",
            scale=alt.Scale(scheme="viridis"),
            legend=alt.Legend(
                title="Vehicle Count", titleFontSize=20, labelFontSize=16, gradientLength=350, gradientThickness=25
            ),
        ),
        size=alt.value(550),
        tooltip=[
            alt.Tooltip("hex_x:Q", title="Longitude", format=".4f"),
            alt.Tooltip("hex_y:Q", title="Latitude", format=".4f"),
            alt.Tooltip("count:Q", title="Vehicles"),
        ],
    )
    .properties(
        width=1600, height=900, title=alt.Title("hexbin-basic · altair · pyplots.ai", fontSize=28, anchor="middle")
    )
    .configure_view(strokeWidth=0)
)

# Save
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
