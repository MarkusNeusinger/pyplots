"""pyplots.ai
hexbin-basic: Basic Hexbin Plot
Library: altair 6.0.0 | Python 3.13.11
Quality: 78/100 | Created: 2025-12-23
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

df = pd.DataFrame({"longitude": longitude, "latitude": latitude})

# Plot - 2D density heatmap (binned approximation of hexbin)
# Note: Altair uses rectangular binning; hexagonal binning not natively supported
chart = (
    alt.Chart(df)
    .mark_rect(cornerRadius=2)
    .encode(
        x=alt.X(
            "longitude:Q",
            bin=alt.Bin(maxbins=30),
            title="Longitude (°W)",
            axis=alt.Axis(labelFontSize=18, titleFontSize=22, format=".2f"),
        ),
        y=alt.Y(
            "latitude:Q",
            bin=alt.Bin(maxbins=30),
            title="Latitude (°N)",
            axis=alt.Axis(labelFontSize=18, titleFontSize=22, format=".3f"),
        ),
        color=alt.Color(
            "count():Q",
            scale=alt.Scale(scheme="viridis"),
            legend=alt.Legend(
                title="Vehicle Count", titleFontSize=20, labelFontSize=16, gradientLength=350, gradientThickness=25
            ),
        ),
        tooltip=[
            alt.Tooltip("longitude:Q", bin=alt.Bin(maxbins=30), title="Longitude Range"),
            alt.Tooltip("latitude:Q", bin=alt.Bin(maxbins=30), title="Latitude Range"),
            alt.Tooltip("count():Q", title="Vehicles"),
        ],
    )
    .properties(
        width=1600, height=900, title=alt.Title("hexbin-basic · altair · pyplots.ai", fontSize=28, anchor="middle")
    )
    .configure_axis(grid=False)
    .configure_view(strokeWidth=0)
)

# Save
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
