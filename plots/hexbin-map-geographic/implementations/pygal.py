""" pyplots.ai
hexbin-map-geographic: Hexagonal Binning Map
Library: pygal 3.1.0 | Python 3.13.11
Quality: 72/100 | Created: 2026-01-20
"""

# Fix module name conflict (this file is named pygal.py)
import sys
from collections import defaultdict


_cwd = sys.path[0] if sys.path and sys.path[0] else None
if _cwd:
    sys.path.remove(_cwd)

import numpy as np  # noqa: E402
import pygal  # noqa: E402
from pygal.style import Style  # noqa: E402


if _cwd:
    sys.path.insert(0, _cwd)

# Data - Simulated NYC taxi pickup locations (Manhattan area)
np.random.seed(42)
n_points = 5000

# NYC Manhattan bounds (approximately)
lat_min, lat_max = 40.70, 40.82
lon_min, lon_max = -74.02, -73.93

# Create multiple hotspots (Midtown, Lower Manhattan, Upper East Side)
# Cluster 1: Midtown (Times Square area)
c1_lat = np.random.normal(40.758, 0.015, n_points // 3)
c1_lon = np.random.normal(-73.985, 0.01, n_points // 3)
c1_vals = np.random.exponential(25, n_points // 3)  # Fare amounts

# Cluster 2: Lower Manhattan (Financial District)
c2_lat = np.random.normal(40.710, 0.012, n_points // 3)
c2_lon = np.random.normal(-74.010, 0.008, n_points // 3)
c2_vals = np.random.exponential(35, n_points // 3)  # Higher fares downtown

# Cluster 3: Upper East Side
c3_lat = np.random.normal(40.775, 0.018, n_points // 3)
c3_lon = np.random.normal(-73.960, 0.012, n_points // 3)
c3_vals = np.random.exponential(20, n_points // 3)

# Combine all points
lat = np.concatenate([c1_lat, c2_lat, c3_lat])
lon = np.concatenate([c1_lon, c2_lon, c3_lon])
values = np.concatenate([c1_vals, c2_vals, c3_vals])

# Clip to bounds
lat = np.clip(lat, lat_min, lat_max)
lon = np.clip(lon, lon_min, lon_max)

# Compute hexagonal binning with aggregation (inline - KISS principle)
gridsize = 25
x = np.asarray(lon)
y = np.asarray(lat)

# Compute data bounds
x_min, x_max = x.min(), x.max()
y_min = y.min()

# Hexagon dimensions
x_range = x_max - x_min
hex_width = x_range / gridsize
hex_height = hex_width * np.sqrt(3) / 2

# Convert points to hex grid coordinates with value aggregation
bins = defaultdict(lambda: {"count": 0, "sum": 0.0, "values": []})

for xi, yi, vi in zip(x, y, values, strict=True):
    col = (xi - x_min) / hex_width
    row_offset = (int(col) % 2) * 0.5
    row = (yi - y_min) / hex_height - row_offset
    col_idx = int(round(col))
    row_idx = int(round(row))
    bins[(col_idx, row_idx)]["count"] += 1
    bins[(col_idx, row_idx)]["sum"] += vi
    bins[(col_idx, row_idx)]["values"].append(vi)

# Convert bin indices back to coordinates with full statistics
hex_data = []

for (col_idx, row_idx), data in bins.items():
    cx = x_min + col_idx * hex_width
    row_offset = (col_idx % 2) * 0.5
    cy = y_min + (row_idx + row_offset) * hex_height
    count = data["count"]
    total = data["sum"]
    mean = total / count if count > 0 else 0
    hex_data.append({"lon": cx, "lat": cy, "count": count, "sum": total, "mean": mean})

# Extract arrays for plotting
hex_lon = np.array([h["lon"] for h in hex_data])
hex_lat = np.array([h["lat"] for h in hex_data])
counts = np.array([h["count"] for h in hex_data])

# Get count statistics for binning
count_min, count_max = counts.min(), counts.max()
count_range = count_max - count_min if count_max > count_min else 1

# Simplified Manhattan coastline (approximate outline)
manhattan_outline = [
    (-74.020, 40.700),
    (-74.010, 40.705),
    (-74.000, 40.710),
    (-73.975, 40.725),
    (-73.970, 40.750),
    (-73.965, 40.775),
    (-73.940, 40.800),
    (-73.930, 40.815),
    (-73.935, 40.820),
    (-73.943, 40.830),
    (-73.950, 40.822),
    (-73.970, 40.810),
    (-73.990, 40.770),
    (-74.010, 40.740),
    (-74.015, 40.720),
    (-74.020, 40.700),
]

# Hudson River (west boundary approximation)
hudson_river = [
    (-74.035, 40.690),
    (-74.025, 40.705),
    (-74.018, 40.720),
    (-74.015, 40.750),
    (-74.005, 40.780),
    (-73.985, 40.810),
    (-73.970, 40.835),
]

# East River (east boundary approximation)
east_river = [
    (-73.935, 40.695),
    (-73.940, 40.720),
    (-73.945, 40.755),
    (-73.925, 40.785),
    (-73.915, 40.810),
    (-73.920, 40.835),
]

# Custom style - YlOrRd colormap for density (5 levels)
# Hide grid lines completely for cleaner map visualization
custom_style = Style(
    background="white",
    plot_background="#E8F4F8",  # Light water blue
    foreground="#333333",
    foreground_strong="#111111",
    foreground_subtle="#666666",
    guide_stroke_color="transparent",  # Hide grid lines completely
    colors=(
        # 3 boundary/river colors (light gray)
        "#AAAAAA",
        "#8899AA",
        "#8899AA",
        # 5 density levels (YlOrRd colormap with transparency)
        "#FFFFB2CC",  # Very low - light yellow (80% opacity)
        "#FECC5CCC",  # Low - yellow
        "#FD8D3CCC",  # Medium - orange
        "#F03B20CC",  # High - red-orange
        "#BD0026CC",  # Very high - dark red
    ),
    opacity=0.75,  # Base transparency for hexagons
    opacity_hover=0.95,
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=40,
    value_font_size=36,
    tooltip_font_size=36,
)

# Create XY chart - disable grid for clean map background
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="hexbin-map-geographic · pygal · pyplots.ai",
    x_title="Longitude (°)",
    y_title="Latitude (°)",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=5,
    legend_box_size=28,
    stroke=False,
    dots_size=30,
    show_x_guides=False,  # Hide x grid lines
    show_y_guides=False,  # Hide y grid lines
    explicit_size=True,
    print_values=False,
    xrange=(lon_min - 0.015, lon_max + 0.015),  # Tighter margins
    range=(lat_min - 0.008, lat_max + 0.008),
)

# Add geographic boundaries as background lines
chart.add(None, manhattan_outline, stroke=True, dots_size=0, show_dots=False, fill=False)
chart.add(None, hudson_river, stroke=True, dots_size=0, show_dots=False, fill=False)
chart.add(None, east_river, stroke=True, dots_size=0, show_dots=False, fill=False)

# Bin hexagons by density into 5 groups
n_bins = 5
bin_edges = np.linspace(count_min, count_max + 1, n_bins + 1)
bin_labels = [
    f"Pickups: {int(bin_edges[0])}-{int(bin_edges[1])}",
    f"Pickups: {int(bin_edges[1])}-{int(bin_edges[2])}",
    f"Pickups: {int(bin_edges[2])}-{int(bin_edges[3])}",
    f"Pickups: {int(bin_edges[3])}-{int(bin_edges[4])}",
    f"Pickups: {int(bin_edges[4])}+",
]

# Create series for each density level with rich tooltips
series_data = [[] for _ in range(n_bins)]
for h in hex_data:
    hx, hy = h["lon"], h["lat"]
    count = h["count"]
    total = h["sum"]
    mean = h["mean"]
    bin_idx = min(int((count - count_min) / count_range * (n_bins - 0.01)), n_bins - 1)
    # Rich tooltip with cell statistics as spec requires
    tooltip = (
        f"Count: {count} pickups | Fares: ${total:.0f} total, ${mean:.2f} avg | Coords: ({hy:.4f}°N, {abs(hx):.4f}°W)"
    )
    point = {"value": (float(hx), float(hy)), "label": tooltip}
    series_data[bin_idx].append(point)

# Add series with varying dot sizes for density visualization
# Using larger sizes to better represent hexagonal cell areas
dot_sizes = [24, 32, 40, 50, 62]
for i in range(n_bins):
    if series_data[i]:
        chart.add(bin_labels[i], series_data[i], dots_size=dot_sizes[i])

# Save PNG (primary output)
chart.render_to_png("plot.png")

# Save interactive HTML with CSS hexagon styling
# Use CSS clip-path to transform circles into hexagons in interactive view
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>hexbin-map-geographic - pygal</title>
    <style>
        body {{ margin: 0; display: flex; justify-content: center; align-items: center;
               min-height: 100vh; background: #f5f5f5; }}
        .chart {{ max-width: 100%; height: auto; }}
        /* Transform dots into hexagons using CSS clip-path */
        .dot {{
            clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
        }}
    </style>
</head>
<body>
    <figure class="chart">
        {chart.render(is_unicode=True)}
    </figure>
</body>
</html>
"""

with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)
