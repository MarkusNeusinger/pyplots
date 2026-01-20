""" pyplots.ai
map-projections: World Map with Different Projections
Library: bokeh 3.8.2 | Python 3.13.11
Quality: 85/100 | Created: 2026-01-20
"""

import numpy as np
from bokeh.io import export_png, save
from bokeh.layouts import column, gridplot
from bokeh.models import ColumnDataSource, Div, Title
from bokeh.plotting import figure
from bokeh.resources import CDN


# Projection functions (lat/lon in radians -> x/y)


def equirectangular(lon, lat):
    """Equirectangular (Plate Carrée) - simple linear mapping"""
    return lon, lat


def mercator(lon, lat):
    """Mercator - conformal, distorts area at poles"""
    # Clip latitude to avoid infinity at poles
    lat = np.clip(lat, -np.pi / 2 * 0.99, np.pi / 2 * 0.99)
    y = np.log(np.tan(np.pi / 4 + lat / 2))
    return lon, y


def sinusoidal(lon, lat):
    """Sinusoidal - equal area, pseudocylindrical"""
    x = lon * np.cos(lat)
    return x, lat


def mollweide(lon, lat):
    """Mollweide - equal area, elliptical"""
    # Newton-Raphson iteration for auxiliary angle theta
    theta = lat.copy()
    for _ in range(10):
        delta = -(2 * theta + np.sin(2 * theta) - np.pi * np.sin(lat)) / (2 + 2 * np.cos(2 * theta) + 1e-10)
        theta += delta
    x = (2 * np.sqrt(2) / np.pi) * lon * np.cos(theta)
    y = np.sqrt(2) * np.sin(theta)
    return x, y


# Generate graticule (latitude/longitude grid lines)
np.random.seed(42)

lats_deg = np.arange(-90, 91, 30)  # Every 30 degrees
lons_deg = np.arange(-180, 181, 30)


def make_graticule(proj_func):
    """Generate graticule lines for a projection"""
    lines_x = []
    lines_y = []

    # Longitude lines (meridians)
    for lon_d in lons_deg:
        lat_range = np.linspace(-85, 85, 100)
        lon_range = np.full_like(lat_range, lon_d)
        x, y = proj_func(np.radians(lon_range), np.radians(lat_range))
        lines_x.append(list(x) + [np.nan])
        lines_y.append(list(y) + [np.nan])

    # Latitude lines (parallels)
    for lat_d in lats_deg:
        lon_range = np.linspace(-180, 180, 200)
        lat_range = np.full_like(lon_range, lat_d)
        x, y = proj_func(np.radians(lon_range), np.radians(lat_range))
        lines_x.append(list(x) + [np.nan])
        lines_y.append(list(y) + [np.nan])

    # Flatten lists
    all_x = [item for sublist in lines_x for item in sublist]
    all_y = [item for sublist in lines_y for item in sublist]

    return all_x, all_y


# Generate Tissot indicatrices (distortion circles)
def make_tissot(proj_func, radius_deg=8):
    """Generate Tissot indicatrix circles"""
    circles_x = []
    circles_y = []

    tissot_lats = [-60, -30, 0, 30, 60]
    tissot_lons = [-150, -90, -30, 30, 90, 150]

    for lat_d in tissot_lats:
        for lon_d in tissot_lons:
            # Create a small circle in lat/lon space
            angles = np.linspace(0, 2 * np.pi, 50)
            circle_lons = lon_d + radius_deg * np.cos(angles)
            circle_lats = lat_d + radius_deg * np.sin(angles)

            # Clip latitudes
            circle_lats = np.clip(circle_lats, -85, 85)

            x, y = proj_func(np.radians(circle_lons), np.radians(circle_lats))
            circles_x.append(list(x) + [np.nan])
            circles_y.append(list(y) + [np.nan])

    all_x = [item for sublist in circles_x for item in sublist]
    all_y = [item for sublist in circles_y for item in sublist]

    return all_x, all_y


# Projections to display
projections = [
    ("Equirectangular (Plate Carrée)", equirectangular),
    ("Mercator", mercator),
    ("Sinusoidal", sinusoidal),
    ("Mollweide", mollweide),
]

# Create plots
plots = []

for name, proj_func in projections:
    # Create figure
    p = figure(width=2400, height=1350, tools="", toolbar_location=None)

    # Add projection name as title
    p.add_layout(Title(text=name, text_font_size="32pt", align="center"), "above")

    # Generate and plot graticule
    grat_x, grat_y = make_graticule(proj_func)
    grat_source = ColumnDataSource(data={"x": grat_x, "y": grat_y})
    p.line(x="x", y="y", source=grat_source, line_color="#306998", line_width=1.5, line_alpha=0.6)

    # Generate and plot Tissot indicatrices
    tissot_x, tissot_y = make_tissot(proj_func)
    tissot_source = ColumnDataSource(data={"x": tissot_x, "y": tissot_y})
    p.line(x="x", y="y", source=tissot_source, line_color="#FFD43B", line_width=2.5, line_alpha=0.9)
    p.patch(x=tissot_x, y=tissot_y, fill_color="#FFD43B", fill_alpha=0.3, line_color=None)

    # Style axes
    p.xaxis.visible = False
    p.yaxis.visible = False
    p.xgrid.visible = False
    p.ygrid.visible = False

    # Background
    p.background_fill_color = "#f5f5f5"
    p.border_fill_color = "#ffffff"
    p.outline_line_color = "#306998"
    p.outline_line_width = 2

    plots.append(p)

# Create grid layout
grid = gridplot([[plots[0], plots[1]], [plots[2], plots[3]]], merge_tools=False)

# Add overall title
title_div = Div(
    text="<h1 style='text-align: center; font-size: 36pt; font-family: sans-serif; "
    "color: #306998; margin: 20px 0;'>map-projections · bokeh · pyplots.ai</h1>"
    "<p style='text-align: center; font-size: 18pt; color: #666; margin-bottom: 10px;'>"
    "Yellow circles (Tissot indicatrices) show how each projection distorts area and shape</p>",
    width=4800,
)

layout = column(title_div, grid)

# Save outputs
export_png(layout, filename="plot.png")
save(layout, filename="plot.html", resources=CDN, title="Map Projections - pyplots.ai")
