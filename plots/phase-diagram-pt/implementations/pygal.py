"""pyplots.ai
phase-diagram-pt: Thermodynamic Phase Diagram (Pressure-Temperature)
Library: pygal 3.1.0 | Python 3.14.3
Quality: 77/100 | Created: 2026-03-14
"""

import xml.etree.ElementTree as ET

import cairosvg
import numpy as np
import pygal
from pygal.style import Style


# Data - Water phase diagram (realistic values)
# Triple point: 273.16 K, 611.73 Pa (0.00604 atm)
# Critical point: 647.1 K, 22.064 MPa (217.7 atm)
triple_t = 273.16
triple_p = 611.73
critical_t = 647.1
critical_p = 22.064e6

# Solid-gas boundary (sublimation curve) - Clausius-Clapeyron approximation
sublimation_temps = np.linspace(200, triple_t, 80)
L_sub = 51059  # J/mol (sublimation enthalpy of water)
R = 8.314
sublimation_pressures = triple_p * np.exp((L_sub / R) * (1 / triple_t - 1 / sublimation_temps))

# Liquid-gas boundary (vaporization curve) - from triple point to critical point
vaporization_temps = np.linspace(triple_t, critical_t, 100)
L_vap = 40700  # J/mol (vaporization enthalpy of water)
vaporization_pressures = triple_p * np.exp((L_vap / R) * (1 / triple_t - 1 / vaporization_temps))

# Solid-liquid boundary (melting curve) - water has negative slope
melting_pressures = np.logspace(np.log10(triple_p), np.log10(critical_p * 5), 80)
melting_temps = triple_t - (melting_pressures - triple_p) * 7.5e-8

# Style - refined palette with stronger visual hierarchy
custom_style = Style(
    background="white",
    plot_background="#fafbfc",
    foreground="#1a1a2e",
    foreground_strong="#1a1a2e",
    foreground_subtle="#e8e8e8",
    colors=(
        "#2563eb",  # Solid-Gas (sublimation) - Vivid Blue
        "#dc6b18",  # Liquid-Gas (vaporization) - Warm Orange
        "#0d9488",  # Solid-Liquid (melting) - Teal
        "#e11d48",  # Triple point - Rose
        "#7c3aed",  # Critical point - Violet
    ),
    font_family="DejaVu Sans, Helvetica, Arial, sans-serif",
    title_font_family="DejaVu Sans, Helvetica, Arial, sans-serif",
    title_font_size=56,
    label_font_size=38,
    major_label_font_size=34,
    value_font_size=28,
    legend_font_size=32,
    legend_font_family="DejaVu Sans, Helvetica, Arial, sans-serif",
    label_font_family="DejaVu Sans, Helvetica, Arial, sans-serif",
    major_label_font_family="DejaVu Sans, Helvetica, Arial, sans-serif",
    value_font_family="DejaVu Sans, Helvetica, Arial, sans-serif",
    stroke_width=5,
    opacity=0.95,
    opacity_hover=1.0,
    guide_stroke_color="#e0e0e0",
    guide_stroke_dasharray="4,4",
    tooltip_font_size=28,
    tooltip_font_family="DejaVu Sans, Helvetica, Arial, sans-serif",
    tooltip_border_radius=8,
)

# Chart - extended x-range to avoid clipping critical point
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="Water Phase Diagram · phase-diagram-pt · pygal · pyplots.ai",
    x_title="Temperature (K)",
    y_title="Pressure (Pa)",
    show_legend=True,
    legend_at_bottom=True,
    legend_box_size=24,
    dots_size=2,
    stroke=True,
    show_x_guides=True,
    show_y_guides=True,
    x_label_rotation=0,
    logarithmic=True,
    explicit_size=True,
    truncate_legend=-1,
    spacing=20,
    margin=40,
    margin_bottom=130,
    margin_left=120,
    margin_right=80,
    tooltip_fancy_mode=True,
    interpolate="cubic",
    interpolation_precision=200,
    xrange=(190, 710),
    secondary_range=(0.1, critical_p * 15),
    print_values=False,
)

# Sublimation curve (Solid-Gas boundary)
sublimation_points = [(float(t), float(p)) for t, p in zip(sublimation_temps, sublimation_pressures, strict=True)]
chart.add(
    "Solid ↔ Gas (Sublimation)",
    sublimation_points,
    show_dots=False,
    stroke_style={"width": 7, "linecap": "round", "linejoin": "round"},
)

# Vaporization curve (Liquid-Gas boundary)
vaporization_points = [(float(t), float(p)) for t, p in zip(vaporization_temps, vaporization_pressures, strict=True)]
chart.add(
    "Liquid ↔ Gas (Vaporization)",
    vaporization_points,
    show_dots=False,
    stroke_style={"width": 7, "linecap": "round", "linejoin": "round"},
)

# Melting curve (Solid-Liquid boundary) - nearly vertical, negative slope for water
melting_points = [(float(t), float(p)) for t, p in zip(melting_temps, melting_pressures, strict=True)]
chart.add(
    "Solid ↔ Liquid (Melting)",
    melting_points,
    show_dots=False,
    stroke_style={"width": 7, "linecap": "round", "linejoin": "round"},
)

# Triple point marker - prominent
chart.add(
    f"Triple Point ({triple_t} K, {triple_p:.0f} Pa)",
    [{"value": (float(triple_t), float(triple_p)), "label": "Triple Point: All three phases coexist"}],
    dots_size=22,
    stroke=False,
)

# Critical point marker - prominent
chart.add(
    f"Critical Point ({critical_t} K, {critical_p / 1e6:.1f} MPa)",
    [{"value": (float(critical_t), float(critical_p)), "label": "Critical Point: Liquid-gas distinction vanishes"}],
    dots_size=22,
    stroke=False,
)

# Render SVG and inject phase region labels
svg_string = chart.render(is_unicode=True)

# Parse SVG to add phase region text labels
root = ET.fromstring(svg_string)
ns = {"svg": "http://www.w3.org/2000/svg"}

# Find the plot area to calculate label positions
# pygal uses a viewBox-based coordinate system at 4800x2700
# The plot area is roughly from x=120 to x=4720, y=80 to y=2400
# Phase regions in data coordinates (approximate pixel positions):
# - SOLID region: left side, upper area (low T, high P)
# - LIQUID region: center-right, upper area (medium T, high P)
# - GAS region: center-right, lower area (high T, low P)
# - SUPERCRITICAL: far right, upper area (beyond critical point)

# Find all graph-related groups to append labels
graphs = root.findall(".//{http://www.w3.org/2000/svg}g[@class='plot overlay']")
if not graphs:
    graphs = root.findall(".//{http://www.w3.org/2000/svg}g")

# We'll add text elements directly to the root SVG
# Phase label positions (approximate pixel coordinates in the 4800x2700 canvas)
phase_labels = [
    {"text": "SOLID", "x": "1050", "y": "600", "size": "72", "color": "#1a1a2e"},
    {"text": "LIQUID", "x": "2600", "y": "550", "size": "72", "color": "#1a1a2e"},
    {"text": "GAS", "x": "2800", "y": "1900", "size": "72", "color": "#1a1a2e"},
    {"text": "SUPERCRITICAL", "x": "3700", "y": "420", "size": "48", "color": "#6b7280"},
    {"text": "FLUID", "x": "3830", "y": "490", "size": "48", "color": "#6b7280"},
]

for label in phase_labels:
    text_elem = ET.SubElement(root, "{http://www.w3.org/2000/svg}text")
    text_elem.set("x", label["x"])
    text_elem.set("y", label["y"])
    text_elem.set(
        "style",
        f"font-family: DejaVu Sans, Helvetica, Arial, sans-serif; "
        f"font-size: {label['size']}px; "
        f"fill: {label['color']}; "
        f"font-weight: 600; "
        f"letter-spacing: 4px; "
        f"opacity: 0.55; "
        f"text-anchor: middle;",
    )
    text_elem.text = label["text"]

# Write modified SVG and convert to PNG
modified_svg = ET.tostring(root, encoding="unicode")
with open("plot.svg", "w") as f:
    f.write(modified_svg)

cairosvg.svg2png(bytestring=modified_svg.encode("utf-8"), write_to="plot.png", output_width=4800, output_height=2700)

# Also save interactive HTML version
chart.render_to_file("plot.html")
