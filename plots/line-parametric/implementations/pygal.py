""" pyplots.ai
line-parametric: Parametric Curve Plot
Library: pygal 3.1.0 | Python 3.14.3
Quality: 81/100 | Created: 2026-03-20
"""

import numpy as np
import pygal
from pygal.style import Style


# Data — parametric curves with parameter t
n_points = 1000
half = n_points // 2

# Lissajous figure: x = sin(3t), y = sin(2t), t ∈ [0, 2π]
t_liss = np.linspace(0, 2 * np.pi, n_points)
lissajous_x = np.sin(3 * t_liss)
lissajous_y = np.sin(2 * t_liss)

# Spiral: x = t·cos(t), y = t·sin(t), t ∈ [0, 4π], normalized to [-1,1]
t_spiral = np.linspace(0, 4 * np.pi, n_points)
raw_spiral_x = t_spiral * np.cos(t_spiral)
raw_spiral_y = t_spiral * np.sin(t_spiral)
spiral_max = max(np.abs(raw_spiral_x).max(), np.abs(raw_spiral_y).max())
spiral_x = raw_spiral_x / spiral_max
spiral_y = raw_spiral_y / spiral_max

# Style — polished design with explicit font sizing
font = "DejaVu Sans, Helvetica, Arial, sans-serif"

custom_style = Style(
    background="white",
    plot_background="#fafafa",
    foreground="#2d2d2d",
    foreground_strong="#1a1a1a",
    foreground_subtle="#e0e0e0",
    guide_stroke_color="#eeeeee",
    major_guide_stroke_color="#dddddd",
    colors=(
        "#08519c",  # Lissajous early — deep blue
        "#e6550d",  # Lissajous late — warm amber
        "#7b3294",  # Spiral early — rich purple
        "#008837",  # Spiral late — forest green
        "#1a1a1a",  # Start points — near-black
        "#666666",  # End points — dark gray
    ),
    font_family=font,
    title_font_family=font,
    title_font_size=52,
    label_font_size=36,
    major_label_font_size=32,
    legend_font_size=34,
    legend_font_family=font,
    value_font_size=28,
    tooltip_font_size=28,
    tooltip_font_family=font,
    opacity=0.9,
    opacity_hover=1.0,
    stroke_opacity=1.0,
    stroke_opacity_hover=1.0,
    stroke_width=10,
)

# Chart — square 3600×3600 for geometric accuracy
chart = pygal.XY(
    width=3600,
    height=3600,
    style=custom_style,
    title="line-parametric · pygal · pyplots.ai",
    x_title="Horizontal Position x(t)",
    y_title="Vertical Position y(t)",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=3,
    legend_box_size=26,
    stroke=True,
    show_dots=False,
    show_x_guides=True,
    show_y_guides=True,
    x_value_formatter=lambda v: f"{v:.1f}",
    value_formatter=lambda v: f"{v:.1f}",
    margin_bottom=160,
    margin_left=100,
    margin_right=80,
    margin_top=80,
    truncate_legend=-1,
    print_values=False,
    xrange=(-1.25, 1.25),
    range=(-1.25, 1.25),
    js=[],
    include_x_axis=True,
)

# Lissajous — two halves showing parameter direction via color shift
liss_early = [(float(lissajous_x[i]), float(lissajous_y[i])) for i in range(half + 1)]
liss_late = [(float(lissajous_x[i]), float(lissajous_y[i])) for i in range(half, n_points)]

chart.add(
    "Lissajous  t: 0 → π  (blue)",
    liss_early,
    stroke_style={"width": 11, "linecap": "round", "linejoin": "round"},
    show_dots=False,
)
chart.add(
    "Lissajous  t: π → 2π  (amber)",
    liss_late,
    stroke_style={"width": 11, "linecap": "round", "linejoin": "round"},
    show_dots=False,
)

# Spiral — two halves showing outward expansion via color shift
spi_early = [(float(spiral_x[i]), float(spiral_y[i])) for i in range(half + 1)]
spi_late = [(float(spiral_x[i]), float(spiral_y[i])) for i in range(half, n_points)]

chart.add(
    "Spiral  t: 0 → 2π  (purple)",
    spi_early,
    stroke_style={"width": 9, "linecap": "round", "linejoin": "round"},
    show_dots=False,
)
chart.add(
    "Spiral  t: 2π → 4π  (green)",
    spi_late,
    stroke_style={"width": 9, "linecap": "round", "linejoin": "round"},
    show_dots=False,
)

# Start points — prominent markers at t=0
chart.add(
    "● Start (t = 0)",
    [
        {"value": (float(lissajous_x[0]), float(lissajous_y[0])), "label": "Lissajous origin"},
        {"value": (float(spiral_x[0]), float(spiral_y[0])), "label": "Spiral origin"},
    ],
    stroke=False,
    dots_size=22,
)

# End points — distinct markers at curve endpoints
chart.add(
    "■ End (t = 2π / 4π)",
    [
        {"value": (float(lissajous_x[-1]), float(lissajous_y[-1])), "label": "Lissajous end"},
        {"value": (float(spiral_x[-1]), float(spiral_y[-1])), "label": "Spiral end"},
    ],
    stroke=False,
    dots_size=18,
)

# Save
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
