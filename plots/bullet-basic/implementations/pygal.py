"""pyplots.ai
bullet-basic: Basic Bullet Chart
Library: pygal 3.1.0 | Python 3.14.3
Quality: /100 | Updated: 2026-02-22
"""

import cairosvg
import pygal
from pygal.style import Style


# Data - Sales KPIs showing actual vs target with qualitative ranges
metrics = [
    {"label": "Revenue", "actual": 275, "target": 250, "max": 300, "fmt": "${}K"},
    {"label": "Profit", "actual": 85, "target": 100, "max": 120, "fmt": "${}K"},
    {"label": "New Orders", "actual": 320, "target": 350, "max": 400, "fmt": "{}"},
    {"label": "Customers", "actual": 1450, "target": 1400, "max": 1600, "fmt": "{}"},
    {"label": "Satisfaction", "actual": 4.2, "target": 4.5, "max": 5.0, "fmt": "{}/5"},
]

# Qualitative range thresholds as percentage of max
POOR_PCT = 50
SATISFACTORY_PCT = 75

# Custom style with grayscale bands for qualitative ranges
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#999999",
    colors=(
        "#E0E0E0",  # Poor range (lightest)
        "#BFBFBF",  # Satisfactory range
        "#969696",  # Good range (darkest)
    ),
    title_font_size=64,
    label_font_size=40,
    major_label_font_size=36,
    legend_font_size=34,
    value_font_size=30,
    tooltip_font_size=30,
)

# Create horizontal stacked bar chart as base for range bands
chart = pygal.HorizontalStackedBar(
    width=4800,
    height=2700,
    title="bullet-basic \u00b7 pygal \u00b7 pyplots.ai",
    style=custom_style,
    show_legend=True,
    legend_at_bottom=True,
    legend_box_size=26,
    print_values=False,
    show_y_guides=False,
    show_x_guides=True,
    margin=70,
    spacing=35,
    x_title="Performance (% of Maximum)",
    range=(0, 100),
)

# Build labels and normalized data
labels = []
actual_pcts = []
target_pcts = []

for m in metrics:
    actual_pcts.append((m["actual"] / m["max"]) * 100)
    target_pcts.append((m["target"] / m["max"]) * 100)
    labels.append(f"{m['label']} ({m['fmt'].format(m['actual'])})")

chart.x_labels = labels

# Stacked segments for qualitative ranges
chart.add("Poor (0-50%)", [POOR_PCT] * len(metrics))
chart.add("Satisfactory (50-75%)", [SATISFACTORY_PCT - POOR_PCT] * len(metrics))
chart.add("Good (75-100%)", [100 - SATISFACTORY_PCT] * len(metrics))

# Render base SVG, then inject actual bars and target markers
svg_string = chart.render().decode("utf-8")

# Plot area coordinates (derived from pygal's SVG output structure)
PLOT_X = 585
PLOT_Y = 169
BAR_X0 = 79.71  # x-axis origin within plot area
PX_PER_PCT = 39.856  # pixels per percentage point (1992.79 / 50)

# Row centers within plot area (bottom to top: Revenue -> Satisfaction)
ROW_CENTERS = [1916.96, 1500.23, 1083.50, 666.77, 250.04]

# Build actual-value bars and target markers
injected = []
for i in range(len(metrics)):
    cy = PLOT_Y + ROW_CENTERS[i]
    x0 = PLOT_X + BAR_X0

    # Actual value: narrow bar centered on row
    w = actual_pcts[i] * PX_PER_PCT
    injected.append(f'<rect x="{x0}" y="{cy - 50}" width="{w}" height="100" fill="#306998"/>')

    # Target marker: thin vertical line perpendicular to bar
    tx = x0 + target_pcts[i] * PX_PER_PCT
    injected.append(f'<rect x="{tx - 4}" y="{cy - 90}" width="8" height="180" fill="#1a1a1a"/>')

# Legend entries for Actual and Target (aligned with pygal's second legend row)
lx_actual = 2692
lx_target = 3350
ly = 2635
injected.append(f'<rect x="{lx_actual}" y="{ly + 4}" width="26" height="26" fill="#306998"/>')
injected.append(
    f'<text x="{lx_actual + 31}" y="{ly + 27}" '
    f'font-family="Consolas, monospace" font-size="34" fill="#333">Actual</text>'
)
injected.append(f'<rect x="{lx_target}" y="{ly + 4}" width="26" height="26" fill="#1a1a1a"/>')
injected.append(
    f'<text x="{lx_target + 31}" y="{ly + 27}" '
    f'font-family="Consolas, monospace" font-size="34" fill="#333">Target</text>'
)

# Inject before closing </svg> tag
svg_output = svg_string.replace("</svg>", "\n".join(injected) + "\n</svg>")

# Save
cairosvg.svg2png(bytestring=svg_output.encode(), write_to="plot.png")
