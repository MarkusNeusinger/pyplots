"""pyplots.ai
chernoff-basic: Chernoff Faces for Multivariate Data
Library: pygal | Python 3.13
Quality: pending | Created: 2025-12-31
"""

import xml.etree.ElementTree as ET

import cairosvg
import numpy as np
import pygal
from pygal.style import Style


# Set seed for reproducibility
np.random.seed(42)

# Data - Car performance metrics (5 cars, 7 attributes each)
# Attributes: Engine Power, Fuel Efficiency, Safety Rating, Comfort, Reliability, Price Value, Handling
car_names = ["Sedan A", "SUV B", "Sports C", "Compact D", "Luxury E"]

# Normalized data (0-1 scale) for each car's attributes
# Each row: [face_width, face_height, eye_size, eye_spacing, mouth_curve, nose_length, eyebrow_slant]
car_data = np.array(
    [
        [0.6, 0.5, 0.7, 0.5, 0.8, 0.4, 0.5],  # Sedan A - balanced, happy
        [0.8, 0.7, 0.5, 0.6, 0.4, 0.7, 0.3],  # SUV B - large, serious
        [0.4, 0.6, 0.9, 0.4, 0.9, 0.3, 0.7],  # Sports C - narrow, excited
        [0.5, 0.4, 0.6, 0.5, 0.6, 0.5, 0.5],  # Compact D - small, neutral
        [0.7, 0.8, 0.8, 0.7, 0.7, 0.6, 0.6],  # Luxury E - large, pleasant
    ]
)

# Group colors for cars (colorblind-safe palette)
face_colors = ["#306998", "#FFD43B", "#4ECDC4", "#FF7043", "#9C88FF"]

# SVG namespace
SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)


def add_element(parent, tag, **attrs):
    """Add SVG element with namespace and attributes."""
    elem = ET.SubElement(parent, f"{{{SVG_NS}}}{tag}")
    for key, val in attrs.items():
        elem.set(key.replace("_", "-"), str(val))
    return elem


def draw_chernoff_face(parent, cx, cy, data, color, label, face_size=200):
    """Draw a single Chernoff face at position (cx, cy) based on normalized data [0-1]."""
    # Unpack facial feature parameters from data - scaled for face_size
    scale = face_size / 200  # Base scale factor
    face_width_factor = 0.6 + data[0] * 0.4  # 0.6-1.0
    face_height_factor = 0.6 + data[1] * 0.4  # 0.6-1.0
    eye_size = (12 + data[2] * 28) * scale  # Scaled eye size
    eye_spacing = (30 + data[3] * 40) * scale  # Scaled eye spacing
    mouth_curve = (-50 + data[4] * 100) * scale  # More pronounced mouth curve
    nose_length = (20 + data[5] * 35) * scale  # Scaled nose length
    eyebrow_slant = -20 + data[6] * 40  # -20 to +20 degrees (more variation)

    face_width = face_size * face_width_factor * 0.45
    face_height = face_size * face_height_factor * 0.55

    # Create group for this face
    face_group = add_element(parent, "g", id=f"face-{label.replace(' ', '-')}")

    # Face outline (ellipse)
    add_element(
        face_group,
        "ellipse",
        cx=cx,
        cy=cy,
        rx=face_width,
        ry=face_height,
        fill=color,
        fill_opacity="0.3",
        stroke=color,
        stroke_width=max(4, 3 * scale),
    )

    # Left eye
    left_eye_x = cx - eye_spacing * 0.5
    left_eye_y = cy - face_height * 0.2
    add_element(
        face_group,
        "circle",
        cx=left_eye_x,
        cy=left_eye_y,
        r=eye_size,
        fill="white",
        stroke="#333",
        stroke_width=max(3, 2.5 * scale),
    )
    # Left pupil
    add_element(face_group, "circle", cx=left_eye_x, cy=left_eye_y, r=eye_size * 0.4, fill="#333")

    # Right eye
    right_eye_x = cx + eye_spacing * 0.5
    right_eye_y = cy - face_height * 0.2
    add_element(
        face_group,
        "circle",
        cx=right_eye_x,
        cy=right_eye_y,
        r=eye_size,
        fill="white",
        stroke="#333",
        stroke_width=max(3, 2.5 * scale),
    )
    # Right pupil
    add_element(face_group, "circle", cx=right_eye_x, cy=right_eye_y, r=eye_size * 0.4, fill="#333")

    # Eyebrows
    brow_length = eye_size * 2.2
    brow_y_offset = eye_size + 20 * scale
    slant_offset = np.tan(np.radians(eyebrow_slant)) * brow_length * 0.5

    # Left eyebrow
    add_element(
        face_group,
        "line",
        x1=left_eye_x - brow_length * 0.5,
        y1=left_eye_y - brow_y_offset + slant_offset,
        x2=left_eye_x + brow_length * 0.5,
        y2=left_eye_y - brow_y_offset - slant_offset,
        stroke="#333",
        stroke_width=max(5, 4 * scale),
        stroke_linecap="round",
    )

    # Right eyebrow (mirrored slant)
    add_element(
        face_group,
        "line",
        x1=right_eye_x - brow_length * 0.5,
        y1=right_eye_y - brow_y_offset - slant_offset,
        x2=right_eye_x + brow_length * 0.5,
        y2=right_eye_y - brow_y_offset + slant_offset,
        stroke="#333",
        stroke_width=max(5, 4 * scale),
        stroke_linecap="round",
    )

    # Nose (vertical line)
    add_element(
        face_group,
        "line",
        x1=cx,
        y1=cy - nose_length * 0.3,
        x2=cx,
        y2=cy + nose_length * 0.5,
        stroke="#333",
        stroke_width=max(4, 3.5 * scale),
        stroke_linecap="round",
    )

    # Mouth (quadratic bezier curve)
    mouth_y = cy + face_height * 0.45
    mouth_width = face_width * 0.55
    mouth_path = f"M {cx - mouth_width} {mouth_y} Q {cx} {mouth_y + mouth_curve} {cx + mouth_width} {mouth_y}"
    add_element(
        face_group,
        "path",
        d=mouth_path,
        fill="none",
        stroke="#333",
        stroke_width=max(5, 4 * scale),
        stroke_linecap="round",
    )

    # Label below face
    text_elem = add_element(
        face_group,
        "text",
        x=cx,
        y=cy + face_height + 70,
        text_anchor="middle",
        font_family="sans-serif",
        font_size=max(36, 28 * scale),
        font_weight="bold",
        fill="#333",
    )
    text_elem.text = label


# Custom style for pygal
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=tuple(face_colors),
    title_font_size=72,
    label_font_size=36,
    major_label_font_size=32,
    legend_font_size=36,
    value_font_size=28,
)

# Create a base pygal XY chart to leverage its SVG rendering infrastructure
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    show_legend=False,
    show_x_guides=False,
    show_y_guides=False,
    show_x_labels=False,
    show_y_labels=False,
    show_dots=False,  # Hide the dummy dots
    margin=50,
    no_data_text="",  # Hide "No data" message
)

# Add dummy data to create valid chart structure (hidden)
chart.add("", [])

# Render to SVG string
svg_string = chart.render().decode("utf-8")

# Parse SVG and add custom Chernoff faces
svg_tree = ET.fromstring(svg_string)

# Create faces group
faces_group = add_element(svg_tree, "g", id="chernoff-faces")

# Calculate face positions in a grid (5 faces in a row)
cols = 5
face_size = 500  # Larger faces for better visibility
margin_x = 500
spacing_x = (4800 - 2 * margin_x) / (cols - 1) if cols > 1 else 0

# Draw each Chernoff face
for i, (name, data, color) in enumerate(zip(car_names, car_data, face_colors, strict=True)):
    col = i % cols
    cx = margin_x + col * spacing_x
    cy = 1100  # Center faces vertically
    draw_chernoff_face(faces_group, cx, cy, data, color, name, face_size)

# Add title
title_elem = add_element(
    svg_tree,
    "text",
    x="2400",
    y="100",
    text_anchor="middle",
    font_family="sans-serif",
    font_size="72",
    font_weight="bold",
    fill="#333",
)
title_elem.text = "Car Performance Comparison · chernoff-basic · pygal · pyplots.ai"

# Add legend for attributes
legend_y = 2100
legend_x_start = 400

legend_title = add_element(
    svg_tree,
    "text",
    x=str(legend_x_start),
    y=str(legend_y),
    font_family="sans-serif",
    font_size="44",
    font_weight="bold",
    fill="#333",
)
legend_title.text = "Feature Mappings:"

feature_mappings = [
    "Face Width = Engine Power",
    "Face Height = Fuel Efficiency",
    "Eye Size = Safety Rating",
    "Eye Spacing = Comfort",
    "Mouth Curve = Reliability",
    "Nose Length = Price Value",
    "Eyebrow Slant = Handling",
]

# Add feature mappings as legend items (two rows)
for i, mapping in enumerate(feature_mappings):
    row = i // 4
    col = i % 4
    text_elem = add_element(
        svg_tree,
        "text",
        x=str(legend_x_start + col * 1150),
        y=str(legend_y + 80 + row * 70),
        font_family="sans-serif",
        font_size="36",
        fill="#555",
    )
    text_elem.text = mapping

# Convert back to string
final_svg = ET.tostring(svg_tree, encoding="unicode")

# Add XML declaration
final_svg = '<?xml version="1.0" encoding="UTF-8"?>\n' + final_svg

# Save as SVG file
with open("plot.svg", "w") as f:
    f.write(final_svg)

# Use cairosvg to convert to PNG
cairosvg.svg2png(bytestring=final_svg.encode(), write_to="plot.png", output_width=4800, output_height=2700)

# Save HTML for interactive version
with open("plot.html", "w") as f:
    f.write(
        """<!DOCTYPE html>
<html>
<head>
    <title>chernoff-basic · pygal · pyplots.ai</title>
    <style>
        body { margin: 0; padding: 20px; background: #f5f5f5; font-family: sans-serif; }
        .container { max-width: 100%; margin: 0 auto; }
        h1 { text-align: center; color: #333; }
        object { width: 100%; height: auto; }
    </style>
</head>
<body>
    <div class="container">
        <object type="image/svg+xml" data="plot.svg">
            Chernoff faces visualization not supported
        </object>
    </div>
</body>
</html>"""
    )
