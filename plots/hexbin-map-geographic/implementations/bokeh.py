"""pyplots.ai
hexbin-map-geographic: Hexagonal Binning Map
Library: bokeh 3.8.2 | Python 3.13.11
Quality: 78/100 | Created: 2026-01-20
"""

import numpy as np
from bokeh.io import export_png, output_file, save
from bokeh.models import ColorBar, ColumnDataSource, HoverTool, LinearColorMapper
from bokeh.plotting import figure
from bokeh.transform import transform
from bokeh.util.hex import hexbin


# Data - Simulated GPS coordinates (NYC taxi pickups)
np.random.seed(42)

# Generate clustered point data to simulate urban hotspots
n_points = 5000

# Create multiple cluster centers (simulating different neighborhoods in NYC)
centers = [
    (-73.98, 40.75),  # Midtown Manhattan
    (-73.96, 40.78),  # Upper East Side
    (-74.00, 40.72),  # West Village
    (-73.99, 40.73),  # Greenwich Village
    (-73.97, 40.76),  # Central Park South
]

# Generate points around cluster centers with varying densities
lon_data = []
lat_data = []
for center_lon, center_lat in centers:
    n_cluster = n_points // len(centers) + np.random.randint(-200, 200)
    lon_data.extend(np.random.normal(center_lon, 0.015, n_cluster))
    lat_data.extend(np.random.normal(center_lat, 0.012, n_cluster))

lon = np.array(lon_data)
lat = np.array(lat_data)

# Convert lat/lon to Web Mercator projection (inline, no function)
k = 6378137  # Earth radius in meters
merc_lon = lon * (k * np.pi / 180.0)
merc_lat = np.log(np.tan((90 + lat) * np.pi / 360.0)) * k

# Compute hexbin aggregation in Web Mercator coordinates
hex_size = 800  # Size in meters (Web Mercator units)
bins = hexbin(merc_lon, merc_lat, hex_size)

# Extract hexagon coordinates and counts
hex_q = bins.q
hex_r = bins.r
hex_counts = bins.counts

# Create ColumnDataSource for hex tiles
hex_source = ColumnDataSource(data={"q": hex_q, "r": hex_r, "counts": hex_counts})

# Create color mapper with viridis-like colors
colors = ["#440154", "#482878", "#3e4989", "#31688e", "#26828e", "#1f9e89", "#35b779", "#6ece58", "#b5de2b", "#fde725"]
mapper = LinearColorMapper(palette=colors, low=min(hex_counts), high=max(hex_counts))

# Calculate bounds for the map (with padding)
x_min, x_max = merc_lon.min() - 2000, merc_lon.max() + 2000
y_min, y_max = merc_lat.min() - 2000, merc_lat.max() + 2000

# Create figure with Web Mercator projection
p = figure(
    width=4800,
    height=2700,
    title="hexbin-map-geographic · bokeh · pyplots.ai",
    x_axis_label="Longitude (Web Mercator meters)",
    y_axis_label="Latitude (Web Mercator meters)",
    x_axis_type="mercator",
    y_axis_type="mercator",
    x_range=(x_min, x_max),
    y_range=(y_min, y_max),
    tools="pan,wheel_zoom,box_zoom,reset",
    background_fill_color="#e6e6e6",
)

# Add base map tile layer for geographic context
p.add_tile("CartoDB Positron")

# Plot hex tiles using ColumnDataSource
p.hex_tile(
    q="q", r="r", size=hex_size, fill_color=transform("counts", mapper), line_color=None, alpha=0.75, source=hex_source
)

# Add hover tool for interactivity
hover = HoverTool(tooltips=[("Pickup Count", "@counts"), ("Cell (q, r)", "(@q, @r)")], mode="mouse")
p.add_tools(hover)

# Add color bar legend with better visibility
color_bar = ColorBar(
    color_mapper=mapper,
    location=(0, 0),
    title="Pickups",
    title_text_font_size="20pt",
    title_text_font_style="bold",
    major_label_text_font_size="18pt",
    width=40,
    padding=15,
    margin=20,
)
p.add_layout(color_bar, "right")

# Style the plot
p.title.text_font_size = "32pt"
p.xaxis.axis_label_text_font_size = "24pt"
p.yaxis.axis_label_text_font_size = "24pt"
p.xaxis.major_label_text_font_size = "18pt"
p.yaxis.major_label_text_font_size = "18pt"

# Grid styling - subtle to not compete with base map
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None

# Save PNG output
export_png(p, filename="plot.png")

# Save interactive HTML
output_file("plot.html")
save(p)
