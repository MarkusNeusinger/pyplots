"""pyplots.ai
venn-basic: Venn Diagram
Library: pygal 3.1.0 | Python 3.13.11
Quality: 74/100 | Created: 2025-12-29
"""

import cairosvg
import numpy as np
import pygal
from pygal.style import Style


# Data: Three product categories with overlapping features
set_labels = ["Product A", "Product B", "Product C"]
set_sizes = [100, 80, 60]

# Overlaps: AB=30, AC=20, BC=25, ABC=10
ab_overlap = 30
ac_overlap = 20
bc_overlap = 25
abc_overlap = 10

# Calculate exclusive regions
only_a = set_sizes[0] - ab_overlap - ac_overlap + abc_overlap  # 60
only_b = set_sizes[1] - ab_overlap - bc_overlap + abc_overlap  # 35
only_c = set_sizes[2] - ac_overlap - bc_overlap + abc_overlap  # 25
only_ab = ab_overlap - abc_overlap  # 20
only_ac = ac_overlap - abc_overlap  # 10
only_bc = bc_overlap - abc_overlap  # 15

# Custom style for Venn diagram (scaled for 3600x3600 canvas)
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#FFD43B", "#4CAF50"),  # Python Blue, Python Yellow, Green
    opacity=0.4,
    opacity_hover=0.5,
    title_font_size=56,
    legend_font_size=32,
    label_font_size=28,
    major_label_font_size=24,
    value_font_size=32,
    stroke_width=4,
)

# Create XY chart with larger margins to prevent label cut-off
chart = pygal.XY(
    width=3600,
    height=3600,
    style=custom_style,
    fill=True,
    stroke=True,
    show_dots=False,
    show_legend=True,
    legend_at_bottom=True,
    legend_box_size=28,
    title="venn-basic · pygal · pyplots.ai",
    show_x_guides=False,
    show_y_guides=False,
    show_x_labels=False,
    show_y_labels=False,
    x_title=None,
    y_title=None,
    margin=150,  # Increased margin to prevent label cut-off
    spacing=15,
    explicit_size=True,
)

# Circle parameters for 3-set Venn diagram
r = 1.0
n_points = 150
theta = np.linspace(0, 2 * np.pi, n_points)

# Circle centers in equilateral triangle arrangement (tighter to fit within margins)
cx_a, cy_a = -0.5, 0.3  # Top left
cx_b, cy_b = 0.5, 0.3  # Top right
cx_c, cy_c = 0.0, -0.5  # Bottom center

# Generate circle points for each set
circle_a = [(cx_a + r * np.cos(t), cy_a + r * np.sin(t)) for t in theta]
circle_b = [(cx_b + r * np.cos(t), cy_b + r * np.sin(t)) for t in theta]
circle_c = [(cx_c + r * np.cos(t), cy_c + r * np.sin(t)) for t in theta]

# Add circles as series (legend shows set sizes)
chart.add(f"{set_labels[0]} (n={set_sizes[0]})", circle_a)
chart.add(f"{set_labels[1]} (n={set_sizes[1]})", circle_b)
chart.add(f"{set_labels[2]} (n={set_sizes[2]})", circle_c)

# Render to SVG
svg_content = chart.render().decode("utf-8")

# Coordinate transformation: scale data coordinates to SVG pixels
scale = 3600 * 0.30  # Scale factor for data to SVG conversion
center_x = 3600 / 2
center_y = 3600 / 2 - 50

# Region count labels (positioned inside each region)
count_style = 'font-size="52px" font-weight="bold" fill="#222" text-anchor="middle" dominant-baseline="middle"'
name_style = 'font-size="40px" font-weight="bold" fill="#333" text-anchor="middle" dominant-baseline="middle"'

labels = [
    # Region counts
    (center_x + (cx_a - 0.4) * scale, center_y - (cy_a + 0.3) * scale, str(only_a), count_style),
    (center_x + (cx_b + 0.4) * scale, center_y - (cy_b + 0.3) * scale, str(only_b), count_style),
    (center_x + cx_c * scale, center_y - (cy_c - 0.5) * scale, str(only_c), count_style),
    (center_x, center_y - (cy_a + 0.45) * scale, str(only_ab), count_style),
    (
        center_x + ((cx_a + cx_c) / 2 - 0.25) * scale,
        center_y - ((cy_a + cy_c) / 2 - 0.1) * scale,
        str(only_ac),
        count_style,
    ),
    (
        center_x + ((cx_b + cx_c) / 2 + 0.25) * scale,
        center_y - ((cy_b + cy_c) / 2 - 0.1) * scale,
        str(only_bc),
        count_style,
    ),
    (center_x, center_y, str(abc_overlap), count_style),
    # Set name labels (positioned inside circles, near top edge - not outside)
    (center_x + cx_a * scale, center_y - (cy_a + 0.75) * scale, set_labels[0], name_style),
    (center_x + cx_b * scale, center_y - (cy_b + 0.75) * scale, set_labels[1], name_style),
    (center_x + cx_c * scale, center_y - (cy_c - 0.85) * scale, set_labels[2], name_style),
]

# Build and insert SVG text elements
text_elements = "\n".join(f'<text x="{x:.0f}" y="{y:.0f}" {s}>{v}</text>' for x, y, v, s in labels)
svg_content = svg_content.replace("</svg>", f"{text_elements}\n</svg>")

# Save SVG (with labels)
with open("plot.svg", "w", encoding="utf-8") as f:
    f.write(svg_content)

# Render to PNG using cairosvg (includes the manually added labels)
cairosvg.svg2png(bytestring=svg_content.encode("utf-8"), write_to="plot.png")

# Create interactive HTML version
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>venn-basic - pygal - pyplots.ai</title>
    <style>
        body {{ margin: 0; padding: 20px; background: #f5f5f5; display: flex; justify-content: center; }}
        svg {{ max-width: 100%; height: auto; }}
    </style>
</head>
<body>
    {svg_content}
</body>
</html>"""

with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)
