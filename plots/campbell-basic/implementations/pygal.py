"""pyplots.ai
campbell-basic: Campbell Diagram
Library: pygal | Python 3.13
Quality: pending | Created: 2026-02-15
"""

import numpy as np
import pygal
from pygal.style import Style


# Data — natural frequencies of a rotor system vs rotational speed
np.random.seed(42)
speed_rpm = np.linspace(0, 6000, 80)
speed_hz = speed_rpm / 60

# Natural frequency modes (Hz) with gyroscopic effects
# 1st Bending: increases slightly with speed
mode1 = 25 + 0.003 * speed_rpm + np.random.normal(0, 0.15, len(speed_rpm))
# 2nd Bending: increases moderately with speed
mode2 = 48 + 0.005 * speed_rpm + np.random.normal(0, 0.15, len(speed_rpm))
# 1st Torsional: nearly constant
mode3 = 62 - 0.001 * speed_rpm + np.random.normal(0, 0.15, len(speed_rpm))
# Axial: decreases slightly with speed
mode4 = 78 - 0.002 * speed_rpm + np.random.normal(0, 0.15, len(speed_rpm))
# 2nd Torsional: increases with speed
mode5 = 92 + 0.004 * speed_rpm + np.random.normal(0, 0.15, len(speed_rpm))

# Engine order lines: frequency = order * speed_rpm / 60
orders = [1, 2, 3]

# Find critical speed intersections (engine order line crosses a mode)
critical_speeds = []
for order in orders:
    eo_freq = order * speed_hz
    for mode, _name in zip(
        [mode1, mode2, mode3, mode4, mode5],
        ["1st Bending", "2nd Bending", "1st Torsional", "Axial", "2nd Torsional"],
        strict=True,
    ):
        diff = eo_freq - mode
        sign_changes = np.where(np.diff(np.sign(diff)))[0]
        for idx in sign_changes:
            frac = abs(diff[idx]) / (abs(diff[idx]) + abs(diff[idx + 1]))
            rpm_interp = speed_rpm[idx] + frac * (speed_rpm[idx + 1] - speed_rpm[idx])
            freq_interp = order * rpm_interp / 60
            if 0 < rpm_interp < 6000:
                critical_speeds.append((float(rpm_interp), float(freq_interp)))

# Style
font = "DejaVu Sans, Helvetica, Arial, sans-serif"
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#2a2a2a",
    foreground_strong="#2a2a2a",
    foreground_subtle="#e0e0e0",
    guide_stroke_color="#e0e0e0",
    colors=("#306998", "#1a9988", "#7b5ea7", "#d4812e", "#5a8c3c", "#777777", "#999999", "#bbbbbb", "#c0392b"),
    font_family=font,
    title_font_family=font,
    title_font_size=56,
    label_font_size=42,
    major_label_font_size=38,
    legend_font_size=32,
    legend_font_family=font,
    value_font_size=28,
    tooltip_font_size=28,
    tooltip_font_family=font,
    opacity=0.9,
    opacity_hover=1.0,
    stroke_opacity=1,
    stroke_opacity_hover=1,
)

# Chart
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="campbell-basic · pygal · pyplots.ai",
    x_title="Rotational Speed (RPM)",
    y_title="Frequency (Hz)",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=5,
    legend_box_size=22,
    stroke=True,
    dots_size=0,
    show_x_guides=True,
    show_y_guides=True,
    x_value_formatter=lambda x: f"{x:.0f}",
    value_formatter=lambda y: f"{y:.1f} Hz",
    margin_bottom=100,
    margin_left=60,
    margin_right=50,
    margin_top=50,
    x_label_rotation=0,
    truncate_legend=-1,
    range=(0, 120),
    xrange=(0, 6000),
    print_values=False,
    print_zeroes=False,
    js=[],
)

# Natural frequency mode curves
modes = [
    (mode1, "1st Bending"),
    (mode2, "2nd Bending"),
    (mode3, "1st Torsional"),
    (mode4, "Axial"),
    (mode5, "2nd Torsional"),
]
for mode_data, label in modes:
    points = [(float(r), float(f)) for r, f in zip(speed_rpm, mode_data, strict=True)]
    chart.add(label, points, stroke_style={"width": 5, "linecap": "round"}, show_dots=False)

# Engine order excitation lines (dashed)
eo_max_rpm = 6000
for order in orders:
    eo_points = [(0.0, 0.0), (float(eo_max_rpm), float(order * eo_max_rpm / 60))]
    # Clip to y_max of 120
    if eo_points[-1][1] > 120:
        clipped_rpm = 120 * 60 / order
        eo_points[-1] = (float(clipped_rpm), 120.0)
    chart.add(
        f"{order}x EO", eo_points, stroke_style={"width": 4, "dasharray": "20, 10", "linecap": "round"}, show_dots=False
    )

# Critical speed markers
chart.add("Critical Speeds", [{"value": pt} for pt in critical_speeds], stroke=False, dots_size=16)

# Save
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
