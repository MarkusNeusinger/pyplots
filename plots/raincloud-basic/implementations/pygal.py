""" pyplots.ai
raincloud-basic: Basic Raincloud Plot
Library: pygal 3.1.0 | Python 3.14
Quality: 85/100 | Created: 2025-12-25
"""

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
group_names = list(data.keys())

# Build color sequence: per group = cloud, rain, box_outline, median_line
box_color = "#333333"
series_colors = []
for gc in group_colors:
    series_colors.extend([gc, gc, box_color, box_color])

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
    opacity=0.80,
    opacity_hover=0.95,
)

# Create HORIZONTAL XY chart
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="raincloud-basic · pygal · pyplots.ai",
    x_title="Reaction Time (ms)",
    y_title="",
    show_legend=False,
    stroke=True,
    fill=True,
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
box_hw = 0.10  # box half-width (vertical extent each side of center)

for i, (category, values) in enumerate(data.items()):
    center_y = i + 1
    values = np.array(values)

    # --- Half-Violin (cloud) - extends UPWARD from category line ---
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

    # Normalize and place cloud ABOVE category line
    density_scaled = density / density.max() * cloud_height

    # Half-violin shape: baseline at center_y, cloud rises upward
    cloud_points = [(float(x_kde[0]), center_y)]
    cloud_points += [
        {"value": (float(x), center_y + float(d)), "label": f"{category} density"}
        for x, d in zip(x_kde, density_scaled, strict=True)
    ]
    cloud_points += [(float(x_kde[-1]), center_y), (float(x_kde[0]), center_y)]
    chart.add(f"{category} cloud", cloud_points, stroke=True, fill=True)

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

    # Box + whiskers + caps as single path
    box_path = [
        # Left cap
        (whisker_low, center_y - box_hw),
        (whisker_low, center_y + box_hw),
        (whisker_low, center_y),
        # Left whisker → box
        (q1, center_y),
        # Box perimeter
        (q1, center_y - box_hw),
        (q3, center_y - box_hw),
        (q3, center_y + box_hw),
        (q1, center_y + box_hw),
        (q1, center_y - box_hw),
        (q1, center_y),
        # Right side
        (q3, center_y),
        (q3, center_y + box_hw),
        (q3, center_y - box_hw),
        (q3, center_y),
        # Right whisker → cap
        (whisker_high, center_y),
        (whisker_high, center_y - box_hw),
        (whisker_high, center_y + box_hw),
    ]
    chart.add("", box_path, stroke=True, fill=False, show_dots=False, stroke_style={"width": 6})

    # Median line (separate, thicker series for emphasis)
    median_line = [(median, center_y - box_hw * 1.2), (median, center_y + box_hw * 1.2)]
    chart.add("", median_line, stroke=True, fill=False, show_dots=False, stroke_style={"width": 9})

# Y-axis labels for treatment groups
chart.y_labels = [
    {"value": 0, "label": ""},
    {"value": 1, "label": "Control"},
    {"value": 2, "label": "Treatment A"},
    {"value": 3, "label": "Treatment B"},
    {"value": 4, "label": ""},
]

# Render base SVG, then inject annotations for data storytelling
base_svg = chart.render().decode("utf-8")

# Compute stats for annotations
annotations_svg = '<g id="annotations">'

# Compute median for each group
medians = {}
for name, vals in data.items():
    medians[name] = float(np.median(vals))

# Annotation: highlight median difference between Control and Treatment B
diff = medians["Control"] - medians["Treatment B"]

# Map data coordinates to SVG pixel positions
# Chart area: x from margin_left to (4800 - margin_right), y from margin_top to (2700 - margin_bottom)
# Data range: x = 100..750, y = -0.2..4.2
svg_ml, svg_mr, svg_mt, svg_mb = 340, 100, 120, 120
plot_x0, plot_x1 = svg_ml + 160, 4800 - svg_mr - 40  # approximate pygal inner offsets
plot_y0, plot_y1 = svg_mt + 100, 2700 - svg_mb - 60
data_x0, data_x1 = 100.0, 750.0
data_y0, data_y1 = -0.2, 4.2


def data_to_svg_x(dx):
    return plot_x0 + (dx - data_x0) / (data_x1 - data_x0) * (plot_x1 - plot_x0)


def data_to_svg_y(dy):
    # SVG y is inverted
    return plot_y1 - (dy - data_y0) / (data_y1 - data_y0) * (plot_y1 - plot_y0)


# Add annotation: median markers with values
for i, name in enumerate(data):
    med = medians[name]
    center_y = i + 1
    sx = data_to_svg_x(med)
    sy = data_to_svg_y(center_y)

    # Median value label above the cloud
    label_y = data_to_svg_y(center_y + 0.42)
    annotations_svg += f"""
    <line x1="{sx:.0f}" y1="{sy:.0f}" x2="{sx:.0f}" y2="{label_y + 10:.0f}"
          stroke="{group_colors[i]}" stroke-width="2" stroke-dasharray="6,4" opacity="0.6"/>
    <text x="{sx:.0f}" y="{label_y:.0f}" text-anchor="middle"
          font-size="38" font-weight="bold" font-family="DejaVu Sans, sans-serif"
          fill="{group_colors[i]}">{med:.0f} ms</text>"""

# Add insight callout: Treatment B faster than Control
callout_x = data_to_svg_x(580)
callout_y = data_to_svg_y(3.8)
annotations_svg += f"""
    <rect x="{callout_x - 200:.0f}" y="{callout_y - 42:.0f}" width="400" height="90"
          rx="12" ry="12" fill="white" stroke="#4CAF50" stroke-width="3" opacity="0.92"/>
    <text x="{callout_x:.0f}" y="{callout_y + 12:.0f}" text-anchor="middle"
          font-size="34" font-weight="bold" font-family="DejaVu Sans, sans-serif"
          fill="#333333">&#x25BC; {diff:.0f} ms faster</text>"""

# Arrow from callout to Treatment B median
tb_med_x = data_to_svg_x(medians["Treatment B"])
tb_med_y = data_to_svg_y(3 + 0.42)
annotations_svg += f"""
    <line x1="{callout_x - 200:.0f}" y1="{callout_y + 10:.0f}"
          x2="{tb_med_x + 50:.0f}" y2="{tb_med_y - 5:.0f}"
          stroke="#4CAF50" stroke-width="2.5" stroke-dasharray="8,5" opacity="0.7"/>"""

# Y-axis label as custom SVG text (avoids pygal's rotation clipping)
y_label_x = 70
y_label_y = (plot_y0 + plot_y1) / 2
annotations_svg += f"""
    <text x="{y_label_x:.0f}" y="{y_label_y:.0f}" text-anchor="middle"
          font-size="54" font-family="DejaVu Sans, sans-serif" fill="#333333"
          transform="rotate(-90, {y_label_x:.0f}, {y_label_y:.0f})">Treatment Group</text>"""

annotations_svg += "\n</g>"

# Inject annotations before closing </svg> tag
svg_with_annotations = base_svg.replace("</svg>", f"{annotations_svg}\n</svg>")

# Save outputs
with open("plot.svg", "w") as f:
    f.write(svg_with_annotations)

cairosvg.svg2png(bytestring=svg_with_annotations.encode("utf-8"), write_to="plot.png")

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
