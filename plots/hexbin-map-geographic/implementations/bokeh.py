""" pyplots.ai
hexbin-map-geographic: Hexagonal Binning Map
Library: bokeh 3.8.2 | Python 3.13.11
Quality: 72/100 | Created: 2026-01-20
"""

import numpy as np
from bokeh.io import export_png, output_file, save
from bokeh.models import ColorBar, ColumnDataSource, HoverTool, LinearColorMapper
from bokeh.plotting import figure
from bokeh.transform import transform
from bokeh.util.hex import hexbin


# Data - Simulated GPS coordinates (e.g., taxi pickups in a city area)
np.random.seed(42)

# Generate clustered point data to simulate urban hotspots
n_points = 5000

# Create multiple cluster centers (simulating different neighborhoods)
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
    # Different cluster sizes
    n_cluster = n_points // len(centers) + np.random.randint(-200, 200)
    lon_data.extend(np.random.normal(center_lon, 0.015, n_cluster))
    lat_data.extend(np.random.normal(center_lat, 0.012, n_cluster))

lon = np.array(lon_data)
lat = np.array(lat_data)

# Compute hexbin aggregation
# Use hexbin utility to compute counts per cell
# Size parameter controls hexagon size (in data coordinates)
hex_size = 0.008  # Adjust for balance between detail and aggregation
bins = hexbin(lon, lat, hex_size)

# Extract hexagon coordinates and counts
hex_q = bins.q
hex_r = bins.r
hex_counts = bins.counts

# Create ColumnDataSource for hex tiles
hex_source = ColumnDataSource(data={"q": hex_q, "r": hex_r, "counts": hex_counts})

# Create color mapper with viridis-like colors
colors = ["#440154", "#482878", "#3e4989", "#31688e", "#26828e", "#1f9e89", "#35b779", "#6ece58", "#b5de2b", "#fde725"]
mapper = LinearColorMapper(palette=colors, low=min(hex_counts), high=max(hex_counts))

# Create figure
p = figure(
    width=4800,
    height=2700,
    title="NYC Taxi Pickups · hexbin-map-geographic · bokeh · pyplots.ai",
    x_axis_label="Longitude",
    y_axis_label="Latitude",
    tools="pan,wheel_zoom,box_zoom,reset",
    match_aspect=True,
    background_fill_color="#f0f0f0",
)

# Plot hex tiles using ColumnDataSource
p.hex_tile(
    q="q", r="r", size=hex_size, fill_color=transform("counts", mapper), line_color=None, alpha=0.85, source=hex_source
)

# Add hover tool for interactivity
hover = HoverTool(tooltips=[("Count", "@counts"), ("Hex (q, r)", "(@q, @r)")], mode="mouse")
p.add_tools(hover)

# Add color bar legend
color_bar = ColorBar(
    color_mapper=mapper,
    location=(0, 0),
    title="Pickup Count",
    title_text_font_size="18pt",
    major_label_text_font_size="16pt",
    width=30,
    padding=10,
)
p.add_layout(color_bar, "right")

# Style the plot
p.title.text_font_size = "28pt"
p.xaxis.axis_label_text_font_size = "22pt"
p.yaxis.axis_label_text_font_size = "22pt"
p.xaxis.major_label_text_font_size = "18pt"
p.yaxis.major_label_text_font_size = "18pt"

# Grid styling
p.xgrid.grid_line_color = "#cccccc"
p.ygrid.grid_line_color = "#cccccc"
p.xgrid.grid_line_alpha = 0.5
p.ygrid.grid_line_alpha = 0.5

# Save PNG output
export_png(p, filename="plot.png")

# Save interactive HTML
output_file("plot.html")
save(p)
