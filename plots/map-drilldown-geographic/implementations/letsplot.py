"""pyplots.ai
map-drilldown-geographic: Drillable Geographic Map
Library: letsplot | Python 3.13
Quality: pending | Created: 2026-01-20
"""

import json

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
        "name": "United Kingdom",
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

# Prepare country data for static bubble map
country_ids = hierarchy_data["world"]["children"]
countries_data = []
for cid in country_ids:
    c = hierarchy_data[cid]
    countries_data.append(
        {
            "name": c["name"],
            "lon": c["lon"],
            "lat": c["lat"],
            "value": c["value"],
            "value_millions": c["value"] / 1_000_000,
            "has_children": len(c.get("children", [])) > 0,
        }
    )

df = pd.DataFrame(countries_data)

# Create static bubble map for PNG
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
    )
    # Bubble markers for countries - sized and colored by value
    + geom_point(
        data=df,
        mapping=aes(x="lon", y="lat", size="value_millions", fill="value_millions"),
        color="#1a3d5c",
        alpha=0.85,
        shape=21,
        stroke=1.5,
    )
    # Country labels
    + geom_text(
        data=df, mapping=aes(x="lon", y="lat", label="name"), size=10, color="#333333", nudge_y=-8, fontface="bold"
    )
    # Scales
    + scale_size(range=[8, 25], name="Sales\n(Millions $)")
    + scale_fill_gradient(low="#FFD43B", high="#306998", name="Sales\n(Millions $)")
    # Coordinate and labels
    + coord_fixed(ratio=1.3, xlim=[-180, 180], ylim=[-60, 75])
    + labs(
        title="map-drilldown-geographic · letsplot · pyplots.ai", subtitle="Global Sales · Click to drill down (HTML)"
    )
    + ggsize(1600, 900)
    + theme_void()
    + theme(
        plot_title=element_text(size=28, face="bold", hjust=0.5),
        plot_subtitle=element_text(size=18, hjust=0.5, color="#666666"),
        legend_title=element_text(size=16),
        legend_text=element_text(size=14),
        legend_position=[0.92, 0.25],
        plot_background=element_rect(fill="#f0f4f8"),
    )
)

# Save static PNG (scale 3x for 4800 × 2700 px)
export_ggsave(plot, "plot.png", path=".", scale=3)

# Color interpolation for HTML
color_low = (255, 212, 59)  # #FFD43B
color_high = (48, 105, 152)  # #306998


def value_to_color(value, min_val, max_val):
    """Map a value to a color between low and high."""
    if max_val == min_val:
        t = 0.5
    else:
        t = (value - min_val) / (max_val - min_val)
    r = int(color_low[0] + t * (color_high[0] - color_low[0]))
    g = int(color_low[1] + t * (color_high[1] - color_low[1]))
    b = int(color_low[2] + t * (color_high[2] - color_low[2]))
    return f"#{r:02x}{g:02x}{b:02x}"


# Prepare levels data for JavaScript
levels_data = {}

# World level
world_data = hierarchy_data["world"]
child_ids = world_data["children"]
child_items = [hierarchy_data[cid] for cid in child_ids]
values = [item["value"] for item in child_items]
min_val, max_val = min(values), max(values)
levels_data["world"] = {
    "name": "World",
    "level": "world",
    "bounds": {"lat_min": -60, "lat_max": 70, "lon_min": -180, "lon_max": 180},
    "items": [
        {
            "id": item["id"],
            "name": item["name"],
            "value": item["value"],
            "lat": item.get("lat", 0),
            "lon": item.get("lon", 0),
            "has_children": len(item.get("children", [])) > 0,
            "color": value_to_color(item["value"], min_val, max_val),
        }
        for item in child_items
    ],
}

# Country levels (USA, Canada)
for country_id in ["usa", "canada"]:
    country = hierarchy_data[country_id]
    if not country.get("children"):
        continue
    child_ids = country["children"]
    child_items = [hierarchy_data[cid] for cid in child_ids]
    values = [item["value"] for item in child_items]
    min_val, max_val = min(values), max(values)

    lats = [item.get("lat", 0) for item in child_items]
    lons = [item.get("lon", 0) for item in child_items]

    if country_id == "usa":
        bounds = {"lat_min": 24, "lat_max": 50, "lon_min": -125, "lon_max": -66}
    else:
        bounds = {"lat_min": 42, "lat_max": 70, "lon_min": -140, "lon_max": -52}

    levels_data[country_id] = {
        "name": country["name"],
        "level": "country",
        "parent": "world",
        "bounds": bounds,
        "items": [
            {
                "id": item["id"],
                "name": item["name"],
                "value": item["value"],
                "lat": item.get("lat", 0),
                "lon": item.get("lon", 0),
                "has_children": len(item.get("children", [])) > 0,
                "color": value_to_color(item["value"], min_val, max_val),
            }
            for item in child_items
        ],
    }

# State levels
for state_id in ["california", "texas", "new_york", "florida", "illinois", "ontario", "quebec", "british_columbia"]:
    state = hierarchy_data[state_id]
    if not state.get("children"):
        continue
    child_ids = state["children"]
    child_items = [hierarchy_data[cid] for cid in child_ids]
    values = [item["value"] for item in child_items]
    min_val, max_val = min(values), max(values)

    lats = [item.get("lat", 0) for item in child_items]
    lons = [item.get("lon", 0) for item in child_items]

    lat_padding = max((max(lats) - min(lats)) * 0.3, 2)
    lon_padding = max((max(lons) - min(lons)) * 0.3, 3)

    levels_data[state_id] = {
        "name": state["name"],
        "level": "state",
        "parent": state["parent"],
        "bounds": {
            "lat_min": min(lats) - lat_padding,
            "lat_max": max(lats) + lat_padding,
            "lon_min": min(lons) - lon_padding,
            "lon_max": max(lons) + lon_padding,
        },
        "items": [
            {
                "id": item["id"],
                "name": item["name"],
                "value": item["value"],
                "lat": item.get("lat", 0),
                "lon": item.get("lon", 0),
                "has_children": False,
                "color": value_to_color(item["value"], min_val, max_val),
            }
            for item in child_items
        ],
    }

# HTML template with interactive map
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>map-drilldown-geographic · letsplot · pyplots.ai</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }}
        .container {{
            background: white;
            border-radius: 16px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            padding: 30px;
            max-width: 1100px;
            width: 100%;
        }}
        h1 {{
            color: #333;
            text-align: center;
            font-size: 26px;
            margin-bottom: 6px;
        }}
        .subtitle {{
            color: #666;
            text-align: center;
            font-size: 15px;
            margin-bottom: 20px;
        }}
        .breadcrumb {{
            background: #306998;
            color: white;
            padding: 12px 18px;
            border-radius: 10px;
            margin-bottom: 20px;
            font-size: 16px;
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        .back-btn {{
            background: #FFD43B;
            color: #333;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .back-btn:hover {{
            background: #E6BE35;
            transform: translateX(-2px);
        }}
        .back-btn:disabled {{
            opacity: 0.4;
            cursor: not-allowed;
            transform: none;
        }}
        .breadcrumb-path {{
            display: flex;
            align-items: center;
            gap: 8px;
            flex-wrap: wrap;
        }}
        .breadcrumb-path span {{
            cursor: pointer;
            transition: opacity 0.2s;
        }}
        .breadcrumb-path span:hover:not(.current) {{
            text-decoration: underline;
            opacity: 0.9;
        }}
        .breadcrumb-path .separator {{
            opacity: 0.6;
        }}
        .breadcrumb-path .current {{
            font-weight: 600;
            cursor: default;
        }}
        #map {{
            height: 500px;
            border-radius: 10px;
            overflow: hidden;
            border: 1px solid #ddd;
        }}
        .legend {{
            background: white;
            padding: 12px 16px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.15);
            line-height: 1.6;
        }}
        .legend-title {{
            font-weight: 600;
            margin-bottom: 8px;
            color: #333;
        }}
        .legend-bar {{
            width: 120px;
            height: 14px;
            background: linear-gradient(to right, #FFD43B, #306998);
            border-radius: 3px;
        }}
        .legend-labels {{
            display: flex;
            justify-content: space-between;
            font-size: 11px;
            color: #666;
            margin-top: 4px;
        }}
        .total-display {{
            text-align: center;
            margin-top: 18px;
            font-size: 18px;
            color: #333;
        }}
        .total-display .amount {{
            font-weight: 700;
            color: #306998;
            font-size: 24px;
        }}
        .hint {{
            text-align: center;
            color: #888;
            margin-top: 14px;
            font-size: 13px;
        }}
        .marker-label {{
            background: rgba(255, 255, 255, 0.95);
            border: none;
            border-radius: 4px;
            padding: 4px 8px;
            font-size: 12px;
            font-weight: 600;
            white-space: nowrap;
            box-shadow: 0 2px 6px rgba(0,0,0,0.15);
        }}
        .leaflet-popup-content-wrapper {{
            border-radius: 10px;
        }}
        .popup-content {{
            padding: 8px 4px;
        }}
        .popup-content h3 {{
            margin: 0 0 8px 0;
            color: #306998;
            font-size: 16px;
        }}
        .popup-content .value {{
            font-size: 20px;
            font-weight: 700;
            color: #333;
        }}
        .popup-content .drill-hint {{
            margin-top: 8px;
            font-size: 12px;
            color: #666;
            font-style: italic;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>map-drilldown-geographic · letsplot · pyplots.ai</h1>
        <p class="subtitle">Sales by Region · Click markers to drill down</p>

        <div class="breadcrumb">
            <button class="back-btn" id="backBtn" disabled>← Back</button>
            <div class="breadcrumb-path" id="breadcrumb-path">
                <span class="current">World</span>
            </div>
        </div>

        <div id="map"></div>

        <div class="total-display">
            Level Total: <span class="amount" id="total-amount">$16,520,000</span>
        </div>

        <p class="hint" id="hint">Click on a marker to drill down to states/provinces</p>
    </div>

    <script>
        const levelsData = {json.dumps(levels_data)};
        const hierarchyData = {json.dumps(hierarchy_data)};

        let currentLevel = 'world';
        let history = [];
        let map;
        let markersLayer;

        // Initialize map
        function initMap() {{
            map = L.map('map', {{
                worldCopyJump: true,
                maxBoundsViscosity: 1.0
            }}).setView([30, 0], 2);

            L.tileLayer('https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
                attribution: '&copy; OpenStreetMap &copy; CARTO',
                subdomains: 'abcd',
                maxZoom: 19
            }}).addTo(map);

            // Add legend
            const legend = L.control({{position: 'bottomright'}});
            legend.onAdd = function() {{
                const div = L.DomUtil.create('div', 'legend');
                div.innerHTML = `
                    <div class="legend-title">Sales Value</div>
                    <div class="legend-bar"></div>
                    <div class="legend-labels">
                        <span>Low</span>
                        <span>High</span>
                    </div>
                `;
                return div;
            }};
            legend.addTo(map);

            markersLayer = L.layerGroup().addTo(map);
            renderLevel('world');
        }}

        function renderLevel(levelId) {{
            const data = levelsData[levelId];
            if (!data) return;

            markersLayer.clearLayers();

            // Fit bounds with animation
            const bounds = data.bounds;
            map.flyToBounds([
                [bounds.lat_min, bounds.lon_min],
                [bounds.lat_max, bounds.lon_max]
            ], {{
                padding: [30, 30],
                duration: 0.8
            }});

            // Add markers for each item
            data.items.forEach(item => {{
                const maxVal = Math.max(...data.items.map(i => i.value));
                const minVal = Math.min(...data.items.map(i => i.value));
                const normalizedSize = minVal === maxVal ? 0.5 :
                    (item.value - minVal) / (maxVal - minVal);
                const radius = 15 + normalizedSize * 25;

                const marker = L.circleMarker([item.lat, item.lon], {{
                    radius: radius,
                    fillColor: item.color,
                    color: '#333',
                    weight: 2,
                    opacity: 1,
                    fillOpacity: 0.85
                }});

                const popupContent = `
                    <div class="popup-content">
                        <h3>${{item.name}}</h3>
                        <div class="value">${{formatCurrency(item.value)}}</div>
                        ${{item.has_children ? '<div class="drill-hint">Click to drill down</div>' : ''}}
                    </div>
                `;
                marker.bindPopup(popupContent);

                marker.on('click', function() {{
                    if (item.has_children && levelsData[item.id]) {{
                        drillDown(item.id);
                    }}
                }});

                marker.on('mouseover', function() {{
                    this.setStyle({{
                        weight: 3,
                        fillOpacity: 1
                    }});
                    this.openPopup();
                }});

                marker.on('mouseout', function() {{
                    this.setStyle({{
                        weight: 2,
                        fillOpacity: 0.85
                    }});
                }});

                markersLayer.addLayer(marker);

                if (radius > 20) {{
                    const label = L.marker([item.lat, item.lon], {{
                        icon: L.divIcon({{
                            className: 'marker-label',
                            html: item.name,
                            iconSize: null
                        }})
                    }});
                    markersLayer.addLayer(label);
                }}
            }});

            const total = data.items.reduce((sum, item) => sum + item.value, 0);
            document.getElementById('total-amount').textContent = formatCurrency(total);

            const hint = document.getElementById('hint');
            const hasChildren = data.items.some(item => item.has_children);
            if (hasChildren) {{
                const levelName = data.level === 'world' ? 'states/provinces' :
                                  data.level === 'country' ? 'cities' : 'details';
                hint.textContent = `Click on a marker to drill down to ${{levelName}}`;
            }} else {{
                hint.textContent = 'Lowest level reached · Use breadcrumb to navigate back';
            }}
        }}

        function formatCurrency(value) {{
            return new Intl.NumberFormat('en-US', {{
                style: 'currency',
                currency: 'USD',
                minimumFractionDigits: 0,
                maximumFractionDigits: 0
            }}).format(value);
        }}

        function drillDown(targetId) {{
            if (levelsData[targetId]) {{
                history.push(currentLevel);
                currentLevel = targetId;
                updateBreadcrumb();
                renderLevel(currentLevel);
            }}
        }}

        function goBack() {{
            if (history.length > 0) {{
                currentLevel = history.pop();
                updateBreadcrumb();
                renderLevel(currentLevel);
            }}
        }}

        function updateBreadcrumb() {{
            const pathDiv = document.getElementById('breadcrumb-path');
            const fullPath = ['world', ...history];
            if (!fullPath.includes(currentLevel)) fullPath.push(currentLevel);

            let html = '';
            fullPath.forEach((id, index) => {{
                if (index > 0) html += '<span class="separator"> > </span>';
                const name = levelsData[id]?.name || hierarchyData[id]?.name || id;
                if (id === currentLevel) {{
                    html += `<span class="current">${{name}}</span>`;
                }} else {{
                    html += `<span onclick="navigateTo('${{id}}')">${{name}}</span>`;
                }}
            }});

            pathDiv.innerHTML = html;
            document.getElementById('backBtn').disabled = currentLevel === 'world';
        }}

        window.navigateTo = function(id) {{
            const idx = history.indexOf(id);
            if (idx >= 0) {{
                history = history.slice(0, idx);
            }} else {{
                history = [];
            }}
            currentLevel = id;
            updateBreadcrumb();
            renderLevel(currentLevel);
        }};

        document.getElementById('backBtn').addEventListener('click', goBack);

        initMap();
    </script>
</body>
</html>"""

with open("plot.html", "w") as f:
    f.write(html_content)
