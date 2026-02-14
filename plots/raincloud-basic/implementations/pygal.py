""" pyplots.ai
raincloud-basic: Basic Raincloud Plot
Library: pygal 3.1.0 | Python 3.14
Quality: 84/100 | Created: 2025-12-25
"""

import re

import cairosvg
import numpy as np
import pygal
from pygal.style import Style


# Data - Reaction times (ms) for different treatment groups
np.random.seed(42)
data = {
    "Control": np.random.normal(450, 80, 60),
    "Treatment A": np.random.normal(380, 60, 55),
    "Treatment B": np.random.normal(320, 50, 50),
}

# Add realistic outliers
data["Control"] = np.append(data["Control"], [650, 680, 250])
data["Treatment A"] = np.append(data["Treatment A"], [550, 200])
data["Treatment B"] = np.append(data["Treatment B"], [480, 180])

# Group colors - colorblind-safe palette
group_colors = ["#306998", "#FFD43B", "#4CAF50"]

# Build color sequence: per group = rain, box_outline, median_line
series_colors = []
for gc in group_colors:
    series_colors.extend([gc, gc, gc])

# Custom style
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#aaaaaa",
    guide_stroke_color="#e0e0e0",
    guide_stroke_dasharray="4,4",
    colors=tuple(series_colors),
    title_font_size=84,
    label_font_size=54,
    major_label_font_size=48,
    legend_font_size=48,
    value_font_size=40,
    tooltip_font_size=36,
    opacity=0.60,
    opacity_hover=0.85,
)

# Create HORIZONTAL XY chart (fill=False; clouds rendered via SVG post-processing)
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="raincloud-basic · pygal · pyplots.ai",
    x_title="Reaction Time (ms)",
    y_title="",
    show_legend=False,
    stroke=True,
    fill=False,
    dots_size=0,
    show_x_guides=True,
    show_y_guides=False,
    xrange=(100, 750),
    range=(-0.2, 4.2),
    margin=40,
    margin_left=340,
    margin_right=100,
    margin_top=120,
    margin_bottom=120,
    explicit_size=True,
)

# Raincloud layout parameters
cloud_height = 0.30
rain_offset = -0.35
n_kde_points = 80
box_hw = 0.14  # box half-width — thicker for visibility

# Store cloud polygon and box data for SVG injection
cloud_polygons = []
box_rects = []

for i, (category, values) in enumerate(data.items()):
    center_y = i + 1
    values = np.array(values)

    # --- Half-Violin KDE (cloud) - compute for later SVG injection ---
    n = len(values)
    std = np.std(values)
    iqr_val = np.percentile(values, 75) - np.percentile(values, 25)
    bandwidth = 0.9 * min(std, iqr_val / 1.34) * n ** (-0.2)

    x_min, x_max = values.min(), values.max()
    padding = (x_max - x_min) * 0.1
    x_kde = np.linspace(x_min - padding, x_max + padding, n_kde_points)

    # Gaussian KDE
    density = np.zeros_like(x_kde)
    for v in values:
        density += np.exp(-0.5 * ((x_kde - v) / bandwidth) ** 2)
    density /= n * bandwidth * np.sqrt(2 * np.pi)

    # Trim KDE tails where density < 5% of peak for clean cloud edges
    peak = density.max()
    above = np.where(density > peak * 0.05)[0]
    x_kde = x_kde[above[0] : above[-1] + 1]
    density = density[above[0] : above[-1] + 1]

    # Normalize density to cloud_height
    density_scaled = density / density.max() * cloud_height

    # Store polygon data points (data coords) for SVG injection
    poly_data = [(float(x_kde[0]), float(center_y))]
    poly_data += [(float(x), float(center_y + d)) for x, d in zip(x_kde, density_scaled, strict=True)]
    poly_data.append((float(x_kde[-1]), float(center_y)))
    cloud_polygons.append((group_colors[i], poly_data))

    # --- Jittered Points (rain) - falls DOWNWARD from category line ---
    np.random.seed(42 + i)
    jitter = np.random.uniform(-0.08, 0.08, len(values))
    rain_points = [
        {"value": (float(v), center_y + rain_offset + float(j)), "label": f"{category}: {v:.0f} ms"}
        for j, v in zip(jitter, values, strict=True)
    ]
    chart.add(f"{category} rain", rain_points, stroke=False, fill=False, dots_size=28)

    # --- Box Plot (centered at category line) ---
    median = float(np.median(values))
    q1 = float(np.percentile(values, 25))
    q3 = float(np.percentile(values, 75))
    iqr = q3 - q1
    whisker_low = float(max(values.min(), q1 - 1.5 * iqr))
    whisker_high = float(min(values.max(), q3 + 1.5 * iqr))

    # Store box rectangle data for SVG fill injection
    box_rects.append((group_colors[i], q1, q3, center_y - box_hw, center_y + box_hw))

    # Box body + whiskers as single path
    box_path = [
        (whisker_low, center_y - box_hw * 0.6),
        (whisker_low, center_y + box_hw * 0.6),
        (whisker_low, center_y),
        (q1, center_y),
        (q1, center_y - box_hw),
        (q3, center_y - box_hw),
        (q3, center_y + box_hw),
        (q1, center_y + box_hw),
        (q1, center_y - box_hw),
        (q1, center_y),
        (q3, center_y),
        (q3, center_y + box_hw),
        (q3, center_y - box_hw),
        (q3, center_y),
        (whisker_high, center_y),
        (whisker_high, center_y - box_hw * 0.6),
        (whisker_high, center_y + box_hw * 0.6),
    ]
    chart.add("", box_path, stroke=True, fill=False, show_dots=False, stroke_style={"width": 10})

    # Median line (thicker for emphasis)
    median_line = [(median, center_y - box_hw * 1.1), (median, center_y + box_hw * 1.1)]
    chart.add("", median_line, stroke=True, fill=False, show_dots=False, stroke_style={"width": 12})

# Y-axis labels for treatment groups
chart.y_labels = [
    {"value": 0, "label": ""},
    {"value": 1, "label": "Control"},
    {"value": 2, "label": "Treatment A"},
    {"value": 3, "label": "Treatment B"},
    {"value": 4, "label": ""},
]

# Render base SVG
base_svg = chart.render().decode("utf-8")

# --- SVG post-processing ---

# Extract plot group's translate transform for absolute positioning


tx_match = re.search(r'translate\((\d+),\s*(\d+)\).*?class="plot"', base_svg)
plot_tx = int(tx_match.group(1)) if tx_match else 706
plot_ty = int(tx_match.group(2)) if tx_match else 214


# Coordinate mapping: data space → plot-local SVG pixel space
# Coefficients derived from pygal's internal scaling for this chart configuration
def sx(dx):
    return 5.907692 * dx - 513.969231


def sy(dy):
    return -482.517483 * dy + 2069.034965


# Absolute SVG coords (for elements injected outside plot group)
def ax(dx):
    return sx(dx) + plot_tx


def ay(dy):
    return sy(dy) + plot_ty


# Inject cloud polygons as SVG shapes (drawn first, behind everything else)
clouds_svg = '<g id="clouds">'
for color, poly in cloud_polygons:
    points = " ".join(f"{sx(px):.1f},{sy(py):.1f}" for px, py in poly)
    clouds_svg += f'<polygon points="{points}" fill="{color}" opacity="0.75" stroke="none"/>'
clouds_svg += "</g>"

# Insert clouds inside the plot group after the plot-area background rect
# The second background rect is inside the plot group (first is canvas-level)
bg_marker = 'class="background"'
first_bg = base_svg.find(bg_marker)
second_bg = base_svg.find(bg_marker, first_bg + 1)
if second_bg > 0:
    bg_end = base_svg.find("/>", second_bg) + 2
    base_svg = base_svg[:bg_end] + clouds_svg + base_svg[bg_end:]

# Compute medians for annotations
medians = {name: float(np.median(vals)) for name, vals in data.items()}
diff = medians["Control"] - medians["Treatment B"]

# Build box fill rectangles (drawn on top of clouds)
# Injected outside the plot group, so use absolute SVG coordinates
box_fills_svg = '<g id="box-fills">'
for color, q1, q3, y_lo, y_hi in box_rects:
    bx, by = ax(q1), ay(y_hi)
    bw, bh = sx(q3) - sx(q1), sy(y_lo) - sy(y_hi)
    box_fills_svg += (
        f'<rect x="{bx:.1f}" y="{by:.1f}" width="{bw:.1f}" height="{bh:.1f}"'
        f' fill="white" fill-opacity="0.75" stroke="{color}" stroke-width="5"/>'
    )
box_fills_svg += "</g>"

# Build annotation SVG elements
annotations_svg = '<g id="annotations">'

# Median value labels above each cloud with dashed leader lines
for i, name in enumerate(data):
    med = medians[name]
    center_y = i + 1
    mx, my = ax(med), ay(center_y)
    label_y = ay(center_y + 0.42)
    annotations_svg += (
        f'<line x1="{mx:.0f}" y1="{my:.0f}" x2="{mx:.0f}" y2="{label_y + 10:.0f}"'
        f' stroke="{group_colors[i]}" stroke-width="2" stroke-dasharray="6,4" opacity="0.6"/>'
        f'<text x="{mx:.0f}" y="{label_y:.0f}" text-anchor="middle"'
        f' font-size="38" font-weight="bold" font-family="DejaVu Sans, sans-serif"'
        f' fill="{group_colors[i]}">{med:.0f} ms</text>'
    )

# Insight callout: Treatment B faster than Control
cx, cy = ax(580), ay(3.8)
annotations_svg += (
    f'<rect x="{cx - 200:.0f}" y="{cy - 42:.0f}" width="400" height="90"'
    f' rx="12" ry="12" fill="white" stroke="#4CAF50" stroke-width="3" opacity="0.92"/>'
    f'<text x="{cx:.0f}" y="{cy + 12:.0f}" text-anchor="middle"'
    f' font-size="34" font-weight="bold" font-family="DejaVu Sans, sans-serif"'
    f' fill="#333333">&#x25BC; {diff:.0f} ms faster</text>'
)

# Dashed arrow from callout to Treatment B median
tb_x, tb_y = ax(medians["Treatment B"]), ay(3 + 0.42)
annotations_svg += (
    f'<line x1="{cx - 200:.0f}" y1="{cy + 10:.0f}"'
    f' x2="{tb_x + 50:.0f}" y2="{tb_y - 5:.0f}"'
    f' stroke="#4CAF50" stroke-width="2.5" stroke-dasharray="8,5" opacity="0.7"/>'
)

# Y-axis label (rotated SVG text avoids pygal clipping)
y_lx, y_ly = 70, (ay(1) + ay(3)) / 2
annotations_svg += (
    f'<text x="{y_lx:.0f}" y="{y_ly:.0f}" text-anchor="middle"'
    f' font-size="54" font-family="DejaVu Sans, sans-serif" fill="#333333"'
    f' transform="rotate(-90, {y_lx:.0f}, {y_ly:.0f})">Treatment Group</text>'
)

annotations_svg += "</g>"

# Inject box fills and annotations before closing </svg> tag
svg_out = base_svg.replace("</svg>", f"{box_fills_svg}\n{annotations_svg}\n</svg>")

# Save outputs
with open("plot.svg", "w") as f:
    f.write(svg_out)

cairosvg.svg2png(bytestring=svg_out.encode("utf-8"), write_to="plot.png")

with open("plot.html", "w") as f:
    f.write("""<!DOCTYPE html>
<html>
<head>
    <title>raincloud-basic · pygal · pyplots.ai</title>
    <style>
        body { margin: 0; padding: 20px; background: #f5f5f5; font-family: sans-serif; }
        .container { max-width: 100%; margin: 0 auto; }
        object { width: 100%; height: auto; }
    </style>
</head>
<body>
    <div class="container">
        <object type="image/svg+xml" data="plot.svg">
            Raincloud plot not supported
        </object>
    </div>
</body>
</html>""")
