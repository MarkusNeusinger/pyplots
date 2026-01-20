""" pyplots.ai
map-tile-background: Map with Tile Background
Library: letsplot 4.8.2 | Python 3.13.11
Quality: 72/100 | Created: 2026-01-20
"""

import numpy as np
import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    coord_fixed,
    element_blank,
    element_line,
    element_rect,
    element_text,
    geom_livemap,
    geom_point,
    geom_polygon,
    ggplot,
    ggsize,
    labs,
    layer_tooltips,
    scale_color_gradient,
    scale_size,
    theme,
    theme_minimal,
    tilesets,
)
from lets_plot.export import ggsave


LetsPlot.setup_html()

# Data: European city landmarks with annual visitor counts (thousands)
np.random.seed(42)

cities_data = {
    "city": [
        "Paris",
        "London",
        "Berlin",
        "Rome",
        "Madrid",
        "Amsterdam",
        "Vienna",
        "Prague",
        "Barcelona",
        "Munich",
        "Brussels",
        "Zurich",
        "Milan",
        "Dublin",
        "Copenhagen",
        "Stockholm",
        "Oslo",
        "Helsinki",
        "Warsaw",
        "Budapest",
    ],
    "lat": [
        48.86,
        51.51,
        52.52,
        41.90,
        40.42,
        52.37,
        48.21,
        50.08,
        41.39,
        48.14,
        50.85,
        47.38,
        45.46,
        53.35,
        55.68,
        59.33,
        59.91,
        60.17,
        52.23,
        47.50,
    ],
    "lon": [
        2.35,
        -0.13,
        13.40,
        12.50,
        -3.70,
        4.90,
        16.37,
        14.44,
        2.17,
        11.58,
        4.35,
        8.54,
        9.19,
        -6.26,
        12.57,
        18.07,
        10.75,
        24.94,
        21.01,
        19.04,
    ],
    "visitors": [
        38000,
        32000,
        14000,
        17000,
        12000,
        9000,
        8000,
        9500,
        12000,
        8500,
        5500,
        4000,
        8000,
        6000,
        4500,
        5000,
        3500,
        3000,
        4000,
        5500,
    ],
}

df = pd.DataFrame(cities_data)

# Simplified Europe continent outline for basemap context (for PNG export)
europe_outline = pd.DataFrame(
    {
        "lon": [-10, -9, -5, 0, 5, 10, 15, 20, 25, 30, 35, 35, 30, 25, 20, 15, 10, 5, 0, -5, -10],
        "lat": [36, 43, 48, 50, 52, 55, 58, 60, 62, 65, 70, 55, 50, 45, 42, 40, 38, 36, 36, 36, 36],
        "region": ["Europe"] * 21,
        "order": list(range(21)),
    }
)

# Scandinavia outline
scandinavia_outline = pd.DataFrame(
    {
        "lon": [5, 8, 10, 15, 20, 25, 30, 28, 22, 18, 12, 8, 5],
        "lat": [58, 58, 60, 62, 65, 68, 70, 62, 58, 55, 56, 58, 58],
        "region": ["Scandinavia"] * 13,
        "order": list(range(13)),
    }
)

# British Isles outline
british_isles = pd.DataFrame(
    {
        "lon": [-10, -8, -5, -3, 0, 2, 1, -1, -3, -5, -8, -10],
        "lat": [50, 55, 58, 59, 55, 52, 50, 50, 50, 49, 50, 50],
        "region": ["British_Isles"] * 12,
        "order": list(range(12)),
    }
)

# Ireland outline
ireland = pd.DataFrame(
    {
        "lon": [-10, -9, -7, -6, -7, -9, -10],
        "lat": [52, 54, 55, 53, 51, 51, 52],
        "region": ["Ireland"] * 7,
        "order": list(range(7)),
    }
)

df_basemap = pd.concat([europe_outline, scandinavia_outline, british_isles, ireland], ignore_index=True)

# Create map with styled basemap that simulates tile appearance
# Using polygon-based approach for reliable PNG export
plot = (
    ggplot()
    # Basemap layers for geographic context (styled to resemble tile backgrounds)
    + geom_polygon(
        aes(x="lon", y="lat", group="region"), data=df_basemap, fill="#E8E8E8", color="#B0B0B0", size=0.5, alpha=0.9
    )
    # Data points layer with visitor encoding
    + geom_point(
        aes(x="lon", y="lat", color="visitors", size="visitors"),
        data=df,
        alpha=0.85,
        shape=21,
        fill="white",
        stroke=1.2,
        tooltips=layer_tooltips().title("@city").line("Visitors|@visitors K/year"),
    )
    + scale_color_gradient(low="#306998", high="#FFD43B", name="Visitors (K)")
    + scale_size(range=[5, 16], name="Visitors (K)")
    + labs(x="Longitude", y="Latitude", title="European Tourism · map-tile-background · letsplot · pyplots.ai")
    + coord_fixed(ratio=1.0, xlim=[-12, 32], ylim=[35, 72])
    + ggsize(1600, 900)
    + theme_minimal()
    + theme(
        plot_title=element_text(size=24, face="bold"),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        legend_title=element_text(size=16),
        legend_text=element_text(size=14),
        legend_position="right",
        panel_grid_major=element_line(color="#D0D0D0", size=0.3),
        panel_grid_minor=element_blank(),
        panel_background=element_rect(fill="#F5F5F5"),
        plot_background=element_rect(fill="#FAFAFA"),
    )
)

# Save PNG (scale 3x for 4800 x 2700 px)
ggsave(plot, "plot.png", path=".", scale=3)

# For HTML, create interactive version with actual tile background
# geom_livemap provides real OpenStreetMap tiles in the interactive view
plot_interactive = (
    ggplot(df, aes(x="lon", y="lat"))
    + geom_livemap(
        zoom=4,
        location=[10, 52],  # Center on Europe
        tiles=tilesets.CARTO_POSITRON,  # Clean, light tile style
    )
    + geom_point(
        aes(color="visitors", size="visitors"),
        alpha=0.85,
        shape=21,
        fill="white",
        stroke=1.2,
        tooltips=layer_tooltips().title("@city").line("Visitors|@visitors K/year"),
    )
    + scale_color_gradient(low="#306998", high="#FFD43B", name="Visitors (K)")
    + scale_size(range=[5, 16], name="Visitors (K)")
    + labs(title="European Tourism · map-tile-background · letsplot · pyplots.ai")
    + ggsize(1600, 900)
    + theme(
        plot_title=element_text(size=24, face="bold"),
        legend_title=element_text(size=16),
        legend_text=element_text(size=14),
        plot_inset=0,
    )
)

# Save HTML with interactive tile background
ggsave(plot_interactive, "plot.html", path=".")
