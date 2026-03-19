"""pyplots.ai
line-growth-percentile: Pediatric Growth Chart with Percentile Curves
Library: pygal 3.1.0 | Python 3.14.3
Quality: 77/100 | Created: 2026-03-19
"""

import io
import xml.etree.ElementTree as ET

import cairosvg
import numpy as np
import pygal
from PIL import Image, ImageDraw, ImageFont
from pygal.style import Style


# Data - WHO-style weight-for-age reference for boys, 0-36 months
np.random.seed(42)
age_months = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 18, 21, 24, 27, 30, 33, 36])

# Synthetic percentile reference data approximating WHO weight-for-age (boys, kg)
percentile_50 = np.array(
    [3.3, 4.5, 5.6, 6.4, 7.0, 7.5, 7.9, 8.3, 8.6, 8.9, 9.2, 9.4, 9.6, 10.3, 10.9, 11.5, 12.2, 12.7, 13.3, 13.8, 14.3]
)
offsets = {
    3: np.linspace(1.1, 3.2, len(age_months)),
    10: np.linspace(0.85, 2.5, len(age_months)),
    25: np.linspace(0.55, 1.5, len(age_months)),
    75: np.linspace(0.55, 1.5, len(age_months)),
    90: np.linspace(0.85, 2.5, len(age_months)),
    97: np.linspace(1.1, 3.2, len(age_months)),
}

percentile_3 = percentile_50 - offsets[3]
percentile_10 = percentile_50 - offsets[10]
percentile_25 = percentile_50 - offsets[25]
percentile_75 = percentile_50 + offsets[75]
percentile_90 = percentile_50 + offsets[90]
percentile_97 = percentile_50 + offsets[97]

# Individual patient data - a boy tracking between 25th and 50th percentiles
patient_ages = np.array([0, 1, 2, 4, 6, 9, 12, 15, 18, 24, 30, 36])
patient_weights = np.array([3.2, 4.3, 5.3, 6.7, 7.5, 8.5, 9.3, 10.0, 10.5, 11.8, 12.8, 13.7])

# Percentile values at age 36 for right-margin labels
percentile_labels = [
    ("P3", float(percentile_3[-1])),
    ("P10", float(percentile_10[-1])),
    ("P25", float(percentile_25[-1])),
    ("P50", float(percentile_50[-1])),
    ("P75", float(percentile_75[-1])),
    ("P90", float(percentile_90[-1])),
    ("P97", float(percentile_97[-1])),
]

# Style - blue tones for boys chart
custom_style = Style(
    background="white",
    plot_background="#FAFCFF",
    foreground="#2C3E50",
    foreground_strong="#1A252F",
    foreground_subtle="#D5D8DC",
    guide_stroke_color="#E8EDF2",
    guide_stroke_dasharray="4,6",
    colors=(
        "#D6EAF8",  # P3-P10 band (lightest blue)
        "#AED6F1",  # P10-P25 band
        "#85C1E9",  # P25-P50 band
        "#85C1E9",  # P50-P75 band
        "#AED6F1",  # P75-P90 band
        "#D6EAF8",  # P90-P97 band
        "#154360",  # P50 median line (dark navy)
        "#C0392B",  # Patient data (bold red)
    ),
    opacity=".55",
    opacity_hover=".80",
    stroke_opacity="1",
    stroke_opacity_hover="1",
    title_font_size=58,
    label_font_size=40,
    major_label_font_size=42,
    legend_font_size=36,
    value_font_size=36,
    value_colors=("transparent",),
    tooltip_font_size=32,
    font_family='Helvetica, Arial, "DejaVu Sans", sans-serif',
)

# Chart
chart = pygal.XY(
    style=custom_style,
    width=4800,
    height=2700,
    explicit_size=True,
    title="WHO Weight-for-Age (Boys) · line-growth-percentile · pygal · pyplots.ai",
    x_title="Age (months)",
    y_title="Weight (kg)",
    show_dots=True,
    dots_size=0,
    show_x_guides=False,
    show_y_guides=True,
    fill=True,
    stroke=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=4,
    legend_box_size=28,
    truncate_legend=-1,
    range=(0, 20),
    x_labels=[0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36],
    x_labels_major=[0, 6, 12, 18, 24, 30, 36],
    show_minor_x_labels=True,
    show_minor_y_labels=False,
    y_labels=list(range(2, 21, 2)),
    print_values=False,
    x_value_formatter=lambda x: f"{x:.0f}",
    value_formatter=lambda x: f"{x:.1f}",
    tooltip_border_radius=8,
    margin_top=30,
    margin_bottom=50,
    margin_left=30,
    margin_right=60,
    spacing=18,
    js=[],
)

# Percentile bands as filled polygons (upper forward, lower reversed)
band_configs = [
    ("P3–P10", percentile_3, percentile_10),
    ("P10–P25", percentile_10, percentile_25),
    ("P25–P50", percentile_25, percentile_50),
    ("P50–P75", percentile_50, percentile_75),
    ("P75–P90", percentile_75, percentile_90),
    ("P90–P97", percentile_90, percentile_97),
]

for label, lower, upper in band_configs:
    polygon = [(float(a), float(u)) for a, u in zip(age_months, upper, strict=True)]
    for a, lo in zip(reversed(age_months), reversed(lower), strict=True):
        polygon.append((float(a), float(lo)))
    chart.add(label, polygon, stroke_style={"width": 0.5, "opacity": 0.1})

# P50 median line - strongly emphasized with dark navy, dashed for distinction
median_data = [(float(a), float(v)) for a, v in zip(age_months, percentile_50, strict=True)]
chart.add(
    "P50 (Median)",
    median_data,
    fill=False,
    stroke=True,
    dots_size=0,
    stroke_style={"width": 7, "linecap": "round", "linejoin": "round", "dasharray": "12,6"},
)

# Patient data - bold connected markers with prominent dots
patient_data = [(float(a), float(w)) for a, w in zip(patient_ages, patient_weights, strict=True)]
chart.add(
    "Patient",
    patient_data,
    fill=False,
    stroke=True,
    dots_size=12,
    stroke_style={"width": 5.5, "linecap": "round", "linejoin": "round"},
)

# Render SVG, add percentile labels via SVG text elements, convert to PNG
svg_data = chart.render()

# Parse SVG to add right-margin percentile labels
ET.register_namespace("", "http://www.w3.org/2000/svg")
ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")
tree = ET.ElementTree(ET.fromstring(svg_data))
root = tree.getroot()
ns = {"svg": "http://www.w3.org/2000/svg"}

# Find plot area bounds from the SVG structure
plot_area = root.find(".//svg:g[@class='plot overlay']", ns)
if plot_area is None:
    plot_area = root.find(".//{http://www.w3.org/2000/svg}g[@class='plot overlay']")

# Render base chart to PNG via cairosvg
png_bytes = cairosvg.svg2png(bytestring=svg_data, output_width=4800, output_height=2700)
img = Image.open(io.BytesIO(png_bytes)).convert("RGBA")

# Add percentile labels on the right margin using PIL
draw = ImageDraw.Draw(img)
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
except OSError:
    font = ImageFont.load_default()

# Map percentile values to pixel y-coordinates
# Chart plot area: approximate from the rendered image
# Y range is 0-20 kg, plot area is roughly between y=80px (top) and y=2340px (bottom)
y_min_val, y_max_val = 0.0, 20.0
plot_top_px = 110
plot_bottom_px = 2340
right_edge_px = 4680

for label, val in percentile_labels:
    frac = (val - y_min_val) / (y_max_val - y_min_val)
    y_px = int(plot_bottom_px - frac * (plot_bottom_px - plot_top_px))
    color = "#154360" if label == "P50" else "#5D6D7E"
    draw.text((right_edge_px, y_px - 18), label, fill=color, font=font)

img = img.convert("RGB")
img.save("plot.png", dpi=(150, 150))

# Also save HTML version
chart.render_to_file("plot.html")
