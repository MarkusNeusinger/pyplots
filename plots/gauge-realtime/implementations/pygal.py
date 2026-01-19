"""pyplots.ai
gauge-realtime: Real-Time Updating Gauge
Library: pygal | Python 3.13
Quality: pending | Created: 2026-01-19
"""

import pygal
from pygal.style import Style


# Data - CPU usage simulation with multiple readings over time
# Simulating real-time updates: showing recent values and current value
readings = [45, 52, 58, 63, 68, 72, 75, 78]  # Progressive CPU usage values
current_value = 78  # Current (latest) CPU usage
max_value = 100
# Thresholds: 0-50 = Normal (green), 50-80 = Warning (yellow), 80-100 = Critical (red)

# Determine zone color for current value
if current_value < 50:
    current_color = "#2ECC71"  # Green - Normal
    zone_status = "Normal"
elif current_value < 80:
    current_color = "#F1C40F"  # Yellow - Warning
    zone_status = "Warning"
else:
    current_color = "#E74C3C"  # Red - Critical
    zone_status = "Critical"

# Custom style for 4800x2700 px
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#1a1a1a",
    foreground_subtle="#666666",
    colors=(current_color, "#BDC3C7", "#95A5A6", "#7F8C8D"),  # Current + faded historical
    title_font_size=72,
    label_font_size=54,
    major_label_font_size=54,
    legend_font_size=48,
    value_font_size=72,
    tooltip_font_size=40,
)

# Create multi-gauge display showing real-time nature
# Using multiple SolidGauges side by side to show "time progression"
chart = pygal.SolidGauge(
    width=4800,
    height=2700,
    style=custom_style,
    title="CPU Usage Monitor · gauge-realtime · pygal · pyplots.ai",
    inner_radius=0.55,
    half_pie=True,
    show_legend=True,
    legend_at_bottom=True,
    print_values=True,
    value_formatter=lambda x: f"{x:.0f}%",
    margin=80,
)

# Add current value prominently with zone indication
chart.add(f"Current: {current_value}% ({zone_status})", [{"value": current_value, "max_value": max_value}])

# Add recent historical values to show real-time updating nature
# Using faded colors to show temporal progression
recent_values = readings[-4:-1]  # Last 3 values before current
time_labels = ["t-1", "t-2", "t-3"]
for i, val in enumerate(reversed(recent_values)):
    chart.add(f"{time_labels[i]}: {val}%", [{"value": val, "max_value": max_value}])

# Save outputs
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
