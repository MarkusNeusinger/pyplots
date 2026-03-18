""" pyplots.ai
star-chart-constellation: Star Chart with Constellations
Library: highcharts unknown | Python 3.14.3
Quality: 89/100 | Created: 2026-03-18
"""

import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.scatter import ScatterSeries
from highcharts_core.options.series.spline import SplineSeries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data — bright stars with constellation lines for a northern hemisphere star chart
np.random.seed(42)

# Real star data: (name, RA hours, Dec degrees, apparent magnitude, constellation)
star_catalog = [
    # Orion
    ("Betelgeuse", 5.92, 7.41, 0.42, "Ori"),
    ("Rigel", 5.24, -8.20, 0.13, "Ori"),
    ("Bellatrix", 5.42, 6.35, 1.64, "Ori"),
    ("Mintaka", 5.53, -0.30, 2.23, "Ori"),
    ("Alnilam", 5.60, -1.20, 1.69, "Ori"),
    ("Alnitak", 5.68, -1.94, 1.77, "Ori"),
    ("Saiph", 5.80, -9.67, 2.09, "Ori"),
    # Ursa Major (Big Dipper)
    ("Dubhe", 11.06, 61.75, 1.79, "UMa"),
    ("Merak", 11.03, 56.38, 2.37, "UMa"),
    ("Phecda", 11.90, 53.69, 2.44, "UMa"),
    ("Megrez", 12.26, 57.03, 3.31, "UMa"),
    ("Alioth", 12.90, 55.96, 1.77, "UMa"),
    ("Mizar", 13.40, 54.93, 2.27, "UMa"),
    ("Alkaid", 13.79, 49.31, 1.86, "UMa"),
    # Cassiopeia
    ("Schedar", 0.68, 56.54, 2.23, "Cas"),
    ("Caph", 0.15, 59.15, 2.27, "Cas"),
    ("Gamma Cas", 0.95, 60.72, 2.47, "Cas"),
    ("Ruchbah", 1.36, 60.24, 2.68, "Cas"),
    ("Segin", 1.91, 63.67, 3.37, "Cas"),
    # Leo
    ("Regulus", 10.14, 11.97, 1.35, "Leo"),
    ("Denebola", 11.82, 14.57, 2.13, "Leo"),
    ("Algieba", 10.33, 19.84, 2.28, "Leo"),
    ("Zosma", 11.24, 20.52, 2.56, "Leo"),
    ("Chertan", 11.24, 15.43, 3.33, "Leo"),
    ("Eta Leo", 10.12, 16.76, 3.52, "Leo"),
    # Cygnus
    ("Deneb", 20.69, 45.28, 1.25, "Cyg"),
    ("Sadr", 20.37, 40.26, 2.20, "Cyg"),
    ("Gienah Cyg", 20.77, 33.97, 2.46, "Cyg"),
    ("Delta Cyg", 19.75, 45.13, 2.87, "Cyg"),
    ("Albireo", 19.51, 27.96, 3.08, "Cyg"),
    # Lyra
    ("Vega", 18.62, 38.78, 0.03, "Lyr"),
    ("Sheliak", 18.83, 33.36, 3.45, "Lyr"),
    ("Sulafat", 18.98, 32.69, 3.24, "Lyr"),
    # Gemini
    ("Pollux", 7.76, 28.03, 1.14, "Gem"),
    ("Castor", 7.58, 31.89, 1.58, "Gem"),
    ("Alhena", 6.63, 16.40, 1.93, "Gem"),
    ("Wasat", 7.07, 21.98, 3.53, "Gem"),
    ("Mebsuta", 6.73, 25.13, 2.98, "Gem"),
    ("Tejat", 6.38, 22.51, 2.88, "Gem"),
    # Taurus
    ("Aldebaran", 4.60, 16.51, 0.85, "Tau"),
    ("Elnath", 5.44, 28.61, 1.65, "Tau"),
    ("Alcyone", 3.79, 24.11, 2.87, "Tau"),
    ("Tianguan", 5.63, 21.14, 3.00, "Tau"),
    # Scorpius
    ("Antares", 16.49, -26.43, 0.96, "Sco"),
    ("Shaula", 17.56, -37.10, 1.63, "Sco"),
    ("Sargas", 17.62, -42.99, 1.87, "Sco"),
    ("Dschubba", 16.01, -22.62, 2.32, "Sco"),
    ("Graffias", 16.09, -19.81, 2.62, "Sco"),
    ("Lesath", 17.53, -37.29, 2.69, "Sco"),
    # Bootes
    ("Arcturus", 14.26, 19.18, -0.05, "Boo"),
    ("Izar", 14.75, 27.07, 2.37, "Boo"),
    ("Muphrid", 13.91, 18.40, 2.68, "Boo"),
    ("Nekkar", 15.03, 40.39, 3.50, "Boo"),
    # Aquila
    ("Altair", 19.85, 8.87, 0.77, "Aql"),
    ("Tarazed", 19.77, 10.61, 2.72, "Aql"),
    ("Alshain", 19.92, 6.41, 3.71, "Aql"),
    # Canis Major
    ("Sirius", 6.75, -16.72, -1.46, "CMa"),
    ("Adhara", 6.98, -28.97, 1.50, "CMa"),
    ("Wezen", 7.14, -26.39, 1.84, "CMa"),
    ("Mirzam", 6.38, -17.96, 1.98, "CMa"),
    ("Aludra", 7.40, -29.30, 2.45, "CMa"),
    # Auriga
    ("Capella", 5.28, 46.00, 0.08, "Aur"),
    ("Menkalinan", 5.99, 44.95, 1.90, "Aur"),
    ("Mahasim", 5.03, 41.08, 3.17, "Aur"),
    ("Hassaleh", 4.95, 33.17, 2.69, "Aur"),
    # Perseus
    ("Mirfak", 3.41, 49.86, 1.79, "Per"),
    ("Algol", 3.14, 40.96, 2.12, "Per"),
    ("Zeta Per", 3.90, 31.88, 2.85, "Per"),
    ("Epsilon Per", 3.96, 40.01, 2.89, "Per"),
    # Andromeda
    ("Alpheratz", 0.14, 29.09, 2.06, "And"),
    ("Mirach", 1.16, 35.62, 2.05, "And"),
    ("Almach", 2.06, 42.33, 2.17, "And"),
]

# Constellation edges (pairs of star names)
constellation_edges = [
    # Orion
    ("Betelgeuse", "Bellatrix"),
    ("Betelgeuse", "Mintaka"),
    ("Bellatrix", "Mintaka"),
    ("Mintaka", "Alnilam"),
    ("Alnilam", "Alnitak"),
    ("Alnitak", "Saiph"),
    ("Mintaka", "Rigel"),
    ("Rigel", "Saiph"),
    # Ursa Major
    ("Dubhe", "Merak"),
    ("Merak", "Phecda"),
    ("Phecda", "Megrez"),
    ("Megrez", "Alioth"),
    ("Alioth", "Mizar"),
    ("Mizar", "Alkaid"),
    ("Megrez", "Dubhe"),
    # Cassiopeia
    ("Caph", "Schedar"),
    ("Schedar", "Gamma Cas"),
    ("Gamma Cas", "Ruchbah"),
    ("Ruchbah", "Segin"),
    # Leo
    ("Regulus", "Eta Leo"),
    ("Eta Leo", "Algieba"),
    ("Algieba", "Zosma"),
    ("Zosma", "Denebola"),
    ("Regulus", "Chertan"),
    ("Chertan", "Denebola"),
    # Cygnus
    ("Deneb", "Sadr"),
    ("Sadr", "Gienah Cyg"),
    ("Sadr", "Delta Cyg"),
    ("Sadr", "Albireo"),
    # Lyra
    ("Vega", "Sheliak"),
    ("Vega", "Sulafat"),
    ("Sheliak", "Sulafat"),
    # Gemini
    ("Castor", "Pollux"),
    ("Castor", "Mebsuta"),
    ("Mebsuta", "Tejat"),
    ("Pollux", "Wasat"),
    ("Wasat", "Alhena"),
    ("Tejat", "Alhena"),
    # Taurus
    ("Aldebaran", "Tianguan"),
    ("Tianguan", "Elnath"),
    ("Aldebaran", "Alcyone"),
    # Scorpius
    ("Graffias", "Dschubba"),
    ("Dschubba", "Antares"),
    ("Antares", "Shaula"),
    ("Shaula", "Lesath"),
    ("Shaula", "Sargas"),
    # Bootes
    ("Arcturus", "Izar"),
    ("Arcturus", "Muphrid"),
    ("Izar", "Nekkar"),
    # Aquila
    ("Altair", "Tarazed"),
    ("Altair", "Alshain"),
    # Canis Major
    ("Sirius", "Mirzam"),
    ("Sirius", "Wezen"),
    ("Wezen", "Adhara"),
    ("Wezen", "Aludra"),
    # Auriga
    ("Capella", "Menkalinan"),
    ("Capella", "Mahasim"),
    ("Mahasim", "Hassaleh"),
    # Perseus
    ("Mirfak", "Algol"),
    ("Mirfak", "Epsilon Per"),
    ("Epsilon Per", "Zeta Per"),
    # Andromeda
    ("Alpheratz", "Mirach"),
    ("Mirach", "Almach"),
]

# Convert RA (hours) to degrees for plotting
star_names = [s[0] for s in star_catalog]
ra_hours = np.array([s[1] for s in star_catalog])
dec_deg = np.array([s[2] for s in star_catalog])
magnitudes = np.array([s[3] for s in star_catalog])
constellations = [s[4] for s in star_catalog]

ra_deg = ra_hours * 15.0  # Convert RA hours to degrees

# Map magnitude to marker radius: brighter (lower mag) = larger
mag_min, mag_max = magnitudes.min(), magnitudes.max()
radius_min, radius_max = 4, 28
star_radii = radius_min + (radius_max - radius_min) * (1 - (magnitudes - mag_min) / (mag_max - mag_min))

# Map magnitude to opacity: brighter stars more opaque
star_opacity = 0.5 + 0.5 * (1 - (magnitudes - mag_min) / (mag_max - mag_min))

# Build star lookup for constellation lines
star_lookup = {s[0]: i for i, s in enumerate(star_catalog)}

# Constellation full names
constellation_names = {
    "Ori": "Orion",
    "UMa": "Ursa Major",
    "Cas": "Cassiopeia",
    "Leo": "Leo",
    "Cyg": "Cygnus",
    "Lyr": "Lyra",
    "Gem": "Gemini",
    "Tau": "Taurus",
    "Sco": "Scorpius",
    "Boo": "Boötes",
    "Aql": "Aquila",
    "CMa": "Canis Major",
    "Aur": "Auriga",
    "Per": "Perseus",
    "And": "Andromeda",
}

# Constellation colors — subtle palette for lines and labels
constellation_colors = {
    "Ori": "#6EC6FF",
    "UMa": "#FFD54F",
    "Cas": "#CE93D8",
    "Leo": "#FFB74D",
    "Cyg": "#81C784",
    "Lyr": "#4FC3F7",
    "Gem": "#AED581",
    "Tau": "#FF8A65",
    "Sco": "#EF5350",
    "Boo": "#FFAB91",
    "Aql": "#80DEEA",
    "CMa": "#90CAF9",
    "Aur": "#FFF176",
    "Per": "#B39DDB",
    "And": "#F48FB1",
}

# Create chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

chart.options.chart = {
    "type": "scatter",
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#0a0e1a",
    "style": {"fontFamily": "'Segoe UI', Helvetica, Arial, sans-serif"},
    "marginTop": 140,
    "marginBottom": 200,
    "marginLeft": 180,
    "marginRight": 100,
    "plotBackgroundColor": {
        "linearGradient": {"x1": 0, "y1": 0, "x2": 0, "y2": 1},
        "stops": [[0, "#070b15"], [0.5, "#0d1326"], [1, "#0a0f1e"]],
    },
}

chart.options.title = {
    "text": "star-chart-constellation · highcharts · pyplots.ai",
    "style": {"fontSize": "56px", "fontWeight": "600", "color": "#c8d6e5", "letterSpacing": "1px"},
    "margin": 40,
}

chart.options.subtitle = {
    "text": "Northern & Southern Hemisphere — 15 Constellations, 70+ Stars to mag 3.7",
    "style": {"fontSize": "34px", "color": "#576574", "fontWeight": "400"},
}

# X-axis: Right Ascension (reversed to match sky convention)
chart.options.x_axis = {
    "title": {
        "text": "Right Ascension (°)",
        "style": {"fontSize": "36px", "color": "#8395a7", "fontWeight": "500"},
        "margin": 20,
    },
    "labels": {"style": {"fontSize": "28px", "color": "#576574"}, "format": "{value}°"},
    "reversed": True,
    "min": -10,
    "max": 370,
    "tickInterval": 30,
    "gridLineWidth": 1,
    "gridLineColor": "rgba(99, 128, 160, 0.12)",
    "gridLineDashStyle": "Dot",
    "lineColor": "rgba(99, 128, 160, 0.3)",
    "lineWidth": 1,
    "tickColor": "rgba(99, 128, 160, 0.3)",
}

# Y-axis: Declination
chart.options.y_axis = {
    "title": {
        "text": "Declination (°)",
        "style": {"fontSize": "36px", "color": "#8395a7", "fontWeight": "500"},
        "margin": 20,
    },
    "labels": {"style": {"fontSize": "28px", "color": "#576574"}, "format": "{value}°"},
    "min": -50,
    "max": 70,
    "tickInterval": 10,
    "gridLineWidth": 1,
    "gridLineColor": "rgba(99, 128, 160, 0.12)",
    "gridLineDashStyle": "Dot",
    "lineColor": "rgba(99, 128, 160, 0.3)",
    "lineWidth": 1,
    "tickColor": "rgba(99, 128, 160, 0.3)",
}

chart.options.legend = {"enabled": False}
chart.options.credits = {"enabled": False}

chart.options.tooltip = {
    "headerFormat": "",
    "pointFormat": (
        '<span style="font-size:22px;color:{point.color}">★</span> '
        '<span style="font-size:24px;color:#c8d6e5">'
        "<b>{point.name}</b><br/>"
        "RA: {point.x:.1f}° · Dec: {point.y:.1f}°<br/>"
        "Magnitude: {point.mag:.2f}</span>"
    ),
    "backgroundColor": "rgba(10, 14, 26, 0.92)",
    "borderColor": "#4FC3F7",
    "borderRadius": 8,
    "borderWidth": 1,
    "style": {"fontSize": "24px", "color": "#c8d6e5"},
}

# Add constellation line series (one per constellation for coloring)
added_constellations = set()
for abbr in constellation_colors:
    edges_for_const = [
        (s1, s2)
        for s1, s2 in constellation_edges
        if star_catalog[star_lookup[s1]][4] == abbr or star_catalog[star_lookup[s2]][4] == abbr
    ]
    if not edges_for_const:
        continue

    for s1, s2 in edges_for_const:
        i1, i2 = star_lookup[s1], star_lookup[s2]
        line = SplineSeries()
        line.data = [[float(ra_deg[i1]), float(dec_deg[i1])], [float(ra_deg[i2]), float(dec_deg[i2])]]
        line.color = constellation_colors[abbr]
        line.opacity = 0.35
        line.line_width = 2
        line.marker = {"enabled": False}
        line.enable_mouse_tracking = False
        line.show_in_legend = False
        line.z_index = 1
        chart.add_series(line)

# Add star scatter series — individual points with custom radius via data point config
star_data_points = []
for i in range(len(star_catalog)):
    star_data_points.append(
        {
            "x": float(ra_deg[i]),
            "y": float(dec_deg[i]),
            "name": star_names[i],
            "mag": float(magnitudes[i]),
            "marker": {
                "radius": float(star_radii[i]),
                "fillColor": {
                    "radialGradient": {"cx": 0.4, "cy": 0.3, "r": 0.7},
                    "stops": [
                        [0, "#ffffff"],
                        [0.3, f"rgba(255, 248, 220, {float(star_opacity[i]):.2f})"],
                        [1, f"rgba(200, 214, 229, {float(star_opacity[i] * 0.3):.2f})"],
                    ],
                },
                "lineWidth": 0,
            },
        }
    )

stars_series = ScatterSeries()
stars_series.data = star_data_points
stars_series.name = "Stars"
stars_series.color = "#FFF8DC"
stars_series.z_index = 3
stars_series.marker = {"symbol": "circle", "lineWidth": 0}
chart.add_series(stars_series)

# Add constellation name labels as a separate scatter series with data labels
label_data = []
for abbr, full_name in constellation_names.items():
    const_stars = [i for i, s in enumerate(star_catalog) if s[4] == abbr]
    if not const_stars:
        continue
    centroid_ra = float(np.mean([ra_deg[i] for i in const_stars]))
    centroid_dec = float(np.mean([dec_deg[i] for i in const_stars]))
    label_data.append(
        {
            "x": centroid_ra,
            "y": centroid_dec,
            "name": full_name,
            "dataLabels": {
                "enabled": True,
                "format": full_name,
                "style": {
                    "fontSize": "26px",
                    "color": constellation_colors[abbr],
                    "textOutline": "2px #0a0e1a",
                    "fontWeight": "600",
                    "letterSpacing": "2px",
                },
                "y": -20,
            },
            "marker": {"radius": 0, "states": {"hover": {"enabled": False}}},
        }
    )

label_series = ScatterSeries()
label_series.data = label_data
label_series.name = "Constellation Labels"
label_series.color = "rgba(0,0,0,0)"
label_series.enable_mouse_tracking = False
label_series.show_in_legend = False
label_series.z_index = 4
label_series.marker = {"radius": 0}
chart.add_series(label_series)

# Add faint background stars for atmosphere
np.random.seed(99)
n_bg_stars = 300
bg_ra = np.random.uniform(0, 360, n_bg_stars)
bg_dec = np.random.uniform(-50, 70, n_bg_stars)
bg_mag = np.random.uniform(4.0, 6.5, n_bg_stars)
bg_radius = 1 + (6.5 - bg_mag) / 2.5

bg_data = []
for i in range(n_bg_stars):
    bg_data.append(
        {
            "x": float(bg_ra[i]),
            "y": float(bg_dec[i]),
            "marker": {
                "radius": float(bg_radius[i]),
                "fillColor": f"rgba(180, 200, 220, {0.15 + 0.15 * (6.5 - float(bg_mag[i])) / 2.5:.2f})",
                "lineWidth": 0,
            },
        }
    )

bg_series = ScatterSeries()
bg_series.data = bg_data
bg_series.name = "Background Stars"
bg_series.color = "rgba(180, 200, 220, 0.2)"
bg_series.enable_mouse_tracking = False
bg_series.show_in_legend = False
bg_series.z_index = 0
bg_series.marker = {"symbol": "circle", "lineWidth": 0}
chart.add_series(bg_series)

# Download Highcharts JS with fallback CDN
js_urls = [("https://code.highcharts.com/highcharts.js", "https://cdn.jsdelivr.net/npm/highcharts@11/highcharts.js")]
js_parts = []
for primary, fallback in js_urls:
    for url in (primary, fallback):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as response:
                js_parts.append(response.read().decode("utf-8"))
            break
        except Exception:
            continue
highcharts_js = "\n".join(js_parts)

# Generate HTML with inline scripts
html_str = chart.to_js_literal()
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
</head>
<body style="margin:0; background:#0a0e1a;">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>{html_str}</script>
</body>
</html>"""

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
time.sleep(5)

container = driver.find_element("id", "container")
container.screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()

# Save HTML for interactive version
with open("plot.html", "w", encoding="utf-8") as f:
    interactive_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://code.highcharts.com/highcharts.js"></script>
</head>
<body style="margin:0; background:#0a0e1a;">
    <div id="container" style="width: 100%; height: 100vh;"></div>
    <script>{html_str}</script>
</body>
</html>"""
    f.write(interactive_html)
