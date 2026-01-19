""" pyplots.ai
map-route-path: Route Path Map
Library: highcharts unknown | Python 3.13.11
Quality: 78/100 | Created: 2026-01-19
"""

import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from highcharts_maps.chart import Chart, HighchartsMapsOptions
from highcharts_maps.options.series.map import MapSeries
from highcharts_maps.options.series.mapline import MapLineSeries
from highcharts_maps.options.series.mappoint import MapPointSeries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - Simulate a hiking trail GPS track through the Swiss Alps
np.random.seed(42)

# Generate a realistic hiking path through mountain terrain
# Start near Zermatt and traverse towards Mont Blanc region
n_points = 150

# Base path coordinates (starting near Zermatt, moving west)
base_lat = np.linspace(46.02, 45.92, n_points)
base_lon = np.linspace(7.75, 6.87, n_points)

# Add realistic GPS noise and terrain variation
lat_noise = np.cumsum(np.random.randn(n_points) * 0.002)
lon_noise = np.cumsum(np.random.randn(n_points) * 0.003)

# Create switchbacks (zigzag pattern for mountain climbing)
switchback = 0.01 * np.sin(np.linspace(0, 12 * np.pi, n_points))

lats = base_lat + lat_noise * 0.3 + switchback
lons = base_lon + lon_noise * 0.3

# Simulate elevation profile (climb then descend)
elevation = 1600 + 1200 * np.sin(np.linspace(0, np.pi, n_points)) + np.random.randn(n_points) * 50

# Create timestamps for the hike (6-hour hike)
start_time = 0  # hours
time_points = np.linspace(start_time, start_time + 6, n_points)

# Prepare waypoint data
waypoints = []
for i in range(n_points):
    waypoints.append(
        {
            "sequence": i + 1,
            "lat": float(lats[i]),
            "lon": float(lons[i]),
            "elevation": float(elevation[i]),
            "time_hrs": float(time_points[i]),
        }
    )

# Create path line data for mapline series
path_data = [[wp["lon"], wp["lat"]] for wp in waypoints]

# Calculate map bounds for better zoom
min_lat = min(lats) - 0.05
max_lat = max(lats) + 0.05
min_lon = min(lons) - 0.1
max_lon = max(lons) + 0.1
center_lat = (min_lat + max_lat) / 2
center_lon = (min_lon + max_lon) / 2

# Create color gradient segments for time progression
# Split path into colored segments based on time
n_segments = 10
colors_gradient = [
    "#1a4f9c",  # Dark blue (start)
    "#2166ac",
    "#4393c3",
    "#92c5de",
    "#d1e5f0",
    "#f7f7f7",
    "#fddbc7",
    "#f4a582",
    "#d6604d",
    "#b2182b",  # Red (end)
]

# Create Chart using highcharts-core library
chart = Chart(container="container")

# Configure chart options
chart.options = HighchartsMapsOptions()
chart.options.chart = {
    "map": None,  # Will be set by topology in JavaScript
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#ffffff",
    "spacing": [120, 100, 100, 100],
}

chart.options.title = {
    "text": "Alpine Hiking Trail · map-route-path · highcharts · pyplots.ai",
    "style": {"fontSize": "56px", "fontWeight": "bold"},
    "y": 70,
}

chart.options.subtitle = {
    "text": "GPS track from Zermatt region through the Swiss Alps (150 waypoints, 6-hour hike)",
    "style": {"fontSize": "40px", "color": "#666666"},
    "y": 120,
}

chart.options.map_navigation = {"enabled": False}

# Use inset to focus on the route area for better layout balance
chart.options.map_view = {
    "projection": {"name": "WebMercator"},
    "insetOptions": {"borderColor": "#cccccc", "borderWidth": 1},
    "fitToGeometry": {
        "type": "Polygon",
        "coordinates": [
            [[min_lon, min_lat], [max_lon, min_lat], [max_lon, max_lat], [min_lon, max_lat], [min_lon, min_lat]]
        ],
    },
    "padding": [50, 50, 50, 50],
}

chart.options.legend = {
    "enabled": True,
    "align": "right",
    "verticalAlign": "middle",
    "layout": "vertical",
    "floating": True,
    "x": -50,
    "y": -50,
    "backgroundColor": "rgba(255, 255, 255, 0.95)",
    "borderColor": "#cccccc",
    "borderWidth": 2,
    "padding": 25,
    "itemStyle": {"fontSize": "32px"},
    "symbolWidth": 60,
    "symbolHeight": 30,
    "symbolRadius": 0,
}

chart.options.tooltip = {
    "useHTML": True,
    "headerFormat": "",
    "pointFormat": '<span style="font-size: 28px;">'
    "Waypoint: <b>{point.sequence}</b><br/>"
    "Elevation: <b>{point.elevation:.0f}m</b><br/>"
    "Time: <b>{point.time_hrs:.1f} hrs</b><br/>"
    "Position: ({point.lat:.4f}°, {point.lon:.4f}°)"
    "</span>",
}

chart.options.plot_options = {
    "mappoint": {"dataLabels": {"enabled": False}},
    "mapline": {"lineWidth": 6, "enableMouseTracking": False},
}

# Add series using the highcharts-core library

# 1. Base map series
base_map = MapSeries()
base_map.name = "Terrain"
base_map.show_in_legend = False
base_map.null_color = "#e8e8e8"
base_map.border_color = "#aaaaaa"
base_map.border_width = 1
base_map.states = {"inactive": {"opacity": 1}}
chart.add_series(base_map)

# 2. Route segments with color gradient for time progression
segment_size = n_points // n_segments
for seg_idx in range(n_segments):
    start_idx = seg_idx * segment_size
    end_idx = min(start_idx + segment_size + 1, n_points)  # +1 for overlap
    segment_coords = path_data[start_idx:end_idx]

    segment = MapLineSeries()
    segment.name = f"Hour {seg_idx * 0.6:.0f}-{(seg_idx + 1) * 0.6:.0f}" if seg_idx < n_segments - 1 else "Route"
    segment.show_in_legend = seg_idx == 0  # Only show first segment in legend as "Route"
    segment.line_width = 20
    segment.color = colors_gradient[seg_idx]
    segment.z_index = 10 + seg_idx
    segment.states = {"inactive": {"opacity": 1}}
    segment.enable_mouse_tracking = False
    segment.data = [
        {"geometry": {"type": "LineString", "coordinates": segment_coords}, "color": colors_gradient[seg_idx]}
    ]
    if seg_idx == 0:
        segment.name = "Route (colored by time)"
    chart.add_series(segment)

# 3. Waypoints (small dots along path)
waypoint_series = MapPointSeries()
waypoint_series.name = "Waypoints"
waypoint_series.show_in_legend = False
waypoint_series.color = "#FFD43B"
waypoint_series.marker = {
    "symbol": "circle",
    "radius": 14,
    "fillColor": "#FFD43B",
    "lineWidth": 3,
    "lineColor": "#306998",
}
waypoint_series.z_index = 15
waypoint_series.data = [
    {
        "lat": wp["lat"],
        "lon": wp["lon"],
        "sequence": wp["sequence"],
        "elevation": wp["elevation"],
        "time_hrs": wp["time_hrs"],
    }
    for wp in waypoints[::10]  # Every 10th point to reduce clutter
]
chart.add_series(waypoint_series)

# 4. Start point marker
start_series = MapPointSeries()
start_series.name = "Start"
start_series.show_in_legend = True
start_series.color = "#10B981"  # Green
start_series.marker = {"symbol": "circle", "radius": 28, "fillColor": "#10B981", "lineWidth": 5, "lineColor": "#ffffff"}
start_series.data_labels = {
    "enabled": True,
    "format": "START",
    "style": {"fontSize": "36px", "fontWeight": "bold", "color": "#10B981", "textOutline": "3px white"},
    "y": -45,
}
start_series.z_index = 20
start_series.data = [
    {
        "lat": waypoints[0]["lat"],
        "lon": waypoints[0]["lon"],
        "sequence": 1,
        "elevation": waypoints[0]["elevation"],
        "time_hrs": waypoints[0]["time_hrs"],
    }
]
chart.add_series(start_series)

# 5. End point marker
end_series = MapPointSeries()
end_series.name = "End"
end_series.show_in_legend = True
end_series.color = "#b2182b"  # Dark red (matching gradient end)
end_series.marker = {"symbol": "square", "radius": 24, "fillColor": "#b2182b", "lineWidth": 5, "lineColor": "#ffffff"}
end_series.data_labels = {
    "enabled": True,
    "format": "END",
    "style": {"fontSize": "36px", "fontWeight": "bold", "color": "#b2182b", "textOutline": "3px white"},
    "y": -45,
}
end_series.z_index = 20
end_series.data = [
    {
        "lat": waypoints[-1]["lat"],
        "lon": waypoints[-1]["lon"],
        "sequence": n_points,
        "elevation": waypoints[-1]["elevation"],
        "time_hrs": waypoints[-1]["time_hrs"],
    }
]
chart.add_series(end_series)

# Generate JavaScript from chart object
chart_js = chart.to_js_literal()

# Download required JavaScript files
highmaps_url = "https://code.highcharts.com/maps/highmaps.js"
switzerland_url = "https://code.highcharts.com/mapdata/countries/ch/ch-all.topo.json"

with urllib.request.urlopen(highmaps_url, timeout=60) as response:
    highmaps_js = response.read().decode("utf-8")

with urllib.request.urlopen(switzerland_url, timeout=60) as response:
    switzerland_topo = response.read().decode("utf-8")

# Generate HTML with inline scripts for headless rendering
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highmaps_js}</script>
</head>
<body style="margin:0;">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>
        var topology = {switzerland_topo};
        {chart_js}
        // Get the chart config from the generated code
        var chartElement = document.getElementById('container');
        // Re-render with topology
        var options = Highcharts.charts[0] ? Highcharts.charts[0].options : null;
        if (options) {{
            options.chart.map = topology;
            Highcharts.mapChart('container', options);
        }}
    </script>
</body>
</html>"""

# Alternative approach: construct config directly for more control
chart_config_str = chart_js.replace("Highcharts.chart('container',", "").rstrip(")")

html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highmaps_js}</script>
</head>
<body style="margin:0;">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>
        var topology = {switzerland_topo};
        var chartConfig = {chart_config_str};
        chartConfig.chart.map = topology;
        Highcharts.mapChart('container', chartConfig);
    </script>
</body>
</html>"""

# Save HTML for interactive version
standalone_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://code.highcharts.com/maps/highmaps.js"></script>
</head>
<body style="margin:0;">
    <div id="container" style="width: 100%; height: 100vh;"></div>
    <script>
        fetch('https://code.highcharts.com/mapdata/countries/ch/ch-all.topo.json')
            .then(response => response.json())
            .then(topology => {{
                var chartConfig = {chart_config_str};
                chartConfig.chart.map = topology;
                Highcharts.mapChart('container', chartConfig);
            }});
    </script>
</body>
</html>"""

with open("plot.html", "w", encoding="utf-8") as f:
    f.write(standalone_html)

# Write temp HTML and take screenshot
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=4800,2700")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(6)  # Wait for map to render
driver.save_screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()  # Clean up temp file
