"""pyplots.ai
heatmap-geographic: Geographic Heatmap for Spatial Density
Library: bokeh | Python 3.13
Quality: pending | Created: 2026-01-10
"""

import numpy as np
from bokeh.io import export_png
from bokeh.models import BasicTicker, ColorBar, LinearColorMapper, WMTSTileSource
from bokeh.plotting import figure, output_file, save


# Data: Simulated environmental monitoring stations across California
np.random.seed(42)

n_points = 500

# Create clusters representing different monitoring regions
# Central California coast cluster
coast_lat = np.random.normal(36.5, 0.8, n_points // 3)
coast_lon = np.random.normal(-121.5, 0.5, n_points // 3)

# Southern California cluster
socal_lat = np.random.normal(34.0, 0.6, n_points // 3)
socal_lon = np.random.normal(-118.0, 0.7, n_points // 3)

# Northern California cluster
norcal_lat = np.random.normal(38.5, 0.5, n_points // 3 + n_points % 3)
norcal_lon = np.random.normal(-122.5, 0.4, n_points // 3 + n_points % 3)

# Combine all clusters
latitudes = np.concatenate([coast_lat, socal_lat, norcal_lat])
longitudes = np.concatenate([coast_lon, socal_lon, norcal_lon])

# Measurement values (e.g., air quality index readings)
values = np.random.exponential(scale=50, size=len(latitudes)) + 20


# Convert lat/lon to Web Mercator projection for Bokeh
# x = lon * 20037508.34 / 180
merc_x = longitudes * 20037508.34 / 180
# y = log(tan((90 + lat) * pi / 360)) / (pi / 180) * 20037508.34 / 180
merc_y = np.log(np.tan((90 + latitudes) * np.pi / 360)) / (np.pi / 180) * 20037508.34 / 180

# Define map boundaries for California in Mercator
lat_min, lat_max = 32.5, 42.0
lon_min, lon_max = -125.0, -114.0
x_min = lon_min * 20037508.34 / 180
x_max = lon_max * 20037508.34 / 180
y_min = np.log(np.tan((90 + lat_min) * np.pi / 360)) / (np.pi / 180) * 20037508.34 / 180
y_max = np.log(np.tan((90 + lat_max) * np.pi / 360)) / (np.pi / 180) * 20037508.34 / 180

# Create 2D histogram for density estimation
grid_resolution = 100
x_bins = np.linspace(x_min, x_max, grid_resolution)
y_bins = np.linspace(y_min, y_max, grid_resolution)

# Compute weighted 2D histogram (density heatmap)
heatmap, x_edges, y_edges = np.histogram2d(merc_x, merc_y, bins=[x_bins, y_bins], weights=values, density=False)

# Apply Gaussian smoothing for continuous appearance
sigma = 3
kernel_size = int(6 * sigma + 1)
if kernel_size % 2 == 0:
    kernel_size += 1
kernel_x_arr = np.arange(kernel_size) - kernel_size // 2
kernel_1d = np.exp(-(kernel_x_arr**2) / (2 * sigma**2))
kernel_1d = kernel_1d / kernel_1d.sum()

# Apply separable 2D filter
heatmap_smooth = np.apply_along_axis(lambda row: np.convolve(row, kernel_1d, mode="same"), axis=0, arr=heatmap)
heatmap_smooth = np.apply_along_axis(lambda col: np.convolve(col, kernel_1d, mode="same"), axis=1, arr=heatmap_smooth)

# Create Bokeh figure with Web Mercator projection
p = figure(
    width=4800,
    height=2700,
    x_range=(x_min, x_max),
    y_range=(y_min, y_max),
    x_axis_type="mercator",
    y_axis_type="mercator",
    title="heatmap-geographic · bokeh · pyplots.ai",
)

# Add map tile provider as basemap (CartoDB Positron)
tile_url = "https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png"
tile_source = WMTSTileSource(url=tile_url)
p.add_tile(tile_source)

# Create color mapper for heatmap
color_mapper = LinearColorMapper(
    palette="YlOrRd9",
    low=0,
    high=np.percentile(heatmap_smooth[heatmap_smooth > 0], 95) if np.any(heatmap_smooth > 0) else 1,
)

# Draw heatmap as image
p.image(
    image=[heatmap_smooth.T],
    x=x_min,
    y=y_min,
    dw=x_max - x_min,
    dh=y_max - y_min,
    color_mapper=color_mapper,
    alpha=0.65,
)

# Scatter original points to show data locations
p.scatter(x=merc_x, y=merc_y, size=8, color="#306998", alpha=0.35, legend_label="Sensor Locations")

# Add colorbar
color_bar = ColorBar(
    color_mapper=color_mapper,
    ticker=BasicTicker(),
    label_standoff=12,
    border_line_color=None,
    location=(0, 0),
    title="Air Quality Index (weighted density)",
    title_text_font_size="20pt",
    major_label_text_font_size="16pt",
    width=30,
)
p.add_layout(color_bar, "right")

# Styling
p.title.text_font_size = "28pt"
p.xaxis.axis_label = "Longitude"
p.yaxis.axis_label = "Latitude"
p.xaxis.axis_label_text_font_size = "22pt"
p.yaxis.axis_label_text_font_size = "22pt"
p.xaxis.major_label_text_font_size = "18pt"
p.yaxis.major_label_text_font_size = "18pt"

# Grid styling
p.xgrid.grid_line_alpha = 0.3
p.ygrid.grid_line_alpha = 0.3
p.xgrid.grid_line_dash = "dashed"
p.ygrid.grid_line_dash = "dashed"

# Legend styling
p.legend.location = "top_right"
p.legend.label_text_font_size = "16pt"
p.legend.background_fill_alpha = 0.7

# Save as PNG
export_png(p, filename="plot.png")

# Save interactive HTML version
output_file("plot.html", title="Geographic Heatmap for Spatial Density")
save(p)
