""" pyplots.ai
skewt-logp-atmospheric: Skew-T Log-P Atmospheric Diagram
Library: pygal 3.1.0 | Python 3.13.11
Quality: 62/100 | Created: 2026-01-17
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

# For Skew-T Log-P: Y-axis uses pressure directly (inverted so 1000 hPa at bottom)
# pygal range_force with min > max inverts the axis
# Use negative log pressure so that surface (1000 hPa) is at bottom with higher y values
# log_p will be 0 at 1000 hPa and positive (higher) going up to lower pressures
log_p = np.log10(1000.0 / pressure)  # 0 at surface, ~1 at 100 hPa

# Apply skew transformation to temperature
# In Skew-T, isotherms are tilted 45 degrees to the right
skew_factor = 35  # Controls the skew angle
temp_skewed = temperature + skew_factor * log_p
dewpoint_skewed = dewpoint + skew_factor * log_p

# Create custom style for meteorological diagram
custom_style = Style(
    background="white",
    plot_background="#f0f4f8",
    foreground="#333333",
    foreground_strong="#222222",
    foreground_subtle="#555555",
    colors=(
        "#c0392b",  # Temperature - dark red
        "#2980b9",  # Dewpoint - blue
        "#27ae60",  # Dry adiabats - green
        "#8e44ad",  # Moist adiabats - purple
        "#e67e22",  # Mixing ratio - orange
        "#7f8c8d",  # Isotherms - gray
    ),
    title_font_size=56,
    label_font_size=32,
    major_label_font_size=28,
    legend_font_size=28,
    value_font_size=22,
    stroke_width=4,
)

# Create XY chart for the sounding
# Y-axis: log_p goes from 0 (surface, 1000 hPa) to ~1 (100 hPa)
# We want surface at bottom, so use range with min=0 at bottom
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="skewt-logp-atmospheric · pygal · pyplots.ai",
    x_title="Temperature (°C)",
    y_title="Pressure (hPa, log scale)",
    show_dots=True,
    dots_size=6,
    stroke_style={"width": 4},
    show_x_guides=True,
    show_y_guides=True,
    x_label_rotation=0,
    legend_at_bottom=True,
    legend_at_bottom_columns=6,
    range=(0, 1.05),  # Y range: 0 (1000 hPa) at bottom to 1 (100 hPa) at top
    xrange=(-60, 80),  # X range for skewed temperature
)

# Custom y-axis labels showing pressure levels
y_labels = [0, 0.033, 0.07, 0.155, 0.301, 0.398, 0.523, 0.602, 0.699, 0.824, 1.0]
p_labels = [1000, 925, 850, 700, 500, 400, 300, 250, 200, 150, 100]

# Add temperature profile (solid red line)
temp_points = [(float(temp_skewed[i]), float(log_p[i])) for i in range(len(pressure))]
chart.add("Temperature (°C)", temp_points, stroke_style={"width": 5})

# Add dewpoint profile (blue, dashed using dasharray)
dewpoint_points = [(float(dewpoint_skewed[i]), float(log_p[i])) for i in range(len(pressure))]
chart.add("Dewpoint (°C)", dewpoint_points, stroke_style={"width": 4, "dasharray": "12,6"})

# Add dry adiabats (potential temperature lines) - curved lines sloping right
# Dry adiabats show how unsaturated air parcels cool as they rise
dry_adiabat_thetas = [280, 300, 320, 340]  # Potential temperatures in K
for theta in dry_adiabat_thetas:
    adiabat_points = []
    for p in np.linspace(1000, 100, 20):
        lp = np.log10(1000.0 / p)
        # Dry adiabatic temperature: T = theta * (p/1000)^(R/Cp)
        T_adiabat = theta * (p / 1000.0) ** 0.286 - 273.15
        T_skewed = T_adiabat + skew_factor * lp
        if -60 <= T_skewed <= 80:
            adiabat_points.append((float(T_skewed), float(lp)))
    if adiabat_points:
        chart.add(f"θ={theta}K", adiabat_points, show_dots=False, stroke_style={"width": 2, "dasharray": "4,4"})

# Add moist adiabats (saturated adiabats) - curved, less steep than dry
# Simplified moist adiabat approximation
moist_adiabat_starts = [-10, 10, 30]  # Starting temperatures at 1000 hPa
for t_start in moist_adiabat_starts:
    moist_points = []
    t_current = t_start
    for p in np.linspace(1000, 200, 15):
        lp = np.log10(1000.0 / p)
        T_skewed = t_current + skew_factor * lp
        if -60 <= T_skewed <= 80:
            moist_points.append((float(T_skewed), float(lp)))
        # Moist adiabatic lapse rate is ~6°C/km (less than dry 10°C/km)
        t_current -= 4.5  # Approximate decrease per pressure level
    if moist_points:
        chart.add(f"Moist {t_start}°C", moist_points, show_dots=False, stroke_style={"width": 2, "dasharray": "8,4"})

# Add mixing ratio lines (nearly vertical, slight tilt)
mixing_ratios = [1, 4, 10, 20]  # g/kg
for mr in mixing_ratios:
    mr_points = []
    for p in np.linspace(1000, 400, 10):
        lp = np.log10(1000.0 / p)
        # Approximate dewpoint for given mixing ratio
        # Td ≈ (243.5 * ln(e/6.112)) / (17.67 - ln(e/6.112))
        # where e = mr * p / (622 + mr)
        e = mr * p / (622 + mr)
        if e > 0:
            td = (243.5 * np.log(e / 6.112)) / (17.67 - np.log(e / 6.112))
            td_skewed = td + skew_factor * lp
            if -60 <= td_skewed <= 80:
                mr_points.append((float(td_skewed), float(lp)))
    if mr_points:
        chart.add(f"r={mr}g/kg", mr_points, show_dots=False, stroke_style={"width": 1, "dasharray": "2,4"})

# Add isotherms (temperature reference lines - diagonal due to skew)
isotherms = [-40, -20, 0, 20, 40]
for isotherm in isotherms:
    isotherm_points = []
    for lp in np.linspace(0, 1.0, 10):
        T_skewed = isotherm + skew_factor * lp
        if -60 <= T_skewed <= 80:
            isotherm_points.append((float(T_skewed), float(lp)))
    if isotherm_points:
        chart.add(f"{isotherm}°C iso", isotherm_points, show_dots=False, stroke_style={"width": 1, "dasharray": "6,3"})

# Render to PNG and HTML
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
