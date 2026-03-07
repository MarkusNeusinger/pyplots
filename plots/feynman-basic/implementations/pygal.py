"""pyplots.ai
feynman-basic: Feynman Diagram for Particle Interactions
Library: pygal 3.1.0 | Python 3.14.3
"""

import math

import numpy as np
import pygal
from pygal.style import Style


# Data — Electron-positron annihilation: e⁻e⁺ → γ → μ⁻μ⁺
# Vertex positions (interaction points)
v1_x, v1_y = 3.0, 3.0
v2_x, v2_y = 7.0, 3.0

# Fermion endpoints
e_minus_in = (0.5, 5.0)
e_plus_in = (0.5, 1.0)
mu_minus_out = (9.5, 5.0)
mu_plus_out = (9.5, 1.0)


# Arrowhead segments at a position along a line
def arrowhead(x1, y1, x2, y2, frac=0.55, size=0.35):
    mx = x1 + frac * (x2 - x1)
    my = y1 + frac * (y2 - y1)
    dx, dy = x2 - x1, y2 - y1
    length = math.hypot(dx, dy)
    ux, uy = dx / length, dy / length
    px, py = -uy, ux
    tip_x = mx + size * 0.5 * ux
    tip_y = my + size * 0.5 * uy
    w1x = mx - size * 0.5 * ux + size * 0.35 * px
    w1y = my - size * 0.5 * uy + size * 0.35 * py
    w2x = mx - size * 0.5 * ux - size * 0.35 * px
    w2y = my - size * 0.5 * uy - size * 0.35 * py
    return [(tip_x, tip_y), (w1x, w1y), None, (tip_x, tip_y), (w2x, w2y), None, (w1x, w1y), (w2x, w2y)]


# Fermion lines with None breaks between segments
fermion_lines = [
    {"value": e_minus_in, "label": "e⁻ incoming fermion"},
    {"value": (v1_x, v1_y), "label": "Vertex 1"},
    None,
    {"value": e_plus_in, "label": "e⁺ incoming antifermion"},
    {"value": (v1_x, v1_y), "label": "Vertex 1"},
    None,
    {"value": (v2_x, v2_y), "label": "Vertex 2"},
    {"value": mu_minus_out, "label": "μ⁻ outgoing fermion"},
    None,
    {"value": (v2_x, v2_y), "label": "Vertex 2"},
    {"value": mu_plus_out, "label": "μ⁺ outgoing antifermion"},
]

# Arrowheads on fermion lines (particle direction arrows)
# Convention: particles forward in time (left→right), antiparticles backward
arrow_data = []
arrow_data += arrowhead(*e_minus_in, v1_x, v1_y)
arrow_data.append(None)
arrow_data += arrowhead(v1_x, v1_y, *e_plus_in)
arrow_data.append(None)
arrow_data += arrowhead(v2_x, v2_y, *mu_minus_out)
arrow_data.append(None)
arrow_data += arrowhead(*mu_plus_out, v2_x, v2_y)

# Photon propagator — sinusoidal path between v1 and v2
n_wave = 300
t = np.linspace(0, 1, n_wave)
photon_x = v1_x + t * (v2_x - v1_x)
photon_y = v1_y + 0.35 * np.sin(t * 16 * np.pi)
photon_line = [
    {"value": (float(x), float(y)), "label": "γ (virtual photon)"} for x, y in zip(photon_x, photon_y, strict=True)
]

# Vertex markers
vertex_points = [
    {"value": (v1_x, v1_y), "label": "Vertex 1 — annihilation point"},
    {"value": (v2_x, v2_y), "label": "Vertex 2 — pair creation point"},
]

# On-diagram particle labels — positions near midpoints of propagators
label_names = ["e⁻", "e⁺", "γ", "μ⁻", "μ⁺"]
label_positions = [
    ((e_minus_in[0] + v1_x) / 2 - 0.3, (e_minus_in[1] + v1_y) / 2 + 0.4),
    ((e_plus_in[0] + v1_x) / 2 - 0.3, (e_plus_in[1] + v1_y) / 2 - 0.4),
    ((v1_x + v2_x) / 2, v1_y + 0.7),
    ((v2_x + mu_minus_out[0]) / 2 + 0.3, (v2_y + mu_minus_out[1]) / 2 + 0.4),
    ((v2_x + mu_plus_out[0]) / 2 + 0.3, (v2_y + mu_plus_out[1]) / 2 - 0.4),
]

# Style
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#1a1a2e",
    foreground_strong="#1a1a2e",
    foreground_subtle="#f0f0f0",
    colors=(
        "#306998",  # fermion lines (Python Blue)
        "#306998",  # arrowheads (same blue)
        "#D4493E",  # photon wavy line (red)
        "#1a1a2e",  # vertex dots (dark)
        "#1a1a2e",  # particle labels (dark)
    ),
    opacity=0.95,
    opacity_hover=1.0,
    title_font_size=38,
    label_font_size=24,
    major_label_font_size=22,
    legend_font_size=24,
    value_font_size=32,
    tooltip_font_size=20,
    stroke_width=4,
    title_font_family="Trebuchet MS, Helvetica, sans-serif",
    label_font_family="Trebuchet MS, Helvetica, sans-serif",
    major_label_font_family="Trebuchet MS, Helvetica, sans-serif",
    legend_font_family="Trebuchet MS, Helvetica, sans-serif",
    value_font_family="Trebuchet MS, Helvetica, sans-serif",
)

# Chart
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="e⁻e⁺ → γ → μ⁻μ⁺ Annihilation · feynman-basic · pygal · pyplots.ai",
    show_x_guides=False,
    show_y_guides=False,
    show_x_labels=False,
    show_y_labels=False,
    x_title="",
    y_title="",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=5,
    legend_box_size=24,
    stroke=True,
    show_dots=False,
    print_values=True,
    margin_top=30,
    margin_bottom=80,
    margin_left=40,
    margin_right=40,
    tooltip_border_radius=8,
    tooltip_fancy_mode=True,
    range=(-0.2, 6.2),
    xrange=(-0.5, 10.5),
)

# Fermion lines
chart.add("Fermions (e⁻, e⁺, μ⁻, μ⁺)", fermion_lines, stroke_width=5, formatter=lambda x: "")

# Arrowheads (same color, no legend text)
chart.add(" ", arrow_data, stroke_width=4, show_dots=False, formatter=lambda x: "")

# Photon propagator
chart.add("Photon propagator (γ)", photon_line, stroke_width=3, formatter=lambda x: "")

# Vertex dots
chart.add("Interaction vertices", vertex_points, stroke=False, show_dots=True, dots_size=20, formatter=lambda x: "")

# On-diagram particle labels using pygal's print_values + per-series formatter
# Each label is a separate series so formatter returns the correct particle symbol
label_series_data = [
    {"value": pos, "label": f"{name} particle label"} for name, pos in zip(label_names, label_positions, strict=True)
]

# Build a lookup mapping position tuple to label name
label_lookup = {pos: name for name, pos in zip(label_names, label_positions, strict=True)}


def label_formatter(val):
    if isinstance(val, (list, tuple)) and len(val) >= 2:
        for (px, py), name in label_lookup.items():
            if abs(val[0] - px) < 0.1 and abs(val[1] - py) < 0.1:
                return name
    return ""


chart.add("Particle labels", label_series_data, show_dots=True, dots_size=1, stroke=False, formatter=label_formatter)

# Save
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
