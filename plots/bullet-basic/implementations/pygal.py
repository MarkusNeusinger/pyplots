""" pyplots.ai
bullet-basic: Basic Bullet Chart
Library: pygal 3.1.0 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-16
"""

import cairosvg
import pygal
from pygal.style import Style


# Data - Sales KPIs showing actual vs target with qualitative ranges
metrics = [
    {"label": "Revenue", "actual": 275, "target": 250, "max": 300, "unit": "$K"},
    {"label": "Profit", "actual": 85, "target": 100, "max": 120, "unit": "$K"},
    {"label": "New Orders", "actual": 320, "target": 350, "max": 400, "unit": ""},
    {"label": "Customers", "actual": 1450, "target": 1400, "max": 1600, "unit": ""},
    {"label": "Satisfaction", "actual": 4.2, "target": 4.5, "max": 5.0, "unit": "/5"},
]

# Qualitative range thresholds as percentage of max
POOR_PCT = 50
SATISFACTORY_PCT = 75

# Custom style for bullet chart with grayscale bands
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=(
        "#E0E0E0",  # Poor range (lightest)
        "#B8B8B8",  # Satisfactory range
        "#909090",  # Good range (darkest)
        "#306998",  # Actual value (Python blue)
        "#1a1a1a",  # Target marker (black)
    ),
    title_font_size=72,
    label_font_size=42,
    major_label_font_size=40,
    legend_font_size=36,
    value_font_size=32,
    tooltip_font_size=32,
)

# Create horizontal stacked bar chart for range bands
chart = pygal.HorizontalStackedBar(
    width=4800,
    height=2700,
    title="bullet-basic · pygal · pyplots.ai",
    style=custom_style,
    show_legend=True,
    legend_at_bottom=True,
    legend_box_size=28,
    print_values=False,
    show_y_guides=False,
    show_x_guides=True,
    x_label_rotation=0,
    margin=80,
    spacing=40,
    x_title="Performance (% of Maximum)",
    range=(0, 100),
)

# Build labels and range data
labels = []
poor_vals = []
satisfactory_vals = []
good_vals = []
actual_pcts = []
target_pcts = []

for m in metrics:
    actual_pct = (m["actual"] / m["max"]) * 100
    target_pct = (m["target"] / m["max"]) * 100
    labels.append(f"{m['label']} ({m['actual']}{m['unit']})")
    # Stacked segments for qualitative ranges
    poor_vals.append(POOR_PCT)
    satisfactory_vals.append(SATISFACTORY_PCT - POOR_PCT)
    good_vals.append(100 - SATISFACTORY_PCT)
    actual_pcts.append(actual_pct)
    target_pcts.append(target_pct)

chart.x_labels = labels
chart.add("Poor (0-50%)", poor_vals)
chart.add("Satisfactory (50-75%)", satisfactory_vals)
chart.add("Good (75-100%)", good_vals)

# Render base chart to SVG, then inject actual bars and target markers
svg_string = chart.render().decode("utf-8")

# Pygal plot coordinates (from SVG analysis):
# Plot area: transform="translate(624, 192)", width=4096, height=2104
# Bars start at x=78.77 within plot (total from origin: 624 + 78.77 = 702.77)
# X-axis 0 maps to ~78.77, 100 maps to ~4017.23 (range of ~3938.46 pixels)
PLOT_OFFSET_X = 624
PLOT_OFFSET_Y = 192
BAR_START_X = 78.77  # Within plot coordinates
X_SCALE = 39.3846  # pixels per percentage point (3938.46 / 100)

# Row Y positions (from SVG: y values in <desc> tags) - relative to plot origin
ROW_Y_CENTERS = [1861.23, 1456.62, 1052.0, 647.38, 242.77]  # Revenue, Profit, Orders, Customers, Satisfaction

# Build custom SVG elements for actual bars and target markers
custom_elements = []
for i, (actual_pct, target_pct) in enumerate(zip(actual_pcts, target_pcts, strict=True)):
    # Calculate positions in plot coordinates
    y_center = PLOT_OFFSET_Y + ROW_Y_CENTERS[i]
    x_start = PLOT_OFFSET_X + BAR_START_X

    # Actual value bar - narrower bar centered on row
    actual_width = actual_pct * X_SCALE
    bar_height = 100  # Thinner than the range bands
    custom_elements.append(
        f'<rect x="{x_start}" y="{y_center - bar_height / 2}" '
        f'width="{actual_width}" height="{bar_height}" fill="#306998"/>'
    )

    # Target marker - thin vertical line extending beyond the bar
    target_x = x_start + target_pct * X_SCALE
    marker_height = 180
    marker_width = 12
    custom_elements.append(
        f'<rect x="{target_x - marker_width / 2}" y="{y_center - marker_height / 2}" '
        f'width="{marker_width}" height="{marker_height}" fill="#1a1a1a"/>'
    )

# Add legend entries for Actual and Target (positioned after existing legend items)
legend_y = 2574  # Same line as existing legend
legend_x_actual = 3200
legend_x_target = 3700
custom_elements.append(f'<rect x="{legend_x_actual}" y="{legend_y}" width="28" height="28" fill="#306998"/>')
custom_elements.append(
    f'<text x="{legend_x_actual + 40}" y="{legend_y + 24}" '
    f'font-family="Consolas, monospace" font-size="36" fill="#333">Actual</text>'
)
custom_elements.append(f'<rect x="{legend_x_target}" y="{legend_y}" width="28" height="28" fill="#1a1a1a"/>')
custom_elements.append(
    f'<text x="{legend_x_target + 40}" y="{legend_y + 24}" '
    f'font-family="Consolas, monospace" font-size="36" fill="#333">Target</text>'
)

# Inject custom elements before closing </svg>
injection = "\n".join(custom_elements)
svg_output = svg_string.replace("</svg>", f"{injection}\n</svg>")

# Save SVG and PNG
with open("plot.html", "w") as f:
    f.write(svg_output)

cairosvg.svg2png(bytestring=svg_output.encode(), write_to="plot.png")
