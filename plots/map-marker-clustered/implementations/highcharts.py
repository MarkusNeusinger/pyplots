""" pyplots.ai
map-marker-clustered: Clustered Marker Map
Library: highcharts unknown | Python 3.13.11
Quality: 85/100 | Created: 2026-01-20
"""

import json
import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Generate sample store location data across the United States
np.random.seed(42)

# Create clusters of stores in major metropolitan areas
cities = {
    "New York": (40.7128, -74.0060, 50),
    "Los Angeles": (34.0522, -118.2437, 45),
    "Chicago": (41.8781, -87.6298, 35),
    "Houston": (29.7604, -95.3698, 30),
    "Phoenix": (33.4484, -112.0740, 25),
    "Philadelphia": (39.9526, -75.1652, 20),
    "San Antonio": (29.4241, -98.4936, 18),
    "San Diego": (32.7157, -117.1611, 22),
    "Dallas": (32.7767, -96.7970, 28),
    "San Francisco": (37.7749, -122.4194, 25),
    "Seattle": (47.6062, -122.3321, 20),
    "Denver": (39.7392, -104.9903, 18),
    "Boston": (42.3601, -71.0589, 22),
    "Atlanta": (33.7490, -84.3880, 24),
    "Miami": (25.7617, -80.1918, 20),
}

categories = ["Grocery", "Electronics", "Clothing", "Home Goods"]
category_colors = {
    "Grocery": "#306998",  # Python Blue
    "Electronics": "#FFD43B",  # Python Yellow
    "Clothing": "#9467BD",  # Purple
    "Home Goods": "#17BECF",  # Cyan
}

# Generate store data
stores = []
for city_name, (lat, lon, count) in cities.items():
    for i in range(count):
        store_lat = lat + np.random.normal(0, 0.15)
        store_lon = lon + np.random.normal(0, 0.15)
        category = np.random.choice(categories)
        stores.append(
            {
                "lat": round(store_lat, 4),
                "lon": round(store_lon, 4),
                "name": f"{city_name} Store #{i + 1}",
                "category": category,
                "color": category_colors[category],
            }
        )

# Download required Highcharts modules
highcharts_url = "https://code.highcharts.com/highcharts.js"
maps_url = "https://code.highcharts.com/maps/modules/map.js"
marker_clusters_url = "https://code.highcharts.com/modules/marker-clusters.js"
us_map_url = "https://code.highcharts.com/mapdata/countries/us/us-all.topo.json"

with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

with urllib.request.urlopen(maps_url, timeout=30) as response:
    maps_js = response.read().decode("utf-8")

with urllib.request.urlopen(marker_clusters_url, timeout=30) as response:
    marker_clusters_js = response.read().decode("utf-8")

with urllib.request.urlopen(us_map_url, timeout=30) as response:
    us_map_data = response.read().decode("utf-8")

# Prepare data for Highcharts
series_data = {}
for store in stores:
    cat = store["category"]
    if cat not in series_data:
        series_data[cat] = []
    series_data[cat].append({"lat": store["lat"], "lon": store["lon"], "name": store["name"]})

# Build series configuration
series_config = []
for cat, points in series_data.items():
    series_config.append(
        {
            "type": "mappoint",
            "name": cat,
            "color": category_colors[cat],
            "data": points,
            "cluster": {
                "enabled": True,
                "allowOverlap": False,
                "animation": {"duration": 450},
                "layoutAlgorithm": {"type": "grid", "gridSize": 70},
                "zones": [
                    {"from": 1, "to": 4, "marker": {"radius": 15}},
                    {"from": 5, "to": 9, "marker": {"radius": 20}},
                    {"from": 10, "to": 19, "marker": {"radius": 25}},
                    {"from": 20, "to": 49, "marker": {"radius": 32}},
                    {"from": 50, "to": 100, "marker": {"radius": 40}},
                ],
            },
            "marker": {"radius": 8, "symbol": "circle"},
        }
    )

series_json = json.dumps(series_config)

# Create HTML with Highcharts map
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <script>{maps_js}</script>
    <script>{marker_clusters_js}</script>
</head>
<body style="margin:0; padding:0; background-color:#ffffff;">
    <div id="container" style="width:4800px; height:2700px;"></div>
    <script>
        var mapData = {us_map_data};

        Highcharts.mapChart('container', {{
            chart: {{
                map: mapData,
                backgroundColor: '#ffffff',
                marginBottom: 120
            }},
            title: {{
                text: 'Retail Store Locations (Clustered) \u00b7 map-marker-clustered \u00b7 highcharts \u00b7 pyplots.ai',
                style: {{
                    fontSize: '48px',
                    fontWeight: 'bold'
                }}
            }},
            subtitle: {{
                text: '420 stores across 15 major US cities - zoom to expand clusters',
                style: {{
                    fontSize: '32px'
                }}
            }},
            mapNavigation: {{
                enabled: true,
                buttonOptions: {{
                    verticalAlign: 'bottom',
                    style: {{
                        fontSize: '24px'
                    }}
                }}
            }},
            legend: {{
                enabled: true,
                align: 'right',
                verticalAlign: 'middle',
                layout: 'vertical',
                itemStyle: {{
                    fontSize: '28px'
                }},
                symbolRadius: 8,
                symbolHeight: 20,
                symbolWidth: 20
            }},
            tooltip: {{
                headerFormat: '',
                pointFormat: '<b>{{point.name}}</b><br>Lat: {{point.lat:.4f}}, Lon: {{point.lon:.4f}}',
                style: {{
                    fontSize: '24px'
                }},
                clusterFormat: '<b>Cluster</b><br>Points: {{point.clusterPointsAmount}}'
            }},
            plotOptions: {{
                mappoint: {{
                    cluster: {{
                        enabled: true,
                        allowOverlap: false,
                        animation: {{
                            duration: 450
                        }},
                        layoutAlgorithm: {{
                            type: 'grid',
                            gridSize: 70
                        }},
                        dataLabels: {{
                            enabled: true,
                            format: '{{point.clusterPointsAmount}}',
                            style: {{
                                fontSize: '20px',
                                fontWeight: 'bold',
                                color: 'white',
                                textOutline: '2px contrast'
                            }}
                        }}
                    }},
                    dataLabels: {{
                        enabled: false
                    }}
                }}
            }},
            series: [{{
                name: 'US States',
                borderColor: '#A0A0A0',
                nullColor: '#f0f0f0',
                showInLegend: false,
                enableMouseTracking: false
            }}, {series_json[1:-1]}]
        }});
    </script>
</body>
</html>"""

# Save interactive HTML
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Take screenshot using Selenium
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
time.sleep(6)  # Wait for chart and map to render
driver.save_screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()  # Clean up temp file
