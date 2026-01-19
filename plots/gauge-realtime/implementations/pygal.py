"""pyplots.ai
gauge-realtime: Real-Time Updating Gauge
Library: pygal 3.1.0 | Python 3.13.11
Quality: 82/100 | Created: 2026-01-19
"""

import pygal
from pygal.style import Style


# Data - CPU usage simulation showing real-time progression across ALL zones
# Thresholds: 0-50 = Normal (green), 50-80 = Warning (yellow), 80-100 = Critical (red)
min_value = 0
max_value = 100
threshold_warning = 50
threshold_critical = 80

# Values covering all three zones to demonstrate the full range of the gauge
# Current value is critical, with history showing descent from normal through warning
values_to_show = [
    85,  # Current - Critical (red)
    68,  # t-1 - Warning (yellow)
    55,  # t-2 - Warning (yellow)
    38,  # t-3 - Normal (green)
]

# Zone colors
COLOR_NORMAL = "#2ECC71"  # Green
COLOR_WARNING = "#F1C40F"  # Yellow
COLOR_CRITICAL = "#E74C3C"  # Red


def get_zone_info(val):
    """Determine zone color and label based on value."""
    if val < threshold_warning:
        return COLOR_NORMAL, "Normal"
    elif val < threshold_critical:
        return COLOR_WARNING, "Warning"
    else:
        return COLOR_CRITICAL, "Critical"


# Build colors and labels for each gauge
colors = []
labels = []
for i, val in enumerate(values_to_show):
    color, zone = get_zone_info(val)
    colors.append(color)
    if i == 0:
        labels.append(f"Current: {val}% ({zone})")
    else:
        labels.append(f"t-{i}: {val}% ({zone})")

# Custom style for 4800x2700 px - larger fonts for better visibility
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#1a1a1a",
    foreground_subtle="#666666",
    colors=tuple(colors),
    title_font_size=96,
    label_font_size=72,
    major_label_font_size=72,
    legend_font_size=56,
    value_font_size=96,
    tooltip_font_size=56,
)

# Create multi-gauge display showing real-time nature
# print_values=False removes value inside arc, keeping only the label below
chart = pygal.SolidGauge(
    width=4800,
    height=2700,
    style=custom_style,
    title=f"gauge-realtime · pygal · pyplots.ai | Range: {min_value}%-{max_value}%",
    inner_radius=0.50,
    half_pie=True,
    show_legend=True,
    legend_at_bottom=True,
    legend_box_size=32,
    print_values=False,
    value_formatter=lambda x: f"{x:.0f}%",
    margin=40,
    spacing=80,
)

# Add gauges - labels include value and zone, title shows min/max range
for i, val in enumerate(values_to_show):
    chart.add(labels[i], [{"value": val, "max_value": max_value}])

# Save outputs
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
