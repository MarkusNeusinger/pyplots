"""pyplots.ai
nyquist-basic: Nyquist Plot for Control Systems
Library: pygal | Python 3.13
Quality: pending | Created: 2026-03-20
"""

import math

import numpy as np
import pygal
from pygal.style import Style


# Data — Transfer function G(s) = 2 / [s(s+1)(s+2)]
omega = np.logspace(-2, 2, 800)
s = 1j * omega
G = 2.0 / (s * (s + 1) * (s + 2))

real_part = G.real
imag_part = G.imag

# Mirror for negative frequencies (Nyquist contour reflection)
real_mirror = real_part[::-1]
imag_mirror = -imag_part[::-1]

# Custom style
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#cccccc",
    colors=(
        "#306998",  # Nyquist curve (positive freq)
        "#7BA1C7",  # Nyquist curve (negative freq)
        "#E74C3C",  # Critical point
        "#AAAAAA",  # Unit circle
    ),
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=42,
    tooltip_font_size=36,
    stroke_width=4,
    opacity=0.9,
    opacity_hover=0.95,
)

# Chart
chart = pygal.XY(
    width=4800,
    height=4800,
    style=custom_style,
    title="nyquist-basic · pygal · pyplots.ai",
    x_title="Real",
    y_title="Imaginary",
    show_legend=True,
    legend_at_bottom=True,
    legend_box_size=36,
    dots_size=3,
    stroke=True,
    show_x_guides=True,
    show_y_guides=True,
    explicit_size=True,
    range=(-2.5, 2.5),
    xrange=(-2.5, 2.5),
)

# Positive frequency curve — subsample for performance
step = 4
nyquist_positive = [(float(real_part[i]), float(imag_part[i])) for i in range(0, len(omega), step)]
chart.add("G(jω), ω ≥ 0", nyquist_positive, show_dots=False, stroke_style={"width": 5})

# Negative frequency curve (mirror)
nyquist_negative = [(float(real_mirror[i]), float(imag_mirror[i])) for i in range(0, len(omega), step)]
chart.add("G(jω), ω < 0", nyquist_negative, show_dots=False, stroke_style={"width": 4, "dasharray": "12,6"})

# Critical point (-1, 0)
chart.add("Critical Point (-1, 0)", [(-1.0, 0.0)], stroke=False, dots_size=24)

# Unit circle
circle_points = []
for angle in range(0, 361, 3):
    rad = math.radians(angle)
    circle_points.append((math.cos(rad), math.sin(rad)))
chart.add("Unit Circle", circle_points, stroke=True, show_dots=False, stroke_style={"width": 3, "dasharray": "8,6"})

# Direction arrows along positive frequency curve at selected frequencies
arrow_indices = [50, 150, 300, 500]
arrow_head_len = 0.06
arrow_head_wid = 0.03

for idx in arrow_indices:
    if idx + 1 >= len(omega):
        continue
    x0, y0 = float(real_part[idx]), float(imag_part[idx])
    x1, y1 = float(real_part[idx + 1]), float(imag_part[idx + 1])

    dx = x1 - x0
    dy = y1 - y0
    length = math.sqrt(dx * dx + dy * dy)
    if length < 1e-12:
        continue
    ux, uy = dx / length, dy / length
    px, py = -uy, ux

    tip_x, tip_y = x0, y0
    hb_x = tip_x - ux * arrow_head_len
    hb_y = tip_y - uy * arrow_head_len

    arrowhead = [
        (hb_x + px * arrow_head_wid, hb_y + py * arrow_head_wid),
        (tip_x, tip_y),
        (hb_x - px * arrow_head_wid, hb_y - py * arrow_head_wid),
        (tip_x, tip_y),
    ]
    chart.add(None, arrowhead, stroke=True, show_dots=False, fill=False, stroke_style={"width": 4})

# Save
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
