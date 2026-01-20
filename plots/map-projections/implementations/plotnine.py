""" pyplots.ai
map-projections: World Map with Different Projections
Library: plotnine 0.15.2 | Python 3.13.11
Quality: 85/100 | Created: 2026-01-20
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    coord_fixed,
    element_blank,
    element_rect,
    element_text,
    facet_wrap,
    geom_path,
    geom_polygon,
    ggplot,
    labs,
    theme,
)


# Seed for reproducibility
np.random.seed(42)


# Simplified world continent boundaries (lon, lat pairs)
# These are stylized coastline approximations for visualization purposes
def get_continent_data():
    continents = []

    # North America
    na_lon = [
        -170,
        -168,
        -145,
        -125,
        -124,
        -117,
        -105,
        -97,
        -82,
        -77,
        -68,
        -55,
        -52,
        -80,
        -87,
        -97,
        -105,
        -125,
        -145,
        -165,
        -170,
    ]
    na_lat = [60, 65, 70, 55, 48, 33, 25, 26, 25, 35, 45, 48, 45, 27, 30, 20, 22, 50, 60, 55, 60]
    for i in range(len(na_lon)):
        continents.append({"continent": "North America", "order": i, "lon": na_lon[i], "lat": na_lat[i]})

    # South America
    sa_lon = [-80, -68, -60, -50, -35, -40, -50, -55, -68, -72, -75, -80, -82, -80]
    sa_lat = [10, 12, 5, 0, -5, -22, -35, -52, -55, -18, -5, 0, 8, 10]
    for i in range(len(sa_lon)):
        continents.append({"continent": "South America", "order": i, "lon": sa_lon[i], "lat": sa_lat[i]})

    # Europe
    eu_lon = [-10, 0, 10, 20, 30, 40, 50, 60, 50, 35, 25, 20, 10, 0, -10, -10]
    eu_lat = [35, 37, 36, 35, 35, 40, 45, 55, 70, 70, 70, 65, 60, 50, 40, 35]
    for i in range(len(eu_lon)):
        continents.append({"continent": "Europe", "order": i, "lon": eu_lon[i], "lat": eu_lat[i]})

    # Africa
    af_lon = [-17, -5, 10, 35, 50, 52, 43, 35, 30, 15, 0, -17, -17]
    af_lat = [15, 37, 37, 32, 12, 0, -25, -35, -35, -25, 5, 20, 15]
    for i in range(len(af_lon)):
        continents.append({"continent": "Africa", "order": i, "lon": af_lon[i], "lat": af_lat[i]})

    # Asia
    as_lon = [60, 80, 100, 120, 140, 145, 140, 130, 105, 100, 80, 60, 45, 30, 25, 30, 35, 50, 60]
    as_lat = [55, 70, 75, 70, 55, 45, 35, 30, 0, 5, 10, 25, 30, 35, 42, 55, 70, 70, 55]
    for i in range(len(as_lon)):
        continents.append({"continent": "Asia", "order": i, "lon": as_lon[i], "lat": as_lat[i]})

    # Australia
    au_lon = [113, 125, 135, 145, 152, 150, 140, 130, 115, 113]
    au_lat = [-22, -15, -12, -15, -25, -38, -38, -33, -35, -22]
    for i in range(len(au_lon)):
        continents.append({"continent": "Australia", "order": i, "lon": au_lon[i], "lat": au_lat[i]})

    # Antarctica (partial)
    an_lon = [-180, -120, -60, 0, 60, 120, 180, 180, -180, -180]
    an_lat = [-65, -70, -72, -70, -72, -70, -65, -85, -85, -65]
    for i in range(len(an_lon)):
        continents.append({"continent": "Antarctica", "order": i, "lon": an_lon[i], "lat": an_lat[i]})

    return pd.DataFrame(continents)


# Projection functions
def mercator(lon, lat):
    """Mercator projection - cylindrical, conformal, extreme polar distortion"""
    x = np.radians(lon)
    # Clip latitude to avoid infinity at poles
    lat_clipped = np.clip(lat, -85, 85)
    y = np.log(np.tan(np.pi / 4 + np.radians(lat_clipped) / 2))
    return x, y


def robinson(lon, lat):
    """Robinson projection - pseudo-cylindrical, compromise projection"""
    # Robinson projection lookup table (simplified)
    lat_table = np.array([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90])
    x_table = np.array(
        [
            1.0000,
            0.9986,
            0.9954,
            0.9900,
            0.9822,
            0.9730,
            0.9600,
            0.9427,
            0.9216,
            0.8962,
            0.8679,
            0.8350,
            0.7986,
            0.7597,
            0.7186,
            0.6732,
            0.6213,
            0.5722,
            0.5322,
        ]
    )
    y_table = np.array(
        [
            0.0000,
            0.0620,
            0.1240,
            0.1860,
            0.2480,
            0.3100,
            0.3720,
            0.4340,
            0.4958,
            0.5571,
            0.6176,
            0.6769,
            0.7346,
            0.7903,
            0.8435,
            0.8936,
            0.9394,
            0.9761,
            1.0000,
        ]
    )

    abs_lat = np.abs(lat)
    x_factor = np.interp(abs_lat, lat_table, x_table)
    y_factor = np.interp(abs_lat, lat_table, y_table)

    x = np.radians(lon) * x_factor * 0.8487
    y = y_factor * np.sign(lat) * 1.3523
    return x, y


def mollweide(lon, lat):
    """Mollweide projection - equal-area, pseudocylindrical"""
    lon_rad = np.radians(lon)
    lat_rad = np.radians(lat)

    # Newton-Raphson iteration to solve for theta
    theta = lat_rad.copy() if isinstance(lat_rad, np.ndarray) else lat_rad
    for _ in range(10):
        denom = 2 + 2 * np.cos(2 * theta)
        # Avoid division by zero at poles
        denom = np.where(np.abs(denom) < 1e-10, 1e-10, denom)
        delta = -(2 * theta + np.sin(2 * theta) - np.pi * np.sin(lat_rad)) / denom
        theta = theta + delta

    x = 2 * np.sqrt(2) / np.pi * lon_rad * np.cos(theta)
    y = np.sqrt(2) * np.sin(theta)
    return x, y


def equirectangular(lon, lat):
    """Equirectangular (Plate Carree) projection - simplest cylindrical"""
    x = np.radians(lon)
    y = np.radians(lat)
    return x, y


# Apply projection to dataframe
def apply_projection(df, projection_func, proj_name):
    result = df.copy()
    x, y = projection_func(df["lon"].values, df["lat"].values)
    result["x"] = x
    result["y"] = y
    result["projection"] = proj_name
    return result


# Generate graticule (latitude/longitude grid lines)
def generate_graticule():
    graticule_data = []

    # Longitude lines (meridians) every 30 degrees
    for lon_val in range(-180, 181, 30):
        lats = np.linspace(-90, 90, 50)
        for i, lat_val in enumerate(lats):
            graticule_data.append(
                {"type": "meridian", "group": f"lon_{lon_val}", "lon": lon_val, "lat": lat_val, "order": i}
            )

    # Latitude lines (parallels) every 30 degrees
    for lat_val in range(-60, 61, 30):
        lons = np.linspace(-180, 180, 100)
        for i, lon_val in enumerate(lons):
            graticule_data.append(
                {"type": "parallel", "group": f"lat_{lat_val}", "lon": lon_val, "lat": lat_val, "order": i}
            )

    return pd.DataFrame(graticule_data)


# Get continent and graticule data
df_continents = get_continent_data()
df_graticule = generate_graticule()

# Define projections to display
projections = [
    ("Equirectangular", equirectangular),
    ("Mercator", mercator),
    ("Robinson", robinson),
    ("Mollweide", mollweide),
]

# Apply all projections to continents
continent_frames = []
for proj_name, proj_func in projections:
    continent_frames.append(apply_projection(df_continents, proj_func, proj_name))
df_all_continents = pd.concat(continent_frames, ignore_index=True)

# Apply all projections to graticule
graticule_frames = []
for proj_name, proj_func in projections:
    graticule_frames.append(apply_projection(df_graticule, proj_func, proj_name))
df_all_graticule = pd.concat(graticule_frames, ignore_index=True)

# Create a unique group identifier for each graticule line per projection
df_all_graticule["proj_group"] = df_all_graticule["projection"] + "_" + df_all_graticule["group"]

# Create a unique group for continents per projection
df_all_continents["proj_continent"] = df_all_continents["projection"] + "_" + df_all_continents["continent"]

# Set projection as ordered categorical for consistent facet ordering
proj_order = ["Equirectangular", "Mercator", "Robinson", "Mollweide"]
df_all_continents["projection"] = pd.Categorical(df_all_continents["projection"], categories=proj_order, ordered=True)
df_all_graticule["projection"] = pd.Categorical(df_all_graticule["projection"], categories=proj_order, ordered=True)

# Create the multi-panel projection comparison plot
plot = (
    ggplot()
    # Draw graticule (grid lines) first
    + geom_path(aes(x="x", y="y", group="proj_group"), data=df_all_graticule, color="#B0C4DE", size=0.3, alpha=0.7)
    # Draw continent polygons on top
    + geom_polygon(
        aes(x="x", y="y", group="proj_continent"),
        data=df_all_continents,
        fill="#306998",
        color="#1a3a52",
        size=0.5,
        alpha=0.85,
    )
    # Facet by projection type
    + facet_wrap("~projection", ncol=2, scales="free")
    + coord_fixed(ratio=1.0)
    + labs(
        title="map-projections · plotnine · pyplots.ai",
        subtitle="Comparison of cartographic projections: Equirectangular, Mercator, Robinson, and Mollweide",
    )
    + theme(
        figure_size=(16, 9),
        plot_title=element_text(size=28, weight="bold", ha="center"),
        plot_subtitle=element_text(size=18, ha="center", color="#555555"),
        strip_text=element_text(size=20, weight="bold"),
        strip_background=element_rect(fill="#f0f0f0"),
        axis_text=element_blank(),
        axis_title=element_blank(),
        axis_ticks=element_blank(),
        panel_grid=element_blank(),
        panel_background=element_rect(fill="#E8F4F8"),
        plot_background=element_rect(fill="white"),
        legend_position="none",
    )
)

# Save the plot
plot.save("plot.png", dpi=300, verbose=False)
