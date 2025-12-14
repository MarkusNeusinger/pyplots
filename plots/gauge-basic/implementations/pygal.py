"""
gauge-basic: Basic Gauge Chart
Library: pygal
"""

import pygal
from pygal.style import Style


# Data - Current sales performance
value = 72  # Current value to display
min_value = 0
max_value = 100
# Thresholds at 30 and 70 create three zones: red (0-30), yellow (30-70), green (70-100)
threshold_low = 30
threshold_high = 70

# Determine zone color based on value
if value < threshold_low:
    value_color = "#E74C3C"  # Red for low zone
elif value < threshold_high:
    value_color = "#F1C40F"  # Yellow for medium zone
else:
    value_color = "#2ECC71"  # Green for high zone

# Custom style for 4800x2700 px
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=(value_color,),
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=48,
    legend_font_size=48,
    value_font_size=56,
    tooltip_font_size=36,
)

# Create SolidGauge chart (semi-circular gauge)
chart = pygal.SolidGauge(
    width=4800,
    height=2700,
    style=custom_style,
    title="gauge-basic · pygal · pyplots.ai",
    inner_radius=0.70,
    half_pie=True,
    show_legend=True,
    legend_at_bottom=True,
    print_values=True,
    value_formatter=lambda x: f"{x:.0f}%",
    margin=50,
)

# Add the current value as main gauge indicator
chart.add(f"Current Sales: {value}%", [{"value": value, "max_value": max_value}])

# Save outputs
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
