"""pyplots.ai
gauge-realtime: Real-Time Updating Gauge
Library: pygal 3.1.0 | Python 3.13.11
Quality: 72/100 | Created: 2026-01-19
"""

import pygal
from pygal.style import Style


# Data - CPU usage simulation with progressive readings
# Simulating real-time updates: showing current and recent values crossing thresholds
readings = [35, 42, 48, 55, 65, 75, 82, 85]  # Progressive CPU usage crossing zones
current_value = 85  # Current (latest) CPU usage - now Critical
min_value = 0
max_value = 100
# Thresholds: 0-50 = Normal (green), 50-80 = Warning (yellow), 80-100 = Critical (red)
threshold_warning = 50
threshold_critical = 80

# Zone colors
COLOR_NORMAL = "#2ECC71"  # Green
COLOR_WARNING = "#F1C40F"  # Yellow
COLOR_CRITICAL = "#E74C3C"  # Red

# Determine colors for all values to be displayed
values_to_show = [current_value] + list(reversed(readings[-4:-1]))  # Current + t-1, t-2, t-3
colors = []
labels = []

for i, val in enumerate(values_to_show):
    if val < threshold_warning:
        colors.append(COLOR_NORMAL)
        zone = "Normal"
    elif val < threshold_critical:
        colors.append(COLOR_WARNING)
        zone = "Warning"
    else:
        colors.append(COLOR_CRITICAL)
        zone = "Critical"

    if i == 0:
        labels.append(f"Current: {val}% ({zone})")
    else:
        labels.append(f"t-{i}: {val}% ({zone})")

# Custom style for 4800x2700 px - larger fonts for better visibility
# Colors assigned per-series for zone visualization
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#1a1a1a",
    foreground_subtle="#666666",
    colors=tuple(colors),  # Dynamic colors based on zone
    title_font_size=96,
    label_font_size=72,
    major_label_font_size=72,
    legend_font_size=56,
    value_font_size=96,
    tooltip_font_size=56,
)

# Create multi-gauge display showing real-time nature
chart = pygal.SolidGauge(
    width=4800,
    height=2700,
    style=custom_style,
    title="gauge-realtime · pygal · pyplots.ai",
    inner_radius=0.50,
    half_pie=True,
    show_legend=True,
    legend_at_bottom=True,
    legend_box_size=32,
    print_values=True,
    value_formatter=lambda x: f"{x:.0f}%",
    margin=40,
    spacing=80,
)

# Add gauges with zone-appropriate colors
# Each gauge shows: value, zone status in legend
# First gauge (current) also shows min/max range indicator
chart.add(f"{labels[0]} | Range: {min_value}-{max_value}%", [{"value": values_to_show[0], "max_value": max_value}])

# Add historical values to show real-time updating nature
for i in range(1, len(values_to_show)):
    chart.add(labels[i], [{"value": values_to_show[i], "max_value": max_value}])

# Save outputs
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
