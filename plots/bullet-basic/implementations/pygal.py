"""
bullet-basic: Basic Bullet Chart
Library: pygal
"""

import pygal
from pygal.style import Style


# Data - Sales KPIs normalized to percentage of max range for comparison
# Bullet chart shows: actual value, target, and qualitative ranges (poor/satisfactory/good)
# All values expressed as percentage of each metric's max range for visual alignment
metrics = [
    {"label": "Revenue", "actual": 275, "target": 250, "max": 300, "fmt": "${v}K"},
    {"label": "Profit", "actual": 85, "target": 100, "max": 100, "fmt": "${v}K"},
    {"label": "New Orders", "actual": 320, "target": 350, "max": 400, "fmt": "{v}"},
    {"label": "Customers", "actual": 1450, "target": 1400, "max": 1600, "fmt": "{v}"},
    {"label": "Satisfaction", "actual": 4.2, "target": 4.5, "max": 5.0, "fmt": "{v}/5"},
]

# Qualitative range thresholds as percentage of max (same for all metrics)
POOR_PCT = 50  # 0-50% = Poor
SATISFACTORY_PCT = 75  # 50-75% = Satisfactory
GOOD_PCT = 100  # 75-100% = Good

# Custom style for 4800x2700 px with bullet chart grayscale bands
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=(
        "#D0D0D0",  # Poor range (light gray)
        "#A0A0A0",  # Satisfactory range (medium gray)
        "#707070",  # Good range (darker gray)
    ),
    title_font_size=72,
    label_font_size=44,
    major_label_font_size=42,
    legend_font_size=42,
    value_font_size=36,
    tooltip_font_size=36,
)

# Create horizontal stacked bar chart to show qualitative range bands
chart = pygal.HorizontalStackedBar(
    width=4800,
    height=2700,
    title="bullet-basic · pygal · pyplots.ai",
    style=custom_style,
    show_legend=True,
    legend_at_bottom=True,
    legend_box_size=30,
    print_values=False,
    show_y_guides=True,
    show_x_guides=False,
    margin=60,
    spacing=50,
    x_title="Performance (%)",
)

# Build stacked bar data for qualitative ranges (normalized to percentage)
labels = []
poor_values = []
satisfactory_values = []
good_values = []

for m in metrics:
    # Calculate actual as percentage of max
    actual_pct = (m["actual"] / m["max"]) * 100
    target_pct = (m["target"] / m["max"]) * 100

    # Create descriptive label showing actual vs target
    status = "✓" if m["actual"] >= m["target"] else "○"
    fmt = m["fmt"]
    actual_str = fmt.replace("{v}", str(m["actual"]))
    target_str = fmt.replace("{v}", str(m["target"]))
    labels.append(f"{m['label']}: {actual_str} {status} (target: {target_str})")

    # Stack ranges as percentage segments
    poor_values.append(POOR_PCT)
    satisfactory_values.append(SATISFACTORY_PCT - POOR_PCT)
    good_values.append(GOOD_PCT - SATISFACTORY_PCT)

# Set metric labels (y-axis)
chart.x_labels = labels

# Add stacked range bands (these form the bullet chart background)
chart.add("Poor (0-50%)", poor_values)
chart.add("Satisfactory (50-75%)", satisfactory_values)
chart.add("Good (75-100%)", good_values)

# Save outputs
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
