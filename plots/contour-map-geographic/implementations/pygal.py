"""pyplots.ai
contour-map-geographic: Contour Lines on Geographic Map
Library: pygal | Python 3.13
Quality: pending | Created: 2026-01-17
"""

# Fix module name conflict (this file is named pygal.py)
import sys
from pathlib import Path


_script_dir = str(Path(__file__).parent)
sys.path = [p for p in sys.path if p != _script_dir]

import cairosvg  # noqa: E402
import numpy as np  # noqa: E402
import pygal  # noqa: E402
from pygal.style import Style  # noqa: E402


# Data - Generate synthetic temperature data over a geographic grid
# Simulating surface temperature contours (isotherms) over a region
np.random.seed(42)

# Define geographic bounds (roughly Europe/Atlantic region)
lon_min, lon_max = -30, 50  # Longitude range
lat_min, lat_max = 25, 70  # Latitude range

# Create regular grid for contour data
n_grid = 40
lon_grid = np.linspace(lon_min, lon_max, n_grid)
lat_grid = np.linspace(lat_min, lat_max, n_grid)
LON, LAT = np.meshgrid(lon_grid, lat_grid)

# Generate synthetic temperature field (°C)
# Use combination of gradients and patterns to simulate weather-like data
# Base: latitude gradient (warmer in south)
temp_base = 25 - (LAT - lat_min) * 0.3

# Add west-east gradient (warmer near coast in winter)
temp_base += (LON - lon_min) * 0.08

# Add high/low pressure systems as temperature anomalies
# High pressure center (warm)
high_lon, high_lat = 15, 50
dist_high = np.sqrt((LON - high_lon) ** 2 + (LAT - high_lat) ** 2)
temp_anomaly1 = 8 * np.exp(-(dist_high**2) / 300)

# Low pressure center (cold)
low_lon, low_lat = -10, 60
dist_low = np.sqrt((LON - low_lon) ** 2 + (LAT - low_lat) ** 2)
temp_anomaly2 = -10 * np.exp(-(dist_low**2) / 250)

# Another warm anomaly in Mediterranean
med_lon, med_lat = 25, 35
dist_med = np.sqrt((LON - med_lon) ** 2 + (LAT - med_lat) ** 2)
temp_anomaly3 = 6 * np.exp(-(dist_med**2) / 200)

# Combine all components
TEMP = temp_base + temp_anomaly1 + temp_anomaly2 + temp_anomaly3

# Add slight noise for realism
TEMP += np.random.normal(0, 0.5, TEMP.shape)

# Define contour levels (every 4°C from -4 to 24)
contour_levels = np.arange(-4, 26, 4)

# Simplified coastlines for Europe/Atlantic (lon, lat format)
coastlines = [
    # British Isles
    [(-10, 50), (-5, 55), (-7, 58), (-2, 59), (0, 61), (2, 57), (-5, 50), (-10, 50)],
    # Iberian Peninsula
    [(-10, 36), (-9, 43), (-2, 43), (4, 42), (-6, 36), (-10, 36)],
    # France/Germany coast
    [(-5, 48), (2, 51), (4, 51), (10, 54), (4, 56), (-2, 53), (-5, 48)],
    # Scandinavia
    [(5, 58), (11, 58), (18, 63), (25, 70), (30, 70), (25, 62), (10, 56), (5, 58)],
    # Italy
    [(8, 44), (18, 40), (12, 38), (8, 44)],
    # North Africa coast
    [(-10, 30), (10, 32), (30, 31), (35, 32), (35, 28), (10, 28), (-10, 30)],
    # Eastern Mediterranean
    [(20, 35), (30, 37), (36, 35), (27, 35), (20, 35)],
]

# Color scale for temperature (blue cold -> yellow/red warm)
temp_colors = [
    "#2166ac",  # -4: Deep blue (very cold)
    "#4393c3",  # 0: Blue (cold)
    "#92c5de",  # 4: Light blue (cool)
    "#d1e5f0",  # 8: Very light blue
    "#fddbc7",  # 12: Light orange
    "#f4a582",  # 16: Orange
    "#d6604d",  # 20: Red-orange
    "#b2182b",  # 24: Red (hot)
]


def get_temp_color(temp):
    """Map temperature to color."""
    idx = int((temp + 4) / 4)
    idx = max(0, min(idx, len(temp_colors) - 1))
    return temp_colors[idx]


# Custom style for 4800x2700 canvas
custom_style = Style(
    background="white",
    plot_background="#C8DDF0",  # Ocean blue
    foreground="#333333",
    foreground_strong="#111111",
    foreground_subtle="#666666",
    guide_stroke_color="#88888844",
    colors=("#666666",) * len(coastlines),  # Gray for coastlines
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=40,
    legend_font_size=44,
    value_font_size=36,
)

# Create base XY chart
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="Surface Temperature Isotherms · contour-map-geographic · pygal · pyplots.ai",
    x_title="Longitude (°E)",
    y_title="Latitude (°N)",
    show_legend=False,
    stroke=True,
    dots_size=0,
    show_x_guides=True,
    show_y_guides=True,
    explicit_size=True,
    print_values=False,
    xrange=(lon_min, lon_max),
    range=(lat_min, lat_max),
    margin=120,
    margin_top=200,
    margin_bottom=200,
    margin_left=280,
    margin_right=300,
)

# Add coastlines as background
for coords in coastlines:
    chart.add(None, coords, stroke=True, dots_size=0, show_dots=False, fill=False)

# Plot dimensions
plot_x = 280
plot_y = 200
plot_width = 4800 - 280 - 300
plot_height = 2700 - 200 - 200


def geo_to_pixel(lon, lat):
    """Convert geographic coordinates to pixel coordinates."""
    px = plot_x + (lon - lon_min) / (lon_max - lon_min) * plot_width
    py = plot_y + plot_height - (lat - lat_min) / (lat_max - lat_min) * plot_height
    return px, py


# Build custom SVG content for contours
svg_parts = []

# Draw filled contours first (background)
cell_w = plot_width / (n_grid - 1)
cell_h = plot_height / (n_grid - 1)

for i in range(n_grid - 1):
    for j in range(n_grid - 1):
        # Average temperature of 4 corners
        avg_temp = (TEMP[i, j] + TEMP[i, j + 1] + TEMP[i + 1, j] + TEMP[i + 1, j + 1]) / 4
        color = get_temp_color(avg_temp)
        px, py = geo_to_pixel(lon_grid[j], lat_grid[i + 1])
        svg_parts.append(
            f'<rect x="{px:.1f}" y="{py:.1f}" width="{cell_w + 1:.1f}" '
            f'height="{cell_h + 1:.1f}" fill="{color}" fill-opacity="0.6" stroke="none"/>'
        )

# Draw contour lines using marching squares algorithm
for level in contour_levels:
    line_color = "#333333"
    line_width = 3 if level % 8 == 0 else 2  # Thicker lines for major contours

    for i in range(n_grid - 1):
        for j in range(n_grid - 1):
            z00, z01 = TEMP[i, j], TEMP[i, j + 1]
            z10, z11 = TEMP[i + 1, j], TEMP[i + 1, j + 1]

            # Marching squares case determination
            case = 0
            if z00 >= level:
                case |= 1
            if z01 >= level:
                case |= 2
            if z11 >= level:
                case |= 4
            if z10 >= level:
                case |= 8

            if case == 0 or case == 15:
                continue

            # Cell corner coordinates
            x0, y0 = geo_to_pixel(lon_grid[j], lat_grid[i + 1])
            x1, y1 = geo_to_pixel(lon_grid[j + 1], lat_grid[i])

            # Linear interpolation helper
            def lerp(v1, v2, lv):
                if abs(v2 - v1) < 1e-10:
                    return 0.5
                return (lv - v1) / (v2 - v1)

            # Calculate edge intersection points
            left = (x0, y0 - cell_h * lerp(z00, z10, level))
            right = (x1, y1 + cell_h * lerp(z01, z11, level))
            top = (x0 + cell_w * lerp(z10, z11, level), y0 - cell_h)
            bottom = (x0 + cell_w * lerp(z00, z01, level), y0)

            # Determine line segments based on marching squares case
            segments = []
            if case in [1, 14]:
                segments.append((left, bottom))
            elif case in [2, 13]:
                segments.append((bottom, right))
            elif case in [3, 12]:
                segments.append((left, right))
            elif case in [4, 11]:
                segments.append((right, top))
            elif case == 5:
                segments.append((left, top))
                segments.append((bottom, right))
            elif case in [6, 9]:
                segments.append((bottom, top))
            elif case in [7, 8]:
                segments.append((left, top))
            elif case == 10:
                segments.append((left, bottom))
                segments.append((right, top))

            for (x1_s, y1_s), (x2_s, y2_s) in segments:
                svg_parts.append(
                    f'<line x1="{x1_s:.1f}" y1="{y1_s:.1f}" x2="{x2_s:.1f}" y2="{y2_s:.1f}" '
                    f'stroke="{line_color}" stroke-width="{line_width}" stroke-opacity="0.8"/>'
                )

# Add contour labels at strategic positions
label_positions = [
    (-20, 45, -4),
    (-15, 58, 0),
    (5, 62, 4),
    (20, 55, 8),
    (30, 50, 12),
    (35, 42, 16),
    (25, 33, 20),
    (10, 32, 24),
]

for lon_l, lat_l, temp_l in label_positions:
    # Check if this label position is within grid bounds
    if lon_min <= lon_l <= lon_max and lat_min <= lat_l <= lat_max:
        px, py = geo_to_pixel(lon_l, lat_l)
        svg_parts.append(
            f'<rect x="{px - 30}" y="{py - 22}" width="60" height="32" fill="white" fill-opacity="0.85" rx="4"/>'
        )
        svg_parts.append(
            f'<text x="{px}" y="{py + 5}" text-anchor="middle" fill="#333333" '
            f'style="font-size:28px;font-weight:bold;font-family:sans-serif">{temp_l}°C</text>'
        )

# Add colorbar
cb_width = 50
cb_height = plot_height * 0.7
cb_x = plot_x + plot_width + 80
cb_y = plot_y + (plot_height - cb_height) / 2

# Draw colorbar gradient
n_cb_segments = len(temp_colors)
seg_h = cb_height / n_cb_segments
for i, color in enumerate(temp_colors[::-1]):  # Reverse so cold is at bottom
    seg_y = cb_y + i * seg_h
    svg_parts.append(f'<rect x="{cb_x}" y="{seg_y:.1f}" width="{cb_width}" height="{seg_h + 1:.1f}" fill="{color}"/>')

# Colorbar border
svg_parts.append(
    f'<rect x="{cb_x}" y="{cb_y}" width="{cb_width}" height="{cb_height}" '
    f'fill="none" stroke="#333333" stroke-width="2"/>'
)

# Colorbar labels
cb_labels = [24, 20, 16, 12, 8, 4, 0, -4]
for i, val in enumerate(cb_labels):
    label_y = cb_y + i * seg_h + seg_h / 2 + 10
    svg_parts.append(
        f'<text x="{cb_x + cb_width + 15}" y="{label_y:.1f}" fill="#333333" '
        f'style="font-size:32px;font-family:sans-serif">{val}°C</text>'
    )

# Colorbar title
svg_parts.append(
    f'<text x="{cb_x + cb_width / 2}" y="{cb_y - 25}" text-anchor="middle" fill="#333333" '
    f'style="font-size:36px;font-weight:bold;font-family:sans-serif">Temperature</text>'
)

# Combine custom SVG
custom_svg = "\n".join(svg_parts)

# Add dummy data point (required by pygal)
chart.add("", [(lon_min, lat_min)])

# Render base chart and inject custom SVG
base_svg = chart.render(is_unicode=True)

# Insert custom contour SVG before the closing </svg> tag
output_svg = base_svg.replace("</svg>", f"{custom_svg}\n</svg>")

# Save SVG
with open("plot.svg", "w", encoding="utf-8") as f:
    f.write(output_svg)

# Convert to PNG using cairosvg
cairosvg.svg2png(bytestring=output_svg.encode("utf-8"), write_to="plot.png")

# Save interactive HTML
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>contour-map-geographic - pygal</title>
    <style>
        body {{ margin: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; background: #f5f5f5; }}
        .chart {{ max-width: 100%; height: auto; }}
    </style>
</head>
<body>
    <figure class="chart">
        {output_svg}
    </figure>
</body>
</html>
"""

with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)
