""" pyplots.ai
campbell-basic: Campbell Diagram
Library: pygal 3.1.0 | Python 3.14.3
Quality: 68/100 | Created: 2026-02-15
"""

import numpy as np
import pygal
from pygal.style import Style


# Data — natural frequencies of a rotor system vs rotational speed
np.random.seed(42)
speed_rpm = np.linspace(0, 6000, 80)
speed_hz = speed_rpm / 60

# Natural frequency modes (Hz) with gyroscopic effects
mode1 = 25 + 0.003 * speed_rpm + np.random.normal(0, 0.15, len(speed_rpm))
mode2 = 48 + 0.005 * speed_rpm + np.random.normal(0, 0.15, len(speed_rpm))
mode3 = 62 - 0.001 * speed_rpm + np.random.normal(0, 0.15, len(speed_rpm))
mode4 = 78 - 0.002 * speed_rpm + np.random.normal(0, 0.15, len(speed_rpm))
mode5 = 92 + 0.004 * speed_rpm + np.random.normal(0, 0.15, len(speed_rpm))

# Engine order lines
orders = [1, 2, 3]

# Find critical speed intersections
modes_data = [mode1, mode2, mode3, mode4, mode5]
mode_names = ["1st Bending", "2nd Bending", "1st Torsional", "Axial", "2nd Torsional"]
critical_speeds = []
for order in orders:
    eo_freq = order * speed_hz
    for mode in modes_data:
        diff = eo_freq - mode
        sign_changes = np.where(np.diff(np.sign(diff)))[0]
        for idx in sign_changes:
            frac = abs(diff[idx]) / (abs(diff[idx]) + abs(diff[idx + 1]))
            rpm_interp = speed_rpm[idx] + frac * (speed_rpm[idx + 1] - speed_rpm[idx])
            freq_interp = order * rpm_interp / 60
            if 0 < rpm_interp < 6000:
                critical_speeds.append((float(rpm_interp), float(freq_interp)))

# Style — 5 mode curves + 3 EO lines + 1 critical speed series
# EO lines use distinct warm/cool colors that contrast with grid and mode curves
font = "DejaVu Sans, Helvetica, Arial, sans-serif"
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#2a2a2a",
    foreground_strong="#2a2a2a",
    foreground_subtle="#d0d0d0",
    guide_stroke_color="#ececec",
    guide_stroke_dasharray="4, 6",
    major_guide_stroke_dasharray="2, 4",
    colors=(
        "#306998",  # 1st Bending — Python Blue
        "#1a9988",  # 2nd Bending — teal
        "#7b5ea7",  # 1st Torsional — purple
        "#d4812e",  # Axial — orange
        "#5a8c3c",  # 2nd Torsional — green
        "#c0392b",  # 1x EO — deep red
        "#1a5276",  # 2x EO — dark navy
        "#6c3483",  # 3x EO — dark violet
        "#ff0000",  # Critical Speeds — bright red
    ),
    font_family=font,
    title_font_family=font,
    title_font_size=56,
    label_font_size=42,
    major_label_font_size=38,
    legend_font_size=30,
    legend_font_family=font,
    value_font_size=28,
    tooltip_font_size=28,
    tooltip_font_family=font,
    opacity=1.0,
    opacity_hover=1.0,
    stroke_opacity=1.0,
    stroke_opacity_hover=1.0,
)

# Chart with pygal-specific configuration
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="campbell-basic · pygal · pyplots.ai",
    x_title="Rotational Speed (RPM)",
    y_title="Frequency (Hz)",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=3,
    legend_box_size=24,
    stroke=True,
    dots_size=0,
    show_x_guides=True,
    show_y_guides=True,
    interpolate="cubic",
    interpolation_precision=200,
    x_value_formatter=lambda x: f"{x:,.0f}",
    value_formatter=lambda y: f"{y:.1f}",
    margin_bottom=80,
    margin_left=80,
    margin_right=60,
    margin_top=50,
    x_label_rotation=0,
    truncate_legend=-1,
    range=(0, 120),
    xrange=(0, 6000),
    print_values=False,
    print_zeroes=False,
    tooltip_fancy_mode=True,
    js=[],
)

# Natural frequency mode curves — solid, thick lines
for mode, label in zip(modes_data, mode_names, strict=True):
    points = [(float(r), float(f)) for r, f in zip(speed_rpm, mode, strict=True)]
    chart.add(label, points, stroke_style={"width": 8, "linecap": "round"}, show_dots=False)

# Engine order excitation lines — dashed, distinct colors, visually separated from grid
eo_labels = ["1× EO", "2× EO", "3× EO"]
eo_dash_patterns = ["24, 12", "18, 8, 6, 8", "12, 6"]
for order, eo_label, dash in zip(orders, eo_labels, eo_dash_patterns, strict=True):
    eo_end_rpm = min(6000.0, 120.0 * 60.0 / order)
    eo_end_hz = order * eo_end_rpm / 60.0
    eo_points = [(0.0, 0.0), (float(eo_end_rpm), float(eo_end_hz))]
    chart.add(eo_label, eo_points, stroke_style={"width": 6, "dasharray": dash, "linecap": "round"}, show_dots=False)

# Critical speed markers — bright red, large dots as visual focal points
critical_points = [{"value": pt, "label": f"Critical: {pt[0]:.0f} RPM / {pt[1]:.1f} Hz"} for pt in critical_speeds]
chart.add("Critical Speeds", critical_points, stroke=False, dots_size=20)

# Save
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
