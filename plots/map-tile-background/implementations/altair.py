"""pyplots.ai
map-tile-background: Map with Tile Background
Library: altair | Python 3.13
Quality: pending | Created: 2026-01-20
"""

import altair as alt
import numpy as np
import pandas as pd


# Data: European landmarks with visitor counts (millions annually)
np.random.seed(42)

landmarks = {
    "name": [
        "Eiffel Tower",
        "Colosseum",
        "Sagrada Familia",
        "Big Ben",
        "Rijksmuseum",
        "Brandenburg Gate",
        "Prague Castle",
        "Schonbrunn Palace",
        "Louvre Museum",
        "Vatican Museums",
        "Alhambra",
        "Buckingham Palace",
        "Anne Frank House",
        "Acropolis",
        "Charles Bridge",
        "Manneken Pis",
        "Tower of Pisa",
        "Notre-Dame",
        "Trevi Fountain",
        "La Rambla",
    ],
    "lat": [
        48.8584,
        41.8902,
        41.4036,
        51.5007,
        52.3600,
        52.5163,
        50.0911,
        48.1845,
        48.8606,
        41.9065,
        37.1760,
        51.5014,
        52.3752,
        37.9715,
        50.0865,
        50.8450,
        43.7230,
        48.8530,
        41.9009,
        41.3809,
    ],
    "lon": [
        2.2945,
        12.4922,
        2.1744,
        -0.1246,
        4.8852,
        13.3777,
        14.4006,
        16.3122,
        2.3376,
        12.4536,
        -3.5881,
        -0.1419,
        4.8840,
        23.7257,
        14.4114,
        4.3499,
        10.3966,
        2.3499,
        12.4833,
        2.1734,
    ],
    "visitors": [7.0, 7.6, 4.5, 2.0, 2.7, 3.0, 1.9, 4.0, 9.6, 6.9, 2.7, 0.8, 1.3, 3.0, 1.5, 0.5, 5.5, 12.0, 3.5, 78.0],
    "category": [
        "Monument",
        "Historical",
        "Religious",
        "Monument",
        "Museum",
        "Monument",
        "Historical",
        "Historical",
        "Museum",
        "Museum",
        "Historical",
        "Historical",
        "Museum",
        "Historical",
        "Monument",
        "Monument",
        "Monument",
        "Religious",
        "Monument",
        "Street",
    ],
}

df = pd.DataFrame(landmarks)

# Tile parameters
zoom = 5
tile_size = 256

# Tile range for Europe at zoom 5 - using 8x5 grid for 16:10 aspect ratio
# This covers from Western Portugal/Spain to Eastern Europe/Greece
tx_min, tx_max = 13, 20  # 8 tiles wide
ty_min, ty_max = 9, 13  # 5 tiles tall

# Number of tiles
n_tiles_x = tx_max - tx_min + 1  # 8 tiles
n_tiles_y = ty_max - ty_min + 1  # 5 tiles

# Chart dimensions - use aspect ratio matching tile grid
# 8:5 tiles = 16:10 aspect ratio ≈ 1600x1000
chart_width = 1600
chart_height = 1000


# Web Mercator projection helpers
def lon_to_tile_x(lon, z):
    """Convert longitude to tile x coordinate."""
    return (lon + 180) / 360 * (2**z)


def lat_to_tile_y(lat, z):
    """Convert latitude to tile y coordinate (Web Mercator)."""
    lat_rad = np.radians(lat)
    return (1 - np.log(np.tan(lat_rad) + 1 / np.cos(lat_rad)) / np.pi) / 2 * (2**z)


# Calculate tile display size
tile_disp_w = chart_width / n_tiles_x
tile_disp_h = chart_height / n_tiles_y

# Generate tile data - position at pixel coordinates within the chart
tiles = []
for tx in range(tx_min, tx_max + 1):
    for ty in range(ty_min, ty_max + 1):
        url = f"https://tile.openstreetmap.org/{zoom}/{tx}/{ty}.png"
        # Position as pixel coordinates (center of each tile cell)
        x_pix = (tx - tx_min + 0.5) * tile_disp_w
        y_pix = (ty - ty_min + 0.5) * tile_disp_h
        tiles.append({"url": url, "x": x_pix, "y": y_pix})

tiles_df = pd.DataFrame(tiles)

# Convert landmark coordinates to pixel coordinates
df["x_pix"] = df["lon"].apply(lambda lon: (lon_to_tile_x(lon, zoom) - tx_min) * tile_disp_w)
df["y_pix"] = df["lat"].apply(lambda lat: (lat_to_tile_y(lat, zoom) - ty_min) * tile_disp_h)

# Filter data points that fall within the chart bounds
df = df[(df["x_pix"] >= 0) & (df["x_pix"] <= chart_width) & (df["y_pix"] >= 0) & (df["y_pix"] <= chart_height)]

# Tile background layer - using pixel coordinates
tile_layer = (
    alt.Chart(tiles_df)
    .mark_image(width=tile_disp_w, height=tile_disp_h)
    .encode(
        url="url:N",
        x=alt.X("x:Q", scale=alt.Scale(domain=[0, chart_width], nice=False), axis=None),
        y=alt.Y("y:Q", scale=alt.Scale(domain=[0, chart_height], nice=False), axis=None),
    )
)

# Category colors (colorblind-safe palette using Python blue/yellow first)
category_colors = {
    "Monument": "#306998",
    "Historical": "#FFD43B",
    "Museum": "#2CA02C",
    "Religious": "#D62728",
    "Street": "#9467BD",
}

# Data points layer
points_layer = (
    alt.Chart(df)
    .mark_circle(opacity=0.85, stroke="#FFFFFF", strokeWidth=2)
    .encode(
        x=alt.X("x_pix:Q", scale=alt.Scale(domain=[0, chart_width], nice=False), axis=None),
        y=alt.Y("y_pix:Q", scale=alt.Scale(domain=[0, chart_height], nice=False), axis=None),
        size=alt.Size(
            "visitors:Q",
            scale=alt.Scale(domain=[0.5, 80], range=[200, 2000]),
            legend=alt.Legend(
                title="Visitors (M/year)", titleFontSize=18, labelFontSize=14, orient="bottom-left", offset=20
            ),
        ),
        color=alt.Color(
            "category:N",
            scale=alt.Scale(domain=list(category_colors.keys()), range=list(category_colors.values())),
            legend=alt.Legend(title="Category", titleFontSize=18, labelFontSize=14, orient="bottom-right", offset=20),
        ),
        tooltip=[
            alt.Tooltip("name:N", title="Landmark"),
            alt.Tooltip("visitors:Q", title="Visitors (M)", format=".1f"),
            alt.Tooltip("category:N", title="Category"),
            alt.Tooltip("lat:Q", title="Latitude", format=".4f"),
            alt.Tooltip("lon:Q", title="Longitude", format=".4f"),
        ],
    )
)

# Text labels for major landmarks (visitors > 5M)
labels_df = df[df["visitors"] > 5].copy()
labels_layer = (
    alt.Chart(labels_df)
    .mark_text(align="left", dx=15, dy=-5, fontSize=14, fontWeight="bold", color="#333333")
    .encode(
        x=alt.X("x_pix:Q", scale=alt.Scale(domain=[0, chart_width], nice=False)),
        y=alt.Y("y_pix:Q", scale=alt.Scale(domain=[0, chart_height], nice=False)),
        text="name:N",
    )
)

# OSM attribution (required by license)
attribution_df = pd.DataFrame(
    {"text": ["© OpenStreetMap contributors"], "x": [chart_width - 10], "y": [chart_height - 10]}
)

attribution_layer = (
    alt.Chart(attribution_df)
    .mark_text(align="right", baseline="bottom", fontSize=12, color="#666666")
    .encode(
        x=alt.X("x:Q", scale=alt.Scale(domain=[0, chart_width], nice=False)),
        y=alt.Y("y:Q", scale=alt.Scale(domain=[0, chart_height], nice=False)),
        text="text:N",
    )
)

# Combine all layers
chart = (
    alt.layer(tile_layer, points_layer, labels_layer, attribution_layer)
    .properties(
        width=chart_width,
        height=chart_height,
        title=alt.Title(
            text="European Landmarks · map-tile-background · altair · pyplots.ai",
            fontSize=28,
            anchor="middle",
            color="#333333",
        ),
    )
    .configure_view(strokeWidth=0)
    .configure_legend(titleColor="#333333", labelColor="#555555", padding=15, cornerRadius=5)
)

# Save as PNG (scale 3x for high resolution)
chart.save("plot.png", scale_factor=3.0)

# Save interactive HTML version
chart.save("plot.html")
