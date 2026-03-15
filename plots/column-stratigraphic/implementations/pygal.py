"""pyplots.ai
column-stratigraphic: Stratigraphic Column with Lithology Patterns
Library: pygal | Python 3.13
Quality: pending | Created: 2026-03-15
"""

import cairosvg
import pygal
from pygal.style import Style


# Data: Synthetic sedimentary section (depth in meters, increasing downward)
layers = [
    {"top": 0, "bottom": 12, "lithology": "sandstone", "formation": "Red Mesa Fm", "age": "Eocene"},
    {"top": 12, "bottom": 25, "lithology": "shale", "formation": "Grey Basin Fm", "age": "Paleocene"},
    {"top": 25, "bottom": 38, "lithology": "limestone", "formation": "Chalk Bluff Fm", "age": "Paleocene"},
    {"top": 38, "bottom": 50, "lithology": "siltstone", "formation": "Iron Creek Mbr", "age": "Late Cretaceous"},
    {"top": 50, "bottom": 68, "lithology": "sandstone", "formation": "Canyon Wall Fm", "age": "Late Cretaceous"},
    {"top": 68, "bottom": 82, "lithology": "shale", "formation": "Dark Hollow Fm", "age": "Early Cretaceous"},
    {"top": 82, "bottom": 90, "lithology": "conglomerate", "formation": "Boulder Bed Mbr", "age": "Early Cretaceous"},
    {"top": 90, "bottom": 108, "lithology": "limestone", "formation": "Shell Bank Fm", "age": "Jurassic"},
    {"top": 108, "bottom": 118, "lithology": "mudstone", "formation": "Quiet Water Fm", "age": "Jurassic"},
    {"top": 118, "bottom": 135, "lithology": "dolomite", "formation": "Crystal Ridge Fm", "age": "Triassic"},
]

# Custom style
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#999999",
    colors=("#306998",),
    title_font_size=56,
    label_font_size=32,
    major_label_font_size=32,
    legend_font_size=28,
    value_font_size=24,
)

# Create a base chart as scaffolding
chart = pygal.Bar(
    width=4800,
    height=2700,
    style=custom_style,
    title="column-stratigraphic · pygal · pyplots.ai",
    show_legend=False,
    show_x_labels=False,
    show_y_labels=False,
    show_x_guides=False,
    show_y_guides=False,
    margin=60,
    margin_top=140,
    margin_bottom=100,
)

# Add dummy data to generate base SVG
chart.add("dummy", [0])

# Render base SVG
svg_string = chart.render().decode("utf-8")

# Layout constants
MARGIN_TOP = 200
MARGIN_BOTTOM = 100
AGE_COL_X = 350
DEPTH_COL_X = 650
COL_LEFT = 780
COL_WIDTH = 500
FORM_LABEL_X = COL_LEFT + COL_WIDTH + 80
PLOT_HEIGHT = 2700 - MARGIN_TOP - MARGIN_BOTTOM

total_depth = layers[-1]["bottom"]
scale = PLOT_HEIGHT / total_depth

# SVG pattern definitions for lithology types (injected inside existing <defs>)
patterns_inner = (
    '<pattern id="pat-sandstone" patternUnits="userSpaceOnUse" width="24" height="24">'
    '<rect width="24" height="24" fill="#FFD700"/>'
    '<circle cx="6" cy="6" r="2.5" fill="#B8860B" opacity="0.7"/>'
    '<circle cx="18" cy="18" r="2.5" fill="#B8860B" opacity="0.7"/>'
    '<circle cx="18" cy="6" r="1.8" fill="#B8860B" opacity="0.5"/>'
    '<circle cx="6" cy="18" r="1.8" fill="#B8860B" opacity="0.5"/>'
    '<circle cx="12" cy="12" r="1.5" fill="#B8860B" opacity="0.35"/>'
    "</pattern>"
    '<pattern id="pat-shale" patternUnits="userSpaceOnUse" width="36" height="14">'
    '<rect width="36" height="14" fill="#A9A9A9"/>'
    '<line x1="2" y1="7" x2="24" y2="7" stroke="#555" stroke-width="1.8"/>'
    "</pattern>"
    '<pattern id="pat-limestone" patternUnits="userSpaceOnUse" width="48" height="28">'
    '<rect width="48" height="28" fill="#87CEEB"/>'
    '<line x1="0" y1="0" x2="48" y2="0" stroke="#4169E1" stroke-width="1.4"/>'
    '<line x1="0" y1="14" x2="48" y2="14" stroke="#4169E1" stroke-width="1.4"/>'
    '<line x1="24" y1="0" x2="24" y2="14" stroke="#4169E1" stroke-width="1.4"/>'
    '<line x1="0" y1="14" x2="0" y2="28" stroke="#4169E1" stroke-width="1.4"/>'
    '<line x1="48" y1="14" x2="48" y2="28" stroke="#4169E1" stroke-width="1.4"/>'
    "</pattern>"
    '<pattern id="pat-siltstone" patternUnits="userSpaceOnUse" width="28" height="20">'
    '<rect width="28" height="20" fill="#D2B48C"/>'
    '<line x1="3" y1="5" x2="12" y2="5" stroke="#8B7355" stroke-width="1.4"/>'
    '<line x1="16" y1="12" x2="25" y2="12" stroke="#8B7355" stroke-width="1.4"/>'
    '<line x1="8" y1="17" x2="18" y2="17" stroke="#8B7355" stroke-width="1.4"/>'
    "</pattern>"
    '<pattern id="pat-conglomerate" patternUnits="userSpaceOnUse" width="36" height="36">'
    '<rect width="36" height="36" fill="#DEB887"/>'
    '<circle cx="10" cy="10" r="6" fill="none" stroke="#8B6914" stroke-width="1.8"/>'
    '<circle cx="26" cy="24" r="7" fill="none" stroke="#8B6914" stroke-width="1.8"/>'
    '<circle cx="6" cy="28" r="4" fill="none" stroke="#8B6914" stroke-width="1.8"/>'
    '<circle cx="24" cy="6" r="4" fill="none" stroke="#8B6914" stroke-width="1.8"/>'
    "</pattern>"
    '<pattern id="pat-mudstone" patternUnits="userSpaceOnUse" width="24" height="10">'
    '<rect width="24" height="10" fill="#B0B0B0"/>'
    '<line x1="0" y1="5" x2="24" y2="5" stroke="#606060" stroke-width="1"/>'
    "</pattern>"
    '<pattern id="pat-dolomite" patternUnits="userSpaceOnUse" width="28" height="28">'
    '<rect width="28" height="28" fill="#E6C8E6"/>'
    '<polyline points="14,2 26,14 14,26 2,14 14,2" fill="none" stroke="#8B008B" stroke-width="1.4"/>'
    "</pattern>"
)

# Build the stratigraphic column elements
elements = []

# Layer rectangles with lithology patterns
for layer in layers:
    y_top = MARGIN_TOP + layer["top"] * scale
    height = (layer["bottom"] - layer["top"]) * scale
    pat_id = f"pat-{layer['lithology']}"

    elements.append(
        f'<rect x="{COL_LEFT}" y="{y_top:.1f}" width="{COL_WIDTH}" '
        f'height="{height:.1f}" fill="url(#{pat_id})" '
        f'stroke="#333" stroke-width="2.5"/>'
    )

    # Formation name label (right side)
    label_y = y_top + height / 2
    elements.append(
        f'<text x="{FORM_LABEL_X}" y="{label_y:.1f}" '
        f'font-family="Consolas, monospace" font-size="34" fill="#333" '
        f'dominant-baseline="central">{layer["formation"]}</text>'
    )

    # Lithology type label (further right, smaller italic)
    elements.append(
        f'<text x="{FORM_LABEL_X + 440}" y="{label_y:.1f}" '
        f'font-family="Consolas, monospace" font-size="26" fill="#888" '
        f'dominant-baseline="central" font-style="italic">{layer["lithology"]}</text>'
    )

# Depth scale header
elements.append(
    f'<text x="{DEPTH_COL_X}" y="{MARGIN_TOP - 45}" '
    f'font-family="Consolas, monospace" font-size="34" fill="#333" '
    f'text-anchor="middle" font-weight="bold">Depth (m)</text>'
)

# Depth tick marks and labels every 10m
for depth in range(0, int(total_depth) + 1, 10):
    y_pos = MARGIN_TOP + depth * scale
    elements.append(
        f'<line x1="{COL_LEFT - 18}" y1="{y_pos:.1f}" '
        f'x2="{COL_LEFT}" y2="{y_pos:.1f}" stroke="#333" stroke-width="2.5"/>'
    )
    elements.append(
        f'<text x="{DEPTH_COL_X + 20}" y="{y_pos + 2:.1f}" '
        f'font-family="Consolas, monospace" font-size="30" fill="#333" '
        f'text-anchor="end" dominant-baseline="central">{depth}</text>'
    )

# Depth axis vertical line
elements.append(
    f'<line x1="{COL_LEFT}" y1="{MARGIN_TOP}" '
    f'x2="{COL_LEFT}" y2="{MARGIN_TOP + total_depth * scale:.1f}" '
    f'stroke="#333" stroke-width="2.5"/>'
)

# Age labels (left side) - group contiguous layers with same age
age_groups = []
current_age = layers[0]["age"]
current_top = layers[0]["top"]
for layer in layers:
    if layer["age"] != current_age:
        age_groups.append({"age": current_age, "top": current_top, "bottom": layer["top"]})
        current_age = layer["age"]
        current_top = layer["top"]
age_groups.append({"age": current_age, "top": current_top, "bottom": layers[-1]["bottom"]})

# Age header
elements.append(
    f'<text x="{AGE_COL_X - 40}" y="{MARGIN_TOP - 45}" '
    f'font-family="Consolas, monospace" font-size="34" fill="#333" '
    f'text-anchor="middle" font-weight="bold">Age</text>'
)

bracket_x = AGE_COL_X + 80
for group in age_groups:
    y_top = MARGIN_TOP + group["top"] * scale
    y_bottom = MARGIN_TOP + group["bottom"] * scale
    y_mid = (y_top + y_bottom) / 2

    # Bracket: vertical line + horizontal ticks
    elements.append(
        f'<line x1="{bracket_x}" y1="{y_top + 2:.1f}" '
        f'x2="{bracket_x}" y2="{y_bottom - 2:.1f}" '
        f'stroke="#555" stroke-width="2.5"/>'
    )
    elements.append(
        f'<line x1="{bracket_x - 12}" y1="{y_top + 2:.1f}" '
        f'x2="{bracket_x}" y2="{y_top + 2:.1f}" '
        f'stroke="#555" stroke-width="2.5"/>'
    )
    elements.append(
        f'<line x1="{bracket_x - 12}" y1="{y_bottom - 2:.1f}" '
        f'x2="{bracket_x}" y2="{y_bottom - 2:.1f}" '
        f'stroke="#555" stroke-width="2.5"/>'
    )

    # Age label (centered on bracket)
    elements.append(
        f'<text x="{AGE_COL_X - 40}" y="{y_mid:.1f}" '
        f'font-family="Consolas, monospace" font-size="28" fill="#555" '
        f'text-anchor="middle" dominant-baseline="central">{group["age"]}</text>'
    )

# Legend for lithology patterns
legend_x = 2600
legend_y = MARGIN_TOP + 30
legend_items = [
    ("sandstone", "Sandstone"),
    ("shale", "Shale"),
    ("limestone", "Limestone"),
    ("siltstone", "Siltstone"),
    ("conglomerate", "Conglomerate"),
    ("mudstone", "Mudstone"),
    ("dolomite", "Dolomite"),
]

elements.append(
    f'<text x="{legend_x}" y="{legend_y}" '
    f'font-family="Consolas, monospace" font-size="36" fill="#333" '
    f'font-weight="bold">Lithology Key</text>'
)

for i, (lith_key, lith_label) in enumerate(legend_items):
    row = i % 4
    col = i // 4
    lx = legend_x + col * 560
    ly = legend_y + 50 + row * 65

    elements.append(
        f'<rect x="{lx}" y="{ly}" width="48" height="36" '
        f'fill="url(#pat-{lith_key})" stroke="#333" stroke-width="1.5" rx="3"/>'
    )
    elements.append(
        f'<text x="{lx + 64}" y="{ly + 18}" '
        f'font-family="Consolas, monospace" font-size="28" fill="#333" '
        f'dominant-baseline="central">{lith_label}</text>'
    )

# Inject patterns and elements into SVG
all_elements = "\n".join(elements)
svg_output = svg_string.replace("<defs>", "<defs>" + patterns_inner, 1)
svg_output = svg_output.replace("</svg>", f"{all_elements}\n</svg>")
svg_output = svg_output.replace(">No data<", "><")

# Save
with open("plot.html", "w") as f:
    f.write(svg_output)

cairosvg.svg2png(bytestring=svg_output.encode(), write_to="plot.png")
