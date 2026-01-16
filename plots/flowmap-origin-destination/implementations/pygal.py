""" pyplots.ai
flowmap-origin-destination: Origin-Destination Flow Map
Library: pygal 3.1.0 | Python 3.13.11
Quality: 88/100 | Created: 2026-01-16
"""

import sys

import numpy as np


# Remove current directory from path to avoid shadowing the pygal package
_cwd = sys.path[0] if sys.path and sys.path[0] else "."
if _cwd in sys.path:
    sys.path.remove(_cwd)

from pygal.graph.graph import Graph  # noqa: E402
from pygal.style import Style  # noqa: E402


sys.path.insert(0, _cwd)


class FlowMap(Graph):
    """Custom Flow Map for pygal - displays origin-destination flows as curved arcs."""

    def __init__(self, *args, **kwargs):
        self.flow_data = kwargs.pop("flow_data", None)
        self.lat_range = kwargs.pop("lat_range", (-90, 90))
        self.lon_range = kwargs.pop("lon_range", (-180, 180))
        self.coastlines = kwargs.pop("coastlines", [])
        self.flow_color = kwargs.pop("flow_color", "#306998")
        self.max_stroke = kwargs.pop("max_stroke", 12)
        self.min_stroke = kwargs.pop("min_stroke", 2)
        super().__init__(*args, **kwargs)

    def _plot(self):
        """Draw the flow map."""
        if self.flow_data is None:
            return

        plot_width = self.view.width
        plot_height = self.view.height

        # Layout margins
        label_margin_left = 180
        label_margin_right = 120
        label_margin_top = 60
        label_margin_bottom = 180

        available_width = plot_width - label_margin_left - label_margin_right
        available_height = plot_height - label_margin_top - label_margin_bottom

        x_offset = self.view.x(0) + label_margin_left
        y_offset = self.view.y(1) + label_margin_top

        # Create group for the flow map
        plot_node = self.nodes["plot"]
        flowmap_group = self.svg.node(plot_node, class_="flow-map")

        # Draw background rectangle for ocean
        bg_rect = self.svg.node(
            flowmap_group, "rect", x=x_offset, y=y_offset, width=available_width, height=available_height
        )
        bg_rect.set("fill", "#C8DDF0")
        bg_rect.set("stroke", "#333333")
        bg_rect.set("stroke-width", "2")

        lat_min, lat_max = self.lat_range
        lon_min, lon_max = self.lon_range

        def lon_to_x(lon):
            return x_offset + (lon - lon_min) / (lon_max - lon_min) * available_width

        def lat_to_y(lat):
            return y_offset + (1 - (lat - lat_min) / (lat_max - lat_min)) * available_height

        # Draw grid lines
        n_lon_lines = 7
        for i in range(n_lon_lines):
            lon = lon_min + (lon_max - lon_min) * i / (n_lon_lines - 1)
            x = lon_to_x(lon)
            line = self.svg.node(flowmap_group, "line", x1=x, y1=y_offset, x2=x, y2=y_offset + available_height)
            line.set("stroke", "#aaaaaa")
            line.set("stroke-width", "1")
            line.set("stroke-opacity", "0.4")

        n_lat_lines = 5
        for i in range(n_lat_lines):
            lat = lat_min + (lat_max - lat_min) * i / (n_lat_lines - 1)
            y = lat_to_y(lat)
            line = self.svg.node(flowmap_group, "line", x1=x_offset, y1=y, x2=x_offset + available_width, y2=y)
            line.set("stroke", "#aaaaaa")
            line.set("stroke-width", "1")
            line.set("stroke-opacity", "0.4")

        # Draw coastlines
        for coastline in self.coastlines:
            if len(coastline) < 2:
                continue
            points = " ".join([f"{lon_to_x(lon)},{lat_to_y(lat)}" for lon, lat in coastline])
            polyline = self.svg.node(flowmap_group, "polyline", points=points)
            polyline.set("fill", "none")
            polyline.set("stroke", "#666666")
            polyline.set("stroke-width", "2")
            polyline.set("stroke-opacity", "0.6")

        # Calculate flow magnitude range for scaling stroke width
        flows = [f["flow"] for f in self.flow_data]
        min_flow = min(flows)
        max_flow = max(flows)

        def flow_to_stroke(flow):
            if max_flow == min_flow:
                return (self.max_stroke + self.min_stroke) / 2
            normalized = (flow - min_flow) / (max_flow - min_flow)
            return self.min_stroke + normalized * (self.max_stroke - self.min_stroke)

        # Sort flows by magnitude (draw smaller first so larger are on top)
        sorted_flows = sorted(self.flow_data, key=lambda f: f["flow"])

        # Draw flow arcs (Bezier curves)
        for flow in sorted_flows:
            o_lat, o_lon = flow["origin_lat"], flow["origin_lon"]
            d_lat, d_lon = flow["dest_lat"], flow["dest_lon"]
            magnitude = flow["flow"]

            x1 = lon_to_x(o_lon)
            y1 = lat_to_y(o_lat)
            x2 = lon_to_x(d_lon)
            y2 = lat_to_y(d_lat)

            # Calculate control point for quadratic Bezier curve
            # Offset perpendicular to the line, with arc curving based on direction
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2

            # Calculate perpendicular offset (curve upward)
            dx = x2 - x1
            dy = y2 - y1
            length = np.sqrt(dx * dx + dy * dy)
            if length > 0:
                # Perpendicular direction (rotate 90 degrees)
                perp_x = -dy / length
                perp_y = dx / length
                # Offset proportional to distance (but capped)
                offset_amount = min(length * 0.3, 150)
                ctrl_x = mid_x + perp_x * offset_amount
                ctrl_y = mid_y + perp_y * offset_amount
            else:
                ctrl_x, ctrl_y = mid_x, mid_y

            # Create quadratic Bezier path
            path_d = f"M {x1},{y1} Q {ctrl_x},{ctrl_y} {x2},{y2}"

            stroke_width = flow_to_stroke(magnitude)
            opacity = 0.5 + 0.3 * (magnitude - min_flow) / (max_flow - min_flow) if max_flow > min_flow else 0.6

            path = self.svg.node(flowmap_group, "path", d=path_d)
            path.set("fill", "none")
            path.set("stroke", self.flow_color)
            path.set("stroke-width", str(stroke_width))
            path.set("stroke-opacity", str(opacity))
            path.set("stroke-linecap", "round")

        # Draw origin and destination markers
        drawn_locations = set()
        for flow in self.flow_data:
            # Origin marker
            o_key = (round(flow["origin_lat"], 2), round(flow["origin_lon"], 2))
            if o_key not in drawn_locations:
                ox = lon_to_x(flow["origin_lon"])
                oy = lat_to_y(flow["origin_lat"])
                circle = self.svg.node(flowmap_group, "circle", cx=ox, cy=oy, r=14)
                circle.set("fill", "#FFD43B")
                circle.set("stroke", "#333333")
                circle.set("stroke-width", "2")
                drawn_locations.add(o_key)

            # Destination marker
            d_key = (round(flow["dest_lat"], 2), round(flow["dest_lon"], 2))
            if d_key not in drawn_locations:
                dx = lon_to_x(flow["dest_lon"])
                dy = lat_to_y(flow["dest_lat"])
                circle = self.svg.node(flowmap_group, "circle", cx=dx, cy=dy, r=14)
                circle.set("fill", "#FFD43B")
                circle.set("stroke", "#333333")
                circle.set("stroke-width", "2")
                drawn_locations.add(d_key)

        # Draw axis labels
        axis_font_size = 48
        tick_font_size = 36

        # X-axis label
        text_node = self.svg.node(
            flowmap_group, "text", x=x_offset + available_width / 2, y=y_offset + available_height + 130
        )
        text_node.set("text-anchor", "middle")
        text_node.set("fill", "#333333")
        text_node.set("style", f"font-size:{axis_font_size}px;font-weight:bold;font-family:sans-serif")
        text_node.text = "Longitude"

        # Y-axis label
        text_node = self.svg.node(flowmap_group, "text", x=x_offset - 100, y=y_offset + available_height / 2)
        text_node.set("text-anchor", "middle")
        text_node.set("fill", "#333333")
        text_node.set("style", f"font-size:{axis_font_size}px;font-weight:bold;font-family:sans-serif")
        text_node.set("transform", f"rotate(-90, {x_offset - 100}, {y_offset + available_height / 2})")
        text_node.text = "Latitude"

        # X-axis ticks
        for i in range(n_lon_lines):
            lon = lon_min + (lon_max - lon_min) * i / (n_lon_lines - 1)
            x = lon_to_x(lon)
            text_node = self.svg.node(flowmap_group, "text", x=x, y=y_offset + available_height + 50)
            text_node.set("text-anchor", "middle")
            text_node.set("fill", "#333333")
            text_node.set("style", f"font-size:{tick_font_size}px;font-family:sans-serif")
            text_node.text = f"{lon:.0f}"

        # Y-axis ticks
        for i in range(n_lat_lines):
            lat = lat_min + (lat_max - lat_min) * i / (n_lat_lines - 1)
            y = lat_to_y(lat)
            text_node = self.svg.node(flowmap_group, "text", x=x_offset - 20, y=y + tick_font_size * 0.35)
            text_node.set("text-anchor", "end")
            text_node.set("fill", "#333333")
            text_node.set("style", f"font-size:{tick_font_size}px;font-family:sans-serif")
            text_node.text = f"{lat:.0f}"

        # Draw legend for flow magnitude
        legend_x = x_offset + available_width + 40
        legend_y = y_offset + 100
        legend_title_size = 40
        legend_text_size = 32

        # Legend title
        text_node = self.svg.node(flowmap_group, "text", x=legend_x, y=legend_y)
        text_node.set("fill", "#333333")
        text_node.set("style", f"font-size:{legend_title_size}px;font-weight:bold;font-family:sans-serif")
        text_node.text = "Flow Volume"

        # Legend items (3 representative widths)
        legend_flows = [min_flow, (min_flow + max_flow) / 2, max_flow]
        legend_labels = ["Low", "Medium", "High"]

        for i, (flow_val, label) in enumerate(zip(legend_flows, legend_labels, strict=True)):
            ly = legend_y + 60 + i * 70
            stroke_w = flow_to_stroke(flow_val)

            # Draw sample line
            line = self.svg.node(flowmap_group, "line", x1=legend_x, y1=ly, x2=legend_x + 80, y2=ly)
            line.set("stroke", self.flow_color)
            line.set("stroke-width", str(stroke_w))
            line.set("stroke-linecap", "round")
            line.set("stroke-opacity", "0.7")

            # Draw label
            text_node = self.svg.node(flowmap_group, "text", x=legend_x + 100, y=ly + legend_text_size * 0.35)
            text_node.set("fill", "#333333")
            text_node.set("style", f"font-size:{legend_text_size}px;font-family:sans-serif")
            text_node.text = f"{label} ({flow_val:.0f})"

        # Legend for markers
        marker_legend_y = legend_y + 300
        text_node = self.svg.node(flowmap_group, "text", x=legend_x, y=marker_legend_y)
        text_node.set("fill", "#333333")
        text_node.set("style", f"font-size:{legend_title_size}px;font-weight:bold;font-family:sans-serif")
        text_node.text = "Locations"

        circle = self.svg.node(flowmap_group, "circle", cx=legend_x + 14, cy=marker_legend_y + 50, r=14)
        circle.set("fill", "#FFD43B")
        circle.set("stroke", "#333333")
        circle.set("stroke-width", "2")

        text_node = self.svg.node(
            flowmap_group, "text", x=legend_x + 40, y=marker_legend_y + 50 + legend_text_size * 0.35
        )
        text_node.set("fill", "#333333")
        text_node.set("style", f"font-size:{legend_text_size}px;font-family:sans-serif")
        text_node.text = "City"

    def _compute(self):
        """Compute the box for rendering."""
        self._box.xmin = 0
        self._box.xmax = 1
        self._box.ymin = 0
        self._box.ymax = 1


# Data: Trade flows between major European ports
np.random.seed(42)

# Major European port cities
ports = {
    "Rotterdam": (51.92, 4.48),
    "Hamburg": (53.55, 9.99),
    "Antwerp": (51.22, 4.40),
    "London": (51.51, -0.13),
    "Le Havre": (49.49, 0.11),
    "Barcelona": (41.39, 2.17),
    "Marseille": (43.30, 5.37),
    "Genoa": (44.41, 8.93),
    "Valencia": (39.47, -0.38),
    "Lisbon": (38.72, -9.14),
    "Piraeus": (37.94, 23.65),
    "Copenhagen": (55.68, 12.57),
    "Gdansk": (54.35, 18.65),
    "Dublin": (53.35, -6.26),
}

# Generate trade flow data between ports
flow_data = []
port_names = list(ports.keys())

# Create flows between major trading pairs
flow_pairs = [
    ("Rotterdam", "Hamburg", 850),
    ("Rotterdam", "Antwerp", 720),
    ("Rotterdam", "London", 680),
    ("Hamburg", "Copenhagen", 450),
    ("Hamburg", "Gdansk", 380),
    ("Antwerp", "Le Havre", 520),
    ("Le Havre", "Barcelona", 340),
    ("Barcelona", "Valencia", 420),
    ("Barcelona", "Marseille", 480),
    ("Marseille", "Genoa", 390),
    ("Genoa", "Barcelona", 360),
    ("Valencia", "Lisbon", 280),
    ("Lisbon", "Le Havre", 310),
    ("Piraeus", "Genoa", 290),
    ("Piraeus", "Marseille", 250),
    ("London", "Dublin", 410),
    ("Rotterdam", "Copenhagen", 370),
    ("Hamburg", "London", 320),
    ("Antwerp", "Barcelona", 260),
    ("Copenhagen", "Gdansk", 220),
]

for origin, dest, flow in flow_pairs:
    o_lat, o_lon = ports[origin]
    d_lat, d_lon = ports[dest]
    flow_data.append(
        {
            "origin_lat": o_lat,
            "origin_lon": o_lon,
            "dest_lat": d_lat,
            "dest_lon": d_lon,
            "flow": flow,
            "origin_name": origin,
            "dest_name": dest,
        }
    )

# Map boundaries for Europe
lat_min, lat_max = 35.0, 58.0
lon_min, lon_max = -12.0, 28.0

# Simplified European coastlines
coastlines = [
    # Iberian Peninsula
    [
        (-9.5, 37.0),
        (-9.0, 38.7),
        (-8.5, 42.0),
        (-2.0, 43.5),
        (3.0, 42.5),
        (0.0, 40.5),
        (-0.5, 38.0),
        (-5.0, 36.0),
        (-9.5, 37.0),
    ],
    # France/Mediterranean
    [(3.0, 42.5), (6.0, 43.0), (9.5, 44.0), (10.5, 44.5), (13.5, 45.5), (12.5, 44.0), (16.0, 41.0)],
    # Italy
    [(9.5, 44.0), (11.0, 42.0), (15.0, 40.0), (18.0, 40.0), (16.0, 41.0)],
    # Balkans/Greece
    [(20.0, 40.0), (23.0, 38.0), (26.0, 40.0), (24.0, 41.5), (20.0, 40.0)],
    # North Sea/Baltic
    [(-6.0, 50.0), (2.0, 51.0), (5.0, 53.0), (8.0, 54.0), (10.0, 55.0), (12.0, 56.0), (18.0, 55.0), (20.0, 54.5)],
    # UK outline
    [
        (-6.0, 50.0),
        (-5.0, 50.0),
        (-3.0, 51.0),
        (1.5, 51.5),
        (0.0, 53.0),
        (-3.0, 54.0),
        (-5.0, 55.0),
        (-6.0, 56.0),
        (-5.0, 58.0),
    ],
    # Ireland
    [(-10.0, 51.5), (-6.0, 51.5), (-6.0, 54.0), (-8.0, 55.5), (-10.0, 53.5), (-10.0, 51.5)],
]

# Custom style
custom_style = Style(
    background="white",
    plot_background="#C8DDF0",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998",),
    title_font_size=64,
    legend_font_size=40,
    label_font_size=42,
    value_font_size=36,
    font_family="sans-serif",
)

# Create flow map chart
chart = FlowMap(
    width=4800,
    height=2700,
    style=custom_style,
    title="flowmap-origin-destination · pygal · pyplots.ai",
    flow_data=flow_data,
    lat_range=(lat_min, lat_max),
    lon_range=(lon_min, lon_max),
    coastlines=coastlines,
    flow_color="#306998",
    max_stroke=14,
    min_stroke=3,
    show_legend=False,
    margin=100,
    margin_top=160,
    margin_bottom=80,
    margin_right=350,
    show_x_labels=False,
    show_y_labels=False,
)

# Add a dummy series to trigger _plot
chart.add("", [0])

# Save outputs
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
