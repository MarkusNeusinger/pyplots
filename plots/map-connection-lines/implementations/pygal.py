"""pyplots.ai
map-connection-lines: Connection Lines Map (Origin-Destination)
Library: pygal | Python 3.13
Quality: pending | Created: 2026-01-21
"""

# Fix module name conflict (this file is named pygal.py)
import sys


_cwd = sys.path[0] if sys.path and sys.path[0] else None
if _cwd:
    sys.path.remove(_cwd)

import numpy as np  # noqa: E402
import pygal  # noqa: E402
from pygal.style import Style  # noqa: E402


if _cwd:
    sys.path.insert(0, _cwd)


# Data - Major international flight routes with passenger volumes (thousands/year)
np.random.seed(42)

# Major world airports with coordinates
airports = {
    "JFK": (40.64, -73.78, "New York"),
    "LAX": (33.94, -118.41, "Los Angeles"),
    "LHR": (51.47, -0.46, "London"),
    "CDG": (49.01, 2.55, "Paris"),
    "DXB": (25.25, 55.36, "Dubai"),
    "HND": (35.55, 139.78, "Tokyo"),
    "SIN": (1.36, 103.99, "Singapore"),
    "SYD": (-33.95, 151.18, "Sydney"),
    "HKG": (22.31, 113.91, "Hong Kong"),
    "FRA": (50.03, 8.57, "Frankfurt"),
    "ORD": (41.98, -87.90, "Chicago"),
    "PEK": (40.08, 116.58, "Beijing"),
    "GRU": (-23.43, -46.47, "Sao Paulo"),
    "JNB": (-26.13, 28.23, "Johannesburg"),
}

# Flight routes with passenger volumes (in thousands)
routes = [
    ("JFK", "LHR", 4200),
    ("JFK", "CDG", 2100),
    ("LAX", "HND", 3500),
    ("LAX", "SYD", 1800),
    ("LHR", "DXB", 3800),
    ("LHR", "HKG", 2900),
    ("LHR", "JFK", 4200),
    ("CDG", "JFK", 2100),
    ("DXB", "SIN", 3200),
    ("DXB", "LHR", 3800),
    ("HND", "SIN", 2400),
    ("HND", "LAX", 3500),
    ("SIN", "SYD", 2800),
    ("SIN", "HKG", 3100),
    ("HKG", "LHR", 2900),
    ("HKG", "SIN", 3100),
    ("FRA", "JFK", 2600),
    ("FRA", "DXB", 2200),
    ("ORD", "LHR", 2800),
    ("ORD", "FRA", 1900),
    ("PEK", "LAX", 2300),
    ("PEK", "FRA", 1700),
    ("GRU", "JFK", 1500),
    ("GRU", "LHR", 1200),
    ("JNB", "DXB", 1400),
    ("JNB", "LHR", 1100),
    ("SYD", "LAX", 1800),
    ("SYD", "SIN", 2800),
]

# Process route data
route_data = []
for origin, dest, volume in routes:
    o_lat, o_lon, o_city = airports[origin]
    d_lat, d_lon, d_city = airports[dest]
    route_data.append(
        {
            "origin_lat": o_lat,
            "origin_lon": o_lon,
            "dest_lat": d_lat,
            "dest_lon": d_lon,
            "volume": volume,
            "origin_city": o_city,
            "dest_city": d_city,
        }
    )

# Simplified world coastlines for geographic context
coastlines = [
    # North America
    [
        (-125, 50),
        (-141, 60),
        (-165, 55),
        (-148, 60),
        (-130, 55),
        (-120, 49),
        (-95, 49),
        (-80, 45),
        (-67, 45),
        (-75, 35),
        (-81, 25),
        (-90, 30),
        (-97, 26),
        (-110, 32),
        (-125, 50),
    ],
    # South America
    [(-78, 10), (-60, 8), (-35, -6), (-42, -23), (-66, -55), (-72, -30), (-78, 10)],
    # Europe/Africa
    [(-10, 36), (10, 37), (30, 31), (42, 14), (35, -22), (17, -30), (0, 6), (-17, 14), (-10, 36)],
    # Northern Europe
    [(-6, 50), (5, 58), (28, 70), (24, 55), (3, 51), (-6, 50)],
    # Asia
    [(28, 70), (100, 77), (170, 60), (120, 32), (100, 14), (72, 25), (40, 46), (28, 70)],
    # India/SE Asia
    [(78, 33), (72, 8), (88, 22), (104, 2), (78, 33)],
    # Japan
    [(130, 32), (145, 44), (130, 32)],
    # Australia
    [(113, -22), (150, -23), (140, -38), (113, -22)],
]

# Custom style for 4800x2700 canvas
custom_style = Style(
    background="white",
    plot_background="#E8F4F8",  # Light ocean blue
    foreground="#333333",
    foreground_strong="#111111",
    foreground_subtle="#666666",
    guide_stroke_color="#88888844",
    guide_stroke_dasharray="4,4",
    colors=(
        # Coastline gray
        "#AAAAAA",
        # Route volume categories (low to high): teal, gold, red-orange
        "#1F9E89",
        "#FFD43B",
        "#E24A33",
        # Airport markers
        "#306998",
    ),
    opacity=0.6,
    opacity_hover=0.9,
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=40,
    legend_font_size=40,
    value_font_size=36,
    tooltip_font_size=36,
)

# Create XY chart
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="map-connection-lines · pygal · pyplots.ai",
    x_title="Longitude (°)",
    y_title="Latitude (°)",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=5,
    legend_box_size=30,
    stroke=True,
    dots_size=3,
    show_x_guides=True,
    show_y_guides=True,
    explicit_size=True,
    print_values=False,
    xrange=(-180, 180),
    range=(-60, 80),
    margin=80,
    margin_top=160,
    margin_bottom=200,
)

# Add coastlines as background
coastline_points = []
for coastline in coastlines:
    for lon, lat in coastline:
        coastline_points.append({"value": (lon, lat), "label": "Coastline"})
    coastline_points.append({"value": (None, None)})  # Break between segments

chart.add("Coastlines", coastline_points, stroke=True, show_dots=False, stroke_style={"width": 2})


# Function to create curved path between two points (great circle approximation)
def create_arc_points(o_lat, o_lon, d_lat, d_lon, n_segments=20):
    """Create curved path points between origin and destination."""
    points = []

    # Calculate midpoint and perpendicular offset for curve
    mid_lon = (o_lon + d_lon) / 2
    mid_lat = (o_lat + d_lat) / 2

    # Vector from origin to destination
    dx = d_lon - o_lon
    dy = d_lat - o_lat
    length = np.sqrt(dx * dx + dy * dy)

    if length > 0:
        # Perpendicular direction for curve offset
        perp_x = -dy / length
        perp_y = dx / length
        # Offset proportional to distance (more curve for longer routes)
        offset_amount = min(length * 0.15, 20.0)
        ctrl_lon = mid_lon + perp_x * offset_amount
        ctrl_lat = mid_lat + perp_y * offset_amount
    else:
        ctrl_lon, ctrl_lat = mid_lon, mid_lat

    # Generate quadratic Bezier curve points
    for i in range(n_segments + 1):
        t = i / n_segments
        lon = (1 - t) ** 2 * o_lon + 2 * (1 - t) * t * ctrl_lon + t**2 * d_lon
        lat = (1 - t) ** 2 * o_lat + 2 * (1 - t) * t * ctrl_lat + t**2 * d_lat
        points.append((lon, lat))

    return points


# Group routes by volume for different line styles
low_routes = []  # < 2000
medium_routes = []  # 2000-3000
high_routes = []  # > 3000

for route in route_data:
    if route["volume"] < 2000:
        low_routes.append(route)
    elif route["volume"] <= 3000:
        medium_routes.append(route)
    else:
        high_routes.append(route)

# Add low volume routes
low_curves = []
for route in low_routes:
    arc_points = create_arc_points(route["origin_lat"], route["origin_lon"], route["dest_lat"], route["dest_lon"])
    label = f"{route['origin_city']} → {route['dest_city']}: {route['volume']}K passengers"
    for lon, lat in arc_points:
        low_curves.append({"value": (lon, lat), "label": label})
    low_curves.append({"value": (None, None)})

chart.add("Routes < 2M", low_curves, stroke=True, show_dots=False, stroke_style={"width": 3, "linecap": "round"})

# Add medium volume routes
medium_curves = []
for route in medium_routes:
    arc_points = create_arc_points(route["origin_lat"], route["origin_lon"], route["dest_lat"], route["dest_lon"])
    label = f"{route['origin_city']} → {route['dest_city']}: {route['volume']}K passengers"
    for lon, lat in arc_points:
        medium_curves.append({"value": (lon, lat), "label": label})
    medium_curves.append({"value": (None, None)})

chart.add("Routes 2-3M", medium_curves, stroke=True, show_dots=False, stroke_style={"width": 6, "linecap": "round"})

# Add high volume routes
high_curves = []
for route in high_routes:
    arc_points = create_arc_points(route["origin_lat"], route["origin_lon"], route["dest_lat"], route["dest_lon"])
    label = f"{route['origin_city']} → {route['dest_city']}: {route['volume']}K passengers"
    for lon, lat in arc_points:
        high_curves.append({"value": (lon, lat), "label": label})
    high_curves.append({"value": (None, None)})

chart.add("Routes > 3M", high_curves, stroke=True, show_dots=False, stroke_style={"width": 10, "linecap": "round"})

# Add airport markers as endpoint layer
airport_points = []
for code, (lat, lon, city) in airports.items():
    airport_points.append({"value": (lon, lat), "label": f"{city} ({code})"})

chart.add("Airports", airport_points, stroke=False, dots_size=20)

# Save outputs
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
