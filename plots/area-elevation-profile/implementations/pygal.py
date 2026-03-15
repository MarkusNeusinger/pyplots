""" pyplots.ai
area-elevation-profile: Terrain Elevation Profile Along Transect
Library: pygal 3.1.0 | Python 3.14.3
Quality: 82/100 | Created: 2026-03-15
"""

import xml.etree.ElementTree as ET

import cairosvg
import numpy as np
import pygal
from pygal.style import Style


# Data - Alpine hiking trail elevation profile (120 km transect, sampled every ~1 km)
np.random.seed(42)

distances_km = np.linspace(0, 120, 200)

# Build realistic terrain with multiple peaks and valleys
base_terrain = (
    800
    + 600 * np.sin(distances_km * np.pi / 40) ** 2
    + 400 * np.sin(distances_km * np.pi / 25 + 1.2) ** 2
    + 300 * np.exp(-((distances_km - 55) ** 2) / 80)
    + 500 * np.exp(-((distances_km - 85) ** 2) / 120)
    - 200 * np.exp(-((distances_km - 30) ** 2) / 50)
)
noise = np.random.normal(0, 25, len(distances_km))
elevation_m = base_terrain + noise
elevation_m = np.maximum(elevation_m, 650)

# Landmarks along the trail
landmarks = [
    {"name": "Grindelwald", "km": 0},
    {"name": "Kleine Scheidegg", "km": 22},
    {"name": "Lauterbrunnen", "km": 38},
    {"name": "Mürren", "km": 55},
    {"name": "Blüemlisalp Hut", "km": 72},
    {"name": "Hohtürli Pass", "km": 85},
    {"name": "Kandersteg", "km": 120},
]

# Get elevation at landmark positions
for lm in landmarks:
    idx = np.argmin(np.abs(distances_km - lm["km"]))
    lm["elev"] = float(elevation_m[idx])

# Custom style
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#2d2d2d",
    foreground_strong="#2d2d2d",
    foreground_subtle="#e0e0e0",
    colors=("#4a7fb5", "#c45a00"),
    font_family="DejaVu Sans, Helvetica, Arial, sans-serif",
    title_font_family="DejaVu Sans, Helvetica, Arial, sans-serif",
    title_font_size=52,
    label_font_size=36,
    major_label_font_size=34,
    value_font_size=28,
    legend_font_size=32,
    legend_font_family="DejaVu Sans, Helvetica, Arial, sans-serif",
    label_font_family="DejaVu Sans, Helvetica, Arial, sans-serif",
    major_label_font_family="DejaVu Sans, Helvetica, Arial, sans-serif",
    value_font_family="DejaVu Sans, Helvetica, Arial, sans-serif",
    opacity=0.55,
    opacity_hover=0.65,
    guide_stroke_color="#e0e0e0",
    guide_stroke_dasharray="3,3",
    major_guide_stroke_color="#cccccc",
    major_guide_stroke_dasharray="6,3",
    stroke_opacity=1.0,
    stroke_opacity_hover=1.0,
    tooltip_font_size=26,
    tooltip_font_family="DejaVu Sans, Helvetica, Arial, sans-serif",
    tooltip_border_radius=8,
)

# Chart - wider y-range to accommodate text labels above peaks
chart = pygal.XY(
    width=4800,
    height=2700,
    title="Bernese Oberland Traverse · area-elevation-profile · pygal · pyplots.ai",
    x_title="Distance (km)",
    y_title="Elevation (m)",
    style=custom_style,
    fill=True,
    show_dots=False,
    stroke_style={"width": 4},
    show_y_guides=True,
    show_x_guides=False,
    show_legend=True,
    legend_at_bottom=True,
    legend_box_size=26,
    value_formatter=lambda x: f"{x:,.0f} m",
    x_value_formatter=lambda x: f"{x:.0f} km",
    interpolate="cubic",
    interpolation_precision=300,
    min_scale=5,
    max_scale=10,
    margin_bottom=80,
    margin_left=100,
    margin_right=100,
    margin_top=60,
    spacing=12,
    tooltip_fancy_mode=True,
    range=(500, 2400),
    xrange=(0, 125),
)

# Elevation profile as filled XY series
profile_data = [
    {"value": (float(d), float(e)), "label": f"{d:.1f} km — {e:.0f} m"}
    for d, e in zip(distances_km, elevation_m, strict=True)
]
chart.add("Elevation Profile", profile_data)

# Landmark markers as separate series with visible dots
landmark_data = [
    {"value": (float(lm["km"]), lm["elev"]), "label": f"{lm['name']} — {lm['elev']:.0f} m"} for lm in landmarks
]
chart.add("Landmarks", landmark_data, fill=False, show_dots=True, dots_size=16, stroke=False)

# Save interactive HTML version
chart.render_to_file("plot.html")

# Render SVG, add text annotations and vertical markers, then convert to PNG
svg_bytes = chart.render()

# Parse SVG
SVG_NS = "http://www.w3.org/2000/svg"
XLINK_NS = "http://www.w3.org/1999/xlink"
ET.register_namespace("", SVG_NS)
ET.register_namespace("xlink", XLINK_NS)
root = ET.fromstring(svg_bytes)

# Build parent map to find circle parents (for coordinate-space matching)
parent_map = {child: parent for parent in root.iter() for child in parent}

# Find landmark circles (main series has show_dots=False, so only landmark dots exist)
landmark_circles = []
for elem in root.iter(f"{{{SVG_NS}}}circle"):
    r_val = elem.get("r", "0")
    try:
        if float(r_val) > 3:
            landmark_circles.append(elem)
    except ValueError:
        pass

# Sort circles left to right by cx
landmark_circles.sort(key=lambda c: float(c.get("cx", "0")))

# Find the bottom of the plot area by locating the lowest horizontal guide line
plot_bottom_y = 0
for line_elem in root.iter(f"{{{SVG_NS}}}line"):
    y1 = line_elem.get("y1", "0")
    y2 = line_elem.get("y2", "0")
    try:
        plot_bottom_y = max(plot_bottom_y, float(y1), float(y2))
    except ValueError:
        pass

# Add annotations as siblings of circles (same coordinate transform)
for i, circle in enumerate(landmark_circles[: len(landmarks)]):
    parent_elem = parent_map.get(circle)
    if parent_elem is None:
        continue

    cx = float(circle.get("cx", "0"))
    cy = float(circle.get("cy", "0"))
    lm = landmarks[i]

    # Determine tag namespace prefix
    ns_prefix = f"{{{SVG_NS}}}"

    # Vertical dashed marker line from dot down to plot bottom
    vline = ET.SubElement(parent_elem, f"{ns_prefix}line")
    vline.set("x1", f"{cx:.1f}")
    vline.set("y1", f"{cy:.1f}")
    vline.set("x2", f"{cx:.1f}")
    vline.set("y2", f"{plot_bottom_y:.1f}")
    vline.set("stroke", "#888888")
    vline.set("stroke-width", "2")
    vline.set("stroke-dasharray", "10,6")
    vline.set("opacity", "0.5")

    # Text anchor: left-align for start, right-align for end, center for middle
    anchor = "middle"
    dx = 0
    if i == 0:
        anchor = "start"
        dx = 8
    elif i == len(landmarks) - 1:
        anchor = "end"
        dx = -8

    # Landmark name label above the dot
    name_text = ET.SubElement(parent_elem, f"{ns_prefix}text")
    name_text.set("x", f"{cx + dx:.1f}")
    name_text.set("y", f"{cy - 45:.1f}")
    name_text.set("text-anchor", anchor)
    name_text.set("font-size", "30")
    name_text.set("font-family", "DejaVu Sans, Helvetica, Arial, sans-serif")
    name_text.set("fill", "#2d2d2d")
    name_text.set("font-weight", "bold")
    name_text.text = lm["name"]

    # Elevation label below the name
    elev_text = ET.SubElement(parent_elem, f"{ns_prefix}text")
    elev_text.set("x", f"{cx + dx:.1f}")
    elev_text.set("y", f"{cy - 22:.1f}")
    elev_text.set("text-anchor", anchor)
    elev_text.set("font-size", "26")
    elev_text.set("font-family", "DejaVu Sans, Helvetica, Arial, sans-serif")
    elev_text.set("fill", "#666666")
    elev_text.text = f"{lm['elev']:.0f} m"

# Convert modified SVG to PNG
modified_svg = ET.tostring(root, encoding="unicode")
cairosvg.svg2png(bytestring=modified_svg.encode("utf-8"), write_to="plot.png")
