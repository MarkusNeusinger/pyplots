"""pyplots.ai
map-route-path: Route Path Map
Library: highcharts | Python 3.13
Quality: pending | Created: 2026-01-19
"""

import json
import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
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

# Create color gradient data based on time/progress
# Use colorStops for visual time progression
gradient_points = []
for i, wp in enumerate(waypoints):
    progress = i / (n_points - 1)  # 0 to 1
    gradient_points.append(
        {
            "lat": wp["lat"],
            "lon": wp["lon"],
            "elevation": wp["elevation"],
            "time_hrs": wp["time_hrs"],
            "progress": progress,
        }
    )

# Chart configuration
chart_config = {
    "chart": {
        "map": None,  # Will be set by topology
        "width": 4800,
        "height": 2700,
        "backgroundColor": "#ffffff",
        "spacing": [120, 100, 100, 100],
    },
    "title": {
        "text": "Alpine Hiking Trail · map-route-path · highcharts · pyplots.ai",
        "style": {"fontSize": "56px", "fontWeight": "bold"},
        "y": 70,
    },
    "subtitle": {
        "text": "GPS track from Zermatt region through the Swiss Alps (150 waypoints, 6-hour hike)",
        "style": {"fontSize": "40px", "color": "#666666"},
        "y": 120,
    },
    "mapNavigation": {"enabled": False},
    "mapView": {
        "projection": {"name": "WebMercator"},
        "center": [7.3, 45.97],  # Center on Swiss Alps route
        "zoom": 10,  # Zoom in to see the route detail
    },
    "legend": {
        "enabled": True,
        "align": "right",
        "verticalAlign": "middle",
        "layout": "vertical",
        "floating": True,
        "x": -50,
        "backgroundColor": "rgba(255, 255, 255, 0.95)",
        "borderColor": "#cccccc",
        "borderWidth": 2,
        "padding": 20,
        "itemStyle": {"fontSize": "28px"},
    },
    "tooltip": {
        "useHTML": True,
        "headerFormat": "",
        "pointFormat": '<span style="font-size: 28px;">'
        "Waypoint: <b>{point.sequence}</b><br/>"
        "Elevation: <b>{point.elevation:.0f}m</b><br/>"
        "Time: <b>{point.time_hrs:.1f} hrs</b><br/>"
        "Position: ({point.lat:.4f}°, {point.lon:.4f}°)"
        "</span>",
    },
    "plotOptions": {
        "mappoint": {"dataLabels": {"enabled": False}},
        "mapline": {"lineWidth": 6, "enableMouseTracking": False},
    },
    "series": [
        # Base map
        {
            "type": "map",
            "name": "Terrain",
            "showInLegend": False,
            "nullColor": "#e8e8e8",
            "borderColor": "#aaaaaa",
            "borderWidth": 1,
            "states": {"inactive": {"opacity": 1}},
        },
        # Route path as mapline
        {
            "type": "mapline",
            "name": "Route",
            "showInLegend": True,
            "data": [{"geometry": {"type": "LineString", "coordinates": path_data}, "color": "#306998"}],
            "lineWidth": 20,
            "color": "#306998",
            "nullColor": "#306998",
            "enableMouseTracking": True,
            "zIndex": 10,
            "states": {"inactive": {"opacity": 1}},
        },
        # Waypoints (small dots along path)
        {
            "type": "mappoint",
            "name": "Waypoints",
            "showInLegend": False,
            "data": [
                {
                    "lat": wp["lat"],
                    "lon": wp["lon"],
                    "sequence": wp["sequence"],
                    "elevation": wp["elevation"],
                    "time_hrs": wp["time_hrs"],
                }
                for wp in waypoints[::10]  # Every 10th point to reduce clutter
            ],
            "color": "#FFD43B",
            "marker": {
                "symbol": "circle",
                "radius": 16,
                "fillColor": "#FFD43B",
                "lineWidth": 4,
                "lineColor": "#306998",
            },
            "zIndex": 15,
        },
        # Start point marker
        {
            "type": "mappoint",
            "name": "Start",
            "showInLegend": True,
            "data": [
                {
                    "lat": waypoints[0]["lat"],
                    "lon": waypoints[0]["lon"],
                    "sequence": 1,
                    "elevation": waypoints[0]["elevation"],
                    "time_hrs": waypoints[0]["time_hrs"],
                }
            ],
            "color": "#10B981",  # Green
            "marker": {
                "symbol": "circle",
                "radius": 28,
                "fillColor": "#10B981",
                "lineWidth": 5,
                "lineColor": "#ffffff",
            },
            "dataLabels": {
                "enabled": True,
                "format": "START",
                "style": {"fontSize": "36px", "fontWeight": "bold", "color": "#10B981", "textOutline": "3px white"},
                "y": -45,
            },
            "zIndex": 20,
        },
        # End point marker
        {
            "type": "mappoint",
            "name": "End",
            "showInLegend": True,
            "data": [
                {
                    "lat": waypoints[-1]["lat"],
                    "lon": waypoints[-1]["lon"],
                    "sequence": n_points,
                    "elevation": waypoints[-1]["elevation"],
                    "time_hrs": waypoints[-1]["time_hrs"],
                }
            ],
            "color": "#DC2626",  # Red
            "marker": {
                "symbol": "square",
                "radius": 24,
                "fillColor": "#DC2626",
                "lineWidth": 5,
                "lineColor": "#ffffff",
            },
            "dataLabels": {
                "enabled": True,
                "format": "END",
                "style": {"fontSize": "36px", "fontWeight": "bold", "color": "#DC2626", "textOutline": "3px white"},
                "y": -45,
            },
            "zIndex": 20,
        },
    ],
}

# Convert to JSON for JavaScript
chart_json = json.dumps(chart_config)

# Download required JavaScript files
highmaps_url = "https://code.highcharts.com/maps/highmaps.js"
europe_url = "https://code.highcharts.com/mapdata/custom/europe.topo.json"

with urllib.request.urlopen(highmaps_url, timeout=60) as response:
    highmaps_js = response.read().decode("utf-8")

with urllib.request.urlopen(europe_url, timeout=60) as response:
    europe_topo = response.read().decode("utf-8")

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
        var topology = {europe_topo};
        var chartConfig = {chart_json};
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
        fetch('https://code.highcharts.com/mapdata/custom/europe.topo.json')
            .then(response => response.json())
            .then(topology => {{
                var chartConfig = {chart_json};
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
