"""pyplots.ai
map-tile-background: Map with Tile Background
Library: pygal 3.1.0 | Python 3.13
Quality: pending | Created: 2026-01-20
"""

import sys


# Fix module name conflict (this file is named pygal.py)
_cwd = sys.path[0] if sys.path and sys.path[0] else None
if _cwd:
    sys.path.remove(_cwd)

import numpy as np  # noqa: E402
from pygal.graph.graph import Graph  # noqa: E402
from pygal.style import Style  # noqa: E402


if _cwd:
    sys.path.insert(0, _cwd)


class TileBackgroundMap(Graph):
    """Custom map chart with simulated tile background for pygal.

    Since pygal doesn't support real tile providers (OpenStreetMap, etc.),
    this creates a geographic coordinate system with a styled background
    that simulates a tile-based map appearance, including grid lines,
    coastlines, and attribution.
    """

    def __init__(self, *args, **kwargs):
        self.point_data = kwargs.pop("point_data", [])
        self.lat_range = kwargs.pop("lat_range", (-90, 90))
        self.lon_range = kwargs.pop("lon_range", (-180, 180))
        self.coastlines = kwargs.pop("coastlines", [])
        self.tile_provider = kwargs.pop("tile_provider", "OpenStreetMap")
        super().__init__(*args, **kwargs)

    def _plot(self):
        """Draw the map with tile-like background and data points."""
        # Use explicit width/height from config
        plot_width = self.width
        plot_height = self.height

        # Layout margins for labels and attribution
        margin_left = 250
        margin_right = 180
        margin_top = 180
        margin_bottom = 350

        map_width = plot_width - margin_left - margin_right
        map_height = plot_height - margin_top - margin_bottom

        x_offset = margin_left
        y_offset = margin_top

        lat_min, lat_max = self.lat_range
        lon_min, lon_max = self.lon_range

        def lon_to_x(lon):
            return x_offset + (lon - lon_min) / (lon_max - lon_min) * map_width

        def lat_to_y(lat):
            return y_offset + (1 - (lat - lat_min) / (lat_max - lat_min)) * map_height

        plot_node = self.nodes["plot"]
        map_group = self.svg.node(plot_node, class_="tile-map")

        # Draw tile-like background (ocean blue with land areas)
        bg_rect = self.svg.node(map_group, "rect", x=x_offset, y=y_offset, width=map_width, height=map_height)
        bg_rect.set("fill", "#aad3df")  # OSM ocean blue
        bg_rect.set("stroke", "#666666")
        bg_rect.set("stroke-width", "2")

        # Draw grid lines (simulating map tiles)
        n_lon_lines = 9
        for i in range(n_lon_lines):
            lon = lon_min + (lon_max - lon_min) * i / (n_lon_lines - 1)
            x = lon_to_x(lon)
            line = self.svg.node(map_group, "line", x1=x, y1=y_offset, x2=x, y2=y_offset + map_height)
            line.set("stroke", "#ffffff")
            line.set("stroke-width", "1")
            line.set("stroke-opacity", "0.4")

        n_lat_lines = 7
        for i in range(n_lat_lines):
            lat = lat_min + (lat_max - lat_min) * i / (n_lat_lines - 1)
            y = lat_to_y(lat)
            line = self.svg.node(map_group, "line", x1=x_offset, y1=y, x2=x_offset + map_width, y2=y)
            line.set("stroke", "#ffffff")
            line.set("stroke-width", "1")
            line.set("stroke-opacity", "0.4")

        # Draw land masses (coastlines filled)
        for coastline in self.coastlines:
            if len(coastline) < 3:
                continue
            points = " ".join([f"{lon_to_x(lon)},{lat_to_y(lat)}" for lon, lat in coastline])
            polygon = self.svg.node(map_group, "polygon", points=points)
            polygon.set("fill", "#f2efe9")  # OSM land beige
            polygon.set("stroke", "#b5a08c")
            polygon.set("stroke-width", "2")

        # Draw data points with size encoding based on value
        if self.point_data:
            values = [p.get("value", 1) for p in self.point_data]
            min_val = min(values) if values else 0
            max_val = max(values) if values else 1
            val_range = max_val - min_val if max_val > min_val else 1

            for point in self.point_data:
                lon = point["lon"]
                lat = point["lat"]
                value = point.get("value", 1)
                label = point.get("label", "")

                cx = lon_to_x(lon)
                cy = lat_to_y(lat)

                # Scale radius based on value (20-60 pixels)
                normalized = (value - min_val) / val_range
                radius = 20 + normalized * 40

                # Draw outer ring for contrast
                outer = self.svg.node(map_group, "circle", cx=cx, cy=cy, r=radius + 3)
                outer.set("fill", "none")
                outer.set("stroke", "#ffffff")
                outer.set("stroke-width", "4")
                outer.set("stroke-opacity", "0.8")

                # Draw main marker
                circle = self.svg.node(map_group, "circle", cx=cx, cy=cy, r=radius)
                circle.set("fill", "#306998")  # Python blue
                circle.set("fill-opacity", "0.75")
                circle.set("stroke", "#1a3a5c")
                circle.set("stroke-width", "2")

                # Add tooltip title element
                if label:
                    title = self.svg.node(circle, "title")
                    title.text = f"{label}: {value:.0f}"

        # Draw axis labels
        axis_font_size = 48
        tick_font_size = 36

        # X-axis tick labels
        n_x_ticks = 7
        for i in range(n_x_ticks):
            lon = lon_min + (lon_max - lon_min) * i / (n_x_ticks - 1)
            x = lon_to_x(lon)
            text_node = self.svg.node(map_group, "text", x=x, y=y_offset + map_height + 60)
            text_node.set("text-anchor", "middle")
            text_node.set("fill", "#333333")
            text_node.set("style", f"font-size:{tick_font_size}px;font-family:sans-serif")
            text_node.text = f"{lon:.0f}°"

        # Y-axis tick labels
        n_y_ticks = 6
        for i in range(n_y_ticks):
            lat = lat_min + (lat_max - lat_min) * i / (n_y_ticks - 1)
            y = lat_to_y(lat)
            text_node = self.svg.node(map_group, "text", x=x_offset - 25, y=y + tick_font_size * 0.35)
            text_node.set("text-anchor", "end")
            text_node.set("fill", "#333333")
            text_node.set("style", f"font-size:{tick_font_size}px;font-family:sans-serif")
            text_node.text = f"{lat:.0f}°"

        # X-axis label (Longitude)
        text_node = self.svg.node(map_group, "text", x=x_offset + map_width / 2, y=y_offset + map_height + 160)
        text_node.set("text-anchor", "middle")
        text_node.set("fill", "#333333")
        text_node.set("style", f"font-size:{axis_font_size}px;font-weight:bold;font-family:sans-serif")
        text_node.text = "Longitude"

        # Y-axis label (Latitude)
        text_node = self.svg.node(map_group, "text", x=x_offset - 140, y=y_offset + map_height / 2)
        text_node.set("text-anchor", "middle")
        text_node.set("fill", "#333333")
        text_node.set("style", f"font-size:{axis_font_size}px;font-weight:bold;font-family:sans-serif")
        text_node.set("transform", f"rotate(-90, {x_offset - 140}, {y_offset + map_height / 2})")
        text_node.text = "Latitude"

        # Add tile provider attribution (required by OSM terms)
        attrib_font_size = 28
        attrib_text = self.svg.node(map_group, "text", x=x_offset + map_width - 10, y=y_offset + map_height - 15)
        attrib_text.set("text-anchor", "end")
        attrib_text.set("fill", "#666666")
        attrib_text.set("style", f"font-size:{attrib_font_size}px;font-family:sans-serif")
        attrib_text.text = f"© {self.tile_provider} style (simulated)"

        # Draw legend
        legend_x = x_offset + map_width - 350
        legend_y = y_offset + 40
        legend_font = 36

        # Legend title
        legend_title = self.svg.node(map_group, "text", x=legend_x, y=legend_y)
        legend_title.set("fill", "#333333")
        legend_title.set("style", f"font-size:{legend_font}px;font-weight:bold;font-family:sans-serif")
        legend_title.text = "Visitor Count"

        # Legend markers (small, medium, large)
        sizes = [(25, "Low"), (40, "Medium"), (55, "High")]
        for i, (size, lbl) in enumerate(sizes):
            cy = legend_y + 60 + i * 70
            cx = legend_x + 30

            # Marker
            marker = self.svg.node(map_group, "circle", cx=cx, cy=cy, r=size / 2)
            marker.set("fill", "#306998")
            marker.set("fill-opacity", "0.75")
            marker.set("stroke", "#1a3a5c")
            marker.set("stroke-width", "2")

            # Label
            label_node = self.svg.node(map_group, "text", x=cx + 45, y=cy + 10)
            label_node.set("fill", "#333333")
            label_node.set("style", f"font-size:{legend_font}px;font-family:sans-serif")
            label_node.text = lbl

    def _compute(self):
        """Compute the box for rendering."""
        self._box.xmin = 0
        self._box.xmax = 1
        self._box.ymin = 0
        self._box.ymax = 1


# Data: European city landmarks with visitor counts (thousands per year)
np.random.seed(42)

# Major European landmarks with coordinates and visitor data
landmarks = [
    {"label": "Eiffel Tower", "lat": 48.8584, "lon": 2.2945, "value": 7000},
    {"label": "Colosseum", "lat": 41.8902, "lon": 12.4922, "value": 6500},
    {"label": "Sagrada Familia", "lat": 41.4036, "lon": 2.1744, "value": 4500},
    {"label": "Big Ben", "lat": 51.5007, "lon": -0.1246, "value": 3500},
    {"label": "Brandenburg Gate", "lat": 52.5163, "lon": 13.3777, "value": 3000},
    {"label": "Acropolis", "lat": 37.9715, "lon": 23.7257, "value": 2900},
    {"label": "Anne Frank House", "lat": 52.3752, "lon": 4.8840, "value": 1300},
    {"label": "Prague Castle", "lat": 50.0911, "lon": 14.4008, "value": 2000},
    {"label": "Schonbrunn Palace", "lat": 48.1845, "lon": 16.3122, "value": 3800},
    {"label": "Rijksmuseum", "lat": 52.3600, "lon": 4.8852, "value": 2700},
    {"label": "Uffizi Gallery", "lat": 43.7677, "lon": 11.2553, "value": 2500},
    {"label": "Tower of London", "lat": 51.5081, "lon": -0.0759, "value": 2900},
    {"label": "Notre-Dame", "lat": 48.8530, "lon": 2.3499, "value": 5000},
    {"label": "Louvre Museum", "lat": 48.8606, "lon": 2.3376, "value": 9600},
    {"label": "Vatican Museums", "lat": 41.9065, "lon": 12.4536, "value": 6800},
]

# Simplified European coastlines (lon, lat pairs)
europe_coastlines = [
    # Iberian Peninsula
    [(-9.5, 37), (-9, 39), (-8, 42), (-4, 44), (0, 42), (3, 42), (4, 41), (0, 38), (-5, 36), (-9.5, 37)],
    # France/Low Countries
    [(3, 42), (7, 44), (6, 46), (2, 51), (-1, 50), (-5, 49), (-4, 44), (0, 42), (3, 42)],
    # British Isles outline
    [(-6, 50), (-5, 54), (-3, 56), (-5, 58), (-2, 59), (1, 53), (0, 51), (-5, 50), (-6, 50)],
    # Italy
    [(7, 44), (14, 46), (18, 40), (16, 38), (12, 37), (8, 39), (7, 44)],
    # Greece/Balkans
    [(14, 46), (23, 46), (26, 42), (24, 35), (20, 36), (14, 40), (14, 46)],
    # Scandinavia (simplified)
    [(5, 58), (6, 62), (12, 66), (20, 70), (28, 70), (30, 60), (25, 55), (12, 54), (8, 56), (5, 58)],
    # Central Europe
    [(14, 46), (18, 50), (24, 55), (20, 55), (14, 54), (8, 56), (6, 54), (6, 46), (14, 46)],
]

# Map bounds for Europe
lat_min, lat_max = 34, 60
lon_min, lon_max = -12, 32

# Custom style for 4800x2700 canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#111111",
    foreground_subtle="#666666",
    colors=("#306998", "#FFD43B"),
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=40,
    legend_font_size=40,
    value_font_size=36,
    tooltip_font_size=36,
)

# Create map chart
chart = TileBackgroundMap(
    width=4800,
    height=2700,
    style=custom_style,
    title="European Landmarks · map-tile-background · pygal · pyplots.ai",
    point_data=landmarks,
    lat_range=(lat_min, lat_max),
    lon_range=(lon_min, lon_max),
    coastlines=europe_coastlines,
    tile_provider="OpenStreetMap",
    show_legend=False,
    margin=20,
    margin_top=100,
    margin_bottom=20,
    margin_left=20,
    margin_right=20,
    show_x_labels=False,
    show_y_labels=False,
)

# Add dummy series to trigger _plot
chart.add("", [0])

# Save outputs
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
