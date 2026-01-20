""" pyplots.ai
map-drilldown-geographic: Drillable Geographic Map
Library: letsplot 4.8.2 | Python 3.13.11
Quality: 82/100 | Created: 2026-01-20
"""

import numpy as np
import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    coord_fixed,
    element_rect,
    element_text,
    geom_point,
    geom_polygon,
    geom_text,
    ggplot,
    ggsize,
    labs,
    layer_tooltips,
    scale_fill_gradient,
    scale_size,
    theme,
    theme_void,
)
from lets_plot.export import ggsave as export_ggsave


LetsPlot.setup_html()

np.random.seed(42)

# Hierarchical data: Sales by geography (Country > State > City)
hierarchy_data = {
    "world": {
        "id": "world",
        "name": "World",
        "level": "world",
        "children": ["usa", "canada", "mexico", "brazil", "uk", "germany", "france", "australia"],
    },
    "usa": {
        "id": "usa",
        "name": "United States",
        "level": "country",
        "parent": "world",
        "value": 4850000,
        "children": ["california", "texas", "new_york", "florida", "illinois"],
        "lat": 39.8,
        "lon": -98.5,
    },
    "canada": {
        "id": "canada",
        "name": "Canada",
        "level": "country",
        "parent": "world",
        "value": 1420000,
        "children": ["ontario", "quebec", "british_columbia"],
        "lat": 56.1,
        "lon": -106.3,
    },
    "mexico": {
        "id": "mexico",
        "name": "Mexico",
        "level": "country",
        "parent": "world",
        "value": 980000,
        "children": [],
        "lat": 23.6,
        "lon": -102.5,
    },
    "brazil": {
        "id": "brazil",
        "name": "Brazil",
        "level": "country",
        "parent": "world",
        "value": 1650000,
        "children": [],
        "lat": -14.2,
        "lon": -51.9,
    },
    "uk": {
        "id": "uk",
        "name": "UK",
        "level": "country",
        "parent": "world",
        "value": 2100000,
        "children": [],
        "lat": 55.4,
        "lon": -3.4,
    },
    "germany": {
        "id": "germany",
        "name": "Germany",
        "level": "country",
        "parent": "world",
        "value": 2350000,
        "children": [],
        "lat": 51.2,
        "lon": 10.5,
    },
    "france": {
        "id": "france",
        "name": "France",
        "level": "country",
        "parent": "world",
        "value": 1890000,
        "children": [],
        "lat": 46.2,
        "lon": 2.2,
    },
    "australia": {
        "id": "australia",
        "name": "Australia",
        "level": "country",
        "parent": "world",
        "value": 1280000,
        "children": [],
        "lat": -25.3,
        "lon": 133.8,
    },
    # US States
    "california": {
        "id": "california",
        "name": "California",
        "level": "state",
        "parent": "usa",
        "value": 1450000,
        "children": ["los_angeles", "san_francisco", "san_diego", "sacramento"],
        "lat": 36.8,
        "lon": -119.4,
    },
    "texas": {
        "id": "texas",
        "name": "Texas",
        "level": "state",
        "parent": "usa",
        "value": 1180000,
        "children": ["houston", "dallas", "austin", "san_antonio"],
        "lat": 31.0,
        "lon": -100.0,
    },
    "new_york": {
        "id": "new_york",
        "name": "New York",
        "level": "state",
        "parent": "usa",
        "value": 980000,
        "children": ["new_york_city", "buffalo", "albany"],
        "lat": 43.0,
        "lon": -75.5,
    },
    "florida": {
        "id": "florida",
        "name": "Florida",
        "level": "state",
        "parent": "usa",
        "value": 720000,
        "children": ["miami", "tampa", "orlando"],
        "lat": 27.7,
        "lon": -81.5,
    },
    "illinois": {
        "id": "illinois",
        "name": "Illinois",
        "level": "state",
        "parent": "usa",
        "value": 520000,
        "children": ["chicago", "springfield"],
        "lat": 40.0,
        "lon": -89.4,
    },
    # Canada Provinces
    "ontario": {
        "id": "ontario",
        "name": "Ontario",
        "level": "state",
        "parent": "canada",
        "value": 680000,
        "children": ["toronto", "ottawa"],
        "lat": 51.3,
        "lon": -85.3,
    },
    "quebec": {
        "id": "quebec",
        "name": "Quebec",
        "level": "state",
        "parent": "canada",
        "value": 420000,
        "children": ["montreal", "quebec_city"],
        "lat": 52.9,
        "lon": -73.5,
    },
    "british_columbia": {
        "id": "british_columbia",
        "name": "British Columbia",
        "level": "state",
        "parent": "canada",
        "value": 320000,
        "children": ["vancouver", "victoria"],
        "lat": 53.7,
        "lon": -127.6,
    },
    # California Cities
    "los_angeles": {
        "id": "los_angeles",
        "name": "Los Angeles",
        "level": "city",
        "parent": "california",
        "value": 580000,
        "lat": 34.05,
        "lon": -118.25,
    },
    "san_francisco": {
        "id": "san_francisco",
        "name": "San Francisco",
        "level": "city",
        "parent": "california",
        "value": 420000,
        "lat": 37.77,
        "lon": -122.42,
    },
    "san_diego": {
        "id": "san_diego",
        "name": "San Diego",
        "level": "city",
        "parent": "california",
        "value": 280000,
        "lat": 32.72,
        "lon": -117.16,
    },
    "sacramento": {
        "id": "sacramento",
        "name": "Sacramento",
        "level": "city",
        "parent": "california",
        "value": 170000,
        "lat": 38.58,
        "lon": -121.49,
    },
    # Texas Cities
    "houston": {
        "id": "houston",
        "name": "Houston",
        "level": "city",
        "parent": "texas",
        "value": 450000,
        "lat": 29.76,
        "lon": -95.37,
    },
    "dallas": {
        "id": "dallas",
        "name": "Dallas",
        "level": "city",
        "parent": "texas",
        "value": 380000,
        "lat": 32.78,
        "lon": -96.80,
    },
    "austin": {
        "id": "austin",
        "name": "Austin",
        "level": "city",
        "parent": "texas",
        "value": 210000,
        "lat": 30.27,
        "lon": -97.74,
    },
    "san_antonio": {
        "id": "san_antonio",
        "name": "San Antonio",
        "level": "city",
        "parent": "texas",
        "value": 140000,
        "lat": 29.42,
        "lon": -98.49,
    },
    # New York Cities
    "new_york_city": {
        "id": "new_york_city",
        "name": "New York City",
        "level": "city",
        "parent": "new_york",
        "value": 720000,
        "lat": 40.71,
        "lon": -74.01,
    },
    "buffalo": {
        "id": "buffalo",
        "name": "Buffalo",
        "level": "city",
        "parent": "new_york",
        "value": 160000,
        "lat": 42.89,
        "lon": -78.88,
    },
    "albany": {
        "id": "albany",
        "name": "Albany",
        "level": "city",
        "parent": "new_york",
        "value": 100000,
        "lat": 42.65,
        "lon": -73.75,
    },
    # Florida Cities
    "miami": {
        "id": "miami",
        "name": "Miami",
        "level": "city",
        "parent": "florida",
        "value": 340000,
        "lat": 25.76,
        "lon": -80.19,
    },
    "tampa": {
        "id": "tampa",
        "name": "Tampa",
        "level": "city",
        "parent": "florida",
        "value": 220000,
        "lat": 27.95,
        "lon": -82.46,
    },
    "orlando": {
        "id": "orlando",
        "name": "Orlando",
        "level": "city",
        "parent": "florida",
        "value": 160000,
        "lat": 28.54,
        "lon": -81.38,
    },
    # Illinois Cities
    "chicago": {
        "id": "chicago",
        "name": "Chicago",
        "level": "city",
        "parent": "illinois",
        "value": 420000,
        "lat": 41.88,
        "lon": -87.63,
    },
    "springfield": {
        "id": "springfield",
        "name": "Springfield",
        "level": "city",
        "parent": "illinois",
        "value": 100000,
        "lat": 39.78,
        "lon": -89.65,
    },
    # Canada Cities
    "toronto": {
        "id": "toronto",
        "name": "Toronto",
        "level": "city",
        "parent": "ontario",
        "value": 480000,
        "lat": 43.65,
        "lon": -79.38,
    },
    "ottawa": {
        "id": "ottawa",
        "name": "Ottawa",
        "level": "city",
        "parent": "ontario",
        "value": 200000,
        "lat": 45.42,
        "lon": -75.70,
    },
    "montreal": {
        "id": "montreal",
        "name": "Montreal",
        "level": "city",
        "parent": "quebec",
        "value": 320000,
        "lat": 45.50,
        "lon": -73.57,
    },
    "quebec_city": {
        "id": "quebec_city",
        "name": "Quebec City",
        "level": "city",
        "parent": "quebec",
        "value": 100000,
        "lat": 46.81,
        "lon": -71.21,
    },
    "vancouver": {
        "id": "vancouver",
        "name": "Vancouver",
        "level": "city",
        "parent": "british_columbia",
        "value": 240000,
        "lat": 49.28,
        "lon": -123.12,
    },
    "victoria": {
        "id": "victoria",
        "name": "Victoria",
        "level": "city",
        "parent": "british_columbia",
        "value": 80000,
        "lat": 48.43,
        "lon": -123.37,
    },
}

# Simplified continent outlines for background context
continent_rows = []

# North America outline
na_coords = [
    (-170, 66),
    (-165, 62),
    (-140, 60),
    (-130, 55),
    (-125, 48),
    (-124, 42),
    (-118, 34),
    (-105, 25),
    (-97, 26),
    (-85, 22),
    (-82, 23),
    (-80, 25),
    (-83, 30),
    (-88, 30),
    (-92, 29),
    (-97, 28),
    (-97, 24),
    (-92, 18),
    (-87, 15),
    (-82, 9),
    (-78, 9),
    (-75, 10),
    (-72, 12),
    (-62, 10),
    (-60, 14),
    (-62, 18),
    (-65, 18),
    (-67, 18),
    (-72, 21),
    (-75, 20),
    (-80, 23),
    (-80, 25),
    (-82, 30),
    (-76, 35),
    (-75, 38),
    (-72, 41),
    (-70, 44),
    (-67, 45),
    (-65, 48),
    (-70, 47),
    (-60, 47),
    (-55, 50),
    (-58, 52),
    (-63, 58),
    (-70, 60),
    (-85, 65),
    (-95, 68),
    (-110, 70),
    (-130, 70),
    (-145, 68),
    (-155, 70),
    (-165, 65),
    (-170, 66),
]
for lon, lat in na_coords:
    continent_rows.append({"lon": lon, "lat": lat, "continent": "North America"})

# South America outline
sa_coords = [
    (-80, 10),
    (-75, 10),
    (-70, 12),
    (-62, 10),
    (-60, 5),
    (-52, 4),
    (-50, 0),
    (-48, -2),
    (-44, -3),
    (-38, -5),
    (-35, -8),
    (-35, -15),
    (-38, -18),
    (-40, -22),
    (-43, -23),
    (-47, -25),
    (-48, -28),
    (-52, -33),
    (-58, -38),
    (-65, -42),
    (-68, -48),
    (-72, -52),
    (-68, -55),
    (-64, -55),
    (-58, -52),
    (-65, -45),
    (-70, -38),
    (-72, -30),
    (-70, -20),
    (-75, -15),
    (-81, -5),
    (-80, 0),
    (-78, 2),
    (-77, 8),
    (-80, 10),
]
for lon, lat in sa_coords:
    continent_rows.append({"lon": lon, "lat": lat, "continent": "South America"})

# Europe outline
europe_coords = [
    (-10, 36),
    (-8, 43),
    (0, 43),
    (3, 42),
    (8, 44),
    (13, 45),
    (14, 42),
    (19, 42),
    (25, 37),
    (28, 41),
    (40, 41),
    (50, 45),
    (55, 50),
    (60, 55),
    (50, 60),
    (60, 70),
    (25, 71),
    (15, 68),
    (5, 62),
    (10, 55),
    (8, 52),
    (-5, 50),
    (-10, 44),
    (-10, 36),
]
for lon, lat in europe_coords:
    continent_rows.append({"lon": lon, "lat": lat, "continent": "Europe"})

# Australia outline
aus_coords = [
    (115, -20),
    (120, -18),
    (128, -15),
    (130, -12),
    (135, -12),
    (137, -16),
    (140, -17),
    (142, -11),
    (145, -15),
    (148, -20),
    (153, -25),
    (153, -30),
    (151, -34),
    (147, -38),
    (143, -38),
    (138, -35),
    (130, -32),
    (125, -35),
    (118, -35),
    (114, -32),
    (114, -26),
    (115, -20),
]
for lon, lat in aus_coords:
    continent_rows.append({"lon": lon, "lat": lat, "continent": "Australia"})

continents = pd.DataFrame(continent_rows)

# Prepare country data for static bubble map with custom label positions
country_ids = hierarchy_data["world"]["children"]
countries_data = []

# Label offset adjustments to avoid overlap (nudge_x, nudge_y in degrees)
# Keep labels close to their bubbles while avoiding collisions
label_offsets = {
    "usa": (0, -8),  # Below bubble
    "canada": (15, 0),  # Right of bubble to avoid US proximity
    "mexico": (0, -8),  # Below bubble
    "brazil": (0, -10),  # Below bubble
    "uk": (-12, -8),  # Left and below to separate from Germany
    "germany": (12, 5),  # Right and up to separate from UK/France
    "france": (-15, -8),  # Left and below to separate from others
    "australia": (-35, 0),  # Left to avoid edge cutoff
}

for cid in country_ids:
    c = hierarchy_data[cid]
    nudge_x, nudge_y = label_offsets.get(cid, (0, -8))
    countries_data.append(
        {
            "name": c["name"],
            "lon": c["lon"],
            "lat": c["lat"],
            "value": c["value"],
            "value_millions": c["value"] / 1_000_000,
            "has_children": len(c.get("children", [])) > 0,
            "label_lon": c["lon"] + nudge_x,
            "label_lat": c["lat"] + nudge_y,
            "sales_formatted": f"${c['value'] / 1_000_000:.2f}M",
        }
    )

df = pd.DataFrame(countries_data)

# Create static bubble map for PNG with tooltips
# Use color gradient only (no size) for cleaner single-legend display
plot = (
    ggplot()
    # Continent outlines for geographic context
    + geom_polygon(
        data=continents,
        mapping=aes(x="lon", y="lat", group="continent"),
        fill="#E8E8E8",
        color="#CCCCCC",
        alpha=0.7,
        size=0.5,
        tooltips="none",
    )
    # Bubble markers for countries - single aesthetic (fill) for unified legend
    + geom_point(
        data=df,
        mapping=aes(x="lon", y="lat", size="value_millions", fill="value_millions"),
        color="#1a3d5c",
        alpha=0.85,
        shape=21,
        stroke=1.5,
        tooltips=layer_tooltips()
        .title("@name")
        .line("Sales|@sales_formatted")
        .line("Click to drill down (HTML version)"),
    )
    # Country labels at adjusted positions with smaller size for Europe
    + geom_text(
        data=df,
        mapping=aes(x="label_lon", y="label_lat", label="name"),
        size=10,
        color="#333333",
        fontface="bold",
        tooltips="none",
    )
    # Scales - hide size legend, only show color gradient
    + scale_size(range=[10, 28], guide="none")
    + scale_fill_gradient(low="#FFD43B", high="#306998", name="Sales (Millions $)")
    # Coordinate and labels - extend xlim to prevent Australia cutoff
    + coord_fixed(ratio=1.3, xlim=[-180, 200], ylim=[-60, 75])
    + labs(
        title="map-drilldown-geographic · letsplot · pyplots.ai",
        subtitle="Global Sales by Country · Drill-down available in HTML version",
    )
    + ggsize(1600, 900)
    + theme_void()
    + theme(
        plot_title=element_text(size=28, face="bold", hjust=0.5),
        plot_subtitle=element_text(size=18, hjust=0.5, color="#666666"),
        legend_title=element_text(size=16),
        legend_text=element_text(size=14),
        legend_position=[0.88, 0.18],
        plot_background=element_rect(fill="#f0f4f8"),
    )
)

# Save static PNG (scale 3x for 4800 × 2700 px)
export_ggsave(plot, "plot.png", path=".", scale=3)

# Save interactive HTML using lets-plot native export
export_ggsave(plot, "plot.html", path=".", iframe=False)
