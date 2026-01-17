"""pyplots.ai
skewt-logp-atmospheric: Skew-T Log-P Atmospheric Diagram
Library: pygal | Python 3.13
Quality: pending | Created: 2025-01-17
"""

import numpy as np
import pygal
from pygal.style import Style


np.random.seed(42)

# Generate realistic atmospheric sounding data
# Pressure levels from surface (1000 hPa) to upper troposphere (100 hPa)
pressure = np.array([1000, 925, 850, 700, 500, 400, 300, 250, 200, 150, 100])

# Temperature profile (typical mid-latitude sounding, decreasing with altitude)
temperature = np.array([25, 20, 15, 5, -15, -28, -45, -52, -58, -62, -55])

# Dewpoint profile (always <= temperature, converges in clouds)
dewpoint = np.array([18, 15, 12, -2, -22, -38, -55, -60, -65, -70, -65])

# Convert pressure to log scale for y-axis
# Higher values = higher altitude (lower pressure)
log_p = np.log10(1000.0 / pressure)

# Apply skew transformation to temperature
# In Skew-T, isotherms are tilted 45 degrees
# x_skewed = T + skew_factor * log(p0/p)
skew_factor = 30  # Controls the skew angle
temp_skewed = temperature + skew_factor * log_p
dewpoint_skewed = dewpoint + skew_factor * log_p

# Create custom style for meteorological diagram
custom_style = Style(
    background="white",
    plot_background="#f8f9fa",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#d62728", "#1f77b4", "#aaaaaa", "#cccccc", "#dddddd"),
    title_font_size=48,
    label_font_size=28,
    major_label_font_size=24,
    legend_font_size=24,
    value_font_size=20,
    stroke_width=4,
)

# Create XY chart for the sounding
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="skewt-logp-atmospheric · pygal · pyplots.ai",
    x_title="Temperature (°C, skewed)",
    y_title="Altitude (log scale)",
    show_dots=True,
    dots_size=8,
    stroke_style={"width": 4},
    show_x_guides=True,
    show_y_guides=True,
    x_label_rotation=0,
    legend_at_bottom=True,
    legend_at_bottom_columns=5,
)

# Add temperature profile (solid red line)
temp_points = [(float(temp_skewed[i]), float(log_p[i])) for i in range(len(pressure))]
chart.add("Temperature", temp_points)

# Add dewpoint profile (blue dashed - pygal doesn't support dashed, use different color)
dewpoint_points = [(float(dewpoint_skewed[i]), float(log_p[i])) for i in range(len(pressure))]
chart.add("Dewpoint", dewpoint_points)

# Add isotherms (vertical reference lines in skewed coordinates)
# These appear as diagonal lines on the chart
isotherms = [-40, -20, 0, 20, 40]
for isotherm in isotherms:
    isotherm_points = [(float(isotherm + skew_factor * lp), float(lp)) for lp in log_p]
    chart.add(f"{isotherm}°C", isotherm_points, show_dots=False, stroke_style={"width": 1, "dasharray": "5,5"})

# Render to PNG and HTML
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
